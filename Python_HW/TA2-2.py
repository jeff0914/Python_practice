

num = input()
list = num.split()
a = str()
i = 0
while i < len(list):
  a += str(int(list[i]) + 1) +' '
  i += 1

print(a.strip())

#--------------------------------------------while and for 迴圈

q = input()

q_sp = q.split()

answer = []
for s in q_sp:
  answer.append(str(int(s)+1))
print(''.join(answer))

#----------------------------------------------串列程式

print(''.join([str(int(s)) +1 for s in input().split()]))

