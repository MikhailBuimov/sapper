import random
import emoji

class Field:
  def __init__(self, x, y):
    self.x=x
    self.y=y
    self.field = [['X']*self.x for j in range(self.y)]
    self.alive=True
    self.bombs=[]
    self.find_bombs=0
  def fill_bombs(self, n):
    while n != len(self.bombs):
      x = random.choice(range(self.x))
      y = random.choice(range(self.y))
      if (x, y) not in self.bombs:
        self.bombs.append((x,y))
  def print_field(self):
    print('\\ x', ' ',*range(1, self.x+1), sep=' ')
    print('y\\')
    for i in range(1, len(self.field)+1):
      temp=[]
      for j in range(len(self.field[i-1])):
        temp.append(' '*(len(str(j))-1) + self.field[i-1][j])
      print(str(i).rjust(3),' ', *temp)
  def print_field_with_bombs(self):
    print('\\ x',' ', *range(1, self.x+1), sep=' ')
    print('y\\')
    for i in range(len(self.field)):
      temp=[str(i+1).rjust(3), ' ',]
      for j in range(len(self.field[i])):
        if (j, i) in self.bombs:
          temp.append(' '*(len(str(j))-1)+'*')
        else:
          temp.append(' '*(len(str(j))-1)+'O')
      print(*temp)
  def empty_count(self):
    c = 0
    for i in self.field:
      for j in i:
        if j == 'X':
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
while field.alive and field.find_bombs!=n_bombs and field.empty_count()!=n_bombs-field.find_bombs:
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
          field.field[y][x]='O'
          if (x, y) in field.bombs:
            field.field[y][x]='*'
            field.find_bombs+=1
    field.print_field()
    print(f'Найденных мин: {field.find_bombs}. Осталось обнаружить {n_bombs-field.find_bombs}.')
    if field.find_bombs==n_bombs or field.empty_count()==n_bombs-field.find_bombs:
      field.print_field_with_bombs()
      print('Победа!')
      print(emoji.emojize('👏👏👏'))
print("Игра окончена")