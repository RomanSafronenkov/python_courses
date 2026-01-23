from random import randint, choice

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        """
        x, y - координаты начала расположения корабля (целые числа);
        length - длина корабля (число палуб: целое значение: 1, 2, 3 или 4);
        tp - ориентация корабля (1 - горизонтальная; 2 - вертикальная).
        """
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        
        self._is_move = True  # может ли перемещаться, при попадании перемещаться уже нельзя
        self._cells = [1 for _ in range(length)]  # 1 - попадания не было, 2 - попадание
        
        self._ship_coords = None
        self._update_coords()
        
    def __setattr__(self, key, value):
        if key == '_tp' and value not in [1, 2]:
            raise ValueError("Ориентация может быть 1 или 2")
        super().__setattr__(key, value)
        
    def _update_coords(self):
        if self._x is not None and self._y is not None:
            if self._tp == 1:
                self._ship_coords = [(self._x+i, self._y) for i in range(self._length)]
            elif self._tp == 2:
                self._ship_coords = [(self._x, self._y+i) for i in range(self._length)]
        
    def set_start_coords(self, x ,y):
        """
        установка начальных координат (запись значений в локальные атрибуты _x, _y)
        """
        self._x = x
        self._y = y
        self._update_coords()
    
    def get_start_coords(self):
        """
        получение начальных координат корабля в виде кортежа x, y
        """
        return self._x, self._y
    
    def move(self, go):
        """
        перемещение корабля в направлении его ориентации на go клеток
        (go = 1 - движение в одну сторону на клетку; go = -1 - движение в другую сторону на одну клетку);
        движение возможно только если флаг _is_move = True
        """
        x = self._x
        y = self._y
        
        if self._is_move:
            if self._tp == 1:
                x += go
            elif self._tp == 2:
                y += go
        self.set_start_coords(x, y)
    
    @staticmethod
    def _create_coord_list(ship):         
        # надо сделать список координат коробля+слой вокруг коробля
        ship_coords = ship._ship_coords[:]
        
        for coord in ship_coords[:]:
            for i in range(-1, 2):
                ship_coords.extend([(coord[0]+i, coord[1]+1), (coord[0]+i, coord[1]), (coord[0]+i, coord[1]-1)])
        return set(ship_coords)
    
    def is_collide(self, ship):
        """
        проверка на столкновение с другим кораблем ship
        (столкновением считается, если другой корабль или пересекается с текущим или просто
        соприкасается, в том числе и по диагонали);
        метод возвращает True, если столкновение есть и False - в противном случае;
        """
        ship_coords_with_extra_layer = self._create_coord_list(self)
        other_ship_coords = set(ship._ship_coords)
        
        # если координаты одного корабля попадают в координаты второго+доп слой вокруг него - столкновение
        return len(ship_coords_with_extra_layer & other_ship_coords) != 0
    
    def is_out_pole(self, size):
        """
        проверка на выход корабля за пределы игрового поля (size - размер игрового поля, обычно, size = 10);
        возвращается булево значение True, если корабль вышел из игрового поля и False - в противном случае;
        """
        return any([x >= size or y >= size for x, y in self._ship_coords])
    
    def __getitem__(self, index):
        return self._cells[index]
    
    def __setitem__(self, index, value):
        if value not in [1, 2]:
            raise ValueError("Значения ячеек должны быть 1 или 2")
        self._cells[index] = value


class GamePole:
    def __init__(self, size, movement_allowed=True):
        self._size = size
        self._ships = []
        
        self.init()
        
        if not movement_allowed:
            for ship in self._ships:
                ship._is_move = False
        
    def init(self):
        """
        начальная инициализация игрового поля; здесь создается список из кораблей (объектов класса Ship):
        однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1
        (ориентация этих кораблей должна быть случайной).
        """
        self._ships = [Ship(4, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))
                      ]
        
        # расстановка случайным образом, при маленьком поле могут влезть не все корабли!
        
        # доступные координаты
        awailable_coords = [(i, j) for i in range(self._size) for j in range(self._size)]
        placed_ships = []
        
        for ship in self._ships:
            # скопируем доступные координаты, чтобы убрать те, которые выходят за пределы поля
            awailable_coords_for_ship = awailable_coords[:]
            
            # в зависимости от ориентации, нужно убирать разные координаты из числа доступных
            length, tp = ship._length, ship._tp
            if tp == 1:
                awailable_coords_for_ship = list(
                    filter(lambda x: x[0] <= self._size - length, awailable_coords_for_ship))
            elif tp == 2:
                awailable_coords_for_ship = list(
                    filter(lambda x: x[1] <= self._size - length, awailable_coords_for_ship))
                
            
            # из оставшихся случайно выбираем координату
            while True:
                # выбираем координату
                x, y = choice(awailable_coords_for_ship)
                ship.set_start_coords(x, y)
                
                # проверяем что при выбранных координатах нет столкновения с другими кораблями
                not_collided = True
                for other_ship in placed_ships:
                    not_collided &= ~ship.is_collide(other_ship)
                    
                if not_collided:
                    # если столкновения нет, прерываем цикл, мы нашли место для корабля
                    break
                else:
                    # если есть столкновение, то удаляем найденную координату из вариантов и повторяем цикл
                    del awailable_coords_for_ship[awailable_coords_for_ship.index((x, y))]
                    ship.set_start_coords(None, None)
            
            # убираем из числа координат те, которые уже заняты
            # либо те, установка в которые приведет к столкновению
            ship_coords = ship._create_coord_list(ship)
            awailable_coords = [coord for coord in awailable_coords if coord not in ship_coords]
            placed_ships.append(ship)
                
    
    def get_ships(self):
        return self._ships
    
    def move_ships(self):
        """
        перемещает каждый корабль из коллекции _ships на одну клетку
        (случайным образом вперед или назад) в направлении ориентации корабля;
        если перемещение в выбранную сторону невозможно (другой корабль или пределы игрового поля),
        то попытаться переместиться в противоположную сторону, иначе (если перемещения невозможны),
        оставаться на месте;
        """
        for ship in self._ships:
            if not ship._is_move:  # если кораблю нельзя перемещаться (в него попали)
                continue
            
            # выбираем случайное направление движения и идем в эту сторону
            go = choice([-1, 1])
            ship.move(go)
            
            movement_allowed = True
            for other_ship in self._ships:
                if other_ship == ship:
                    continue
                    
                # нет ли столкновений с другими кораблями
                movement_allowed &= ~ship.is_collide(other_ship)
            
            # не выходит ли корабль после перемещения за игровое поле
            movement_allowed &= ~ship.is_out_pole(self._size)
            
            # отрицательных координат быть не должно
            movement_allowed &= all([coord[0] >= 0 and coord[1] >= 0 for coord in ship._ship_coords])

            if not movement_allowed:  # если в выбранном направлении нельзя перемещаться
                ship.move(-2*go)  # вернуться где был и шагнуть один раз в противоположную сторону
                
                opposite_movement_allowed = True
                for other_ship in self._ships:
                    if other_ship == ship:
                        continue

                    # нет ли столкновений с другими кораблями
                    opposite_movement_allowed &= ~ship.is_collide(other_ship)
                    
                # не выходит ли корабль после перемещения за игровое поле
                opposite_movement_allowed &= ~ship.is_out_pole(self._size)
                
                # отрицательных координат быть не должно
                opposite_movement_allowed &= all([coord[0] >= 0 and coord[1] >= 0 for coord in ship._ship_coords])
                
                if not opposite_movement_allowed:  # если никуда нельзя перемещаться: вернуться где был
                    ship.move(go)
                
    
    def show(self, prettified=True):
        """
        отображение игрового поля в консоли
        (корабли должны отображаться значениями из коллекции _cells каждого корабля, вода - значением 0);
        """
        if not prettified:
            view = ""
            pole = self.get_pole()

            for row in pole:
                view += ' '.join(list(map(str, row))) + '\n'
            view = view.rstrip('\n')
            print(view)
        
        # отображение с координатами + с символами юникода
        else:
            mapping = {
                0: "\u25A0",
                1: "\u25A1",
                2: "\u2670"
            }

            view = "  " + " ".join(list(map(str, range(self._size)))) + "\n"
            pole = self.get_pole()

            for i, row in enumerate(pole):
                view += f'{i} ' + ' '.join(list(map(lambda x: mapping[x], row))) + '\n'
            view = view.rstrip('\n')
            print(view)
    
    def get_pole(self):
        """
        получение текущего игрового поля
        в виде двумерного (вложенного) кортежа размерами size x size элементов.
        """
        pole = [[0 for i in range(self._size)] for j in range(self._size)]
        for ship in self._ships:
            coords = ship._ship_coords
            for i, coord in enumerate(coords):
                pole[coord[0]][coord[1]] = ship[i]
        return tuple([tuple(row) for row in pole])
    

class SeaBattle:
    def __init__(self, size=10, movement_allowed=False):
        """
        Инциализация игры Морской бой
        Включает в себя задание параметра size: размер игрового поля
        
        В данной версии игры после каждого хода неповрежденные корабли могут перемещаться на 1 клетку
        Если не мешают другим кораблям и не выходят за границы поля
        
        Игра продолжается до тех пор, пока не выиграет игрок или компьютер
        """
        self._size = size
        self.movement_allowed = movement_allowed
        
        self.player_pole = GamePole(size, movement_allowed)
        self.player_made_shots = [[0 for i in range(self._size)] for j in range(self._size)]
        
        self.computer_pole = GamePole(size, movement_allowed)
        self.computer_made_shots = [[0 for i in range(self._size)] for j in range(self._size)]
        
    def play(self):
        """
        Логика игры, поочередно делаются ходы до тех пор, пока не найдется победитель
        """
        while True:
            self.player_turn()
            self.computer_turn()
            
            if self.is_win("player"):
                print('Поздравляем! Вы выиграли!')
                break
                
            if self.is_win("computer"):
                print('Увы, неудача!')
                break
    
    def player_turn(self):
        """
        Логика хода игрока
        """
        
        # посмотрим на сделанные выстрелы и на свое поле
        self.show_made_shots("player")
        print()
        self.player_pole.show()
        
        # сделаем ход, пока идут попадания делаем ходы дальше
        while True:
            try:
                x, y = map(int, input("Введите координаты для выстрела через пробел: ").split())
            except Exception:
                continue
            
            if not self.check_shot("player", (x, y)):
                print("Промах!")
                break
                
            else:
                print(f"Попадание! {(x, y)}")
                
    def computer_turn(self, debug=False):
        """
        Логика хода компьютера
        """
        if debug:
            # посмотрим на сделанные выстрелы и на свое поле
            self.show_made_shots("computer")
            print()
            self.computer_pole.show()
        
        # сделаем ход, пока идут попадания делаем ходы дальше
        while True:
            # нет смысла стрелять в уже подбитые корабли
            helper = self.computer_made_shots
            
            # стреляем только там где 0, то есть где нет подбитого корабля
            awailable_coords_to_shoot = [
                (x, y) for x in range(len(helper)) for y in range(len(helper[x])) if helper[x][y] == 0]
            x, y = choice(awailable_coords_to_shoot)
            
            print(f"Компьютер делает выстрел в {(x, y)}")
            
            if not self.check_shot("computer", (x, y)):
                print("Промах!")
                break
                
            else:
                print(f"Попадание! {(x, y)}")
        
            
    def check_shot(self, who, coord):
        """
        Проверка на попадание, who (str, "player", "computer") - кто стрелял
        Ставит кораблю в ячейку 2 и возвращает True, если есть попадание, иначе возвращает False
        """
        if who == 'player':
            pole = self.computer_pole
            helper = self.player_made_shots
        elif who == 'computer':
            pole = self.player_pole
            helper = self.computer_made_shots
        else:
            raise ValueError("Параметр who принимает значения 'player' или 'computer'")
            
        ships = pole.get_ships()
        
        for ship in ships:
            ship_coords = ship._ship_coords
            
            # если координата есть в списке координат корабля, значит есть попадание
            if coord in ship_coords:
                idx = ship_coords.index(coord)
                ship[idx] = 2
                ship._is_move = False
                
                # запишем в спомогательное поле
                helper[coord[0]][coord[1]] = 2
                
                if all([cell == 2 for cell in ship]):
                    print('Корабль уничтожен!')
                
                return True
            elif not self.movement_allowed:
                # если корабли не двигаются, можно записывать куда уже был выстрел
                helper[coord[0]][coord[1]] = 3
                
        return False
    
    def show_made_shots(self, who):
        """
        Вспомогательная функция, которая помогает игроку понимать, где находятся уже подбитые им корабли
        """
        mapping = {
            0: "\u25A0",
            1: "\u25A1",
            2: "\u2670",
            3: "\u25FF"
        }

        view = "  " + " ".join(list(map(str, range(self._size)))) + "\n"
        if who == 'player':
            pole = self.player_made_shots
        elif who == 'computer':
            pole = self.computer_made_shots
        else:
            raise ValueError("Параметр who принимает значения 'player' или 'computer'")
            
        for i, row in enumerate(pole):
            view += f'{i} ' + ' '.join(list(map(lambda x: mapping[x], row))) + '\n'
        view = view.rstrip('\n')
        print(view)
    
    def is_win(self, who):
        """
        Проверка на то, выиграл ли игрок или компьютер.
        Параметр who принимает значения: "player", "computer"
        Возвращает True, если у противника не осталось целых кораблей
        """
        if who == 'player':
            pole = self.computer_pole
            
        elif who == 'computer':
            pole = self.player_pole
            
        else:
            raise ValueError("Параметр who принимает значения 'player' или 'computer'")
            
        ships = pole.get_ships()
        all_defeated = True  # все корабли уничтожены
        for ship in ships:
            all_defeated &= all([cell == 2 for cell in ship])
            
        return all_defeated

if __name__ == '__main__':
    game = SeaBattle()
    game.play()