`timescale 1ns / 1ps
module next_pc(
input branch, 
input zero, 
input jmp, 
input jr,
input clkin,
input [31:0] expand,
input [31:0] instruction,
input reset,
input [31:0]RsData,
input jal,
output reg[31:0]jrpc,
output reg[31:0] pc
); 
    wire PCSrc1, PCSrc2;
    wire [31:0] J_Addr,branch_Addr;
    reg [31:0] add4,next_pc;
    wire z;     
    assign z = instruction[26] ? ~zero :zero;  //beq和bne
    assign branch_Addr = add4 + (expand << 2);
    assign J_Addr =jr? RsData:{add4[31:28], instruction[25:0], 2'b00}; 
    //PC的多选器
    assign PCSrc1 = (branch & z)? 1'b1:1'b0;
   assign PCSrc2 = (jmp | jr)? 1'b1:1'b0;
    always@(*)begin
        casex({PCSrc2, PCSrc1})
            2'b00:next_pc<=add4;
            2'b01:next_pc<=branch_Addr;
            2'b1x:next_pc<=J_Addr;
            default:next_pc<=add4;
        endcase
end
always@ (posedge clkin)
begin
if(reset) begin pc = 32'b00000000010000000000000000000000; add4 = pc+4;end
else begin jrpc = jal ? pc+4 : 0;pc = next_pc; add4 = pc+4;end
end
endmodule
