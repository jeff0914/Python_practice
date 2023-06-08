in_txt = input()

i_list = in_txt.split(',')

m_list = i_list[0].split()
c_list = i_list[1].split()

count = 0

if m_list[0] in c_list:
  count += 1

if m_list[1] in c_list:
  count += 1

if m_list[2] in c_list:
  count += 1

if m_list[3] in c_list:
  count += 1

if m_list[4] in c_list:
  count += 1

if count < 3:
  print(0)
elif count == 3:
  print(100)
elif count == 4:
  print(1000)
else:
  print(10000)
