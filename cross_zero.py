# ------------------------------------------------------
# Игра крестики-нолики в режиме терминала
# ------------------------------------------------------
# Правила игры:
# 1. Номерация строк и столбцов 0...2
# 2. В ответ на приглашение: "Ваш ход. Строка Столбец:" введите
# номер_строки пробел номер_столбца
# Программа проверяет правильность ввода
# 3. Для выхода из программы в ответ на приглашение:
# "Ваш ход. Строка Столбец:" введите 'exit'
# 4. При завершении игры программы выведет приглашение:
# 'Игра закончена. Вы хотите начать новую игру (да/нет): ' введите 'да' или 'нет'
# 5. После хода игрока или компьютера выводится игровое поле с результатом хода
# и оценивается ситуация, сложившаяся в игре


# game_run –      в эту переменную будем записывать False при завершении игры,
#                 чтобы запретить делать ходы когда уже выявлен победитель.
# cross_count -   в этой переменной мы будем отслеживать количество крестиков на поле.
#                 Чтобы по выставлению пятого крестика, в случае если никто не выиграл фиксировать ничью.
# table -         массив - игровое поле

import random

game_run = True
cross_count = 0     # Счетчик 'x'
zero_count = 0      # Счетчик '0'
table = []

# Результат игры:
# 0 - игра продолжается
# 1 - победа игрока
# 2 - победа компьютера
result_game = 0


def print_table(table):
    """Печать игрового поля"""
    for row in table:
        print(' '.join([str(elem) for elem in row]))


def dead_heat():
    """Проверка на ничью. Количество 'x' = 4. Количество '0' = 4"""
    if cross_count == 4 and zero_count == 4:
        return True  # Ничья
    else:
        return False  # Ничья


def check_table(smb):
    """Проверка поля по строкам, столбцам и диагоналям"""
    for n in range(3):
        result = check_line(table[n][0], table[n][1], table[n][2], smb)  # Проверка строк
        if result:
            return result

        result = check_line(table[0][n], table[1][n], table[2][n], smb)  # Проверка столбцов
        if result:
            return result

    result = check_line(table[0][0], table[1][1], table[2][2], smb)  # Проверка левой диагонали
    if result:
        return result

    result = check_line(table[2][0], table[1][1], table[0][2], smb)  # Проверка правой диагонали
    if result:
        return result


def check_line(a1, a2, a3, smb):
    """Проверка линии"""
    if a1 == smb and a2 == smb and a3 == smb:
        if smb == 'x':
            return 1  # Выиграл игрок
        elif smb == '0':
            return 2  # Выиграл компьютер
    else:
        return 0  # Игра продолжается


def can_win(a1, a2, a3, smb):
    """Компьютер завершает строку"""
    global zero_count
    res = False
    result: int = 0
    r0 = a1[0]
    c0 = a1[1]

    r1 = a2[0]
    c1 = a2[1]

    r2 = a3[0]
    c2 = a3[1]

    if table[r0][c0] == smb and table[r1][c1] == smb and table[r2][c2] == '-':
        table[r2][c2] = '0'
        zero_count += 1
        res = True
    if table[r0][c0] == smb and table[r1][c1] == '-' and table[r2][c2] == smb:
        table[r1][c1] = '0'
        zero_count += 1
        res = True
    if table[r0][c0] == '-' and table[r1][c1] == smb and table[r2][c2] == smb:
        table[r0][c0] = '0'
        zero_count += 1
        res = True

    if smb == '0':
        result = 2 if res else 0  # Выиграл компьютер или продолжение игры
        return result
    elif smb == 'x':
        result = 2 if res else 0  # Выиграл компьютер или продолжение игры
        return result
#        return 0                  # Строка завершена без выигрыша. Игра продолжается


def computer_move():
    """Компьютер просматривает строки, столбцы и диагонали. Готовит свой ход"""
    global zero_count
    # ------------------------------------------------------
    # Выигрышное завершение линии компьютера
    # ------------------------------------------------------
    for n in range(3):
        result = can_win([n, 0], [n, 1], [n, 2], '0')  # Проверка строк
        if result:
            return result
        result = can_win([0, n], [1, n], [2, n], '0')  # Проверка столбцов
        if result:
            return result
    result = can_win([0, 0], [1, 1], [2, 2], '0')  # Проверка левой диагонали
    if result:
        return result
    result = can_win([2, 0], [1, 1], [0, 2], '0')  # Проверка правой диагонали
    if result:
        return result

    # ------------------------------------------------------
    # Блокирование линии игрока
    # ------------------------------------------------------
    for n in range(3):
        if can_win([n, 0], [n, 1], [n, 2], 'x'):
            return
        if can_win([0, n], [1, n], [2, n], 'x'):
            return
    if can_win([0, 0], [1, 1], [2, 2], 'x'):
        return
    if can_win([2, 0], [1, 1], [0, 2], 'x'):
        return

    # Если нет линий, которые можно закрыть, случайным образом выбираем
    # свободную ячейку. Это блок определяет стратегию игры
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if table[row][col] == '-':
            table[row][col] = 'O'
            zero_count += 1
            break
    return 0    # Игра продолжается


def new_game():
    """Вывод игрового поля в начале игры"""
    m = 3
    table = [['-'] * m for i in range(m)]
    print_table(table)
    return table


def check_field(row, col):
    """Проверка: свободно ли поле"""
    if table[row][col] == '-':
        return True  # Если поле свободно, разрешаем ввести символ игрока
    else:
        return False  # Если поле занято, предложить игроку выбрать другое поле


# Вывод игрового поля при первом запуске программы
table = new_game()
# ----------------------------------------------------------------
#   Основной цикл
# ----------------------------------------------------------------
while True:
    if game_run:  # Игра разрешена

        # ----------------------------------------------------------------
        #  Ход игрока
        # ----------------------------------------------------------------
        s = input('Ваш ход. Строка Столбец:')
        if s == 'exit':
            print('Игра закончена.')
            exit()
        else:
            try:  # Обработка исключения, если введена не цифра, или не введен номер столбца
                row, col = list(map(int, s.split()))
            except Exception:
                print('Вы не ввели номер столбца!')
            else:
                if check_field(row, col):  # Проверка: поле свободно
                    table[row][col] = 'x'
                    cross_count += 1       # Увеличиваем счетчик 'x'
                    print_table(table)

                    if dead_heat():  # Проверка на ничью. Игроки сделали по 4 хода
                        game_run = False  # Игра остановлена
                        print('Игра завершена. Ничья!')
                        continue  # Возврат в начало цикла
                    else:
                        game_run = True  # Игра продолжается

                    result_game = check_table('x')  # Оценка хода игрока
                    if result_game == 1:
                        game_run = False  # Игра остановлена
                        print('Вы выиграли!')
                        continue
                    elif result_game == 2:
                        game_run = False  # Игра остановлена
                        print('Вы проиграли.')
                        continue
                    elif result_game == 0:
                        game_run = True  # Игра продолжается

                else:
                    print('Это поле занято!')
                    continue  # Возврат в начало цикла

        # ----------------------------------------------------------------
        #  Ход компьютера
        # ----------------------------------------------------------------
        result_game = computer_move()
        print('Ход компьютера.')
        print_table(table)
        if dead_heat():  # Проверка на ничью. Игроки сделали по 4 хода
            game_run = False  # Игра остановлена
            print('Игра завершена. Ничья!')
            continue  # Возврат в начало цикла
        if result_game == 2:
            game_run = False  # Игра остановлена
            print('Вы проиграли.')
        elif result_game == 0:
            game_run = True  # Игра продолжается

    else:  # Игра завершена
        s = input('Игра закончена. Вы хотите начать новую игру (да/нет): ')
        if s == 'нет':
            exit()
        elif s == 'да':
            table = new_game()
            game_run = True
            cross_count = 0
        else:
            print('Ответ неверный!')

