_main:
	and rsp,~15
	mov rdi,1
	lea rsi,[rip+outstr]
	mov rdx,1
	mov rax,0
	call _fprintf
	call _exit
	
outstr:
	.asciz "%d\n"
