import os
import sys
import random
from time import sleep
import argparse

import pygame

from src.game.grid.grid import Grid
from src.game.player.player import Player
from src.game.path_algorithm.a_star import AStar
from src.game.path_algorithm.dijkstra import Dijkstra
from src.game.path_algorithm.DFS import DFS

from src.game.game_scene import GameScene
from src.game.menu import Menu

from src.game.huffman.main import decompress_map

from src.config import MAP_ASSETS_DIR
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT

def handle_mouse_click():
    global goal, grid
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        goal = grid.pixel_to_cell(pos)
        grid.path = []
        grid.explored = []
        grid.goal = goal
        solver.goal = goal
        print(f"Goal: {goal}")

def main():
    parser = argparse.ArgumentParser(description="Grid game")
    parser.add_argument("map_file", help="Path to the map file")
    args = parser.parse_args()

    # Decompress maps
    decompress_map(args.map_file + '.png')

    # Initialize Pygame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


    try:
        while True:
            menu = Menu(window)

            game_scene = GameScene(window)

            running, game_running = menu.run()

            if not running and not game_running:
                    return

            game_scene.run(map_file=args.map_file + '.png')
    finally:
        # delete map file
        print('Deleting map file...')
        os.remove(os.path.join(MAP_ASSETS_DIR, f'{args.map_file}') + '.png')

if __name__ == "__main__":
    main()