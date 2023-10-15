import random
import emoji

class Field:
  def __init__(self, x, y):
    self.numbers = {0:emoji.emojize(":keycap_0:"), 1:emoji.emojize(":keycap_1:"), 2:emoji.emojize(":keycap_2:"),
                    3:emoji.emojize(":keycap_3:"), 4:emoji.emojize(":keycap_4:"), 5:emoji.emojize(":keycap_5:"),
                    6:emoji.emojize(":keycap_6:"), 7:emoji.emojize(":keycap_7:"), 8:emoji.emojize(":keycap_8:"),
                    9:emoji.emojize(":keycap_9:")}
    self.x=x
    self.y=y
    self.field = [[emoji.emojize(":blue_square:")]*self.x for j in range(self.y)]
    self.alive=True
    self.bombs=[]
    self.find_bombs=[]
  def fill_bombs(self, n):
    while n != len(self.bombs):
      x = random.choice(range(self.x))
      y = random.choice(range(self.y))
      if (x, y) not in self.bombs:
        self.bombs.append((x,y))
  def print_field(self):
    print('\\ x',*[self.numbers[i] for i in range(1, self.x+1)])
    print('y\\')
    for i in range(1, len(self.field)+1):
      temp=[]
      for j in range(len(self.field[i-1])):
        temp.append(self.field[i-1][j])
      print(str(self.numbers[i]).rjust(3)+'   ',*temp, sep='')
  def print_field_with_bombs(self):
    print('\\ x',*[self.numbers[i] for i in range(1, self.x+1)])
    print('y\\')
    for i in range(1,len(self.field)+1):
      temp=[]
      for j in range(len(self.field[i-1])):
        if (j, i-1) in self.bombs:
          temp.append(emoji.emojize(':bomb:').strip())
        else:
          temp.append(emoji.emojize(":stop_button:")+' ')
      print(str(self.numbers[i]).rjust(3),'   ', *temp, sep='')
  def empty_count(self):
    c = 0
    for i in self.field:
      for j in i:
        if j == emoji.emojize(":blue_square:"):
          c+=1
    return c
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

x = input("Задаем ширину игрового поля. Введите число от 2 до 100:")
while not correct_num(x, 2, 100):
  print('Некорректное значение!')
  x = input("Задаем ширину игрового поля. Введите число от 2 до 100:")
y = input("Задаем высоту игрового поля. Введите число от 2 до 100:")
while not correct_num(y, 2, 100):
  print('Некорректное значение!')
  y = input("Задаем высоту игрового поля. Введите число от 2 до 100:")
x = int(x)
y = int(y)
max_bombs = x * y - 1
n_bombs = input(f'Задаем количество бомб. Введите число от 1 до {max_bombs}')
while not correct_num(n_bombs, 1, max_bombs):
  print('Некорректное значение!')
  n_bombs = input(f'Задаем количество бомб. Введите число от 1 до {max_bombs}')
n_bombs=int(n_bombs)

field = Field(x, y)
field.fill_bombs(n_bombs)
field.print_field()
while field.alive and len(field.find_bombs)!=n_bombs and field.empty_count()!=n_bombs-len(field.find_bombs):
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
    for y in range(len(field.field)):
      for x in range(len(field.field[y])):
        if x in range(step[0]-1, step[0]+2) and y in range(step[1]-1, step[1]+2) and field.empty_count()!=0 and field.empty_count()!=len(field.bombs):
          if (x, y) in field.bombs:
            field.field[y][x]=emoji.emojize(":bomb:")
            if (x,y) not in field.find_bombs:
              field.find_bombs.append((x,y))
          else:
            field.field[y][x]=emoji.emojize(":stop_button:")+" "
    field.print_field()
    print(f'Найденных мин: {len(field.find_bombs)}. Осталось обнаружить {n_bombs-len(field.find_bombs)}.')
if len(field.find_bombs)==n_bombs or field.empty_count()==n_bombs-len(field.find_bombs):
  field.print_field_with_bombs()
  print('Победа!')
  print(emoji.emojize('👏👏👏'))
print("Игра окончена")