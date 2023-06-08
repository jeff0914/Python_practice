i = 0
n = int(input())
list1= []

for s in range(i, n + 1):
  if s > 1:
    for i in range(2, s):
      if (s % i) == 0:
        break
    else:
      list1.append(s)
list2 =list1[::-1]
print(list2[0])