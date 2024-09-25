import pygame
from game import initialize_game, create_grid, draw_grid, validate_swap, check_for_matches, remove_and_refill, update_score, check_win, are_adjacent, refill_grid_until_no_matches
from config import *


def get_tile_pos(mouse_pos):
    """
    Converts mouse click position into grid coordinates.
    :param mouse_pos: Tuple of mouse x and y coordinates.
    :return: Tuple of grid coordinates (x, y).
    """
    x, y = mouse_pos
    return x // TILE_SIZE, y // TILE_SIZE


def main():
    # Initialize game and load assets
    tile_images, match_sound, win_sound = initialize_game()
    pygame.mixer.music.play(-1)  # Loop background music

    # Create the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("消消乐游戏")

    # Create grid and initialize variables
    grid = create_grid()
    running = True
    selected_tile = None
    score = 0
    moves = MAX_MOVES  # Track remaining moves

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                tile_pos = get_tile_pos(mouse_pos)

                if not selected_tile:
                    selected_tile = tile_pos
                else:
                    # Check if the selected tiles are adjacent
                    if are_adjacent(selected_tile, tile_pos):
                        # Validate the swap to ensure a match is made
                        if validate_swap(grid, selected_tile, tile_pos):
                            # Check for any matches after the swap
                            matched, special_tiles = check_for_matches(grid)
                            if matched:
                                pygame.mixer.Sound.play(match_sound)
                                score = update_score(matched, score)
                                remove_and_refill(grid, matched, special_tiles)
                                # Continuously refill and remove matches until no further matches
                                refill_grid_until_no_matches(grid)
                                moves -= 1  # Reduce move count after a valid move
                                won, status = check_win(score, moves)
                                if won:
                                    running = False
                                    if status == "win":
                                        pygame.mixer.Sound.play(win_sound)
                                    # Show winning or losing screen here
                    selected_tile = None  # Reset selection after swap attempt

        # Redraw the screen and grid
        screen.fill((255, 255, 255))  # Background color
        draw_grid(screen, grid, tile_images)  # Ensure the screen is passed correctly
        pygame.display.update()


if __name__ == "__main__":
    main()