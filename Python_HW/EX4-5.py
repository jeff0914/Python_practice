num = int(input())
count = 0
while num > 0:
  if num % 2 == 0:
    num = num / 2
    count += 1
  elif num % 2 !=0:
    num = num -1
    count += 1
  else:
    num = 0
    break
print(count)
  

