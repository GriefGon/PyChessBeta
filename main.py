import pygame
from pygame import mixer
import sys
import json, random
from Classes import *
from functions import *

# Initializing Pygame
pygame.init()

# Initializing Pygame Essential Variable
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 60

# Caption and icon
pygame.display.set_caption("PyChessBeta")
pygame.display.set_icon(pygame.image.load('Pieces/icon.ico'))

# Sounds
move_sound = Sound('Pieces/move.wav')
capture_sound = Sound('Pieces/capture.wav')

# Accounts Loading
accounts = {}
with open("data/accounts.json") as f:
    accounts = json.load(f)
    accounts = {key : User(value['name'], value['password'], value['wins'], value['losses'], value['draws'], value['games'])
                for key, value in accounts.items()}

# Colors
whisper = pygame.Color(234, 234, 234)
dirty_white = pygame.Color(254, 254, 254)
black = pygame.Color(0, 0, 0)
dark_gray = pygame.Color(32, 32, 32)
light_gray = pygame.Color(128, 128, 128)
#FFDE59
#FF3131
#00bf63
yellow = "#FFDE59"
red = "#FF3131"
green = "#00bf63"
colors = {"draw" : "#FFDE59", "loss" : "#FF3131", "win" : "#00bf63"}

# Main Game Loop
frame = "login" # Current Frame
running = True
while running:

    # username and password values placeholder
    username_value = ""
    password_value = ""

    # activated by mouseclick
    username_active = False
    password_active = False

    # for the cursor ticks
    cursor_visible = True
    cursor_timer = 0

    # Text
    wrong_password = pygame.font.SysFont("FF Mark 05", 17).render("The password you have entered is incorrect.", True, "#e88545")
    account_not_found1 = pygame.font.SysFont("FF Mark 05", 17).render("Your login credentials does not match a Pychess", True, "#e88545")
    account_not_found2 = pygame.font.SysFont("FF Mark 05", 17).render("Beta account. Please try again.", True, "#e88545")

    # error
    error1 = False
    error2 = False

    see_password = True

    while frame == "login":
            clock.tick(FPS)

            events = pygame.event.get()

            mouse = pygame.mouse.get_pos()

            # static
            background = set_bg("assets/login_bg.png", 1280, 720, screen)
            logo = make_img("assets/logo.png", 200, 200, 84, 10, screen)
            signin_text = make_text("FF Mark W05", 30, "SIGN IN", dark_gray, screen, 140, 180)

            # interactive
            username_box = InputBox(whisper, dirty_white, black, screen, 55, 225, 260, 40, 0, 1, 3, mouse, username_active,
                                    "FF Mark W05", 21, dark_gray, username_value, 263, 10, "USERNAME", 14, 13, 70, 240, light_gray)

            if see_password:
                password_box = InputBox(whisper, dirty_white, black, screen, 55, 275, 260, 40, 0, 1, 3, mouse, password_active,
                                        "FF Mark W05", 33, dark_gray, "*" * len(password_value), 263, 10, "PASSWORD", 14, 13, 70, 290, light_gray)
            else:
                password_box = InputBox(whisper, dirty_white, black, screen, 55, 275, 260, 40, 0, 1, 3, mouse, password_active,
                                        "FF Mark W05", 21, dark_gray, password_value, 263, 10, "PASSWORD", 14, 13, 70, 290, light_gray)

            register_text = make_hov_text("FF Mark W05", 17, "REGISTER", light_gray, dark_gray, screen,
                                          68, 328, mouse)

            if len(username_value) and len(password_value):
                enter_button = make_hov_img("assets/unhovered_enter.png", "assets/hovered_enter.png",
                                            60, 60, 152, 500, screen, mouse)
            else:
                enter_button = make_img("assets/inactive_enter.png", 60, 60, 152, 500, screen)

            if error1:
                username_box.make_the_box(True)
                password_box.make_the_box(True)
                screen.blit(wrong_password, (60, 348))
            elif error2:
                username_box.make_the_box(True)
                password_box.make_the_box(True)
                screen.blit(account_not_found1, (60, 348))
                screen.blit(account_not_found2, (60, 368))
            else:
                username_box.make_the_box()
                password_box.make_the_box()

            if see_password:
                eye = make_img("assets/inactive_eye.png", 36, 20, 270, 285, screen)
            else:
                eye = make_img("assets/active_eye.png", 36, 20, 270, 285, screen)

            cursor_timer += clock.get_time()
            if cursor_timer >= 150:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            # Render the cursor
            if (username_active or password_active) and cursor_visible and not see_password:
                cursor_x = 65 + username_box.input_font.size(username_value if username_active else password_value)[0]
                cursor_y = 243 if username_active else 293
                pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 16))
            elif password_active and cursor_visible and see_password:
                cursor_x = 65 + password_box.input_font.size(username_value if username_active else "*" * len(password_value))[0]
                cursor_y = 243 if username_active else 293
                pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 16))
            elif username_active and cursor_visible and see_password:
                cursor_x = 65 + username_box.input_font.size(username_value if username_active else "*" * len(password_value))[0]
                cursor_y = 243 if username_active else 293
                pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 16))

            for event in events:
                if event.type == pygame.QUIT:
                    savetofile(accounts)
                    pygame.quit()
                    sys.exit()
                # for clicking events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if eye.collidepoint(mouse):
                            see_password = not see_password
                        elif username_box.check_collision(mouse):  # username box click
                            username_active = True
                            password_active = False
                        elif password_box.check_collision(mouse):  # password box click
                            username_active = False
                            password_active = True
                        elif enter_button.collidepoint(mouse):
                            if len(username_value) and len(password_value):
                                if username_value in accounts.keys():
                                    if accounts[username_value].login(password_value):
                                        player_one = accounts[username_value]
                                        frame = "prep"
                                    else:
                                        error1 = True
                                        error2 = False
                                else:
                                    error1 = False
                                    error2 = True
                        elif register_text.collidepoint(mouse):  # register text click
                            frame = "signup"
                        else:  # default
                            username_active = False
                            password_active = False
                # for type events
                if username_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: # backspace
                            username_value = username_value[:-1]
                            username_box.input_render()

                    if event.type == pygame.TEXTINPUT: # for typing
                        if len(username_value) < 16:
                            username_value += event.text
                            username_box.input_render()

                if password_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            password_value = password_value[:-1]
                            password_box.input_render()

                    if event.type == pygame.TEXTINPUT:
                        if len(password_value) < 16:
                            password_value += event.text
                            password_box.input_render()

            username_box.inputbox_text()
            password_box.inputbox_text()

            pygame.display.update()

    # username and password values placeholder
    username_value = ""
    password_value = ""
    confirm_password_value = ""

    guidelines1 = "Username not taken."
    guidelines2 = "Password must be 8 characters long or more."
    guidelines3 = "Password must contain at least one letter"
    guidelines4 = "and one number."
    guidelines5 = "Passwords match."

    # activated by mouseclick line 57
    username_active = False
    password_active = False
    confirm_password_active = False

    # for the cursor ticks
    cursor_visible = True
    cursor_timer = 0

    # Error
    error = False

    while frame == "signup":
        clock.tick(FPS)

        events = pygame.event.get()

        mouse = pygame.mouse.get_pos()


        # validations 
        if username_value not in accounts and len(username_value):
            username_not_taken = True
        else:
            username_not_taken = False
        if len(password_value) < 8:
            password_min_len = False
        else:
            password_min_len = True
        if passvalidation(password_value):
            password_onelet_onenum = True
        else:
            password_onelet_onenum = False
        if password_value == confirm_password_value and len(password_value):
            matching_password = True
        else:
            matching_password = False

        # static
        background = set_bg("assets/signup_bg.png", 1280, 720, screen)
        Header = make_text("FF Mark W05", 28, "CREATE YOUR ACCOUNT", dark_gray, screen, 515, 195)

        # interactive
        username_box = InputBox(whisper, dirty_white, black, screen, 450, 235, 380, 45, 0, 1, 3, mouse, username_active,
                                    "FF Mark W05", 21, dark_gray, username_value, 263, 10, "USERNAME", 18, 15, 470, 250, light_gray)

        if not username_not_taken:
            username_guidelines = make_text("FF Mark W05", 22, guidelines1, "#afaeae", screen, 490, 292)
            check = pygame.image.load("assets/grey_check.png")
            screen.blit(check, (460, 289))        
        else:
            username_guidelines = make_text("FF Mark W05", 22, guidelines1, green, screen, 490, 292)
            check = pygame.image.load("assets/green_check.png")
            screen.blit(check, (460, 289))
        password_box = InputBox(whisper, dirty_white, black, screen, 450, 320, 380, 45, 0, 1, 3, mouse, password_active,
                                    "FF Mark W05", 21, dark_gray, password_value, 263, 10, "PASSWORD", 18, 15, 470, 338, light_gray)

        if not password_min_len:
            password_guidelines = make_text("FF Mark W05", 22, guidelines2, "#afaeae", screen, 490, 377)
            check = pygame.image.load("assets/grey_check.png")
            screen.blit(check, (460, 374))
        else:
            password_guidelines = make_text("FF Mark W05", 22, guidelines2, green, screen, 490, 377)
            check = pygame.image.load("assets/green_check.png")
            screen.blit(check, (460, 374))
        if not password_onelet_onenum:
            password_guidelines2 = make_text("FF Mark W05", 22, guidelines3, "#afaeae", screen, 490, 402)
            password_guidelines3 = make_text("FF Mark W05", 22, guidelines4, "#afaeae", screen, 490, 422)
            check = pygame.image.load("assets/grey_check.png")
            screen.blit(check, (460, 399))
        else:
            password_guidelines2 = make_text("FF Mark W05", 22, guidelines3, green, screen, 490, 402)
            password_guidelines3 = make_text("FF Mark W05", 22, guidelines4, green, screen, 490, 422)
            check = pygame.image.load("assets/green_check.png")
            screen.blit(check, (460, 399))
        confirm_password_box = InputBox(whisper, dirty_white, black, screen, 450, 445, 380, 45, 0, 1, 3, mouse, confirm_password_active,
                                    "FF Mark W05", 21, dark_gray, confirm_password_value, 263, 10, "CONFIRM PASSWORD", 18, 15, 470, 463, light_gray)

        if not matching_password:
            confirm_password_guideline = make_text("FF Mark W05", 22, guidelines5, "#afaeae", screen, 490, 502)
            check = pygame.image.load("assets/grey_check.png")
            screen.blit(check, (460, 499))        
        else:
            confirm_password_guideline = make_text("FF Mark W05", 22, guidelines5, green, screen, 490, 502)
            check = pygame.image.load("assets/green_check.png")
            screen.blit(check, (460, 499))

        if len(username_value) and len(password_value) and len(confirm_password_value):
            enter_button = make_hov_img("assets/unhovered_enter.png", "assets/hovered_enter.png",
                                            60, 60, 610, 540, screen, mouse)
        else:
            enter_button = make_img("assets/inactive_enter.png", 60, 60, 610, 540, screen)

        login_text = make_text("FF Mark W05", 21, "ALREADY HAVE AN ACCOUNT?", dark_gray, screen, 530, 625)

        if error:
            username_box.make_the_box(True)
            password_box.make_the_box(True)
            confirm_password_box.make_the_box(True)
        else:
            username_box.make_the_box()
            password_box.make_the_box()
            confirm_password_box.make_the_box()

        cursor_timer += clock.get_time()
        if cursor_timer >= 150:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Render the cursor
        if (username_active or password_active or confirm_password_active) and cursor_visible:
            if confirm_password_active:
                cursor_x = 460 + confirm_password_box.input_font.size(confirm_password_value)[0]
                cursor_y = 463
            else:
                cursor_x = 460 + username_box.input_font.size(username_value if username_active else password_value)[0]
                cursor_y = 252 if username_active else 338
            pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 16))

        for event in events:
            if event.type == pygame.QUIT:
                savetofile(accounts)
                pygame.quit()
                sys.exit()
            # for clicking events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if username_box.check_collision(mouse):  # username box click
                        username_active = True
                        password_active = False
                        confirm_password_active = False
                    elif password_box.check_collision(mouse):  # password box click
                        username_active = False
                        password_active = True
                        confirm_password_active = False
                    elif confirm_password_box.check_collision(mouse):
                        username_active = False
                        password_active = False
                        confirm_password_active = True
                    elif login_text.collidepoint(mouse):  # register text click
                        frame = "login"
                    elif enter_button.collidepoint(mouse):
                        if all((password_min_len, matching_password, password_onelet_onenum, username_not_taken)):
                            accounts[username_value] = User(username_value, password_value)
                            player_one = accounts[username_value]
                            frame = "prep"
                        else:
                            error = True
                    else:  # default
                        username_active = False
                        password_active = False
                        confirm_password_active = False
            # for type events
            if username_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # backspace
                        username_value = username_value[:-1]
                        username_box.input_render()
                if event.type == pygame.TEXTINPUT: # for typing
                    if len(username_value) < 16:
                        username_value += event.text
                        username_box.input_render()

            if password_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        password_value = password_value[:-1]
                        password_box.input_render()
                if event.type == pygame.TEXTINPUT:
                    if len(password_value) < 16:
                        password_value += event.text
                        password_box.input_render()

            if confirm_password_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_value = confirm_password_value[:-1]
                        confirm_password_box.input_render()
                if event.type == pygame.TEXTINPUT:
                    if len(confirm_password_value) < 16:
                        confirm_password_value += event.text
                        confirm_password_box.input_render()

        #  printing the boxes, static texts, interactive texts, and input texts
        username_box.inputbox_text(offset_y = 8)
        password_box.inputbox_text(offset_y = 11)
        confirm_password_box.inputbox_text(offset_y = 11)
        # username_box.print_input()

        pygame.display.update()

        # colors to be used
        
    #3d1686 - lightest purple
    #2d0f66 - medj lighter lang
    #230056 - medj darker lang
    #1a013d - darkest purple
    p1 = "#3d1686"
    p2 = "#2d0f66"
    p3 = "#230056"
    p4 = "#1a013d"

    username_value = ""
    password_value = ""

    username_active = False
    password_active = False

    error1 = False
    error2 = False
    error3 = False

    # Text
    wrong_password1 = pygame.font.SysFont("FF Mark 05", 15).render("The password you have entered is ", True, "#e88545")
    wrong_password2 = pygame.font.SysFont("FF Mark 05", 15).render("incorrect.", True, "#e88545")
    account_not_found1 = pygame.font.SysFont("FF Mark 05", 15).render("Your login credentials does", True, "#e88545")
    account_not_found2 = pygame.font.SysFont("FF Mark 05", 15).render("not match a Pychess Beta account.", True, "#e88545")
    same_account = pygame.font.SysFont("FF Mark 05", 15).render("You cannot fight against yourself.", True, "#e88545")

    # cursor
    cursor_visible = True
    cursor_timer = 0

    game_index = 0
    sel = ""
    bg = pygame.image.load("Pieces/unselected_bg.png")
    selected = None
    moves = []
    board = Board()
    see_password = True

    while frame == "prep":

        if sel == "black":
            bg = pygame.image.load("Pieces/black_selected_bg.png")
        elif sel == "white":
            bg = pygame.image.load("Pieces/white_selected_bg.png")
        elif sel == "random":
            bg = pygame.image.load("Pieces/random_selected_bg.png")

        screen.blit(bg, (0, 0))

        # Mouse and Keyboard Keys
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()


        username_text = font(30).render(player_one.name, True, dirty_white)
        screen.blit(username_text, username_text.get_rect(center=(140,43)))

        wins_text = font(20).render("WINS", True, green)
        screen.blit(wins_text, wins_text.get_rect(center=(48, 100)))
        losses_text = font(20).render("LOSSES", True, red)
        screen.blit(losses_text, losses_text.get_rect(center=(144, 100)))
        draws_text = font(20).render("DRAWS", True, yellow)
        screen.blit(draws_text, draws_text.get_rect(center=(238, 100)))
        no_of_wins_text = font(20).render(str(player_one.wins), True, dirty_white)
        screen.blit(no_of_wins_text, no_of_wins_text.get_rect(center=(48,122)))
        no_of_losses_text = font(20).render(str(player_one.losses), True, dirty_white)
        screen.blit(no_of_losses_text, no_of_losses_text.get_rect(center=(144,122)))
        no_of_draws_text = font(20).render(str(player_one.draws), True, dirty_white)
        screen.blit(no_of_draws_text, no_of_draws_text.get_rect(center=(238,122)))

        try:
            current_games = enumerate(list(reversed(player_one.games))[game_index:game_index+10])
        except:
            current_games = enumerate(list(reversed(player_one.games))[game_index:game_index])  

        for i, game in current_games:
            games_txt = font(20).render("vs. " + game[1], True, colors[game[0]])
            screen.blit(games_txt, games_txt.get_rect(topleft=(20,184 + i * 40)))

        scroll_games = pygame.Rect(0, 133, 290, 440)

        start_button = pygame.Rect(0, 0, 110, 36)
        start_button.center = (1075, 480)

        black_button = pygame.Rect(0, 0, 40, 40)
        black_button.center = (1010, 435)

        white_black_button = pygame.Rect(0, 0, 40, 40)
        white_black_button.center = (1076, 435)

        white_button = pygame.Rect(0, 0, 40, 40)
        white_button.center = (1137, 435)

        up_button = pygame.Rect(0, 0, 20, 20)
        up_button.center = (246, 155)

        down_button = pygame.Rect(0, 0, 20, 20)
        down_button.center = (267, 155)

        sign_out_button = pygame.Rect(0, 0, 120, 30)
        sign_out_button.center = (143, 690)

        username_box = InputBox(whisper, dirty_white, black, screen, 990, 252, 170, 35, 0, 1, 3,
                                            mouse, username_active, "FF MARK W05", 19, dark_gray, username_value, 170, 10,
                                            "USERNAME", 16, 15, 1005, 265, light_gray)

        if see_password:
            password_box = InputBox(whisper, dirty_white, black, screen, 990, 292, 170, 35, 0, 1, 3,
                                                mouse, password_active, "FF MARK W05", 29, dark_gray, len(password_value) * "*", 170, 10,
                                                "PASSWORD", 16, 15, 1005, 305, light_gray)
        else:
            password_box = InputBox(whisper, dirty_white, black, screen, 990, 292, 170, 35, 0, 1, 3,
                                                mouse, password_active, "FF MARK W05", 19, dark_gray, password_value, 170, 10,
                                                "PASSWORD", 16, 15, 1005, 305, light_gray)

        if error1:
            username_box.make_the_box(True)
            password_box.make_the_box(True)
            screen.blit(wrong_password1, (990, 338))
            screen.blit(wrong_password2, (990, 353))
        elif error2:
            username_box.make_the_box(True)
            password_box.make_the_box(True)
            screen.blit(account_not_found1, (990, 338))
            screen.blit(account_not_found2, (990, 353))
        elif error3:
            username_box.make_the_box(True)
            password_box.make_the_box(True)
            screen.blit(same_account, (990, 338))
        else:
            username_box.make_the_box()
            password_box.make_the_box()

        if see_password:
            eye = make_img("assets/inactive_eye.png", 36, 20, 1120, 300, screen)
        else:
            eye = make_img("assets/active_eye.png", 36, 20, 1120, 300, screen)

        cursor_timer += clock.get_time()
        if cursor_timer >= 150:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Render the cursor
        if (username_active or password_active) and cursor_visible and not see_password:
            cursor_x = 1000 + username_box.input_font.size(username_value if username_active else password_value)[0]
            cursor_y = 270 if username_active else 310
            pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 14))
        elif password_active and cursor_visible and see_password:
            cursor_x = 1000 + password_box.input_font.size(username_value if username_active else "*" * len(password_value))[0]
            cursor_y = 270 if username_active else 310
            pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 14))
        elif username_active and cursor_visible and see_password:
            cursor_x = 1000 + username_box.input_font.size(username_value if username_active else "*" * len(password_value))[0]
            cursor_y = 270 if username_active else 310
            pygame.draw.rect(screen, dark_gray, (cursor_x, cursor_y, 1, 14))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                savetofile(accounts)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if scroll_games.collidepoint(mouse):
                    if event.button == 4:
                        if game_index > 0:
                            game_index -= 1
                    if event.button == 5:
                        if game_index < len(player_one.games) - 10:
                            game_index += 1
                if event.button == 1:
                    if eye.collidepoint(mouse):
                        see_password = not see_password
                    elif up_button.collidepoint(mouse):
                        if game_index > 0:
                            game_index -= 1
                    elif down_button.collidepoint(mouse):
                        if game_index < len(player_one.games) - 10:
                            game_index += 1
                    elif sign_out_button.collidepoint(mouse):
                        frame = "login"
                    elif white_button.collidepoint(mouse):
                        sel = "white"
                    elif black_button.collidepoint(mouse):
                        sel = "black"
                    elif white_black_button.collidepoint(mouse):
                        sel = "random"
                    elif username_box.check_collision(mouse):
                        username_active = True
                        password_active = False
                    elif password_box.check_collision(mouse):
                        username_active = False
                        password_active = True
                    elif start_button.collidepoint(mouse) and sel != "":
                        if len(username_value) and len(password_value):
                            if username_value == player_one.name:
                                error1 = False
                                error2 = False
                                error3 = True
                            elif username_value in accounts.keys():
                                if accounts[username_value].login(password_value):
                                    player_two = accounts[username_value]
                                    frame = "game"
                                else:
                                    error1 = True
                                    error2 = False
                                    error3 = False
                            else:
                                error1 = False
                                error2 = True
                                error3 = False
                    else:  # default
                        username_active = False
                        password_active = False

            #for type events
            if username_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # backspace
                        username_value = username_value[:-1]
                        username_box.input_render()

                if event.type == pygame.TEXTINPUT: # for typing
                    if len(username_value) < 16:
                        username_value += event.text
                        username_box.input_render()

            if password_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        password_value = password_value[:-1]
                        password_box.input_render()

                if event.type == pygame.TEXTINPUT:
                    if len(password_value) < 16:
                        password_value += event.text
                        password_box.input_render()

        username_box.inputbox_text()
        password_box.inputbox_text()

        redraw(screen, board, moves)
        # Limiting FPS
        clock.tick(FPS)
        # Updating Screen
        pygame.display.update()

    if sel == "white":
        player_one_color = "white"
        color = "black"
    elif sel == "black":
        player_one_color = "black"
        color = "white"
    elif sel == "random":
        if random.randrange(1, 3) == 1:
            player_one_color = "white"
            color = "black"
        else:
            player_one_color = "black"
            color = "white"

    state = None
    draw_black, draw_white = False, False
    surrender_white, surrender_black = False, False
    prevmov = []
    move_index = 0
    bg = pygame.image.load("assets/game_bg.png")
    end_game = False
    while frame == "game":
        
        screen.blit(bg, (0, 0))

        # Mouse and Keyboard Keys
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        username_text = font(30).render(player_one.name, True, dirty_white)
        screen.blit(username_text, username_text.get_rect(center=(140,43)))

        if player_one_color == "white":
            player_one_text = font(23).render(player_one.name, True, dirty_white)
            screen.blit(player_one_text, (950, 615))
            text = font(23).render(player_two.name, True, dirty_white)
            screen.blit(text, (950, 82))
        elif player_one_color == "black":
            player_one_text = font(23).render(player_one.name, True, dirty_white)
            screen.blit(player_one_text, (950, 82))
            text = font(23).render(player_two.name, True, dirty_white)
            screen.blit(text, (950, 615))

        wins_text = font(20).render("WINS", True, green)
        screen.blit(wins_text, wins_text.get_rect(center=(48, 100)))
        losses_text = font(20).render("LOSSES", True, red)
        screen.blit(losses_text, losses_text.get_rect(center=(144, 100)))
        draws_text = font(20).render("DRAWS", True, yellow)
        screen.blit(draws_text, draws_text.get_rect(center=(238, 100)))
        no_of_wins_text = font(20).render(str(player_one.wins), True, dirty_white)
        screen.blit(no_of_wins_text, no_of_wins_text.get_rect(center=(48,122)))
        no_of_losses_text = font(20).render(str(player_one.losses), True, dirty_white)
        screen.blit(no_of_losses_text, no_of_losses_text.get_rect(center=(144,122)))
        no_of_draws_text = font(20).render(str(player_one.draws), True, dirty_white)
        screen.blit(no_of_draws_text, no_of_draws_text.get_rect(center=(238,122)))

        scroll_games = pygame.Rect(0, 133, 290, 440)

        if board.promotion and board.turn == 0:
            bg = pygame.image.load("assets/black_promote.png")
        elif board.promotion:
            bg = pygame.image.load("assets/white_promote.png")
        elif not draw_black and not draw_white and not surrender_black and not surrender_white and not end_game:
            bg = pygame.image.load("assets/game_bg.png")

        try:
            current_games = enumerate(list(reversed(player_one.games))[game_index:game_index+10])
        except:
            current_games = enumerate(list(reversed(player_one.games))[game_index:game_index])  

        for i, game in current_games:
            game_txt = font(20).render("vs. " + game[1], True, colors[game[0]])
            screen.blit(game_txt, game_txt.get_rect(topleft=(20,184 + i * 40)))

        try:
            current_moves = enumerate(prevmov[move_index:move_index+26])
        except:
            current_moves = enumerate(prevmov[move_index:move_index])

        if not board.promotion and not draw_black and not draw_white and not surrender_black and not surrender_white and not end_game:
            for i, m in current_moves:
                move_number = font(20).render(str(i//2 + 1 + move_index//2)+ ".", True, light_gray)
                screen.blit(move_number, move_number.get_rect(center=(1005, 243 + i//2 * 20)))
                move_txt = font(18).render(m.replace("-", " "), True, dirty_white)
                screen.blit(move_txt, move_txt.get_rect(topleft=(1038 + (i%2 * 70), 230 + (i//2 * 20))))

        scroll_moves = pygame.Rect(974, 210, 200, 300)

        sign_out_button = pygame.Rect(0, 0, 120, 30)
        sign_out_button.center = (143, 690)

        up_button = pygame.Rect(0, 0, 20, 20)
        up_button.center = (246, 155)

        down_button = pygame.Rect(0, 0, 20, 20)
        down_button.center = (267, 155)

        up_move_button = pygame.Rect(974, 153, 200, 50)
        down_move_button = pygame.Rect(974, 513, 200, 50)

        surrender_button_white = pygame.Rect(0, 0, 20, 35)
        surrender_button_white.center = (1163, 627)

        draw_button_white = pygame.Rect(0, 0, 20, 35)
        draw_button_white.center = (1187, 627)

        surrender_button_black = pygame.Rect(0, 0, 20, 35)
        surrender_button_black.center = (1163, 93)

        draw_button_black = pygame.Rect(0, 0, 20, 35)
        draw_button_black.center = (1187, 93)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                savetofile(accounts)
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if board.promotion:
                    board.promotion = False

                    if board.turn != 0:
                        color = "Pieces/white"
                        team = 0
                    else:
                        color = "Pieces/black"
                        team = 1

                    if event.key in (pygame.K_1, pygame.K_KP_1) :
                        board.board[index_y][index_x][1] = Queen(team, f"{color}_queen.png")
                    elif event.key in (pygame.K_2, pygame.K_KP_2):
                        board.board[index_y][index_x][1] = Rook(team, f"{color}_rook.png", -1)
                    elif event.key in (pygame.K_3, pygame.K_KP_3):
                        board.board[index_y][index_x][1] = Bishop(team, f"{color}_bishop.png")
                    elif event.key in (pygame.K_4, pygame.K_KP_4):
                        board.board[index_y][index_x][1] = Knight(team, f"{color}_knight.png")
                    else:
                        board.promotion = True

                    all_moves = board.get_all_moves((board.turn + 1) % 2)
                    board.check_check(all_moves)
                    board.check_checkmate_or_stalemate()
                    board.check_draw()

            elif event.type == pygame.MOUSEBUTTONDOWN and not (board.promotion or board.checkmate or board.stalemate or board.draw) and not end_game:
                x, y = pygame.mouse.get_pos()
                index_x, index_y = (x - 360) // 70, (y - 80) // 70

                if 0 <= index_x < 8 and 0 <= index_y < 8:
                    tile = board.board[index_y][index_x][1]

                    if selected is not None and (index_y, index_x) in moves:
                        board.last_move = (index_y, index_x)
                        board.reset_en_passant()
                        board.check = 0
                        move_notation = generate_notation(((aux_index_y, aux_index_x), (index_y, index_x)), board)
                        prevmov.append(move_notation)
                        if type(selected).__name__ == "King":
                            if index_x - aux_index_x == 2:
                                selected.castle(1, board.board)
                            if index_x - aux_index_x == -2:
                                selected.castle(0, board.board)

                            selected.short_castle = False
                            selected.long_castle = False
                        elif type(selected).__name__ == "Rook":
                            for line in board.board:
                                for _, row in line:
                                    if type(row).__name__ == "King" and row.team == selected.team:
                                        king = row

                            if selected.side == 0:
                                king.long_castle = False
                            elif selected.side == 1:
                                king.short_castle = False
                        elif type(selected).__name__ == "Pawn":
                            if abs(index_y - aux_index_y) == 2:
                                selected.en_passant = True
                            if board.board[index_y][index_x][1] == 0 and aux_index_x != index_x:
                                selected.do_en_passant(index_x, index_y, board.board)
                            if (selected.team == 0 and index_y == 0) or (selected.team == 1 and index_y == 7):
                                board.promotion = True

                        if board.board[index_y][index_x][1] != 0:
                            capture_sound.play()
                        else:
                            move_sound.play()

                        board.board[aux_index_y][aux_index_x][1] = 0
                        board.board[index_y][index_x][1] = selected
                        all_moves = board.get_all_moves(board.turn)

                        board.turn = (board.turn + 1) % 2
                        board.check_check(all_moves)
                        board.check_checkmate_or_stalemate()
                        board.check_draw()

                        moves = []
                        selected = None
                    elif tile != 0 and tile.team == board.turn:
                        moves = []
                        selected = board.board[index_y][index_x][1]

                        if type(selected).__name__ == "King":
                            aux_moves = board.get_king_legal_moves(index_x, index_y)
                        else:
                            aux_moves = board.get_legal_moves(index_x, index_y, selected)

                        for move in aux_moves:
                            try:
                                if board.board[move[0]][move[1]][1].team != board.turn:
                                    moves.append(move)
                            except AttributeError:
                                moves.append(move)

                        aux_index_x, aux_index_y = index_x, index_y

            if event.type == pygame.MOUSEBUTTONDOWN:
                if scroll_games.collidepoint(mouse):
                    if event.button == 4:
                        if game_index > 0:
                            game_index -= 1
                    if event.button == 5:
                        if game_index < len(player_one.games) - 10:
                            game_index += 1
                if scroll_moves.collidepoint(mouse):
                    if event.button == 4:
                        if move_index > 0:
                            move_index -= 2
                    elif event.button == 5:
                        if move_index < len(prevmov) - 26:
                            move_index += 2
                if sign_out_button.collidepoint(mouse):
                    frame = "login"
                elif end_game:
                    if up_move_button.collidepoint(mouse):
                        board = Board()
                        end_game = False
                        state = None
                        prevmov = []
                        bg = pygame.image.load("assets/game_bg.png")
                    elif down_move_button.collidepoint(mouse):
                        frame = "prep"
                elif draw_white or draw_black:
                    if event.button == 1:
                        if up_move_button.collidepoint(mouse):
                            state = "draw"
                            draw_white, draw_black = False, False
                        elif down_move_button.collidepoint(mouse):
                            draw_white, draw_black = False, False
                            bg = pygame.image.load("assets/game_bg.png")
                elif surrender_white or surrender_black:
                    if event.button == 1:
                        if up_move_button.collidepoint(mouse):
                            if surrender_white:
                                state = "black"
                            elif surrender_black:
                                state = "white"
                            surrender_black, surrender_white = False, False
                        elif down_move_button.collidepoint(mouse):
                            surrender_black, surrender_white = False, False
                            bg = pygame.image.load("assets/game_bg.png")      
                else:
                    if up_button.collidepoint(mouse):
                        if game_index > 0:
                            game_index -= 1
                    elif down_button.collidepoint(mouse):
                        if game_index < len(player_one.games) - 10:
                            game_index += 1
                    elif up_move_button.collidepoint(mouse):
                        if move_index > 0:
                            move_index -= 2
                    elif down_move_button.collidepoint(mouse):
                        if move_index < len(prevmov) - 26:
                            move_index += 2
                    elif surrender_button_white.collidepoint(mouse):
                        surrender_white = True
                    elif surrender_button_black.collidepoint(mouse):
                        surrender_black = True
                    elif draw_button_black.collidepoint(mouse):
                        draw_black = True
                    elif draw_button_white.collidepoint(mouse):
                        draw_white = True
                    elif sign_out_button.collidepoint(mouse):
                        frame = "login"

        if draw_white or draw_black:
            if up_move_button.collidepoint(mouse):
                bg = pygame.image.load("assets/draw_accept.png")
            elif down_move_button.collidepoint(mouse):
                bg = pygame.image.load("assets/draw_cancel.png")
            else:
                bg = pygame.image.load("assets/draw_neutral.png")

        if surrender_white or surrender_black:
            if up_move_button.collidepoint(mouse):
                bg = pygame.image.load("assets/surrender_accept.png")
            elif down_move_button.collidepoint(mouse):
                bg = pygame.image.load("assets/surrender_cancel.png")
            else:
                bg = pygame.image.load("assets/surrender_neutral.png")

        if end_game:
            if winner == "white":
                winner_text = font(30).render("White Wins!", True, dirty_white)
                screen.blit(winner_text, winner_text.get_rect(center=(1075, 360)))
            elif winner == "black":
                winner_text = font(30).render("Black Wins!", True, dirty_white)
                screen.blit(winner_text, winner_text.get_rect(center=(1075, 360)))
            elif winner == "draw":
                winner_text = font(30).render("Its a Draw!", True, dirty_white)
                screen.blit(winner_text, winner_text.get_rect(center=(1075, 360)))

            if up_move_button.collidepoint(mouse):
                bg = pygame.image.load("assets/end_rematch.png")
            elif down_move_button.collidepoint(mouse):
                bg = pygame.image.load("assets/end_new_game.png")
            else:
                bg = pygame.image.load("assets/end_neutral.png")

        if board.print_winner() == "white" or state == "white":
            winner = "white"
            if player_one_color == "white":
                accounts[player_one.name].wins += 1
                accounts[player_one.name].games.append(["win", player_two.name])
                accounts[player_two.name].losses += 1
                accounts[player_two.name].games.append(["loss", player_one.name])
            elif player_one_color == "black":
                accounts[player_two.name].wins += 1
                accounts[player_two.name].games.append(["win", player_one.name])
                accounts[player_one.name].losses += 1
                accounts[player_one.name].games.append(["loss", player_two.name])
        elif board.print_winner() == "black" or state == "black":
            winner = "black"
            if player_one_color == "black":
                accounts[player_one.name].wins += 1
                accounts[player_one.name].games.append(["win", player_two.name])
                accounts[player_two.name].losses += 1
                accounts[player_two.name].games.append(["loss", player_one.name])
            elif player_one_color == "white":
                accounts[player_two.name].wins += 1
                accounts[player_two.name].games.append(["win", player_one.name])
                accounts[player_one.name].losses += 1
                accounts[player_one.name].games.append(["loss", player_two.name])
        elif board.print_winner() == "draw" or state == "draw":
            winner = "draw"
            accounts[player_one.name].draws += 1
            accounts[player_one.name].games.append(["draw", player_two.name])
            accounts[player_two.name].draws += 1
            accounts[player_two.name].games.append(["draw", player_one.name])
            
        if board.print_winner() != None or state != None:
            board.checkmate = False
            state = None
            end_game = True
            board.stalemate = False

        redraw(screen, board, moves)
        clock.tick(FPS)
        pygame.display.update()