import random
import curses
import time

SNAKE_CHAR = 'o'
APPLE_CHAR = 'o'
FIELD_WIDTH = 50
FIELD_HEIGHT = 20

def tela_inicial(win):
    curses.echo()
    win.addstr(10, 10, 'apples:')
    win.refresh()
    num_apples = int(win.getstr().decode())
    curses.noecho()
    return num_apples


def desenhar_campo(win, snake_position, apple_positions, score):
    win.clear()
    win.border(0)
    win.addstr(0, 2, f'score: {score}')

    win.attron(curses.color_pair(1))

    for p in snake_position:
        win.addch(p[0], p[1], SNAKE_CHAR)

    win.attroff(curses.color_pair(1))

    win.attron(curses.color_pair(2))

    for p in apple_positions:
        win.addch(p[0], p[1], APPLE_CHAR)

    win.attroff(curses.color_pair(2))


def main(stdscr):
    stdscr = curses.initscr()
    h, w = stdscr.getmaxyx()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    num_apples = tela_inicial(stdscr)
    
    snake_head = [10, 15]
    snake_position = [[15, 10], [14, 10], [13, 10]]
    score = 0
    
    key = curses.KEY_RIGHT
    
    apple_positions = [[random.randint(1, h-2), random.randint(1, w-2)] for _ in range(num_apples)]
    
    while True:
        stdscr.timeout(100)
        proxima_tecla = stdscr.getch()
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
        
        desenhar_campo(stdscr, snake_position, apple_positions, score)
        
        for apple_position in apple_positions:
            if snake_head == apple_position:
                score += 1
                apple_positions.remove(apple_position)
                new_apple_position = [random.randint(1, h-2), random.randint(1, w-2)]
                apple_positions.append(new_apple_position)
                snake_position.append(snake_position[-1])
            
        else:
            cauda_cobra = snake_position.pop()
            stdscr.addch(cauda_cobra[0], cauda_cobra[1], ' ')
        
        if (
            snake_head[0] >= h - 1
            or snake_head[0] <= 0
            or snake_head[1] >= w - 1
            or snake_head[1] <= 0
            or snake_head in snake_position[1:]
        ):
            stdscr.addstr(h // 2, w // 2 - 7, f'score: {score}')
            stdscr.refresh()
            time.sleep(3)
            break

curses.wrapper(main)
