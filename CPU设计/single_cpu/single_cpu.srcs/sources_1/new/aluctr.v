`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/16 23:04:17
// Design Name: 
// Module Name: aluctr
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


module aluctr(
input [3:0] ALUOp, input [5:0] funct, output reg [3:0]  ALUCtr , output reg jr
);

always @(ALUOp or funct) //  如果操作码或者功能码变化执行操作
begin 
jr=0;
casex({ALUOp, funct}) // 拼接操作码和功能码便于下一步的判断
10'b0000xxxxxx: ALUCtr = 4'b0010; // lw，sw，addi ，addiu
10'b0001xxxxxx: ALUCtr = 4'b0110; // beq 
10'b0110xxxxxx: ALUCtr = 4'b0110; // bne？？？
10'b1111100000: ALUCtr = 4'b0010; // add 
10'b1111100001: ALUCtr = 4'b0010; // addu
10'b1111100010: ALUCtr = 4'b0110; // sub 
10'b1111100011: ALUCtr = 4'b0110; // subu
10'b1111100100: ALUCtr = 4'b0000; // and 
10'b1111100101: ALUCtr = 4'b0001; // or 
10'b1111000000: ALUCtr = 4'b0011; // sll
10'b1111000100: ALUCtr = 4'b1001; // sllv
10'b1111000010: ALUCtr = 4'b0101; // srl
10'b1111000110: ALUCtr = 4'b1010; // srlv
10'b1111000011: ALUCtr = 4'b1000; // sra
10'b1111000111: ALUCtr = 4'b1011; // srav
10'b1111101010: ALUCtr = 4'b0111; // slt
10'b1111101011: ALUCtr = 4'b0111; // sltu
10'b1111100111: ALUCtr = 4'b0100; // nor
10'b1111001000:  jr = 1; // jr

10'b0010xxxxxx: ALUCtr = 4'b0001; // ori
10'b0011xxxxxx: ALUCtr = 4'b0111; // slti , sltiu
10'b1100xxxxxx: ALUCtr = 4'b1100; // xori
10'b0100xxxxxx: ALUCtr = 4'b0000; // andi
10'b1011xxxxxx: ALUCtr = 4'b1101; // lui

default:begin ALUCtr = 4'b0010; jr=0; end
endcase 
end
endmodule

