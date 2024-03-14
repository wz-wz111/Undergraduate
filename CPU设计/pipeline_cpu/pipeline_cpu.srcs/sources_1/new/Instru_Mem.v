`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/12/23 22:46:09
// Design Name: 
// Module Name: Instru_Mem
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


module InstMemory(
    input [31:0] ReadAddress,
    output reg [31:0] Instruction
    );
    reg [63:0] InstMemoryFile[31:0];
    
    always @(ReadAddress)
    begin
       Instruction=InstMemoryFile[(ReadAddress>>2)];
    end
    
    initial begin
    
        $readmemb("C:\Users\HUAWEI\Desktop\cpu.txt",InstMemoryFile);
    end
endmodule
