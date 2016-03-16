.intel_syntax noprefix
.data
_x:
.int 0
_y:
.int 0
.text
.globl start
start:
push 2
lea rax,[rip+x]
pop rbx
mov [rax],rbx
push 3
lea rax,[rip+y]
pop rbx
mov [rax],rbx

        

mov rax,2
lea rdi,[rip+printf_string]
mov rsi,'x'
mov rdx,[rip+_x]
call _printf

        

mov rax,2
lea rdi,[rip+printf_string]
mov rsi,'y'
mov rdx,[rip+_y]
call _printf

mov rax, 0x2000001
mov rdi, 0
syscall
printf_string: .asciz "%c: %d\n"
