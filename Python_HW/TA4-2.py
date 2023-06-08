# n = input()
# for i in range(1,int(n)):
#     print('*' * i)
n = input()
n1 = int(n)
r = 1
while r <= n1 :
    c = 1			
    while c <= r:
        print('*',end='')	
        c += 1
    print()			 
    r +=1


