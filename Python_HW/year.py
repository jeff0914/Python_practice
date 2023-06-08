year = int(input())
text = 'a normal year'               
if year%4 == 0:
    text = 'a leap year'           
if year%100 == 0:
    text = 'a normal year'          
if year%400 == 0:
    text = 'a leap year'           
print(f'{text}')


