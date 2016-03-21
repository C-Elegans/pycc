.intel_syntax noprefix
.data
_y: .int 0
.text
.globl test
_test:
push rbp
mov rbp,rsp
sub rsp,16
mov DWORD PTR [rbp-4],1
mov eax,[rbp-4]
 
mov rsp,rbp
pop rbp
ret
.globl main
_main:
push rbp
mov rbp,rsp
sub rsp,16
mov DWORD PTR [rbp-4],1
mov eax,[rbp-4]
push rax
mov DWORD PTR [rip+_y],1
mov eax,[rbp-4]
push rax
cmp rax,0
je block_0_end
//if
block_0_begin:
mov DWORD PTR [rip+_y],1
block_0_end:
xor rax,rax
mov rsp,rbp
pop rbp
ret

.globl start
start:
call _main

mov rax,2
lea rdi,[rip+printf_string]
mov rsi,'y'
mov rdx,[rip+_y]
call _printf

mov rax, 0x2000001
mov rdi, 0
syscall
printf_string: .asciz "%c: %d\n"
