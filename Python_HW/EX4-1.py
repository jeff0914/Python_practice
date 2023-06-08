str = input("")
str1_reversed=("")
i = len(str)
while i > 0: 
    str1_reversed += str[i-1]
    i = i - 1
print(str1_reversed) 