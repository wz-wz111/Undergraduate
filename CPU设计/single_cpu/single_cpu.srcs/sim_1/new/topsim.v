`timescale 1ns / 1ps
module topsim; 
// Inputs 
reg clk; 
reg reset; 
//wire [31:0] next_PC;
wire [6:0] sm_duan;//段码
wire [3:0] sm_wei;//哪个数码管
wire [31:0]  PC;          
wire [31:0]aluRes;        
wire[31:0] memreaddata;   
wire [31:0]instruction; 
wire [31:0] display_content;
wire [15:0] disp_num    ;
wire clk_cpu;
wire OF,CF,PF,ZF; //alu运算为零标志 
// Instantiate the Unit Under Test (UUT) 
top uut ( 
.clk(clk), 
.reset(reset) ,
.PC(PC),
.clk_cpu(clk_cpu),
.SW(2'b01),
.run(1'b1),
.aluRes(aluRes),
.instruction(instruction),
.sm_duan(sm_duan),
.display_content(display_content),
.disp_num(disp_num ),
.memreaddata(memreaddata),
 .sm_wei(sm_wei),
 .OF(OF),
 .CF(CF),
 .PF(PF),
 .ZF(ZF)
); 
//wire reg_dst,jmp,branch, memread, memwrite, memtoreg,alu_src; 
//ire[1:0] aluop;
// input clk,                  //clk for display


//reg clkin;//1.33秒一个时钟周期，以此为cpu的时钟周期    10^8/0.75*10^8=4/3=1.33 always @(posedge clk)
//if(clk_cnt==32'd75_000_000) 
//begin
//clk_cnt <= 1'b0; 
//clkin <= ~clkin;
//end 
//else
//clk_cnt <= clk_cnt + 1'b1;
//initial pc=0;
//   always@(posedge clkin or posedge reset)begin
//       if(reset)
//       pc=32'h00000000;
//       else
//       pc=next_PC;
//   end

initial begin 
// Initialize Inputs 
clk = 0; 
reset = 1; 

//pc=0;
// Wait 100 ns for global reset to finish 
#10; 
reset = 0; 
end 
parameter PERIOD = 20; 
always begin 
clk = 1'b1; 
#(PERIOD / 2) clk = 1'b0; 
#(PERIOD / 2) ; 
end 
endmodule 
