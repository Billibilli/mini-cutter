def fib(max):
	a,b=0,1
	while a<max:
		print "haha"
		yield a
		a,b=b,a+b

for n in fib(1000):
	print n
