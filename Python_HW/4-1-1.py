q = input("")

q_sp = q.split()

i = 0
answer = []
while i < len(q_sp):
  answer.append(q_sp[i][::-1])

  i += 1
print(' '.join(answer))
