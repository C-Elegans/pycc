
test(int x)-> int{
	print x*4
}
main() -> int{
	int x=0
	for(int i=0;i<=20;i++) {
		x=x+i
		test(i)
	}
	
	
	return 0

}
