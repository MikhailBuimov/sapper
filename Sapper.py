import random
import emoji
from wcwidth import wcswidth


class Field:
  def __init__(self, x, y):
    self.numbers = {0:emoji.emojize(":keycap_0:"), 1:emoji.emojize(":keycap_1:"), 2:emoji.emojize(":keycap_2:"),
                    3:emoji.emojize(":keycap_3:"), 4:emoji.emojize(":keycap_4:"), 5:emoji.emojize(":keycap_5:"),
                    6:emoji.emojize(":keycap_6:"), 7:emoji.emojize(":keycap_7:"), 8:emoji.emojize(":keycap_8:"),
                    9:emoji.emojize(":keycap_9:")}
    self.x=x
    self.y=y
    self.x_axies = [Field.num_to_emoji_num(i) for i in range(1, self.x+1)]
    self.y_axies = [Field.num_to_emoji_num(i) for i in range(1, self.y+1)] 
    self.field = [[emoji.emojize(":blue_square:")]*self.x for j in range(self.y)]
    self.alive=True
    self.bombs=[]
    self.found_bombs=[]
  @staticmethod
  def num_to_emoji_num(num):
    numbers = {0:emoji.emojize(":keycap_0:"), 1:emoji.emojize(":keycap_1:"), 2:emoji.emojize(":keycap_2:"),
                    3:emoji.emojize(":keycap_3:"), 4:emoji.emojize(":keycap_4:"), 5:emoji.emojize(":keycap_5:"),
                    6:emoji.emojize(":keycap_6:"), 7:emoji.emojize(":keycap_7:"), 8:emoji.emojize(":keycap_8:"),
                    9:emoji.emojize(":keycap_9:")}
    res = []
    while num:
      digit = num % 10
      res.append(numbers[digit])
      num=num//10
    return ' '.join(reversed(res))
  def fill_bombs(self, n):
    while n != len(self.bombs):
      x = random.choice(range(self.x))
      y = random.choice(range(self.y))
      if (x, y) not in self.bombs:
        self.bombs.append((x,y))

  def print_field(self):
    max_x = max(len(item) for item in self.x_axies)
    max_y = max(len(item) for item in self.y_axies)

    print('\\ x'+' '*(max_x-1), *[el.ljust(max_x+1, ' ') for el in self.x_axies])
    print('y\\')

    for i in range(1, len(self.field) + 1):
      current = self.y_axies[i - 1]
      formula = (max(max_y, len(current)) - min(max_y, len(current))) // 2 + len(current)
      y_label = str(current).ljust(formula, ' ')
      field_row = [el.ljust(max_x-1, ' ') for el in self.field[i - 1]]
      print(y_label, ' ', *field_row)


  def print_field_with_bombs(self):
    print('\\ x',*[Field.num_to_emoji_num(i) for i in range(1, self.x+1)])
    print('y\\')
    for i in range(1,len(self.field)+1):
      temp=[]
      for j in range(len(self.field[i-1])):
        if (j, i-1) in self.bombs:
          temp.append(emoji.emojize(':bomb:').strip())
        else:
          temp.append(emoji.emojize(":stop_button:")+' ')
      print(str(Field.num_to_emoji_num(i)).rjust(3),'   ', *temp, sep='')
  def empty_count(self):
    c = 0
    for i in self.field:
      for j in i:
        if j == emoji.emojize(":blue_square:"):
          c+=1
    return c
  def open_cells(self, x, y):
    for j in range(len(self.field)):
      for i in range(len(self.field[y])):
        if i in range(x-1, x+2) and j in range(y-1, y+2):
          if (i, j) in self.bombs and (i, j) not in self.found_bombs:
            self.found_bombs.append((i, j))
            self.field[j][i]=emoji.emojize(':bomb:')
            self.open_cells(i,j)
          elif (i, j) not in self.found_bombs:
            self.field[j][i]=emoji.emojize(":stop_button:")+' '

def correct_num(num, a, b):
  try:
    num=int(num)
  except:
    return False
  return num in range(a, b+1)
def correct_step(step, x, y):
  try:
    f, s=step.split()
    f = int(f)
    s = int(s)
  except:
    return False
  return f in range(1, x+2) and s in range(1, y+2)


x = input("Задаем ширину игрового поля. Введите число от 2 до 20: ")
while not correct_num(x, 2, 20):
  print('Некорректное значение!')
  x = input("Задаем ширину игрового поля. Введите число от 2 до 20:")
y = input("Задаем высоту игрового поля. Введите число от 2 до 20: ")
while not correct_num(y, 2, 20):
  print('Некорректное значение!')
  y = input("Задаем высоту игрового поля. Введите число от 2 до 20:")
x = int(x)
y = int(y)
max_bombs = x * y - 1
n_bombs = input(f'Задаем количество бомб. Введите число от 1 до {max_bombs}: ')
while not correct_num(n_bombs, 1, max_bombs):
  print('Некорректное значение!')
  n_bombs = input(f'Задаем количество бомб. Введите число от 1 до {max_bombs}: ')
n_bombs=int(n_bombs)

field = Field(x, y)
field.fill_bombs(n_bombs)
field.print_field()
while field.alive and len(field.found_bombs)!=n_bombs and field.empty_count()!=n_bombs-len(field.found_bombs):
  step = input('Не попадите на мину! Для хода введите координаты ячейки в формате "х y"')
  while not correct_step(step, x, y):
    print("Некорректный ввод!")
    step = input('Не попадите на мину! Для хода введите координаты ячейки в формате "х y"')
  step=tuple(map(lambda num:int(num)-1, step.split()))

  if step in field.bombs:
    print("МИНА! БУБУБУБУХХ!!!")
    print(emoji.emojize('💥💥💥'))
    field.print_field_with_bombs()
    print("Вы проиграли!")
    field.alive = False
  else:
    field.open_cells(step[0],step[1])
    field.print_field()
    print(f'Найденных мин: {len(field.found_bombs)}. Осталось обнаружить {n_bombs-len(field.found_bombs)}.')
if len(field.found_bombs)==n_bombs or field.empty_count()==n_bombs-len(field.found_bombs):
  field.print_field_with_bombs()
  print('Победа!')
  print(emoji.emojize('👏👏👏'))
print("Игра окончена")