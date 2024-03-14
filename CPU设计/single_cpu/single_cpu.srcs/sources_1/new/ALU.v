`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/16 23:08:34
// Design Name: 
// Module Name: ALU
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

module alu(aluCtr,A,B,F,ZF,CF,OF,SF,PF,shamt

    );
    parameter SIZE = 32;//����λ��
    
        input [4:0] shamt;
    
        input [3:0] aluCtr;//�������
        input [SIZE-1:0] A;//��������
        input [SIZE-1:0] B;//��������
        output [SIZE-1:0] F;//������
        output       ZF, //0��־λ, ������Ϊ0(ȫ��)����1, ������0
                     CF, //����λ��־λ, ȡ���λ��λC,�ӷ�ʱC=1��CF=1��ʾ�н�λ,����ʱC=0��CF=1��ʾ�н�λ
                       OF, //�����־λ�����з��������������壬�����OF=1������Ϊ0                     
                       SF, //���ű�־λ����F�����λ��ͬ
                     PF; //��ż��־λ��F��������1����PF=1������Ϊ0    
       reg [SIZE-1:0] F;
        reg C,ZF,CF,OF,SF,PF;//CΪ���λ��λ
        always@(*)
        begin
            C=0;
            case(aluCtr)
                4'b0000:begin F=A&B; end    //��λ��
                4'b0001:begin F=A|B; end    //��λ��
                4'b0100:begin F=~(A|B); end    //nor
                4'b1100:begin F=A^B; end    //��λ���
                4'b0101:begin F=B>>shamt; end //��B����shamtλ
                4'b1010:begin F=B>>A; end //��B����Aλ  (srlv)
                4'b1000:begin F=($signed(B)) >>> shamt; end //sra
                4'b1011:begin F=($signed(B)) >>> A; end //srav
                4'b0010:begin {C,F}=A+B; end //�ӷ�
                4'b0110:begin {C,F}=A-B; end //����
                  4'b0111:begin F=A<B; end//A<B��F=1������F=0 slt           
                 4'b0011:begin F= B << shamt; end   //��B����shantλ
                 4'b1001:begin F= B << A; end   //��B����Aλ
                 4'b1101:begin F= B << 16; end   //��B����16λ
            endcase
            ZF = F==0;//FȫΪ0����ZF=1
            CF = C; //��λ��λ��־
            OF = A[SIZE-1]^B[SIZE-1]^F[SIZE-1]^C;//�����־��ʽ
            SF = F[SIZE-1];//���ű�־,ȡF�����λ
            PF = ~^F;//��ż��־��F��������1����F=1��ż����1����F=0
        end

endmodule

