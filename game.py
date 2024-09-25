import pygame
import random
from config import *


def initialize_game():
    """
    Initializes Pygame and loads game assets like images and sounds.
    Returns the loaded tile images and sounds.
    """
    pygame.init()

    # Load sounds
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    match_sound = pygame.mixer.Sound(MATCH_SOUND)
    win_sound = pygame.mixer.Sound(WIN_SOUND)

    # Load tile images and scale them to the TILE_SIZE
    tile_images = {
        "red": pygame.transform.scale(pygame.image.load(IMAGE_PATH + "red_tile.png"), (TILE_SIZE, TILE_SIZE)),
        "green": pygame.transform.scale(pygame.image.load(IMAGE_PATH + "green_tile.png"), (TILE_SIZE, TILE_SIZE)),
        "blue": pygame.transform.scale(pygame.image.load(IMAGE_PATH + "blue_tile.png"), (TILE_SIZE, TILE_SIZE)),
        "yellow": pygame.transform.scale(pygame.image.load(IMAGE_PATH + "yellow_tile.png"), (TILE_SIZE, TILE_SIZE)),
        "purple": pygame.transform.scale(pygame.image.load(IMAGE_PATH + "purple_tile.png"), (TILE_SIZE, TILE_SIZE)),
        "bomb": pygame.transform.scale(pygame.image.load(IMAGE_PATH + "bomb.png"), (TILE_SIZE, TILE_SIZE)),
    }

    return tile_images, match_sound, win_sound


def create_grid():
    """
    Creates a randomized grid for the game.
    Ensures that the grid has random tile types from the TILES list and no initial matches.
    Grid size is dynamically set based on SCREEN_WIDTH and TILE_SIZE.
    Returns the grid.
    """
    grid_size = SCREEN_WIDTH // TILE_SIZE
    grid = []
    while True:
        grid = [[random.choice(TILES) for _ in range(grid_size)] for _ in range(grid_size)]
        if not has_initial_matches(grid):
            break
    return grid


def has_initial_matches(grid):
    """
    Checks if the generated grid contains any initial matches (3 or more tiles of the same type in a row or column).
    :param grid: The generated grid.
    :return: True if there are matches, False otherwise.
    """
    matched, _ = check_for_matches(grid)
    return bool(matched)


def draw_grid(screen, grid, tile_images):
    """
    Draws the game grid on the screen.
    :param screen: Pygame screen surface.
    :param grid: The game grid with tile types.
    :param tile_images: Dictionary of tile images.
    """
    grid_size = SCREEN_WIDTH // TILE_SIZE
    for row in range(grid_size):
        for col in range(grid_size):
            tile_type = grid[row][col]
            if tile_type in tile_images:
                screen.blit(tile_images[tile_type], (col * TILE_SIZE, row * TILE_SIZE))


def swap_tiles(grid, pos1, pos2):
    """
    Swaps the positions of two tiles in the grid.
    :param grid: The game grid.
    :param pos1: Position 1 (tuple of x, y).
    :param pos2: Position 2 (tuple of x, y).
    """
    grid[pos1[1]][pos1[0]], grid[pos2[1]][pos2[0]] = grid[pos2[1]][pos2[0]], grid[pos1[1]][pos1[0]]


def are_adjacent(pos1, pos2):
    """
    Checks if two positions are adjacent in the grid.
    :param pos1: Position 1 (tuple of x, y).
    :param pos2: Position 2 (tuple of x, y).
    :return: True if positions are adjacent, else False.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1


def check_for_matches(grid):
    """
    Checks the grid for any horizontal or vertical matches of three or more tiles.
    Returns a set of matched tile positions and information about special tiles.
    """
    matched = set()
    special_tiles = []  # Store the position and type of special tiles

    grid_size = SCREEN_WIDTH // TILE_SIZE

    # Horizontal check
    for row in range(grid_size):
        for col in range(grid_size - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matched.update([(row, col), (row, col + 1), (row, col + 2)])
                # Check if we matched 4 or more
                if col + 3 < grid_size and grid[row][col] == grid[row][col + 3]:
                    matched.add((row, col + 3))
                    special_tiles.append(((row, col + 1), "horizontal_bomb"))  # Create special tile

    # Vertical check
    for col in range(grid_size):
        for row in range(grid_size - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matched.update([(row, col), (row + 1, col), (row + 2, col)])
                # Check if we matched 4 or more
                if row + 3 < grid_size and grid[row][col] == grid[row + 3][col]:
                    matched.add((row + 3, col))
                    special_tiles.append(((row + 1, col), "vertical_bomb"))

    return matched, special_tiles


def validate_swap(grid, pos1, pos2):
    """
    Temporarily swaps the tiles, checks for a match, and reverts the swap if no match is found.
    :param grid: The game grid.
    :param pos1: First tile position.
    :param pos2: Second tile position.
    :return: True if a valid match was made, False otherwise.
    """
    # Perform a temporary swap
    swap_tiles(grid, pos1, pos2)

    # Check for matches after the swap
    matched, _ = check_for_matches(grid)

    if matched:
        return True  # Keep the swap if there's a match
    else:
        # Revert the swap if no match is found
        swap_tiles(grid, pos1, pos2)
        return False


def remove_and_refill(grid, matched, special_tiles):
    """
    Removes matched tiles and refills the grid with new random tiles.
    Ensures that tiles above the cleared spaces fall down to fill the gaps and new tiles are generated at the top.
    :param grid: The game grid.
    :param matched: Set of matched tile positions.
    :param special_tiles: List of special tiles to create.
    """
    grid_size = SCREEN_WIDTH // TILE_SIZE

    # First, clear the matched tiles
    for row, col in matched:
        grid[row][col] = None  # Clear matched tiles

    # Apply gravity: for each column, make tiles fall down
    for col in range(grid_size):
        empty_rows = [row for row in range(grid_size) if grid[row][col] is None]
        
        # For each empty row, move down all tiles above it
        for empty_row in reversed(empty_rows):
            for row_above in range(empty_row, 0, -1):
                grid[row_above][col] = grid[row_above - 1][col]
            grid[0][col] = random.choice(TILES)  # Refill the topmost empty position with a new tile

    # Add special tiles (if any)
    for (row, col), tile_type in special_tiles:
        grid[row][col] = tile_type  # Replace with special tile


def refill_grid_until_no_matches(grid):
    """
    Continuously refills the grid and removes matches until no more matches exist.
    :param grid: The game grid.
    """
    while True:
        matched, special_tiles = check_for_matches(grid)
        if not matched:
            break
        remove_and_refill(grid, matched, special_tiles)


def update_score(matched, score):
    """
    Updates the score based on matched tiles.
    :param matched: Set of matched tile positions.
    :param score: Current score.
    :return: Updated score.
    """
    return score + len(matched) * MATCH_SCORE


def check_win(score, moves):
    """
    Checks if the player's score has reached the target score or if they have run out of moves.
    Plays win sound if the player wins.
    :param score: Player's current score.
    :param moves: Number of remaining moves.
    :return: True if the player has won or lost, False otherwise.
    """
    if score >= TARGET_SCORE:
        return True, "win"
    elif moves <= 0:
        return True, "lose"
    return False, None