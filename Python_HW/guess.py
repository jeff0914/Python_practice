import random

secret_num = random.randint(1,100)

start_num = 1
end_num = 100

while True:
  guess = int(input(f'由{start_num}~{end_num}猜一個數字:'))
  if guess == secret_num:
    print("猜對啦!")
    break
  else:
    if guess < secret_num:
      start_num = guess
    else:
      end_num = guess

