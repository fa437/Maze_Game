#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 3 10:16:20 2025

@author: fa19984

Program: Maze Game

This a Maze game created for end of semester project for Informatics II,
I Will be using graphics.py to handle the GUI and python to achieve this.
"""

from graphics import *
import time

# Configuration
GRID_SIZE = 10
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Maze layout (1 = wall, 0 = path)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

START = (1, 1)
GOAL = (8, 8)

def draw_maze(win):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            rect.setFill("black" if MAZE[row][col] == 1 else "white")
            rect.draw(win)

def create_player(x, y):
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    player = Circle(Point(cx, cy), CELL_SIZE // 3)
    player.setFill("red")
    player.draw(win)
    return player

def move_player(player, dx, dy, pos):
    new_x = pos[0] + dx
    new_y = pos[1] + dy
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        if MAZE[new_y][new_x] == 0:
            player.move(dx * CELL_SIZE, dy * CELL_SIZE)
            return new_x, new_y
    return pos

def main():
    global win
    win = GraphWin("Maze Game", WINDOW_SIZE, WINDOW_SIZE)
    draw_maze(win)

    pos = START
    player = create_player(*pos)

    # Timer setup
    start_time = time.time()
    timer_text = Text(Point(60, 20), "Time: 0.0s")
    timer_text.setSize(12)
    timer_text.draw(win)

    while True:
        # Update timer
        elapsed = time.time() - start_time
        timer_text.setText(f"Time: {elapsed:.1f}s")

        # Get key (non-blocking)
        key = win.checkKey().lower()
        if key == "q":
            break

        dx = dy = 0
        if key == "w": dy = -1
        elif key == "s": dy = 1
        elif key == "a": dx = -1
        elif key == "d": dx = 1

        if key in "wasd":
            pos = move_player(player, dx, dy, pos)
            if pos == GOAL:
                win_msg = Text(Point(WINDOW_SIZE // 2, WINDOW_SIZE // 2), f"You Win! Time: {elapsed:.1f}s")
                win_msg.setSize(16)
                win_msg.setStyle("bold")
                win_msg.setFill("green")
                win_msg.draw(win)
                win.getMouse()
                break

    win.close()

if __name__ == "__main__":
    main()
