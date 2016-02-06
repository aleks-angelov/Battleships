#! /usr/bin/python

import random
import subprocess

col_labels = "  0 1 2 3 4 5 6 7 8 9 "
random.seed(None)

enemy_field = [[False for efcol in xrange(10)] for efrow in xrange(10)]
enemy_board = [["-" for ebcol in xrange(10)] for ebrow in xrange(10)]
enemy_choices = [(ex, ey) for ex in xrange(10) for ey in xrange(10)]

player_field = [[False for pfcol in xrange(10)] for pfrow in xrange(10)]
player_board = [["-" for pbcol in xrange(10)] for pbrow in xrange(10)]

enemy_remaining = 15
player_remaining = 15


def introduction():
    subprocess.call("clear")

    print "\n\tWelcome to Battleships! In this turn-based classic game, you will\n" \
          "\tplace several ships on a large board and take turns trying to pin-\n" \
          "\tpoint the location of the computer's ships. The objective of the\n" \
          "\tgame is to be the first to mark all the ships of the other player.\n"

    print "\n\tPlace your ships:"
    method = raw_input("\n\t(c)ustom or (r)andom placement: ")
    while method != 'c' and method != 'r':
        print "\n\tInvalid input. Please try again:"
        method = raw_input("\n\t(c)ustom or (r)andom placement: ")

    if method == 'c':
        player_custom()
    elif method == 'r':
        player_random()

    show_player()
    raw_input("\tPress Enter to continue. ")


def show_player():
    subprocess.call("clear")

    print "\t   Your placement:\n"
    print "\t", col_labels
    for row in xrange(10):
        print "\t", row,
        for col in xrange(10):
            print player_board[row][col],
        print

    print "\n\tEmpty: -      Ship: +\n"


def show_boards():
    subprocess.call("clear")

    print "\t     Enemy board:\t\t     Your board:\n"
    print "\t", col_labels, "\t\t", col_labels
    for row in xrange(10):
        print "\t", row,
        for col in xrange(10):
            print enemy_board[row][col],

        print "\t\t", row,
        for col in xrange(10):
            print player_board[row][col],
        print

    print "\n\tHit: x\t      Miss: o\t\tEmpty: -      Ship: +\n"


def player_custom():
    s = 5
    invalid_direction = False
    invalid_position = False
    occupied = False

    while s > 0:
        show_player()

        if invalid_direction:
            print "\tInvalid direction. Please try again:\n"
        if invalid_position:
            print "\tInvalid position. Please try again:\n"
        if occupied:
            print "\tSpace is occupied. Please try again:\n"

        print "\tShip size: %d\n" % s
        invalid_direction = False
        invalid_position = False
        occupied = False

        direction = raw_input("\t(h)orizontal or (v)ertical: ")
        if direction == 'h':
            coord = raw_input("\n\tRow (0-9) and column (0-%d) of left end: " % (10 - s)).split()
            try:
                x = int(coord[0])
                y = int(coord[1])
            except ValueError:
                invalid_position = True
                continue

            if x < 0 or x > 9 or y < 0 or y > (10 - s):
                invalid_position = True
                continue

            for j in range(y, y + s):
                if player_field[x][j]:
                    occupied = True
                    break

            if not occupied:
                for j in range(y, y + s):
                    player_field[x][j] = True
                    player_board[x][j] = '+'
                s -= 1

        elif direction == 'v':
            coord = raw_input("\n\tRow (0-%d) and column (0-9) of top end: " % (10 - s)).split()
            try:
                x = int(coord[0])
                y = int(coord[1])
            except ValueError:
                invalid_position = True
                continue

            if x < 0 or x > (10 - s) or y < 0 or y > 9:
                invalid_position = True
                continue

            for i in range(x, x + s):
                if player_field[i][y]:
                    occupied = True
                    break

            if not occupied:
                for i in range(x, x + s):
                    player_field[i][y] = True
                    player_board[i][y] = '+'
                s -= 1

        else:
            invalid_direction = True
            continue


def player_random():
    for s in xrange(5, 0, -1):
        direction = random.randint(0, 1)
        if direction == 0:
            x = -1
            y = -1
            empty = False

            while not empty:
                x = random.randint(0, 9)
                y = random.randint(0, 10 - s)
                occupied = False

                for j in range(y, y + s):
                    if player_field[x][j]:
                        occupied = True
                        break

                if not occupied:
                    empty = True

            for j in range(y, y + s):
                player_field[x][j] = True
                player_board[x][j] = '+'

        elif direction == 1:
            x = -1
            y = -1
            empty = False

            while not empty:
                x = random.randint(0, 10 - s)
                y = random.randint(0, 9)
                occupied = False

                for i in range(x, x + s):
                    if player_field[i][y]:
                        occupied = True
                        break

                if not occupied:
                    empty = True

            for i in range(x, x + s):
                player_field[i][y] = True
                player_board[i][y] = '+'


def enemy_positioning():
    for s in xrange(5, 0, -1):
        direction = random.randint(0, 1)
        if direction == 0:
            x = -1
            y = -1
            empty = False

            while not empty:
                x = random.randint(0, 9)
                y = random.randint(0, 10 - s)
                occupied = False

                for j in range(y, y + s):
                    if enemy_field[x][j]:
                        occupied = True
                        break

                if not occupied:
                    empty = True

            for j in range(y, y + s):
                enemy_field[x][j] = True

        elif direction == 1:
            x = -1
            y = -1
            empty = False

            while not empty:
                x = random.randint(0, 10 - s)
                y = random.randint(0, 9)
                occupied = False

                for i in range(x, x + s):
                    if enemy_field[i][y]:
                        occupied = True
                        break

                if not occupied:
                    empty = True

            for i in range(x, x + s):
                enemy_field[i][y] = True


def player_turn(valid):
    show_boards()
    print "\tYOUR TURN:",

    if not valid:
        print "Invalid position. Please try again:",

    coord = raw_input("\n\n\tRow (0-9) and column (0-9) to attack: ").split()
    try:
        x = int(coord[0])
        y = int(coord[1])
    except (IndexError, ValueError):
        player_turn(False)
        return

    if x < 0 or x > 9 or y < 0 or y > 9:
        player_turn(False)
        return

    if not enemy_field[x][y]:
        if enemy_board[x][y] == '-':
            enemy_board[x][y] = 'o'
            print "\n\tAttack result: miss\n"

        else:
            print "\n\tAttack result: miss (repeated)\n"

    else:
        if enemy_board[x][y] == '-':
            enemy_board[x][y] = 'x'
            global enemy_remaining
            enemy_remaining -= 1
            print "\n\tAttack result: hit!\n"

        else:
            print "\n\tAttack result: hit! (repeated)\n"

    raw_input("\tPress Enter to continue. ")


def enemy_turn():
    show_boards()
    print "\tENEMY TURN:\n"

    pos = enemy_choices.pop(random.randint(0, len(enemy_choices) - 1))
    x = pos[0]
    y = pos[1]
    print "\tEnemy has attacked: %d %d\n" % (x, y)

    if not player_field[x][y]:
        player_board[x][y] = 'o'
        print "\tAttack result: miss\n"

    else:
        player_board[x][y] = 'x'
        global player_remaining
        player_remaining -= 1
        print "\tAttack result: hit!\n"

    raw_input("\tPress Enter to continue. ")


def game_over(winner):
    subprocess.call("clear")

    if winner:
        print "\n\tCongratulations, you won!\n"

    else:
        print "\n\tUnfortunately, you lost.\n"


def main_cycle():
    introduction()
    enemy_positioning()

    while enemy_remaining > 0 and player_remaining > 0:
        player_turn(True)
        enemy_turn()

    if enemy_remaining == 0:
        game_over(True)
    else:
        game_over(False)

    exit(0)


main_cycle()
