op = input()

if '+' in op:
  num = op.split('+')
  print(int(num[0]) + int(num[1]))
elif '-' in op:
  num = op.split('-')
  print(int(num[0]) - int(num[1]))
elif '*' in op:
  num = op.split('*')
  print(int(num[0]) * int(num[1]))
else:
  num = op.split('/')
  print(int(num[0]) // int(num[1]))