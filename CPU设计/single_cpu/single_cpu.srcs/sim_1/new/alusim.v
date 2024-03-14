`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/21 23:27:48
// Design Name: 
// Module Name: alusim
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


`timescale 1ns / 1ps

module alusim; 
// Inputs 
reg [31:0] input1; 
reg [31:0] input2; 
reg [3:0] aluCtr; 
// Outputs 
wire [31:0] aluRes; 
wire zero; 
// Instantiate the Unit Under Test (UUT) 
alu alu(
.A(input1), //写入alu的第一个操作数必是Rs
.B(input2),
.aluCtr(aluCtr),

.F(aluRes));

//alu uut ( 
//.input1(input1), 
//.input2(input2), 
//.aluCtr(aluCtr), 
//.aluRes(aluRes), 
//.zero(zero) 
//); 
initial begin 
// Initialize Inputs 
input1 = 1; 
input2 = 16; 
aluCtr = 4'b1001; 
#100; 
input1 = 2; 
input2 = 16; 
aluCtr = 4'b1010; 
#100 
input1 = 1; 
input2 = 16; 
aluCtr = 4'b1011; 
#100 
input1 = 1; 
input2 = 0; 
aluCtr = 4'b0000; 
#100 
input1 = 1; 
input2 = 0; 
aluCtr = 4'b0001; 
#100 
input1 = 1; 
input2 = 0; 
aluCtr = 4'b0111; 
#100 
input1 = 0; 
input2 = 1; 
aluCtr = 4'b0111; 
end 
endmodule
