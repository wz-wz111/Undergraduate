`timescale 1ns / 1ps
module IF_ID_Reg(
	clk, reset, PC_add_4_in, Instruct_in,PC_add_4_out, Instruct_out,flush_IF_ID,IF_ID_write);
//input	
input clk;
input reset;
input IF_ID_write;
input [31:0] PC_add_4_in;
input [31:0] Instruct_in;
input flush_IF_ID;
//output
output reg [31:0] PC_add_4_out;
output reg [31:0] Instruct_out;
always @(posedge clk or negedge reset) begin
	if (reset || flush_IF_ID) begin
	PC_add_4_out <= 32'h0000_0000;
	Instruct_out <= 32'h0000_0000;
	end
	else 
	if(IF_ID_write)
	begin
	PC_add_4_out <= PC_add_4_in;
	Instruct_out <= Instruct_in;
	     end
	end
endmodule
