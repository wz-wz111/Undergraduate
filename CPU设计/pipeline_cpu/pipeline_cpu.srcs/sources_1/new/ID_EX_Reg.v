`timescale 1ns / 1ps
module ID_EX_Reg(
	clk, reset,	PC_add_4_in, DataBusA_in, 	DataBusB_in, ALUCtr_in, flush_ID_EX, opCode_in ,
	Rs_in, Rt_in,Rd_in, Shamt_in,	RegDst_in,PCSrc_in, MemRead_in, MemWrite_in, 	aluop_in, expand_in, branch_in,
	MemToReg_in, ALUFun_in, ALUSrc_in, 	RegWrite_in, Sign_in,PC_add_4_out, DataBusA_out, expand_out, beq_bne_in,
	DataBusB_out, Rs_out, Rt_out, Rd_out, Shamt_out, RegDst_out, PCSrc_out,MemRead_out, MemWrite_out,aluop_out,
	ALUCtr_out, branch_out,beq_bne_out, opCode_out,
	MemToReg_out, ALUFun_out,ALUSrc_out, 	RegWrite_out,Sign_out);
input clk;//
input reset;//
input [31:0] DataBusA_in;//dataA
input [31:0] DataBusB_in;//
input [4:0] Rs_in,Rt_in,Rd_in,Shamt_in;//
input [1:0] RegDst_in;//
input [2:0] PCSrc_in;//¡¢
input MemRead_in,MemWrite_in,ALUSrc_in;
input RegWrite_in,Sign_in;
input [1:0] MemToReg_in;
input [5:0] ALUFun_in , opCode_in;
input [31:0] PC_add_4_in;
input [3:0] aluop_in,ALUCtr_in;
input [31:0] expand_in, branch_in;
input flush_ID_EX,beq_bne_in;
output reg [31:0] PC_add_4_out,DataBusA_out,DataBusB_out,expand_out;
output reg [4:0] Rs_out,Rt_out, Rd_out,Shamt_out;
output reg [1:0] RegDst_out;
output reg [2:0] PCSrc_out;
output reg MemRead_out,MemWrite_out,beq_bne_out;
output reg [1:0] MemToReg_out;
output reg [5:0] ALUFun_out, opCode_out;
output reg ALUSrc_out,RegWrite_out,Sign_out, branch_out;
output reg [3:0] aluop_out,ALUCtr_out;
always @(posedge clk or negedge reset) begin
	if (reset || flush_ID_EX) begin
PC_add_4_out <= 32'h0000_0000;DataBusA_out <= 32'h0000_0000;
DataBusB_out <= 32'h0000_0000;expand_out <= 32'h0000_0000;
Rs_out <= 5'h00;	Rt_out <= 5'h00;
Rd_out <= 5'h00;	Shamt_out <= 5'h00; opCode_out<= 5'h00;
RegDst_out <= 2'h0;	PCSrc_out <= 3'h0;
MemRead_out <= 1'h0;MemWrite_out <= 1'h0;
MemToReg_out <= 2'h0;	ALUFun_out <= 6'h00;  aluop_out<=4'h0; ALUCtr_out<=4'h0;
ALUSrc_out <= 1'h0;	beq_bne_out<= 1'h0;
RegWrite_out <= 1'h0;	Sign_out <= 1'h0; branch_out <= 1'h0;
	end
else begin
    PC_add_4_out <= PC_add_4_in;
    DataBusA_out <= DataBusA_in;
    DataBusB_out <= DataBusB_in;
        Rs_out <= Rs_in;
        Rt_out <= Rt_in;
        Rd_out <= Rd_in;
        Shamt_out <= Shamt_in;
        RegDst_out <= RegDst_in;
        PCSrc_out <= PCSrc_in;
    MemRead_out <= MemRead_in;
    MemWrite_out <= MemWrite_in;
    MemToReg_out <= MemToReg_in;
        ALUFun_out <= ALUFun_in;
    ALUSrc_out <= ALUSrc_in;
    RegWrite_out <= RegWrite_in;
    Sign_out <= Sign_in;
    aluop_out<= aluop_in;
    ALUCtr_out<= ALUCtr_in;
    expand_out<= expand_in;
    branch_out <= branch_in;
    beq_bne_out <= beq_bne_in;
    opCode_out<=opCode_in;
            end
        end
    endmodule

