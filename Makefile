all: test
	./test
test:test.o
	ld -lc test.o -o test
test.o:test.s
	as -c test.s -o test.o
test.s:test.c
	python compiler.py test.c test.s	
clean:
	rm *.o
	rm *.s
	rm test
