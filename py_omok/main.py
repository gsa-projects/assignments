import sys
from os import path
from pygame import *
from pygame.locals import *
from base import *

def on_click(mouse_pos, board: Board):
    # 유저 착수
    placement_pos = tuple(map(board.nth, mouse_pos))
    if not board.empty(placement_pos): return

    counts = board.get_counts(placement_pos, user_stone)

    # NOTE
    print(counts)

    if all(count <= 5 for count in counts.values()):
        board.placement(placement_pos, user_stone)

        if any(count == 5 for count in counts.values()):
            print("유저 승")
            quit()
            sys.exit()
    else:
        print('장목이라 착수 안 됨')

    # 봇 착수
    placement_pos = board.best_pos()
    board.placement(placement_pos, bot_stone)

    # NOTE
    print(placement_pos)

    counts = board.get_counts(placement_pos, bot_stone)
    if any(count == 5 for count in counts.values()):
        print("AI 승")
        quit()
        sys.exit()

def main(mouse_pos, board: Board):
    for evt in event.get():
        if evt.type == QUIT:
            quit()
            sys.exit()

        elif evt.type == MOUSEBUTTONDOWN:
            on_click(mouse_pos, board)

    screen.blit(board_image.image, (0, 0))
    for i in range(15):
        for j in range(15):
            if not board.empty((i, j)):
                screen.blit(board[i, j].image, tuple(map(board.to_pos, (i, j))))
    screen.blit(user_stone.image, tuple(map(board.nth_to_pos, mouse_pos)))

if __name__ == "__main__":
    init()
    assets = path.join(path.dirname(__file__), "assets")
    white_stone = Image(path.join(assets, 'white_stone.png'))
    black_stone = Image(path.join(assets, 'black_stone.png'))
    bot_stone, user_stone = white_stone, black_stone

    board_image = Image(path.join(assets, 'board.png'))
    board = Board(startpx=(30, 30), endpx=(590, 590), steppx=40, stone_size=user_stone.get_width())

    display.set_caption("Omok")
    screen = display.set_mode(board_image.get_size())
    clock = time.Clock()
    fps = 30

    RIGHT, DOWN, RIGHT_DOWN, RIGHT_UP = (1, 0), (0, 1), (1, 1), (1, -1)

    while True:
        user_stone.set_alpha(128)
        main(mouse.get_pos(), board)
        display.update()
        clock.tick(fps)