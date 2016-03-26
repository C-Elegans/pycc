all: main
	./main
main:main.o
	ld -lc main.o -o main
main.o:main.s
	as -c main.s -o main.o
main.s:main.c
	python compiler.py main.c main.s	
clean:
	rm *.s
	rm *.o
	rm main
check:
	python test.py
