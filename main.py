from enum import Enum
import random
import pygame
import time

import Card_Priorities

window_height = 650
window_width = 1200
global speed
# pygame related
pygame.init()
pygame.display.set_caption("UNO Flip")
window = pygame.display.set_mode((window_width, window_height))
refresh_controller = pygame.time.Clock()


class LightColor(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    BLACK = 5


class DarkColor(Enum):
    PINK = 1
    CYAN = 2
    ORANGE = 3
    PURPLE = 4
    WHITE = 5


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    DRAW_1 = 10
    SKIP = 11
    REVERSE = 12
    WILD = 13
    WILD_DRAW_2 = 14
    FLIP = 15
    DRAW_5 = 16
    SKIP_EVERYONE = 17
    WILD_DRAW_COLOR = 18


class Card:
    light_side = None
    dark_side = None

    def __init__(self, _light_side, _dark_side):
        self.light_side = _light_side
        self.dark_side = _dark_side


# Variablen
players = []  # Liste mit Länge entsprechend der Anzahl an Spielern. Jedes Listenelement von players repräsentiert die Handkarten des Spielers
com_players = []  # Liste mit Länge entsprechend der Anzahl an Spielern. Jedes Listenelement zeigt, ob der entsprechende Spieler computergesteuert (True) ist
global player
player = 0
global light
light = True
global clockwise
clockwise = True

discard_pile = []  # Ablagestapel
draw_pile = []  # Ziehstapel
global upper_card  # Karte, die oben auf dem Ablagestapel liegt
upper_card = None
global played_card  # Karte, die vom vorangegangenen Spieler gespielt wurde
played_card = None
global wished_light_color
wished_light_color = LightColor.BLACK
global wished_dark_color
wished_dark_color = DarkColor.WHITE

# für die repaint-Methode:
global card_width
global card_height
global discard_pile_pos_x
discard_pile_pos_x = window_width * 0.7
global discard_pile_pos_y
discard_pile_pos_y = window_height * 0.36
draw_pile_pos_x = window_width * 0.25
draw_pile_pos_y = window_height * 0.36
player_1_pos_x = window_width * 0.3
player_1_pos_y = window_height * 0.65
player_2_pos_x = 100
player_2_pos_y = 100
player_3_pos_x = window_width * 0.3
player_3_pos_y = window_height * 0.06
player_4_pos_x = 1000
player_4_pos_y = 100
card_gap = 40
global arrow_pos_x
arrow_pos_x = 0
global arrow_pos_y
arrow_pos_y = 0
selected_card_pos_x = window_width - 130  # zeigt den Kopf der aktuell ausgewählten Karte unten rechts nochmal an (falls der Spieler wegen zu vieler Karten auf der Hand nicht sieht)
selected_card_pos_y = window_height - card_gap * 1.2
selected_card_opposite_pos_x = 10
selected_card_opposite_pos_y = selected_card_pos_y

# Texte
global action_text
action_text = ""
global uno_text
uno_text = ""
global wished_color_text
wished_color_text = ""

# sonstige Hilfsvariablen:
global w_pressed
global index
index = 0
global color_wished

# Bilder (Karten) laden
png_red_one = pygame.image.load("unoflip_symbols/unoflip_red_1.png")
png_red_two = pygame.image.load("unoflip_symbols/unoflip_red_2.png")
png_red_three = pygame.image.load("unoflip_symbols/unoflip_red_3.png")
png_red_four = pygame.image.load("unoflip_symbols/unoflip_red_4.png")
png_red_five = pygame.image.load("unoflip_symbols/unoflip_red_5.png")
png_red_six = pygame.image.load("unoflip_symbols/unoflip_red_6.png")
png_red_seven = pygame.image.load("unoflip_symbols/unoflip_red_7.png")
png_red_eight = pygame.image.load("unoflip_symbols/unoflip_red_8.png")
png_red_nine = pygame.image.load("unoflip_symbols/unoflip_red_9.png")
png_red_reverse = pygame.image.load("unoflip_symbols/unoflip_red_reverse.png")
png_red_skip = pygame.image.load("unoflip_symbols/unoflip_red_skip.png")
png_red_draw_one = pygame.image.load("unoflip_symbols/unoflip_red_draw1.png")
png_red_flip = pygame.image.load("unoflip_symbols/unoflip_red_flip.png")

png_green_one = pygame.image.load("unoflip_symbols/unoflip_green_1.png")
png_green_two = pygame.image.load("unoflip_symbols/unoflip_green_2.png")
png_green_three = pygame.image.load("unoflip_symbols/unoflip_green_3.png")
png_green_four = pygame.image.load("unoflip_symbols/unoflip_green_4.png")
png_green_five = pygame.image.load("unoflip_symbols/unoflip_green_5.png")
png_green_six = pygame.image.load("unoflip_symbols/unoflip_green_6.png")
png_green_seven = pygame.image.load("unoflip_symbols/unoflip_green_7.png")
png_green_eight = pygame.image.load("unoflip_symbols/unoflip_green_8.png")
png_green_nine = pygame.image.load("unoflip_symbols/unoflip_green_9.png")
png_green_reverse = pygame.image.load("unoflip_symbols/unoflip_green_reverse.png")
png_green_skip = pygame.image.load("unoflip_symbols/unoflip_green_skip.png")
png_green_draw_one = pygame.image.load("unoflip_symbols/unoflip_green_draw1.png")
png_green_flip = pygame.image.load("unoflip_symbols/unoflip_green_flip.png")

png_yellow_one = pygame.image.load("unoflip_symbols/unoflip_yellow_1.png")
png_yellow_two = pygame.image.load("unoflip_symbols/unoflip_yellow_2.png")
png_yellow_three = pygame.image.load("unoflip_symbols/unoflip_yellow_3.png")
png_yellow_four = pygame.image.load("unoflip_symbols/unoflip_yellow_4.png")
png_yellow_five = pygame.image.load("unoflip_symbols/unoflip_yellow_5.png")
png_yellow_six = pygame.image.load("unoflip_symbols/unoflip_yellow_6.png")
png_yellow_seven = pygame.image.load("unoflip_symbols/unoflip_yellow_7.png")
png_yellow_eight = pygame.image.load("unoflip_symbols/unoflip_yellow_8.png")
png_yellow_nine = pygame.image.load("unoflip_symbols/unoflip_yellow_9.png")
png_yellow_reverse = pygame.image.load("unoflip_symbols/unoflip_yellow_reverse.png")
png_yellow_skip = pygame.image.load("unoflip_symbols/unoflip_yellow_skip.png")
png_yellow_draw_one = pygame.image.load("unoflip_symbols/unoflip_yellow_draw1.png")
png_yellow_flip = pygame.image.load("unoflip_symbols/unoflip_yellow_flip.png")

png_blue_one = pygame.image.load("unoflip_symbols/unoflip_blue_1.png")
png_blue_two = pygame.image.load("unoflip_symbols/unoflip_blue_2.png")
png_blue_three = pygame.image.load("unoflip_symbols/unoflip_blue_3.png")
png_blue_four = pygame.image.load("unoflip_symbols/unoflip_blue_4.png")
png_blue_five = pygame.image.load("unoflip_symbols/unoflip_blue_5.png")
png_blue_six = pygame.image.load("unoflip_symbols/unoflip_blue_6.png")
png_blue_seven = pygame.image.load("unoflip_symbols/unoflip_blue_7.png")
png_blue_eight = pygame.image.load("unoflip_symbols/unoflip_blue_8.png")
png_blue_nine = pygame.image.load("unoflip_symbols/unoflip_blue_9.png")
png_blue_reverse = pygame.image.load("unoflip_symbols/unoflip_blue_reverse.png")
png_blue_skip = pygame.image.load("unoflip_symbols/unoflip_blue_skip.png")
png_blue_draw_one = pygame.image.load("unoflip_symbols/unoflip_blue_draw1.png")
png_blue_flip = pygame.image.load("unoflip_symbols/unoflip_blue_flip.png")

png_black_wild = pygame.image.load("unoflip_symbols/unoflip_black_wild.png")
png_black_wild_draw_two = pygame.image.load("unoflip_symbols/unoflip_black_wilddraw2.png")

png_pink_one = pygame.image.load("unoflip_symbols/unoflip_pink_1.png")
png_pink_two = pygame.image.load("unoflip_symbols/unoflip_pink_2.png")
png_pink_three = pygame.image.load("unoflip_symbols/unoflip_pink_3.png")
png_pink_four = pygame.image.load("unoflip_symbols/unoflip_pink_4.png")
png_pink_five = pygame.image.load("unoflip_symbols/unoflip_pink_5.png")
png_pink_six = pygame.image.load("unoflip_symbols/unoflip_pink_6.png")
png_pink_seven = pygame.image.load("unoflip_symbols/unoflip_pink_7.png")
png_pink_eight = pygame.image.load("unoflip_symbols/unoflip_pink_8.png")
png_pink_nine = pygame.image.load("unoflip_symbols/unoflip_pink_9.png")
png_pink_reverse = pygame.image.load("unoflip_symbols/unoflip_pink_reverse.png")
png_pink_skip_everyone = pygame.image.load("unoflip_symbols/unoflip_pink_skipeveryone.png")
png_pink_draw_five = pygame.image.load("unoflip_symbols/unoflip_pink_draw5.png")
png_pink_flip = pygame.image.load("unoflip_symbols/unoflip_pink_flip.png")

png_cyan_one = pygame.image.load("unoflip_symbols/unoflip_cyan_1.png")
png_cyan_two = pygame.image.load("unoflip_symbols/unoflip_cyan_2.png")
png_cyan_three = pygame.image.load("unoflip_symbols/unoflip_cyan_3.png")
png_cyan_four = pygame.image.load("unoflip_symbols/unoflip_cyan_4.png")
png_cyan_five = pygame.image.load("unoflip_symbols/unoflip_cyan_5.png")
png_cyan_six = pygame.image.load("unoflip_symbols/unoflip_cyan_6.png")
png_cyan_seven = pygame.image.load("unoflip_symbols/unoflip_cyan_7.png")
png_cyan_eight = pygame.image.load("unoflip_symbols/unoflip_cyan_8.png")
png_cyan_nine = pygame.image.load("unoflip_symbols/unoflip_cyan_9.png")
png_cyan_reverse = pygame.image.load("unoflip_symbols/unoflip_cyan_reverse.png")
png_cyan_skip_everyone = pygame.image.load("unoflip_symbols/unoflip_cyan_skipeveryone.png")
png_cyan_draw_five = pygame.image.load("unoflip_symbols/unoflip_cyan_draw5.png")
png_cyan_flip = pygame.image.load("unoflip_symbols/unoflip_cyan_flip.png")

png_orange_one = pygame.image.load("unoflip_symbols/unoflip_orange_1.png")
png_orange_two = pygame.image.load("unoflip_symbols/unoflip_orange_2.png")
png_orange_three = pygame.image.load("unoflip_symbols/unoflip_orange_3.png")
png_orange_four = pygame.image.load("unoflip_symbols/unoflip_orange_4.png")
png_orange_five = pygame.image.load("unoflip_symbols/unoflip_orange_5.png")
png_orange_six = pygame.image.load("unoflip_symbols/unoflip_orange_6.png")
png_orange_seven = pygame.image.load("unoflip_symbols/unoflip_orange_7.png")
png_orange_eight = pygame.image.load("unoflip_symbols/unoflip_orange_8.png")
png_orange_nine = pygame.image.load("unoflip_symbols/unoflip_orange_9.png")
png_orange_reverse = pygame.image.load("unoflip_symbols/unoflip_orange_reverse.png")
png_orange_skip_everyone = pygame.image.load("unoflip_symbols/unoflip_orange_skipeveryone.png")
png_orange_draw_five = pygame.image.load("unoflip_symbols/unoflip_orange_draw5.png")
png_orange_flip = pygame.image.load("unoflip_symbols/unoflip_orange_flip.png")

png_purple_one = pygame.image.load("unoflip_symbols/unoflip_purple_1.png")
png_purple_two = pygame.image.load("unoflip_symbols/unoflip_purple_2.png")
png_purple_three = pygame.image.load("unoflip_symbols/unoflip_purple_3.png")
png_purple_four = pygame.image.load("unoflip_symbols/unoflip_purple_4.png")
png_purple_five = pygame.image.load("unoflip_symbols/unoflip_purple_5.png")
png_purple_six = pygame.image.load("unoflip_symbols/unoflip_purple_6.png")
png_purple_seven = pygame.image.load("unoflip_symbols/unoflip_purple_7.png")
png_purple_eight = pygame.image.load("unoflip_symbols/unoflip_purple_8.png")
png_purple_nine = pygame.image.load("unoflip_symbols/unoflip_purple_9.png")
png_purple_reverse = pygame.image.load("unoflip_symbols/unoflip_purple_reverse.png")
png_purple_skip_everyone = pygame.image.load("unoflip_symbols/unoflip_purple_skipeveryone.png")
png_purple_draw_five = pygame.image.load("unoflip_symbols/unoflip_purple_draw5.png")
png_purple_flip = pygame.image.load("unoflip_symbols/unoflip_purple_flip.png")

png_white_wild = pygame.image.load("unoflip_symbols/unoflip_white_wild.png")
png_white_wild_draw_color = pygame.image.load("unoflip_symbols/unoflip_white_wilddrawcolor.png")

# Sonstige Bilder laden
arrow_up = pygame.image.load("unoflip_symbols/unoflip_arrow_up.png")
arrow_right = pygame.image.load("unoflip_symbols/unoflip_arrow_right.png")
arrow_down = pygame.image.load("unoflip_symbols/unoflip_arrow_down.png")
arrow_left = pygame.image.load("unoflip_symbols/unoflip_arrow_left.png")


# Setting Methoden


def set_speed(n):
    global speed
    speed = n


def set_players(n):
    for i in range(0, n):
        players.append([])


def set_card_size(c_width, c_height):
    global card_width
    global card_height
    card_width = c_width
    card_height = c_height


# Spiellogik


def deal_cards(n):
    for player in players:
        drawn_cards = 0
        while drawn_cards < 7:
            player.append(draw_pile[len(draw_pile) - 1])
            del draw_pile[len(draw_pile) - 1]
            drawn_cards += 1


def reveal_card():
    discard_pile.append(draw_pile[len(draw_pile) - 1])
    del draw_pile[len(draw_pile) - 1]
    return discard_pile[len(discard_pile) - 1]


def light_card_is_valid(chosen_card):  # chosen_card ist Card
    card_color = chosen_card.light_side[0]
    card_symbol = chosen_card.light_side[1]
    upper_card_color = upper_card.light_side[0]
    upper_card_symbol = upper_card.light_side[1]
    # gleiche Farbe, Symbol oder Joker
    if card_color == upper_card_color or card_symbol == upper_card_symbol or card_color == card_color.BLACK:
        return True
    # Wenn Joker oben liegt, gewünschte Farbe spielen:
    elif upper_card_color == upper_card_color.BLACK:
        if wished_light_color == wished_light_color.RED:
            if card_color == card_color.RED:
                return True
        elif wished_light_color == wished_light_color.GREEN:
            if card_color == card_color.GREEN:
                return True
        elif wished_light_color == wished_light_color.YELLOW:
            if card_color == card_color.YELLOW:
                return True
        elif wished_light_color == wished_light_color.BLUE:
            if card_color == card_color.BLUE:
                return True
    else:
        return False


def dark_card_is_valid(chosen_card):  # chosen_card ist Card
    card_color = chosen_card.dark_side[0]
    card_symbol = chosen_card.dark_side[1]
    upper_card_color = upper_card.dark_side[0]
    upper_card_symbol = upper_card.dark_side[1]
    # gleiche Farbe, Symbol oder Joker
    if card_color == upper_card_color or card_symbol == upper_card_symbol or card_color == card_color.WHITE:
        return True
    # Wenn Joker oben liegt, gewünschte Farbe spielen:
    elif upper_card_color == upper_card_color.WHITE:
        if wished_dark_color == wished_dark_color.PINK:
            if card_color == card_color.PINK:
                return True
        elif wished_dark_color == wished_dark_color.CYAN:
            if card_color == card_color.CYAN:
                return True
        elif wished_dark_color == wished_dark_color.ORANGE:
            if card_color == card_color.ORANGE:
                return True
        elif wished_dark_color == wished_dark_color.PURPLE:
            if card_color == card_color.PURPLE:
                return True
    else:
        return False


def card_light_is_number(card):
    card_number = card.light_side[1]
    if card_number == card_number.ONE or card_number == card_number.TWO or card_number == card_number.THREE or card_number == card_number.FOUR or card_number == card_number.FIVE or card_number == card_number.SIX or card_number == card_number.SEVEN or card_number == card_number.EIGHT or card_number == card_number.NINE:
        return True
    else:
        return False


def card_dark_is_number(card):
    card_number = card.dark_side[1]
    if card_number == card_number.ONE or card_number == card_number.TWO or card_number == card_number.THREE or card_number == card_number.FOUR or card_number == card_number.FIVE or card_number == card_number.SIX or card_number == card_number.SEVEN or card_number == card_number.EIGHT or card_number == card_number.NINE:
        return True
    else:
        return False


def player_is_com():  # überprüfe, ob der Spieler, der grad dran ist, computergesteuert ist
    if com_players[player]:
        return True
    else:
        return False


def play_card(
        card_to_play):  # player, der eine Karte aus seiner Hand spielt; card_to_play ist der index der zu spielenden Karte
    discard_pile.append(players[player][card_to_play])
    now_played_card = players[player][card_to_play]
    del players[player][card_to_play]
    return now_played_card


def draw_cards(cards_to_draw):
    num_of_drawn_cards = 0
    while num_of_drawn_cards < cards_to_draw:
        players[player].append(draw_pile[len(draw_pile) - 1])
        draw_pile.pop()
        num_of_drawn_cards += 1
        refresh_screen()
        time.sleep(0.4)


def wish_for_color(color_int):
    global light
    if light:
        global wished_light_color
        if color_int == 1:
            wished_light_color = wished_light_color.RED
        elif color_int == 2:
            wished_light_color = wished_light_color.GREEN
        elif color_int == 3:
            wished_light_color = wished_light_color.YELLOW
        elif color_int == 4:
            wished_light_color = wished_light_color.BLUE
    else:
        global wished_dark_color
        if color_int == 1:
            wished_dark_color = wished_dark_color.PINK
        elif color_int == 2:
            wished_dark_color = wished_dark_color.CYAN
        elif color_int == 3:
            wished_dark_color = wished_dark_color.ORANGE
        elif color_int == 4:
            wished_dark_color = wished_dark_color.PURPLE


def handle_keys_one_to_four():
    global color_wished
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_1:
            wish_for_color(1)
            color_wished = True
            return 1
        elif event.key == pygame.K_2:
            wish_for_color(2)
            color_wished = True
            return 2
        elif event.key == pygame.K_3:
            wish_for_color(3)
            color_wished = True
            return 3
        elif event.key == pygame.K_4:
            wish_for_color(4)
            color_wished = True
            return 4


def draw_color():  # Solange Karten ziehen, bis die gewünschte Farbe gezogen wurde
    while True:
        draw_cards(1)
        if wished_dark_color == wished_dark_color.PINK:
            if players[player][len(players[player]) - 1].dark_side[0] == \
                    players[player][len(players[player]) - 1].dark_side[0].PINK:
                break
        elif wished_dark_color == wished_dark_color.CYAN:
            if players[player][len(players[player]) - 1].dark_side[0] == \
                    players[player][len(players[player]) - 1].dark_side[0].CYAN:
                break
        elif wished_dark_color == wished_dark_color.ORANGE:
            if players[player][len(players[player]) - 1].dark_side[0] == \
                    players[player][len(players[player]) - 1].dark_side[0].ORANGE:
                break
        elif wished_dark_color == wished_dark_color.PURPLE:
            if players[player][len(players[player]) - 1].dark_side[0] == \
                    players[player][len(players[player]) - 1].dark_side[0].PURPLE:
                break
        continue


def reverse_game():
    global clockwise
    if clockwise:
        clockwise = False
    else:
        clockwise = True


def change_player():  # ändert den Spieler, der dran ist
    global player
    global clockwise
    if clockwise:
        if player >= len(players) - 1:
            player = 0
        else:
            player += 1
    else:
        if player == 0:
            player = len(players) - 1
        else:
            player -= 1


def identify_next_player(
        player):  # gibt den Spieler zurück, der nach dem jetzigen Spieler dran ist (für com-Unterstützung)
    if clockwise:
        if player >= len(players) - 1:
            next_player = 0
        else:
            next_player = player + 1
    else:
        if player == 0:
            next_player = len(players) - 1
        else:
            next_player = player - 1
    return next_player


def identify_next_next_player():  # gibt den Spieler zurück, der nach dem nächsten Spieler dran ist (für com-Unterstützung)
    next_player = identify_next_player(player)
    next_next_player = identify_next_player(next_player)
    return next_next_player


def identify_prev_player():  # gibt den Spieler zurück, der vor dem jetzigen Spieler dran ist (für com-Unterstützung)
    if clockwise:
        if player == 0:
            prev_player = len(players) - 1
        else:
            prev_player = player - 1
    else:
        if player == len(players) - 1:
            prev_player = 0
        else:
            prev_player = player + 1
    return prev_player


def paint_card_light(card, pos_x, pos_y):
    if card.light_side[0] == card.light_side[0].RED:
        if card.light_side[1] == card.light_side[1].ONE:
            window.blit(png_red_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].TWO:
            window.blit(png_red_two, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].THREE:
            window.blit(png_red_three, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FOUR:
            window.blit(png_red_four, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FIVE:
            window.blit(png_red_five, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SIX:
            window.blit(png_red_six, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SEVEN:
            window.blit(png_red_seven, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].EIGHT:
            window.blit(png_red_eight, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].NINE:
            window.blit(png_red_nine, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].REVERSE:
            window.blit(png_red_reverse, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SKIP:
            window.blit(png_red_skip, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].DRAW_1:
            window.blit(png_red_draw_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FLIP:
            window.blit(png_red_flip, (pos_x, pos_y))

    if card.light_side[0] == card.light_side[0].GREEN:
        if card.light_side[1] == card.light_side[1].ONE:
            window.blit(png_green_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].TWO:
            window.blit(png_green_two, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].THREE:
            window.blit(png_green_three, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FOUR:
            window.blit(png_green_four, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FIVE:
            window.blit(png_green_five, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SIX:
            window.blit(png_green_six, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SEVEN:
            window.blit(png_green_seven, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].EIGHT:
            window.blit(png_green_eight, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].NINE:
            window.blit(png_green_nine, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].REVERSE:
            window.blit(png_green_reverse, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SKIP:
            window.blit(png_green_skip, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].DRAW_1:
            window.blit(png_green_draw_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FLIP:
            window.blit(png_green_flip, (pos_x, pos_y))

    if card.light_side[0] == card.light_side[0].YELLOW:
        if card.light_side[1] == card.light_side[1].ONE:
            window.blit(png_yellow_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].TWO:
            window.blit(png_yellow_two, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].THREE:
            window.blit(png_yellow_three, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FOUR:
            window.blit(png_yellow_four, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FIVE:
            window.blit(png_yellow_five, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SIX:
            window.blit(png_yellow_six, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SEVEN:
            window.blit(png_yellow_seven, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].EIGHT:
            window.blit(png_yellow_eight, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].NINE:
            window.blit(png_yellow_nine, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].REVERSE:
            window.blit(png_yellow_reverse, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SKIP:
            window.blit(png_yellow_skip, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].DRAW_1:
            window.blit(png_yellow_draw_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FLIP:
            window.blit(png_yellow_flip, (pos_x, pos_y))

    if card.light_side[0] == card.light_side[0].BLUE:
        if card.light_side[1] == card.light_side[1].ONE:
            window.blit(png_blue_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].TWO:
            window.blit(png_blue_two, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].THREE:
            window.blit(png_blue_three, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FOUR:
            window.blit(png_blue_four, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FIVE:
            window.blit(png_blue_five, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SIX:
            window.blit(png_blue_six, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SEVEN:
            window.blit(png_blue_seven, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].EIGHT:
            window.blit(png_blue_eight, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].NINE:
            window.blit(png_blue_nine, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].REVERSE:
            window.blit(png_blue_reverse, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].SKIP:
            window.blit(png_blue_skip, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].DRAW_1:
            window.blit(png_blue_draw_one, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].FLIP:
            window.blit(png_blue_flip, (pos_x, pos_y))

    if card.light_side[0] == card.light_side[0].BLACK:
        if card.light_side[1] == card.light_side[1].WILD:
            window.blit(png_black_wild, (pos_x, pos_y))
        elif card.light_side[1] == card.light_side[1].WILD_DRAW_2:
            window.blit(png_black_wild_draw_two, (pos_x, pos_y))


def paint_card_dark(card, pos_x, pos_y):
    if card.dark_side[0] == card.dark_side[0].PINK:
        if card.dark_side[1] == card.dark_side[1].ONE:
            window.blit(png_pink_one, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].TWO:
            window.blit(png_pink_two, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].THREE:
            window.blit(png_pink_three, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FOUR:
            window.blit(png_pink_four, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FIVE:
            window.blit(png_pink_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SIX:
            window.blit(png_pink_six, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SEVEN:
            window.blit(png_pink_seven, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].EIGHT:
            window.blit(png_pink_eight, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].NINE:
            window.blit(png_pink_nine, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].REVERSE:
            window.blit(png_pink_reverse, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SKIP_EVERYONE:
            window.blit(png_pink_skip_everyone, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].DRAW_5:
            window.blit(png_pink_draw_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FLIP:
            window.blit(png_pink_flip, (pos_x, pos_y))

    if card.dark_side[0] == card.dark_side[0].CYAN:
        if card.dark_side[1] == card.dark_side[1].ONE:
            window.blit(png_cyan_one, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].TWO:
            window.blit(png_cyan_two, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].THREE:
            window.blit(png_cyan_three, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FOUR:
            window.blit(png_cyan_four, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FIVE:
            window.blit(png_cyan_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SIX:
            window.blit(png_cyan_six, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SEVEN:
            window.blit(png_cyan_seven, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].EIGHT:
            window.blit(png_cyan_eight, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].NINE:
            window.blit(png_cyan_nine, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].REVERSE:
            window.blit(png_cyan_reverse, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SKIP_EVERYONE:
            window.blit(png_cyan_skip_everyone, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].DRAW_5:
            window.blit(png_cyan_draw_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FLIP:
            window.blit(png_cyan_flip, (pos_x, pos_y))

    if card.dark_side[0] == card.dark_side[0].ORANGE:
        if card.dark_side[1] == card.dark_side[1].ONE:
            window.blit(png_orange_one, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].TWO:
            window.blit(png_orange_two, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].THREE:
            window.blit(png_orange_three, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FOUR:
            window.blit(png_orange_four, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FIVE:
            window.blit(png_orange_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SIX:
            window.blit(png_orange_six, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SEVEN:
            window.blit(png_orange_seven, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].EIGHT:
            window.blit(png_orange_eight, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].NINE:
            window.blit(png_orange_nine, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].REVERSE:
            window.blit(png_orange_reverse, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SKIP_EVERYONE:
            window.blit(png_orange_skip_everyone, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].DRAW_5:
            window.blit(png_orange_draw_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FLIP:
            window.blit(png_orange_flip, (pos_x, pos_y))

    if card.dark_side[0] == card.dark_side[0].PURPLE:
        if card.dark_side[1] == card.dark_side[1].ONE:
            window.blit(png_purple_one, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].TWO:
            window.blit(png_purple_two, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].THREE:
            window.blit(png_purple_three, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FOUR:
            window.blit(png_purple_four, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FIVE:
            window.blit(png_purple_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SIX:
            window.blit(png_purple_six, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SEVEN:
            window.blit(png_purple_seven, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].EIGHT:
            window.blit(png_purple_eight, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].NINE:
            window.blit(png_purple_nine, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].REVERSE:
            window.blit(png_purple_reverse, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].SKIP_EVERYONE:
            window.blit(png_purple_skip_everyone, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].DRAW_5:
            window.blit(png_purple_draw_five, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].FLIP:
            window.blit(png_purple_flip, (pos_x, pos_y))

    if card.dark_side[0] == card.dark_side[0].WHITE:
        if card.dark_side[1] == card.dark_side[1].WILD:
            window.blit(png_white_wild, (pos_x, pos_y))
        elif card.dark_side[1] == card.dark_side[1].WILD_DRAW_COLOR:
            window.blit(png_white_wild_draw_color, (pos_x, pos_y))


def paint_player_hand_light():
    # Karten von Spieler 1, 2, 3, ... zeichnen
    for p in range(0, len(players)):
        if player == p and not player_is_com():  # ist Spieler p an der Reihe und KEIN com-Spieler? -> helle Karten zeichnen
            for i in range(0, len(players[player])):
                if p == 0:
                    paint_card_light(players[player][i], player_1_pos_x + i * card_gap, player_1_pos_y)
                elif p == 1:
                    paint_card_light(players[player][i], player_2_pos_x, player_2_pos_y + i * card_gap)
                elif p == 2:
                    paint_card_light(players[player][i], player_3_pos_x + i * card_gap, player_3_pos_y)
                elif p == 3:
                    paint_card_light(players[player][i], player_4_pos_x, player_4_pos_y + i * card_gap)
        else:  # ist Spieler p nicht an der Reihe? -> dunkle Karten zeichnen
            for i in range(0, len(players[p])):
                if p == 0:
                    paint_card_dark(players[p][i], player_1_pos_x + i * card_gap, player_1_pos_y)
                elif p == 1:
                    paint_card_dark(players[p][i], player_2_pos_x, player_2_pos_y + i * card_gap)
                elif p == 2:
                    paint_card_dark(players[p][i], player_3_pos_x + i * card_gap, player_3_pos_y)
                elif p == 3:
                    paint_card_dark(players[p][i], player_4_pos_x, player_4_pos_y + i * card_gap)


def paint_player_hand_dark():
    # Karten von Spieler 1, 2, 3, ... zeichnen
    for p in range(0, len(players)):
        if player == p and not player_is_com():  # ist Spieler p an der Reihe und KEIN com-Spieler? -> dunkle Karten zeichnen
            for i in range(0, len(players[player])):
                if p == 0:
                    paint_card_dark(players[player][i], player_1_pos_x + i * card_gap, player_1_pos_y)
                elif p == 1:
                    paint_card_dark(players[player][i], player_2_pos_x, player_2_pos_y + i * card_gap)
                elif p == 2:
                    paint_card_dark(players[player][i], player_3_pos_x + i * card_gap, player_3_pos_y)
                elif p == 3:
                    paint_card_dark(players[player][i], player_4_pos_x, player_4_pos_y + i * card_gap)
        else:  # ist Spieler p nicht an der Reihe? -> helle Karten zeichnen
            for i in range(0, len(players[p])):
                if p == 0:
                    paint_card_light(players[p][i], player_1_pos_x + i * card_gap, player_1_pos_y)
                elif p == 1:
                    paint_card_light(players[p][i], player_2_pos_x, player_2_pos_y + i * card_gap)
                elif p == 2:
                    paint_card_light(players[p][i], player_3_pos_x + i * card_gap, player_3_pos_y)
                elif p == 3:
                    paint_card_light(players[p][i], player_4_pos_x, player_4_pos_y + i * card_gap)


def paint_arrow():
    if player == 0:
        window.blit(arrow_up, (arrow_pos_x, arrow_pos_y))
    elif player == 1:
        window.blit(arrow_right, (arrow_pos_x, arrow_pos_y))
    elif player == 2:
        window.blit(arrow_down, (arrow_pos_x, arrow_pos_y))
    elif player == 3:
        window.blit(arrow_left, (arrow_pos_x, arrow_pos_y))


def repaint_light():
    window.fill(pygame.Color(200, 200, 200))

    # Ablagestapel zeichnen
    paint_card_light(upper_card, discard_pile_pos_x, discard_pile_pos_y)

    # Ziehstapel zeichnen
    paint_card_dark(draw_pile[len(draw_pile) - 1], draw_pile_pos_x, draw_pile_pos_y)

    # Karten des Spielers zeichnen
    paint_player_hand_light()

    # Auswahlpfeil zeichnen
    if not player_is_com():
        paint_arrow()

    # Texte einblenden
    write_text(action_text, "action")
    write_text(uno_text, "uno")
    write_text(wished_color_text, "wished color")

    # aktuell gewählte Karte unten rechts einblenden und ggü. liegende Seite der gewählten Karte unten links einblenden
    if not player_is_com() and 0 <= index < len(players[player]):
        paint_card_light(players[player][index], selected_card_pos_x, selected_card_pos_y)
        paint_card_dark(players[player][index], selected_card_opposite_pos_x, selected_card_opposite_pos_y)


def repaint_dark():
    window.fill(pygame.Color(70, 50, 70))

    # Ablagestapel zeichnen
    paint_card_dark(upper_card, discard_pile_pos_x, discard_pile_pos_y)

    # Ziehstapel zeichnen
    paint_card_light(draw_pile[len(draw_pile) - 1], draw_pile_pos_x, draw_pile_pos_y)

    # Karten von Spieler 1, 2, 3, ... zeichnen
    paint_player_hand_dark()

    # Auswahlpfeil zeichnen
    if not player_is_com():
        paint_arrow()

    # Texte einblenden
    write_text(action_text, "action")
    write_text(uno_text, "uno")
    write_text(wished_color_text, "wished color")

    # aktuell gewählte Karte unten rechts einblenden und ggü. liegende Seite der gewählten Karte unten links einblenden
    if not player_is_com() and 0 <= index < len(players[player]):
        paint_card_dark(players[player][index], selected_card_pos_x, selected_card_pos_y)
        paint_card_light(players[player][index], selected_card_opposite_pos_x, selected_card_opposite_pos_y)


def refresh_screen():
    pygame.display.update()
    if light:
        repaint_light()
    else:
        repaint_dark()


def set_arrow_position():  # setzt die Position des Pfeiles, der die aktuell gewählte Karte anzeigt
    global arrow_pos_x
    global arrow_pos_y
    if player == 0 and not player_is_com():
        arrow_pos_x = player_1_pos_x + index * card_gap
        arrow_pos_y = player_1_pos_y + card_height + 5
    elif player == 1 and not player_is_com():
        arrow_pos_x = player_2_pos_x - 35
        arrow_pos_y = player_2_pos_y + index * card_gap
    elif player == 2 and not player_is_com():
        arrow_pos_x = player_3_pos_x + index * card_gap
        arrow_pos_y = player_3_pos_y - 35
    elif player == 3 and not player_is_com():
        arrow_pos_x = player_4_pos_x + card_width
        arrow_pos_y = player_4_pos_y + index * card_gap


def handle_keys():
    global index
    global w_pressed
    refresh_screen()
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_a:
            if index <= 0:
                index = len(players[player]) - 1
            else:
                index -= 1
            set_arrow_position()
        elif event.key == pygame.K_d:
            if index >= len(players[player]) - 1:
                index = 0
            else:
                index += 1
            set_arrow_position()
        elif event.key == pygame.K_w:
            w_pressed = True
            return index
        # freiwillig Karte ziehen:
        elif event.key == pygame.K_s:
            w_pressed = True
            return -1


def choose_card():  # Karte mit Tasten (W, A, D) auswählen und index der gewünschten Karte übergeben
    global w_pressed
    w_pressed = False
    global index
    index = 0  # index für jeden neuen Spieler zurücksetzen
    set_arrow_position()
    while not w_pressed:
        i = handle_keys()
    return i


def choose_color():
    global color_wished
    color_wished = False
    while not color_wished:
        handle_keys_one_to_four()


def refill_draw_pile():
    while len(discard_pile) > 0:
        discard_pile_random_index = random.randint(0, len(discard_pile) - 1)
        draw_pile.append(discard_pile[discard_pile_random_index])
        del discard_pile[discard_pile_random_index]


def write_text(text,
               type_of_text):  # Text auf screen schreiben, Farbe/Position/Größe je nach type_of_text (action, wished color, uno, game over)
    if type_of_text == "action":
        color = pygame.Color(255, 255, 255)
        x_pos = window_width * 0.5
        y_pos = window_height * 0.4
        fonttype = "Arial"
        fontsize = 30
    elif type_of_text == "wished color":
        color = pygame.Color(255, 255, 255)
        x_pos = window_width * 0.5
        y_pos = window_height * 0.5
        fonttype = "Arial"
        fontsize = 20
        # auf deutsch übersetzen:
        if text == "RED":
            text = "ROT"
        elif text == "GREEN":
            text = "GRÜN"
        elif text == "YELLOW":
            text = "GELB"
        elif text == "BLUE":
            text = "BLAU"
        elif text == "PINK":
            text = "ROSA"
        elif text == "CYAN":
            text = "TÜRKIS"
        elif text == "ORANGE":
            text = "ORANGE"
        elif text == "PURPLE":
            text = "LILA"
    elif type_of_text == "uno":
        color = pygame.Color(255, 0, 34)
        x_pos = window_width * 0.5
        y_pos = window_height * 0.45
        fonttype = "Arial"
        fontsize = 40

    font = pygame.font.SysFont(fonttype, fontsize)  # Schriftart für Screeneinblendungen festlegen
    render = font.render(text, True, color)
    rect = render.get_rect()
    rect.midtop = (x_pos, y_pos)
    window.blit(render, rect)
    pygame.display.flip()


def check_for_uno():  # überprüfen, ob der Spieler nur noch eine Karte auf der Hand hat
    global uno_text
    if len(players[player]) == 1:
        uno_text = "Spieler " + str(player + 1) + ": UNO!"
        refresh_screen()
        time.sleep(1)
    else:
        uno_text = ""


def check_for_game_over():  # überprüfen, ob der Spieler keine Karte auf der Hand hat (Spiel vorbei)
    global uno_text
    if len(players[player]) == 0:
        uno_text = "Spieler " + str(player + 1) + " hat gewonnen!"
        refresh_screen()
        return True
    else:
        return False


def count_light_colors_on_hand():  # zählt, welche Farben wie oft auf der Spielerhand vertreten sind (für com-Unterstützung)
    num_red = 0
    num_green = 0
    num_yellow = 0
    num_blue = 0

    for card in players[player]:
        if card.light_side[0] == card.light_side[0].RED:
            num_red += 1
        elif card.light_side[0] == card.light_side[0].GREEN:
            num_green += 1
        elif card.light_side[0] == card.light_side[0].YELLOW:
            num_yellow += 1
        elif card.light_side[0] == card.light_side[0].BLUE:
            num_blue += 1
    num_color_list = [num_red, num_green, num_yellow, num_blue]
    return num_color_list


def count_dark_colors_on_hand():
    num_pink = 0
    num_cyan = 0
    num_orange = 0
    num_purple = 0

    for card in players[player]:
        if card.dark_side[0] == card.dark_side[0].PINK:
            num_pink += 1
        elif card.dark_side[0] == card.dark_side[0].CYAN:
            num_cyan += 1
        elif card.dark_side[0] == card.dark_side[0].ORANGE:
            num_orange += 1
        elif card.dark_side[0] == card.dark_side[0].PURPLE:
            num_purple += 1
    num_color_list = [num_pink, num_cyan, num_orange, num_purple]
    return num_color_list


def determine_color_to_wish(num_color_list):  # Farbe (1, 2, 3, 4) ermitteln und wünschen (für com-Unterstützung)
    num_color_list_max_ints = []
    max_int = max(num_color_list)
    for i in range(0, 4):
        if num_color_list[i] == max_int:
            num_color_list_max_ints.append(i)
    wish_for_color(random.choice(num_color_list_max_ints) + 1)


def determine_card_priorities(card_list):
    priority_list = []
    priority = 0
    next_player = identify_next_player(player)
    next_next_player = identify_next_next_player()
    prev_player = identify_prev_player()
    num_playable_cards = 0
    card_to_play = None  # Karte, die am Ende des Entscheidungsprozesses gespielt wird (index)
    # priority modifier (+ priority):
    priority_modifier_draw_one = 1
    priority_modifier_skip = 1
    priority_modifier_reverse = 1
    priority_modifier_wild = 1
    priority_modifier_wild_draw_two = 1
    priority_modifier_draw_five = 1
    priority_modifier_skip_everyone = 1
    priority_modifier_wild_draw_color = 1

    # Extra Priorität geben je nach Spielsituation:
    # Sonderfall 1: nächster Spieler hat nur eine Karte auf der Hand -> nächsten Spieler ziehen lassen
    if len(players[next_player]) == 1:
        priority_modifier_draw_one += 20
        priority_modifier_wild_draw_two += 10
        priority_modifier_draw_five += 20
        priority_modifier_wild_draw_color += 10
    # Sonderfall 2: nächster Spieler hat <= 3 Karten auf der Hand -> Ziehkarten höhere Priorität geben
    if len(players[next_player]) <= 3:
        priority_modifier_draw_one += 10
        priority_modifier_wild_draw_two += 5
        priority_modifier_draw_five += 10
        priority_modifier_wild_draw_color += 5
    # Sonderfall 3: bei mindestens 3 Spielern: übernächster Spieler hat nur eine Karte -> keine Aussetzkarte spielen
    if len(players) >= 3 and len(players[next_next_player]) == 1:
        priority_modifier_skip = 0
    # Sonderfall 4: vorangegangener Spieler hat nur eine Karte -> keine Reversekarte spielen
    if len(players[prev_player]) == 1:
        priority_modifier_reverse = 0

    # alle Handkarten durchgehen spielbare Indexe in eine Prioritätsliste geben. Karten mit höherer Priorität mehrfach in die Liste eintragen
    for i in range(0, len(card_list)):
        if light:
            if light_card_is_valid(players[player][i]):
                num_playable_cards += 1
                # Wenn Karte spielbar, dann je nach Prioritätsschlüssel an Liste anhängen
                if card_light_is_number(players[player][i]):
                    priority = Card_Priorities.light_number_priority
                elif players[player][i].light_side[1] == players[player][i].light_side[1].SKIP:
                    priority = Card_Priorities.light_skip_priority * priority_modifier_skip
                elif players[player][i].light_side[1] == players[player][i].light_side[1].REVERSE:
                    priority = Card_Priorities.light_reverse_priority * priority_modifier_reverse
                elif players[player][i].light_side[1] == players[player][i].light_side[1].DRAW_1:
                    priority = Card_Priorities.light_draw_one_priority * priority_modifier_draw_one
                elif players[player][i].light_side[1] == players[player][i].light_side[1].WILD:
                    priority = Card_Priorities.light_wild_priority * priority_modifier_wild
                elif players[player][i].light_side[1] == players[player][i].light_side[1].WILD_DRAW_2:
                    priority = Card_Priorities.light_wild_draw_two_priority * priority_modifier_wild_draw_two
                for j in range(0, int(priority)):
                    priority_list.append(i)
        else:
            if dark_card_is_valid(players[player][i]):
                num_playable_cards += 1
                # Wenn Karte spielbar, dann je nach Prioritätsschlüssel an Liste anhängen
                if card_dark_is_number(players[player][i]):
                    priority = Card_Priorities.dark_number_priority
                elif players[player][i].dark_side[1] == players[player][i].dark_side[1].SKIP_EVERYONE:
                    priority = Card_Priorities.dark_skip_everyone_priority * priority_modifier_skip_everyone
                elif players[player][i].dark_side[1] == players[player][i].dark_side[1].REVERSE:
                    priority = Card_Priorities.dark_reverse_priority * priority_modifier_reverse
                elif players[player][i].dark_side[1] == players[player][i].dark_side[1].DRAW_5:
                    priority = Card_Priorities.dark_draw_five_priority * priority_modifier_draw_five
                elif players[player][i].dark_side[1] == players[player][i].dark_side[1].WILD:
                    priority = Card_Priorities.dark_wild_priority * priority_modifier_wild
                elif players[player][i].dark_side[1] == players[player][i].dark_side[1].WILD_DRAW_COLOR:
                    priority = Card_Priorities.dark_wild_draw_color_priority * priority_modifier_wild_draw_color
                for j in range(0, int(priority)):
                    priority_list.append(i)

    return priority_list


def process_com_turn():
    global played_card
    card_to_play = None
    priority_list = determine_card_priorities(players[player])

    # wenn keine Karte in Prioritätsliste gefunden, dann Karte ziehen (selbst wenn Karte spielbar)
    if len(priority_list) == 0:
        draw_cards(1)
        # wenn gezogene Karte spielbar, dann spielen
        priority_list_2 = determine_card_priorities([players[player][len(players[player]) - 1]])
        if len(priority_list_2) != 0:  # Prioritätsliste nicht (oder nach gezogener Karte nichtmehr) leer? -> random-Funktion wählt einen Index aus
            card_to_play = random.choice(priority_list_2)
    else:
        card_to_play = random.choice(priority_list)

    # Karte mit gewähltem Index spielen (und als played_card setzen)
    if card_to_play is not None:
        played_card = play_card(card_to_play)

    # Wenn Joker gespielt wurde, Farbe wünschen:
    if played_card is not None:
        if light:
            if played_card.light_side[0] == played_card.light_side[0].BLACK:
                num_color_list = count_light_colors_on_hand()
                determine_color_to_wish(num_color_list)
        else:
            if played_card.dark_side[0] == played_card.dark_side[0].WHITE:
                num_color_list = count_dark_colors_on_hand()
                determine_color_to_wish(num_color_list)
    time.sleep(1)


def gameloop_light_side():
    # Hilfsvariablen:
    global wished_light_color  # Farbe, die beim Spielen eines Jokers gewünscht wird
    global upper_card
    global played_card
    global light
    global action_text
    global uno_text
    global wished_color_text
    played_card = None  # played_card beim ersten Mal in der light_gameloop zurücksetzen, da sie direkt nach dem umdrehen nicht relevant ist
    light = True

    while True:
        upper_card = discard_pile[len(discard_pile) - 1]
        action_text = "Spieler " + str(player + 1) + " ist dran"
        repaint_light()
        refresh_screen()
        if wished_light_color.name != "BLACK" and upper_card.light_side[0] == upper_card.light_side[
            0].BLACK:  # Wenn Joker oben liegt...
            wished_color_text = str(wished_light_color.name)
            refresh_screen()

        # Spieler verarbeitet zuletzt gelegte Karte (+1, +5, +2W, CW inkl. aussetzen)
        if played_card is not None:
            if played_card.light_side[1] == played_card.light_side[1].DRAW_1:
                draw_cards(1)
                change_player()
                played_card = None
                continue
            elif played_card.light_side[1] == played_card.light_side[1].WILD_DRAW_2:
                draw_cards(2)
                change_player()
                played_card = None
                continue

        played_card = None  # played_card zurücksetzen

        # Wenn Spieler computergesteuert, keine Eingaben machen
        if player_is_com():
            process_com_turn()
        else:  # sonst (Nutzereingaben abfragen)
            # Spieler wählt eine Karte von seiner Hand
            card_to_play = choose_card()

            # Wenn Karte korrekt, dann spielen, sonst andere Karte wählen...
            while True:
                # Karte ziehen?
                if card_to_play == -1:
                    draw_cards(1)
                    refresh_screen()
                    # gerade gezogene Karte spielen?
                    if light_card_is_valid(players[player][len(players[player]) - 1]):
                        refresh_screen()
                        action_text = "Gezogene Karte spielen? (w)"
                        refresh_screen()
                        play_drawn_card = choose_card()
                        if play_drawn_card != -1:
                            played_card = play_card(len(players[player]) - 1)
                    else:
                        time.sleep(1)
                    refresh_screen()
                    break

                # Karte im Gültigkeitsbereich?
                elif card_to_play < 0 or card_to_play >= len(players[player]):
                    refresh_screen()
                    card_to_play = choose_card()
                # wenn hier angelangt, ist die Eingabe eine gültige Handkarte
                # prüfe ob Karte spielbar
                elif light_card_is_valid(players[player][card_to_play]):
                    played_card = play_card(card_to_play)
                    break
                else:
                    refresh_screen()
                    action_text = "Karte nicht spielbar"
                    refresh_screen()
                    card_to_play = choose_card()

        check_for_uno()

        if check_for_game_over():  # wenn Spiel vorbei, aus der while Schleife ausbrechen
            time.sleep(3)
            break

        # Wenn JOKER gespielt wurde, dann Farbe wünschen
        if played_card is not None:
            if not player_is_com():
                if played_card.light_side[0] == played_card.light_side[0].BLACK:
                    refresh_screen()
                    wished_color_text = "Farbe wünschen (1=rot, 2=grün, 3=gelb, 4=blau)"
                    refresh_screen()
                    choose_color()  # händelt über Tasteneingabe (1-4) die zu wünschende Farbe und setzt sie fest

            # ggf. gespielte Aktionskarte (reverse, skip, flip, skip all) verarbeiten
            # REVERSE
            if played_card.light_side[1] == played_card.light_side[1].REVERSE:
                reverse_game()
            # SKIP nächsten Spieler
            elif played_card.light_side[1] == played_card.light_side[1].SKIP:
                change_player()  # einmal zusätzlich den Spieler weiterschalten (sodass am Ende ein Spieler übersprungen wird)

        # nächster Spieler (je nach Spielrichtung)
        change_player()

        # Wenn notwendig, Nachziehstapel auffüllen
        if len(draw_pile) == 0:
            refill_draw_pile()

        # wenn die FLIP Karte gelegt wurde, das Spiel statt mit der light-gameloop mit der dark-gameloop fortsetzen
        if played_card is not None:
            if played_card.light_side[1] == played_card.light_side[1].FLIP:
                # Ablage- und Ziehstapel umdrehen
                discard_pile.reverse()
                draw_pile.reverse()
                # Spiel in der anderen gameloop fortsetzen
                action_text = ""
                uno_text = ""
                wished_color_text = ""
                gameloop_dark_side()
                if check_for_game_over():  # nochmal abfragen, damit Spiel auch zuende geht
                    break

        action_text = ""
        uno_text = ""
        wished_color_text = ""


def gameloop_dark_side():
    # Hilfsvariablen:
    global wished_dark_color  # Farbe, die beim Spielen eines Jokers gewünscht wird
    global upper_card
    global played_card
    global light
    global action_text
    global uno_text
    global wished_color_text
    played_card = None  # played_card beim ersten Mal in der dark_gameloop zurücksetzen, da sie direkt nach dem umdrehen nicht relevant ist
    light = False  # dunkle Seite wird gespielt

    while True:
        upper_card = discard_pile[len(discard_pile) - 1]
        action_text = "Spieler " + str(player + 1) + " ist dran"
        repaint_dark()
        refresh_screen()
        if wished_dark_color.name != "BLACK" and upper_card.dark_side[0] == upper_card.dark_side[
            0].WHITE:  # Wenn Joker oben liegt...
            wished_color_text = str(wished_dark_color.name)
            refresh_screen()

        # Spieler verarbeitet zuletzt gelegte Karte (+1, +5, +2W, CW inkl. aussetzen)
        if played_card is not None:
            if played_card.dark_side[1] == played_card.dark_side[1].DRAW_5:
                draw_cards(5)
                change_player()
                played_card = None
                continue
            elif played_card.dark_side[1] == played_card.dark_side[1].WILD_DRAW_COLOR:
                draw_color()
                change_player()
                played_card = None
                continue

        played_card = None  # played_card zurücksetzen

        # Wenn Spieler computergesteuert, keine Eingaben machen
        if player_is_com():
            process_com_turn()
        else:  # sonst (Nutzereingaben abfragen)
            # Spieler wählt eine Karte von seiner Hand
            card_to_play = choose_card()

            # Wenn Karte korrekt, dann spielen, sonst andere Karte wählen...
            while True:
                # Karte ziehen?
                if card_to_play == -1:
                    draw_cards(1)
                    refresh_screen()
                    # gerade gezogene Karte spielen?
                    if dark_card_is_valid(players[player][len(players[player]) - 1]):
                        refresh_screen()
                        action_text = "Gezogene Karte spielen? (w)"
                        refresh_screen()
                        play_drawn_card = choose_card()
                        if play_drawn_card != -1:
                            played_card = play_card(len(players[player]) - 1)
                    else:
                        time.sleep(1)
                    refresh_screen()
                    break
                # Karte im Gültigkeitsbereich?
                elif card_to_play < 0 or card_to_play >= len(players[player]):
                    refresh_screen()
                    card_to_play = choose_card()
                # wenn hier angelangt, ist die Eingabe eine gültige Handkarte
                # prüfe ob Karte spielbar
                elif dark_card_is_valid(players[player][card_to_play]):
                    played_card = play_card(card_to_play)
                    break
                else:
                    refresh_screen()
                    action_text = "Karte nicht spielbar"
                    refresh_screen()
                    card_to_play = choose_card()

        check_for_uno()

        if check_for_game_over():  # wenn Spiel vorbei, aus der while Schleife ausbrechen
            time.sleep(3)
            break

        # Wenn JOKER gespielt wurde, dann Farbe wünschen
        if played_card is not None:
            if not player_is_com():
                if played_card.dark_side[0] == played_card.dark_side[0].WHITE:
                    refresh_screen()
                    wished_color_text = "Farbe wünschen (1=rosa, 2=türkis, 3=orange, 4=lila)"
                    refresh_screen()
                    choose_color()  # händelt über Tasteneingabe (1-4) die zu wünschende Farbe und setzt sie fest

            # ggf. gespielte Aktionskarte (reverse, skip, flip, skip all) verarbeiten
            # REVERSE
            if played_card.dark_side[1] == played_card.dark_side[1].REVERSE:
                reverse_game()
            # SKIP alle Spieler
            elif played_card.dark_side[1] == played_card.dark_side[1].SKIP_EVERYONE:
                for player_to_skip in range(1,
                                            len(players)):  # so viele Spieler weiterschalten, wie teilnehmen (-> ursprünglicher Spieler ist wieder dran)
                    change_player()

        # nächster Spieler (je nach Spielrichtung)
        change_player()

        # Wenn notwendig, Nachziehstapel auffüllen
        if len(draw_pile) == 0:
            refill_draw_pile()

        # wenn die FLIP Karte gelegt wurde, das Spiel statt mit der dark-gameloop mit der light-gameloop fortsetzen
        if played_card is not None:
            if played_card.dark_side[1] == played_card.dark_side[1].FLIP:
                # Ablage- und Ziehstapel umdrehen
                discard_pile.reverse()
                draw_pile.reverse()
                # Spiel in der anderen gameloop fortsetzen
                action_text = ""
                uno_text = ""
                wished_color_text = ""
                gameloop_light_side()
                if check_for_game_over():  # nochmal abfragen, damit Spiel auch zuende geht
                    break

        action_text = ""
        uno_text = ""
        wished_color_text = ""


if __name__ == "__main__":
    # Spielparameter anpassen
    set_speed(60)
    set_card_size(120, 180)
    set_players(4)
    com_players = [False, True, True, True]
    num_starting_cards_per_player = 7
    # Karten initialisieren
    from UNO_Cards import light_cards, dark_cards

    # Karten aus zufälligen Kombinationen aus light side und dark side zusammensetzen; Fertige Karten auf den Nachziehstapel legen
    while len(light_cards) > 0 and len(dark_cards) > 0:
        light_side_random_index = random.randint(0, len(light_cards) - 1)
        dark_side_random_index = random.randint(0, len(dark_cards) - 1)
        light_side = light_cards[light_side_random_index]
        dark_side = dark_cards[dark_side_random_index]
        draw_pile.append(Card(light_side, dark_side))
        # genommene Karten aus den UNO_Cards Listen entfernen
        del light_cards[light_side_random_index]
        del dark_cards[dark_side_random_index]

    # Karten austeilen
    deal_cards(num_starting_cards_per_player)

    # Erste Karte Aufdecken (muss Zahl sein)

    first_card = reveal_card()
    while not card_light_is_number(first_card):
        first_card = reveal_card()

    gameloop_light_side()
