`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/17 15:55:47
// Design Name: 
// Module Name: DM_unit
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


module DM_unit(input clk, Wr,
             input reset,
            input [15:0] DMAdr, 
		     input [31:0] wd,
			 output reg[31:0] rd);
			reg [31:0] RAM[15:0]; 
//read
//always @ (posedge clk£©
//begin
// rd=RAM[DMAdr];
//end
//write
integer i;
always @ (posedge clk,posedge reset)
begin
    rd=RAM[DMAdr];
    if(reset)begin
        for(i = 0; i < 256; i = i + 1) 
            RAM[i]=0;       
    end	
    else if (Wr) begin
      RAM[DMAdr] =wd;
        end           
    end  
 endmodule

