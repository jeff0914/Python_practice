# m = input()
# x = 0
# y = 0
# for i in m:
#   if i == "U":
#     y += 1
#   elif i == "D":
#     y += -1
#   elif i == "L":
#     x += -1
#   else:
#     i == "R"
#     x += 1
# if x == 0 and y == 0:
#   print("Y")
# else:
#   print("N")



class Robot:

    def __init__ (self, x:int, y:int, actions:str) -> None:
        self.x = x
        self.y = y
        self.orgin_x = x
        self.orgin_y = y
        for action in actions:
          if action == "U":
            self.up()
          elif action == "D":
            self.down()
          elif action == "L":
            self.left()
          else:
            action == "R"
            self.right()  
    
    def is_org(self) -> bool:
        return self.x == self.orgin_x and self.y == self.orgin_y

    def up(self) -> None:
        self.y += 1

    def down(self) -> None:
        self.y += -1

    def left(self) -> None:
        self.x += -1

    def right(self) -> None:
        self.x += 1

    def __str__(self) ->str:
        return f'{self.x},{self.y}'

print(Robot(0, 0, "DDDDDLLDUUURRRR"))
actions = (Robot(0, 0, "DDDDDLLDUUURRRR"))  
print(actions.is_org())