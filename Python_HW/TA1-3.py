txt = input()

i_list = txt.split()

c_list = ['星期五', '星期六','星期日']

if i_list[0] in c_list:
  print('不開市')
else:
  print(int(i_list[1]) * int(i_list[2]))