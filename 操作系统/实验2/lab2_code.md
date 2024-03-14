# Q14
~~~
org 0x7c00
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
mov ax, 0xb800
mov gs, ax

;清屏
mov ah,0x00
mov ax,3
int 0x10
;移动光标
mov ah,0x02
mov bh,0
mov dh,0
mov dl,34
int 0x10
;打印名字、学号
mov bh,0
mov ah,0x0e 
mov al, 'W'
int 10h
mov al, 'u'
int 10h
mov al, 'Z'
int 10h
mov al, 'h'
int 10h
mov al, 'e'
int 10h
mov al, 'n'
int 10h
mov al, ' '
int 10h
mov al, '2';
int 10h
mov al, '1'
int 10h
mov al, '3'
int 10h
mov al, '0'
int 10h
mov al, '7'
int 10h
mov al, '3'
int 10h
mov al, '7'
int 10h
mov al, '1'
int 10h
;

;字符弹射

drow dw 1         ;每次row的位移
dcol dw 1         ;每次col的位移
;初始位置
row dw 2
col dw 0

mov al,0x30
Start:
    push ax
    mov dx,[row]    ;dx--row
    mov cx,[col]       ;cx--col
    Row_judge:
        cmp dx,1
        je  down
        cmp dx,23
        je  up
    Col_judge:
        cmp cx,0
        je  right
        cmp cx,79
        je  left
    ;未触及边界
    jmp my_print

    up:
        mov ax,-1
        mov [drow],ax
        jmp Col_judge
    down:
        mov ax,1
        mov [drow],ax
        jmp Col_judge
    left:
        mov ax,-1
        mov [dcol],ax
        jmp my_print
    right:
        mov ax,1
        mov [dcol],ax
        jmp my_print

    my_print:
        pop ax
        ;得到当前位置
        add dx,[drow]
        add cx,[dcol]
        mov [row],dx
        mov [col],cx
        ;设置数字
        mov ah,dl
        add al,3
        cmp al,0x3a
        jl less_then
        sub al,10
    less_then:
        ;打印
        imul bx,dx,80
        add bx,cx
        imul bx,2
        mov [gs:bx],ax
        ;对称打印
        sub al,1
        ;计算对称Row
        mov bx, 24
        sub bx, dx
        mov dx, bx
        ;计算对称Col
        mov bx, 80
        sub bx, cx
        mov cx, bx
        ;打印
        imul bx, dx, 80
        add bx, cx ; cor = 80 * row + col
        imul bx, 2
        mov [gs:bx], ax


    push cx
    mov cx,0x7777
delay_1:
    push cx
    mov cx,0x77
delay_2:
    loop delay_2
    pop cx
    loop delay_1
    pop cx
;---------------------
jmp Start

jmp $ ; 死循环

times 510 - ($ - $$) db 0
db 0x55, 0xaa
~~~

# Q16
## (1)
~~~
org 0x7c00
[bits 16]
mov ah, 0x03       ; 设置BIOS中断功能号为0x03，表示获取光标位置
mov bh, 0x00       ; 设置显示页面号为0
int 0x10           ; 调用BIOS中断0x10
mov ah, 0x02       ; 设置BIOS中断功能号为0x02，表示设置光标位置
mov bh, 0x00       ; 设置显示页面号为0
mov dh, dl         ; 将光标的列号移动到行号中
mov dl, 0x01       ; 设置光标所在的列号
int 0x10           ; 调用BIOS中断0x10
jmp $ ; 死循环

times 510 - ($ - $$) db 0
db 0x55, 0xaa
~~~
## (2)
~~~
org 0x7c00      ; 设置代码起始地址
bits 16          ; 设置为16位模式

msg db "21307371", 0    ; 字符串末尾需要添加一个null字符

start:
    mov ax, 0       ; 清空AX寄存器
    mov ds, ax      ; 将DS寄存器设置为0
    mov ah, 0x0e    
    mov bh,0

    mov si, msg    ; 将SI寄存器设置为字符串的地址
    call print_str  ; 调用打印字符串的函数

    ; 无限循环
    jmp $           ; 跳回当前地址

print_str:
    lodsb           ; 从SI指向的地址读取一个字节到AL寄存器，并将SI自动加1
    or al, al       ; 检查AL寄存器是否为0
    jz done         ; 如果为0，结束函数
    int 0x10        ; 调用屏幕中断服务程序，打印字符
    jmp print_str   ; 继续打印下一个字符
done:
    ret             ; 返回

times 510-($-$$) db 0 ; 填充剩余的空间，使代码长度为510字节
dw 0xaa55             ; 添加引导扇区的标志
~~~
## (3)
~~~
org 0x7c00 ;程序入口地址
[bits 16]
xor ax, ax ; eax = 0
;初始化段寄存器,段地址全部设为0
mov ds, ax
mov ss,ax
mov es,ax
mov fs, ax
mov gs, ax

mov sp,0x7c00
mov ax,0xb800
mov gs,ax
; 获取光标位置
mov ah, 0x03 
mov bh,0x00
int 0x10

keyboard_input:
mov ah, 0x00    ;键盘输入
int 0x16
cmp al,0x1b     ;判断输入是否为esc，若是则结束
je end

input:
;设置光标位置
mov ah ,0x02
mov bh, 0x00
int 0x10
add dl, 1       ;移向下一位
mov ah, 0x09
mov bh ,0X00
mov bl,0x04     
mov cx,0x01
int 0x10        ;打印字符

jmp keyboard_input

end:
jmp $ ; 死循环

times 510 - ($ - $$) db 0
db 0x55, 0xaa
~~~
# Q17
~~~
; If you meet compile error, try 'sudo apt install gcc-multilib g++-multilib' first

%include "head.include"
; you code here

your_if:
mov eax,[a1]
xor ebx,ebx
cmp eax, 12        ;比较a1和12的大小
jl if_less_than_12 ;如果a1小于12，跳转到if_less_than_12标签
cmp eax, 24        ;比较a1和24的大小
jl if_less_than_24 ;如果a1小于24，跳转到if_less_than_24标签
shl eax, 4         ;将a1左移4位，相当于a1乘以16
mov ebx, eax       ;将结果存储到if_flag中
jmp end_if         ;跳转到end_if标签，结束if语句
if_less_than_12:
shr eax, 1         ;将a1右移1位，相当于除以2
add eax, 1         ;将a1除以2后再加1
mov ebx, eax       ;将结果存储到if_flag中
jmp end_if         ;跳转到end_if标签，结束if语句
if_less_than_24:
mov ebx, 24         ;将24存储到if_flag中
sub ebx, eax        ;计算24-a1的值
imul ebx, eax       ;将24-a1乘以a1
end_if:
mov [if_flag],ebx

; put your implementation here

your_while:
mov ecx, [a2]              ; 将a2存储到ECX寄存器中
while_loop:
    cmp ecx, 12          ; 比较ECX和12
    jl end_while         ; 如果ECX < 12，则跳出while循环
    call my_random       ; 调用my_random函数，将随机数存储在EAX中
    mov edx,ecx
    sub edx,12
    add edx,[while_flag]
    mov [edx], eax  ; 将随机数存储在while_flag数组中
    dec ecx              ; 将ECX减1
    jmp while_loop       ; 跳转到while循环的开头
end_while:
mov [a2],ecx



; put your implementation here

%include "end.include"

your_function:
; put your implementation here
mov ecx,[your_string]
my_while:
pushad
push word [ecx];
mov di, [ecx]
call print_a_char
pop bx
popad
inc ecx
mov al,[ecx]
cmp al,0
jne my_while

ret

~~~