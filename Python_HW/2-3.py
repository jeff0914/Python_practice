a = input()

q = int(a)

s = [0, 1]

while not (len(s) >= q):
    s.append(s[-1] + s[-2])

print(s[q - 1])