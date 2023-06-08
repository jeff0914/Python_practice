#print((lambda n : (n[1]+200-n[0])%200)([int(i) for i in input().split()]))

a = list(map(int, input().split()))
x = int(a[0])
y = int(a[1])
z= x - y
print(abs(z))
