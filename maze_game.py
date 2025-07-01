#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 3 10:16:20 2025

@author: fa19984

Program: Maze Game

This a Maze game created for end of semester project for Informatics II,
I will be using graphics.py to handle the GUI and python to achieve this.
"""

from graphics import *
import time

CELL_SIZE = 60
GRID_SIZE = 10
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Maze definitions
MAPS = {
    "1": {
        "name": "Easy",
        "maze": [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,1],
            [1,1,1,0,1,0,1,1,0,1],
            [1,0,0,0,1,0,0,1,0,1],
            [1,0,1,1,1,1,0,1,0,1],
            [1,0,1,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1]
        ],
        "start": (1, 1),
        "goal": (8, 8)
    },
    "2": {
        "name": "Medium",
        "maze": [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,0,0,1,0,0,1],
            [1,0,1,0,1,0,1,0,1,1],
            [1,0,0,0,1,0,0,0,0,1],
            [1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,1,0,1],
            [1,0,1,1,1,1,0,1,0,1],
            [1,0,1,0,0,0,0,1,0,1],
            [1,0,0,0,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1]
        ],
        "start": (1, 1),
        "goal": (8, 8)
    },
    "3": {
        "name": "Hard",
        "maze": [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,0,1],
            [1,0,1,0,1,0,1,0,0,1],
            [1,0,1,0,1,0,1,0,1,1],
            [1,0,1,0,0,0,1,0,0,1],
            [1,0,1,0,1,0,1,1,0,1],
            [1,0,0,0,1,0,0,1,0,1],
            [1,1,1,0,1,1,0,1,0,1],
            [1,1,1,1,1,1,1,1,1,1]
        ],
        "start": (1, 1),
        "goal": (8, 8)
    }
}

def draw_maze(win, maze, goal):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            if (col, row) == goal:
                rect.setFill("lightgreen")
            else:
                rect.setFill("black" if maze[row][col] == 1 else "white")
            rect.draw(win)

def create_player(win, x, y):
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    player = Circle(Point(cx, cy), CELL_SIZE // 3)
    player.setFill("red")
    player.draw(win)
    return player

def move_player(player, dx, dy, pos, maze):
    new_x = pos[0] + dx
    new_y = pos[1] + dy
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE: #this is to make sure the new pos is inside the maze boundaries
        if maze[new_y][new_x] == 0:
            player.move(dx * CELL_SIZE, dy * CELL_SIZE)
            return new_x, new_y
    return pos

def show_menu(unlocked_levels):
    menu_win = GraphWin("Maze Game - Menu", 400, 300)
    menu_win.setBackground("lightblue")
    title = Text(Point(200, 40), "Select Level")
    title.setSize(20)
    title.setStyle("bold")
    title.draw(menu_win)

    options = [("1", "Easy"), ("2", "Medium"), ("3", "Hard"), ("q", "Quit Game")]
    y = 100
    for key, label in options:
        if key == "q":
            t = Text(Point(200, y), "Press Q to Quit Game")
            t.setTextColor("black")
        else:
            txt = f"{label}" + (" (locked)" if key not in unlocked_levels else "")
            t = Text(Point(200, y), f"Press {key.upper()} for {txt}")
            t.setTextColor("gray" if key not in unlocked_levels else "black")
        t.setSize(14)
        t.draw(menu_win)
        y += 40

    while True:
        key = menu_win.getKey().lower()
        if key == "q":
            menu_win.close()
            return key
        elif key in MAPS and key in unlocked_levels:
            menu_win.close()
            return key

def wait_for_enter(win):
    msg = Text(Point(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 40), "Press ENTER to continue")
    msg.setSize(12)
    msg.setFill("gray")
    msg.draw(win)
    while win.getKey().lower() != "return":
        pass

def play_level(level_data):
    maze = level_data["maze"]
    start = level_data["start"]
    goal = level_data["goal"]

    win = GraphWin(f"Maze - {level_data['name']}", WINDOW_SIZE, WINDOW_SIZE)
    draw_maze(win, maze, goal)

    pos = start
    player = create_player(win, *pos)

    timer_text = Text(Point(60, 20), "Time: 0.0s")
    timer_text.setSize(12)
    timer_text.setTextColor("white")
    timer_text.draw(win)

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        timer_text.setText(f"Time: {elapsed:.1f}s")

        key = win.checkKey().lower()

        if key in ["q", "escape"]:
            overlay = Rectangle(Point(100, 200), Point(500, 300))
            overlay.setFill("white")
            overlay.setOutline("black")
            overlay.draw(win)

            msg = Text(Point(300, 230), "Are you sure you want to quit?")
            msg.setSize(14)
            msg.setStyle("bold")
            msg.draw(win)

            yes_text = Text(Point(240, 270), "Y = Yes")
            yes_text.setFill("red")
            yes_text.setSize(12)
            yes_text.draw(win)

            no_text = Text(Point(360, 270), "N = No")
            no_text.setFill("green")
            no_text.setSize(12)
            no_text.draw(win)

            # Wait for response
            while True:
                confirm_key = win.getKey().lower()
                if confirm_key == "y":
                    win.close()
                    return False
                elif confirm_key == "n":
                    # Undraw prompt
                    overlay.undraw()
                    msg.undraw()
                    yes_text.undraw()
                    no_text.undraw()
                    break
            continue  # go back to top of loop

        dx = dy = 0
        if key == "w": dy = -1
        elif key == "s": dy = 1
        elif key == "a": dx = -1
        elif key == "d": dx = 1

        if key in "wasd":
            pos = move_player(player, dx, dy, pos, maze)
            if pos == goal:
                win_msg = Text(Point(WINDOW_SIZE // 2, WINDOW_SIZE // 2), f"You Win! Time: {elapsed:.1f}s")
                win_msg.setSize(16)
                win_msg.setStyle("bold")
                win_msg.setFill("green")
                win_msg.draw(win)
                wait_for_enter(win)
                win.close()
                return True

    win.close()
    return False

def main():
    unlocked_levels = {"1"}  # Only Easy is unlocked at start
    while True:
        selected = show_menu(unlocked_levels)
        if selected == "q":
            break
        won = play_level(MAPS[selected])
        if won and selected == "1":
            unlocked_levels.add("2")
        elif won and selected == "2":
            unlocked_levels.add("3")

if __name__ == "__main__":
    main()
