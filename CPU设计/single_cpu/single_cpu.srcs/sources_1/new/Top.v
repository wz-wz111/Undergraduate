`timescale 1ns / 1ps
module top(
input clk, input reset, input step, input run,
//input clk,                  //clk for display
output OF,CF,PF,ZF, //alu运算为零标志
input [2:0] SW,        //开关
output [6:0] sm_duan,  //段码
output [3:0] sm_wei,//哪个数码管
output [31:0]  PC,          
output [31:0]aluRes,           
output[31:0] memreaddata,      
output [31:0]instruction,
output [31:0] display_content,
output [15:0] disp_num,
output clk_cpu
);
//integer clk_cnt;
//reg clkin;//1.33秒一个时钟周期，以此为cpu的时钟周期	10^8/0.75*10^8=4/3=1.33 
//always @(posedge clk)
//if(clk_cnt==32'd75_000_000) 
//begin
//clk_cnt <= 1'b0; 
//clkin <= ~clkin;
//end 
//else
//clk_cnt <= clk_cnt + 1'b1;

assign clk_cpu=(run == 1)?clk:step;
 //控制数码管显示

  //显示内容选择    
   assign display_content = (SW[1:0] == 2'b00)? instruction:
                       (SW[1:0] == 2'b01)? PC:
                       (SW[1:0] == 2'b10)? aluRes: memreaddata;
   //高低16位选择                     
   assign disp_num = (SW[2] == 1)? display_content[31:16]:
display_content[15:0]; 

//...............................实例化数码管显示模块
display Smg(.clk(clk),.sm_wei(sm_wei),.data(disp_num ),.sm_duan(sm_duan));

// 复用器信号线
//wire[31:0] expand2, mux4, mux5, address, jmpaddr;
//数据存储器
//reg[31:0] next_PC;
// 指令存储器 
//wire [31:0] instruction; 
reg[7:0] Addr;
// CPU 控制信号线
wire reg_dst,jmp,branch, memread, memwrite, memtoreg,alu_src,ExtOp,lui,jr,jal; 
wire[3:0] aluop;
wire regwrite;
// ALU 控制信号线
 
//wire[31:0] aluRes; //alu运算结果
// ALU控制信号线
wire[3:0] aluCtr;//根据aluop和指令后6位 选择alu运算类型
//wire[31:0] aluRes; //alu运算结果
wire[31:0] input2;  //ALU的第二个操作数来自寄存器堆输出或指令低16位的符号扩展
wire [15:0]data;    //imm
// 寄存器信号线
wire[31:0] RsData, RtData;

wire[31:0] expand; 
wire[4:0] shamt;
wire [4:0]regWriteAddr;
wire[31:0]regWriteData, W_Data;
assign shamt=instruction[10:6];
assign regWriteAddr = reg_dst ? instruction[15:11] : instruction[20:16];//写寄存器的目标寄存器来自rt或rd
assign data=aluRes[15:0];//imm
assign regWriteData = memtoreg ? memreaddata : aluRes; //写入寄存器的数据来自ALU或数据存储器 
assign input2 = alu_src ? expand : RtData; //ALU的第二个操作数来自寄存器堆输出或指令低16位的符号扩展
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
// 例化指令存储器
IM_unit IM (
                .clka(~clk_cpu),    // input wire clka
                .ena(1'b1),      // input wire ena数据输出允许
                .addra(PC[9:2]),  // input wire [7 : 0] addra
                .douta(instruction)  // output wire [31 : 0] douta
 );

// 实例化控制器模块
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

//  实例化 ALU 控制模块
aluctr aluctr1(
.ALUOp(aluop),
.funct(instruction[5:0]),
.jr(jr),
.ALUCtr(aluCtr));
// 。。。。。。。。。。。。。。。。。。。。。。。。。实例化寄存器模块
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

// 。。。。。。。。。。。。。。。。。。。。。。实例化ALU模块
alu alu(
.shamt(shamt),
.A(RsData), //写入alu的第一个操作数必是Rs
.B(input2),
.aluCtr(aluCtr),
.ZF(ZF),
.OF(OF),
.CF(CF),
.PF(PF),
.F(aluRes));
//实例化符号扩展模块
signext signext(.inst(instruction[15:0]),.ExtOp(ExtOp), .data(expand));
//实例化数据存储器
 DM_unit dm(.clk(clk_cpu), .Wr(memwrite),
            .reset(reset),           
             .DMAdr(aluRes), 
             .wd(RtData),
             .rd( memreaddata));




endmodule
