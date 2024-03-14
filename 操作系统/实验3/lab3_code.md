# 任务二
~~~
;org 0x7c00
[bits 16]
xor ax, ax ; eax = 0
; 初始化段寄存器, 段地址全部设为0
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

; 初始化栈指针
mov sp, 0x7c00
mov ax, 1                ; 逻辑扇区号第0~15位
mov cx, 0                ; 逻辑扇区号第16~31位
mov bx, 0x7e00           ; bootloader的加载地址
load_bootloader:
    call asm_read_hard_disk  ; 读取硬盘
    inc ax
    cmp ax, 5
    jle load_bootloader
jmp 0x0000:0x7e00        ; 跳转到bootloader

jmp $ ; 死循环

asm_read_hard_disk:                           
; 从硬盘读取一个逻辑扇区

; 参数列表
; ax=逻辑扇区号0~15位
; cx=逻辑扇区号16~28位
; ds:bx=读取出的数据放入地址
    push ax             ;保证逻辑扇区号不会被改变
    push cx
;LBA ->  CHS
    xor dx, dx
    div word[SectorsPerTrack]       ;得到（LBA DIV PS）和 （LBA MOD PS）
    inc dl
    mov byte[sector],dl                 ;扇区编号从1开始
    xor dx, dx
    div  word [HeadsPerCylinder]        ;得到（LBA DIV PS）MOD PH 和 LBA DIV（PH×PS）
    mov  byte [head], dl
    mov  byte [cylinder], al
    
;
    mov ah, 02h      ; AH = 02h，读取扇区
    mov al, 01h      ; AL = 01h，读取一个扇区
    mov ch, [cylinder] ; cylinder是逻辑扇区号转换后的柱面号
    mov dh, [head]     ; head是逻辑扇区号转换后的磁头号
    mov cl, [sector]   ; sector是逻辑扇区号转换后的扇区号
    mov dl, 80h      ; DL = 80h，读取80h号硬盘
    int 0x13          ; 调用INT 13h中断读取硬盘数据
    add bx,512
    pop cx
    pop ax
    ret

cylinder db 0
head db 0
sector db 0
SectorsPerTrack dw  63
HeadsPerCylinder dw 18


times 510 - ($ - $$) db 0
db 0x55, 0xaa
~~~

# 任务四
~~~
%include "boot.inc"
;org 0x7e00
[bits 16]
;清屏
mov ah,0x00
mov ax,3
int 0x10

;空描述符
mov dword [GDT_START_ADDRESS+0x00],0x00
mov dword [GDT_START_ADDRESS+0x04],0x00  

;创建描述符，这是一个数据段，对应0~4GB的线性地址空间
mov dword [GDT_START_ADDRESS+0x08],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x0c],0x00cf9200    ; 粒度为4KB，存储器段描述符 

;建立保护模式下的堆栈段描述符      
mov dword [GDT_START_ADDRESS+0x10],0x00000000    ; 基地址为0x00000000，界限0x0 
mov dword [GDT_START_ADDRESS+0x14],0x00409600    ; 粒度为1个字节

;建立保护模式下的显存描述符   
mov dword [GDT_START_ADDRESS+0x18],0x80007fff    ; 基地址为0x000B8000，界限0x07FFF 
mov dword [GDT_START_ADDRESS+0x1c],0x0040920b    ; 粒度为字节

;创建保护模式下平坦模式代码段描述符
mov dword [GDT_START_ADDRESS+0x20],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x24],0x00cf9800    ; 粒度为4kb，代码段描述符 

;初始化描述符表寄存器GDTR
mov word [pgdt], 39      ;描述符表的界限   
lgdt [pgdt]
      
in al,0x92                         ;南桥芯片内的端口 
or al,0000_0010B
out 0x92,al                        ;打开A20
在进入保护模式后，按照如下要求，编写并执行一个自己定义的32位汇编程序，要求简单说一说你的实现思路，并提供结果截图。
使用两种不同的自定义颜色和一个自定义的起始位置(x,y)，使得bootloader加载后，在显示屏坐标(x,y)处开始输出自己的学号+姓名拼音首字母缩写，要求相邻字符前景色和背景色必须是相互对调的。公告图片中提供了学号为21307233，姓名为宋小宝，自定义位置(12,12)的输出样式，仅供参考
cli                                ;中断机制尚未工作
mov eax,cr0
or eax,1
mov cr0,eax                        ;设置PE位
      
;以下进入保护模式
jmp dword CODE_SELECTOR:protect_mode_begin

;16位的描述符选择子：32位偏移
;清流水线并串行化处理器
[bits 32]           
protect_mode_begin:                              

mov eax, DATA_SELECTOR                     ;加载数据段(0..4GB)选择子
mov ds, eax
mov es, eax
mov eax, STACK_SELECTOR
mov ss, eax
mov eax, VIDEO_SELECTOR
mov gs, eax

;使用两种不同的自定义颜色和一个自定义的起始位置(x,y)，
;使得bootloader加载后，在显示屏坐标(x,y)处开始输出自己的学号+姓名拼音首字母缩写，
;要求相邻字符前景色和背景色必须是相互对调的。
;公告图片中提供了学号为21307233，姓名为宋小宝，自定义位置(12,12)的输出样式，仅供参考。


mov ecx, my_string_end - my_string
mov ebx, 0x366
mov esi, my_string
output_my_string:
    mov ah, 0x15
    mov al, [esi]
    mov word[gs:bx], ax
    inc esi
    add ebx,2
    mov ah, 0x51
    mov al, [esi]
    mov word[gs:bx], ax
    inc esi
    add ebx,2
    sub ecx,1
    loop output_my_string


jmp $ ; 死循环

pgdt dw 0
     dd GDT_START_ADDRESS

my_string db '21307371wz'
my_string_end:

~~~