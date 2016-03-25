
test(int x)-> int{
	return x*4
}
main() -> int{
	int x=0
	for(int i=0;i<=20;i++) {
		x=x+i
		print test(i)
	}
	
	
	return 0
}
