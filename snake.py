import random
import curses
import time

sc = curses.initscr()
h, w = sc.getmaxyx()
win = curses.newwin(h, w, 0, 0)
win.keypad(1)
curses.curs_set(0)

curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

snake_head = [10, 15]
snake_position = [[15, 10], [14, 10], [13, 10]]
apple_position = [20, 20]
score = 0

win.attron(curses.color_pair(2))
win.addch(apple_position[0], apple_position[1], 'o')
win.attroff(curses.color_pair(2))

key = curses.KEY_RIGHT

def colisao_com_limites(cabeca_cobra):
    if cabeca_cobra[0] >= h-1 or cabeca_cobra[0] <= 0 or cabeca_cobra[1] >= w-1 or cabeca_cobra[1] <= 0:
        return 1
    else:
        return 0

def colisao_com_simesma(posicao_cobra):
    cabeca_cobra = posicao_cobra[0]
    if cabeca_cobra in posicao_cobra[1:]:
        return 1
    else:
        return 0

while True:
    win.border(0)
    win.timeout(100)
    proxima_tecla = win.getch()
    if proxima_tecla == -1:
        key = key
    else:
        key = proxima_tecla
    
    if key == curses.KEY_DOWN:
        snake_head[0] += 1
    if key == curses.KEY_UP:
        snake_head[0] -= 1
    if key == curses.KEY_LEFT:
        snake_head[1] -= 1
    if key == curses.KEY_RIGHT:
        snake_head[1] += 1
    
    snake_position.insert(0, list(snake_head))
    
    if snake_head == apple_position:
        score += 1
        apple_position = [random.randint(1, h-2), random.randint(1, w-2)]
        
        win.attron(curses.color_pair(2))
        win.addch(apple_position[0], apple_position[1], 'o')
        win.attroff(curses.color_pair(2))
        
    else:
        cauda_cobra = snake_position.pop()
        win.addch(cauda_cobra[0], cauda_cobra[1], ' ')
    
    win.attron(curses.color_pair(1))
    win.addch(snake_head[0], snake_head[1], 'o')
    win.attroff(curses.color_pair(1))
    
    if colisao_com_limites(snake_head) == 1 or colisao_com_simesma(snake_position) == 1:
        win.addstr(int(h/2), int(w/2)-7, f'Score: {score}')
        win.refresh()
        time.sleep(3)
        break

curses.endwin()
