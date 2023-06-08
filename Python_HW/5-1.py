s = input()
res = []
for i in range(len(s)):
        char = s[i]
        if s.count(char) == 1:
            res.append(char)
        else:
            for j in range(i+1, len(s)):
                if s[j] == char:
                    break
            else:
                res.append(char)
print(''.join(res))