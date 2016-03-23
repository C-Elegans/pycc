int y = 0
int blah = 4
test() -> int{
	int r=1
	return r
}
main() -> int{
	int x=0
	while(x<15){
		y=x
		y=~y
	
		x++
		print y
	}
	return 0
}
