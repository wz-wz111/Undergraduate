`timescale 1ns / 1ps
module top(
input clk, input reset, input step, input run,
//input clk,                  //clk for display
output OF,CF,PF,ZF, //alu����Ϊ���־
input [2:0] SW,        //����
output [6:0] sm_duan,  //����
output [3:0] sm_wei,//�ĸ������
output [31:0]  PC,          
output [31:0]aluRes,           
output[31:0] memreaddata,      
output [31:0]instruction,
output [31:0] display_content,
output [15:0] disp_num,
output clk_cpu
);
//integer clk_cnt;
//reg clkin;//1.33��һ��ʱ�����ڣ��Դ�Ϊcpu��ʱ������	10^8/0.75*10^8=4/3=1.33 
//always @(posedge clk)
//if(clk_cnt==32'd75_000_000) 
//begin
//clk_cnt <= 1'b0; 
//clkin <= ~clkin;
//end 
//else
//clk_cnt <= clk_cnt + 1'b1;

assign clk_cpu=(run == 1)?clk:step;
 //�����������ʾ

  //��ʾ����ѡ��    
   assign display_content = (SW[1:0] == 2'b00)? instruction:
                       (SW[1:0] == 2'b01)? PC:
                       (SW[1:0] == 2'b10)? aluRes: memreaddata;
   //�ߵ�16λѡ��                     
   assign disp_num = (SW[2] == 1)? display_content[31:16]:
display_content[15:0]; 

//...............................ʵ�����������ʾģ��
display Smg(.clk(clk),.sm_wei(sm_wei),.data(disp_num ),.sm_duan(sm_duan));

// �������ź���
//wire[31:0] expand2, mux4, mux5, address, jmpaddr;
//���ݴ洢��
//reg[31:0] next_PC;
// ָ��洢�� 
//wire [31:0] instruction; 
reg[7:0] Addr;
// CPU �����ź���
wire reg_dst,jmp,branch, memread, memwrite, memtoreg,alu_src,ExtOp,lui,jr,jal; 
wire[3:0] aluop;
wire regwrite;
// ALU �����ź���
 
//wire[31:0] aluRes; //alu������
// ALU�����ź���
wire[3:0] aluCtr;//����aluop��ָ���6λ ѡ��alu��������
//wire[31:0] aluRes; //alu������
wire[31:0] input2;  //ALU�ĵڶ������������ԼĴ����������ָ���16λ�ķ�����չ
wire [15:0]data;    //imm
// �Ĵ����ź���
wire[31:0] RsData, RtData;

wire[31:0] expand; 
wire[4:0] shamt;
wire [4:0]regWriteAddr;
wire[31:0]regWriteData, W_Data;
assign shamt=instruction[10:6];
assign regWriteAddr = reg_dst ? instruction[15:11] : instruction[20:16];//д�Ĵ�����Ŀ��Ĵ�������rt��rd
assign data=aluRes[15:0];//imm
assign regWriteData = memtoreg ? memreaddata : aluRes; //д��Ĵ�������������ALU�����ݴ洢�� 
assign input2 = alu_src ? expand : RtData; //ALU�ĵڶ������������ԼĴ����������ָ���16λ�ķ�����չ
wire [31:0]  jrpc;
assign W_Data = jal ? jrpc :regWriteData;
//initial PC=0;
//always@(posedge clkin or posedge reset)begin
//       if(reset)
//       begin PC=32'h00000000; end
//       else
//       begin PC=PC+4; end
//   end

next_pc  next_pc(
.branch(branch), .zero(ZF), .jmp(jmp), .jr(jr),.clkin(clk_cpu),.expand(expand),.instruction(instruction), .reset(reset), .RsData(RsData), .jal(jal), .jrpc(jrpc) ,
.pc(PC)
); 
// ����ָ��洢��
IM_unit IM (
                .clka(~clk_cpu),    // input wire clka
                .ena(1'b1),      // input wire ena�����������
                .addra(PC[9:2]),  // input wire [7 : 0] addra
                .douta(instruction)  // output wire [31 : 0] douta
 );

// ʵ����������ģ��
ctr mainctr(
.opCode(instruction[31:26]),
.regDst(reg_dst),
.aluSrc(alu_src),
.memToReg(memtoreg),
.regWrite(regwrite),
.memRead(memread),
.memWrite(memwrite),
.branch(branch),
.ExtOp(ExtOp),
.aluop(aluop),
.jmp(jmp),
.jal(jal)
);

//  ʵ���� ALU ����ģ��
aluctr aluctr1(
.ALUOp(aluop),
.funct(instruction[5:0]),
.jr(jr),
.ALUCtr(aluCtr));
// ��������������������������������������������������ʵ�����Ĵ���ģ��
RegFile regfile(
.R_Addr_A(instruction[25:21]),    //rs
.R_Addr_B(instruction[20:16]),      //rt
.Clk(!clk_cpu),
.Clr(reset),
.jal(jal),
.W_Addr(regWriteAddr),
.W_Data(W_Data),
.Write_Reg(regwrite),
.R_Data_A(RsData),
.R_Data_B(RtData)
);

// ��������������������������������������������ʵ����ALUģ��
alu alu(
.shamt(shamt),
.A(RsData), //д��alu�ĵ�һ������������Rs
.B(input2),
.aluCtr(aluCtr),
.ZF(ZF),
.OF(OF),
.CF(CF),
.PF(PF),
.F(aluRes));
//ʵ����������չģ��
signext signext(.inst(instruction[15:0]),.ExtOp(ExtOp), .data(expand));
//ʵ�������ݴ洢��
 DM_unit dm(.clk(clk_cpu), .Wr(memwrite),
            .reset(reset),           
             .DMAdr(aluRes), 
             .wd(RtData),
             .rd( memreaddata));




endmodule
