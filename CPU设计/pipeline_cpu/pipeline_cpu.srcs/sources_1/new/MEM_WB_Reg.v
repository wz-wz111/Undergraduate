`timescale 1ns / 1ps
module MEM_WB_Reg(clk, reset, PC_add_4_in, ALUOut_in, MemReadData_in, Rt_in, Rd_in, RegDst_in, MemToReg_in, RegWrite_in, 
	AddrC_in, PC_add_4_out, ALUOut_out, MemReadData_out, Rt_out, Rd_out, RegDst_out, MemToReg_out, RegWrite_out, AddrC_out);

input clk,reset,RegWrite_in;
input [31:0] PC_add_4_in, ALUOut_in,MemReadData_in;
input [4:0] Rt_in,Rd_in,AddrC_in;
input [1:0] RegDst_in,MemToReg_in;
output reg [31:0] PC_add_4_out,ALUOut_out,MemReadData_out;
output reg [4:0] Rt_out,Rd_out,AddrC_out;
output reg [1:0] RegDst_out,MemToReg_out;
output reg RegWrite_out;
always @(posedge clk or negedge reset) begin
	if (reset) begin
PC_add_4_out <= 32'h0000_0000;
ALUOut_out <= 32'h0000_0000;
MemReadData_out <= 32'h0000_0000;
Rt_out <= 5'h00;	Rd_out <= 5'h00;
RegDst_out <= 2'h0;	MemToReg_out <= 2'h0;
RegWrite_out <= 1'h0;	AddrC_out <= 5'h0;
	end
	
else begin
    PC_add_4_out <= PC_add_4_in;
    ALUOut_out <= ALUOut_in;
    MemReadData_out <= MemReadData_in;
    Rt_out <= Rt_in;
    Rd_out <= Rd_in;
    RegDst_out <= RegDst_in;
    MemToReg_out <= MemToReg_in;
    RegWrite_out <= RegWrite_in;
    AddrC_out <= AddrC_in;
        end
    end
    endmodule

