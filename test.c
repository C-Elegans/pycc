int y = 0
test() -> int{
	int r=1
	y=1
	return r
}
 main() -> int{
	int x=0
	test()
	x=5
	x=x+y
	y=x
	
	return 0
}
