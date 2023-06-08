# t = input()
# n1, n2 = t.split()
# n1 = int(n1)
# n2 = int(n2)

# i = 0
# while i < n1:
#     j = 0
#     while j < n2:
#         print(f'{i+1}x{j+1}={(i+1)*(j+1)}')
#         j += 1
#     i += 1

t = input()
i1, k1 = t.split()
i1 = int(i1)
k1 = int(k1)

g = 0
while g < i1:
   f = 0
   while f < k1:
      if g == f:
        f += 1
        continue
      print(f'{g+1}x{f+1}={(g+1)*(f+1)}')
      f += 1  
   g += 1