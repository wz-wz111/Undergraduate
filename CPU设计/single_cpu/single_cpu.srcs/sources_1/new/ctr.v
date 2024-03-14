`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/16 22:23:35
// Design Name: 
// Module Name: ctr
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


module ctr(
input [5:0] opCode, output reg regDst, output reg aluSrc, output reg memToReg, output reg regWrite, output reg memRead, output reg memWrite, output reg branch, output reg eq, output reg jal,
output reg ExtOp, //������չ��ʽ��1 Ϊ sign-extend��0 Ϊ zero-extend
output reg[3:0] aluop, // ���� ALU ����������� ALU ����
output reg jmp
);

always@(opCode) begin
jal = 0;
// ������ı�ʱ�ı�����ź�
case(opCode) 6'b000010: begin
regDst = 0;  aluSrc = 0; memToReg = 0;
regWrite = 0; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0000; jmp = 1; ExtOp = 1; 
end // 'J ��' ָ�������: 000010������ ALU

6'b000011: begin
regDst = 0;  aluSrc = 0; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0000; jmp = 1; ExtOp = 1;  jal = 1;
end // 'Jal ��' ָ�������: 000011������ ALU

6'b000000: begin
regDst = 1;  aluSrc = 0; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b1111; jmp = 0; ExtOp = 1;
end // 'R ��' ָ�������: 000000

//'I'��ָ�������
6'b100011: begin
regDst = 0;  aluSrc = 1; memToReg = 1;
regWrite = 1; memRead = 1; memWrite = 0; branch = 0; aluop = 4'b0000; jmp = 0; ExtOp = 1;
end // 'lw' ָ�������: 100011

6'b101011: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 0; memRead = 0; memWrite = 1; branch = 0; aluop = 4'b0000; jmp = 0; ExtOp = 1;
end // 'sw' ָ�������: 101011

6'b000100: begin
regDst = 0;  aluSrc = 0; memToReg = 0;
regWrite = 0; memRead = 0; memWrite = 0; branch = 1; aluop = 4'b0110; jmp = 0; ExtOp = 1;
end // 'beq' ָ�������: 000100

6'b000101: begin
regDst = 0;  aluSrc = 0; memToReg = 0;
regWrite = 0; memRead = 0; memWrite = 0; branch = 1; aluop = 4'b0110; jmp = 0; ExtOp = 1;
end // 'bne' ָ�������: 000101

6'b001000: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0;
 
branch = 0; aluop = 4'b0000; jmp = 0;
ExtOp = 1;
end // 'addi' ָ�������: 001000

6'b001001: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0;
 
branch = 0; aluop = 4'b0000; jmp = 0;
ExtOp = 0;
end // 'addiu' ָ�������: 001001

6'b001100: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0100; jmp = 0; ExtOp = 0;
end // 'andi' ָ�������: 001100

6'b001101: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0010; jmp = 0; ExtOp = 0;
end // 'ori' ָ�������: 001101

6'b001110: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b1100; jmp = 0; ExtOp = 0;
end // 'xori' ָ�������: 001110
 
6'b001010: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0011; jmp = 0; ExtOp = 1;
end // 'slti' ָ�������: 001010

6'b001011: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0011; jmp = 0; ExtOp = 0;
end // 'sltiu' ָ�������: 001011

6'b001111: begin
regDst = 0;  aluSrc = 1; memToReg = 0;
regWrite = 1; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b1011; jmp = 0; ExtOp = 1;
end // 'lui' ָ�������: 001111

default: begin
regDst = 0;  aluSrc = 0; memToReg = 0;
regWrite = 0; memRead = 0; memWrite = 0; branch = 0; aluop = 4'b0000; jmp = 0; ExtOp = 0;
end // Ĭ������
endcase end
endmodule

