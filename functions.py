import pygame, json

def set_bg(path, sizex, sizey, screen):
    background = pygame.image.load(path)
    background = pygame.transform.scale(background, (sizex, sizey))
    screen.blit(background, (0, 0))

def make_img(path, sizex, sizey, posx, posy, screen):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (sizex, sizey))
    screen.blit(image, (posx, posy))
    return image.get_rect(topleft=(posx, posy))

def make_hov_img(path, hovpath, sizex, sizey, posx, posy, screen, mouse):
    unhov_img = pygame.image.load(path)
    unhov_img = pygame.transform.scale(unhov_img, (sizex, sizey))
    hov_img = pygame.image.load(hovpath)
    hov_img = pygame.transform.scale(hov_img, (sizex, sizey))
    if hov_img.get_rect(topleft=(posx, posy)).collidepoint(mouse):
        screen.blit(hov_img, (posx, posy))
    else:
        screen.blit(unhov_img, (posx, posy))
    return hov_img.get_rect(topleft=(posx, posy))

def make_text(font_style, font_size, value, font_color, display, posx, posy):
    font = pygame.font.SysFont(font_style, font_size)
    text = font.render(value, True, font_color)
    display.blit(text, (posx, posy))
    return text.get_rect(topleft=(posx, posy))

def make_hov_text(font_style, font_size, value, unhov_color, hov_color, display, posx, posy, mouse):
    font = pygame.font.SysFont(font_style, font_size)
    text = font.render(value, True, unhov_color)
    if text.get_rect(topleft=(posx, posy)).collidepoint(mouse):
        font = pygame.font.SysFont(font_style, font_size)
        text = font.render(value, True, hov_color)
    display.blit(text, (posx, posy))
    return text.get_rect(topleft=(posx, posy))
def passvalidation(password):
    for i in password:
        if i.isalpha():
            for i in password:
                if i.isdigit():
                    return True
    return False
def savetofile(accounts):
    print(accounts)
    accounts = {key:value.__dict__ for key, value in accounts.items()} 
    with open("data/accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)
def font(size, style=None):
    # if style != None:
    #     return pygame.font.Font(f'assets/fonts/{style}', size)
    return pygame.font.Font("assets/fonts/normal.otf", size)

def redraw(screen, board, moves):
        screen_x = 1280
        screen_y = 720
        board_width, board_height = board.image.get_size()
        board_x = (screen_x - board_width - 50) // 2  # Calculate the x-coordinate to center the board
        board_y = (screen_y - board_height) // 2  # Calculate the y-coordinate to center the board
        screen.blit(board.image, (board_x, board_y))  # Blit the board image at the centered position

        y = 0
        for line in board.board:
            x = 0
            for pos, row in line:
                if type(row).__name__ == "King" and row.team == board.turn:
                    if board.check > 0:
                        screen.blit(pygame.image.load("Pieces/red_dot.png"), (board_x + pos[0] - 20, board_y + pos[1] - 20))
                
                if row != 0:
                    piece_x = board_x + pos[0]  # Adjust the x-coordinate relative to the centered board
                    piece_y = board_y + pos[1]  # Adjust the y-coordinate relative to the centered board
                    screen.blit(row.image, (piece_x, piece_y))

                if (y, x) in moves:
                    screen.blit(pygame.image.load("Pieces/orange_dot.png"), (board_x + pos[0] + 4, board_y + pos[1] + 5))
                x += 1

            y += 1
        
def generate_notation(move, board):
        piece = board.board[move[0][0]][move[0][1]][1]
        dest = move[1]

        piece_type = type(piece).__name__
        notation = ""
        if piece_type != "Pawn":
            if piece_type != "Knight":
                notation += piece_type[0]
            else:
                notation += "N"
        notation += chr(ord('a') + move[0][1])
        notation += str(8 - move[0][0])
        notation += '-'
        notation += chr(ord('a') + dest[1])
        notation += str(8 - dest[0])
        return notation
