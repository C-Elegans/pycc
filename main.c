
fib(int n) -> int{
	if(n==0){
	return 0
	}
	if(n==1){
	return 1
	}
	int n1 = fib(n-1)
	int n2 = fib(n-2)
	return n1+n2
}
main() -> int{
	for(int i=1;i<20;i++){
	print fib(i)
	
	}
	
	return 0

}
