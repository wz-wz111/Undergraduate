[bits 32]

global asm_hello_world

asm_hello_world:
    push eax
    xor eax, eax

    mov ecx, my_string_end - my_string
    xor ebx,ebx
    mov esi, my_string
    output_my_string:
        mov ah, 0x15
        mov al, [esi]
        mov word[gs:bx], ax
        inc esi
        add ebx,2
        loop output_my_string

        pop eax
        ret

my_string db '21307371wz'
my_string_end:
