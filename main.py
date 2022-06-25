import pygame
from ast import literal_eval

from GameField import GameField
from Agent import Agent

WIDTH = 1000
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def render_all(background_image, gfield, age=0, action=0, invalid_action_count=0):
    hp = gfield.get_player().get_hp()
    action_decoder = {0: 'x', 1: 'u', 2: 'd', 3: 'l', 4: 'r'}
    screen.blit(background_image, (0, 0))
    for sub in gfield.get_field():
        for cell in sub:
            cell.draw(screen)
    gfield.get_player().draw(screen)
    pygame.draw.rect(screen, BLACK, pygame.Rect(801, 0, 199, 800))
    text_surface = my_font.render(f'HP  {hp}', False, WHITE)
    screen.blit(text_surface, (802, 70))
    text_surface = my_font.render(f'Age {age}', False, WHITE)
    screen.blit(text_surface, (802, 120))
    text_surface = my_font.render(f'Action {action_decoder[action]}', False, WHITE)
    screen.blit(text_surface, (802, 170))
    text_surface = my_font.render(f'# of invalid', False, RED)
    screen.blit(text_surface, (802, 220))
    text_surface = my_font.render(f'actions {invalid_action_count}', False, RED)
    screen.blit(text_surface, (802, 270))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Pygame initialisation
    pygame.init()
    pygame.font.init()

    # Initialisation of the graphics/game components
    my_font = pygame.font.SysFont('Old English Text MT', 40)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulation")
    clock = pygame.time.Clock()
    background_image = pygame.image.load('image/background.jpg')
    fps = 2

    # Initialisation of the simulation logic objects
    with open('policy_soft_300_elite25.txt', 'r') as file:
        fdict = file.read()
    POLICY = literal_eval(fdict)
    gfield = GameField()
    agent = Agent(POLICY, gfield.get_player_locality())
    is_alive = True

    # Game loop
    running = True
    pause = False
    iterations = 0
    invalid_action_count = 0
    render_all(background_image=background_image, gfield=gfield)
    while running:
        if not pause:
            # Simulation logic part
            action, _ = agent.make_action(gfield.get_player_locality())
            gfield.set_action(action)
            action_result, is_alive = gfield.tick()

            if not is_alive:
                pause = True
            if action_result == 1:
                invalid_action_count += 1
            iterations += 1

            render_all(background_image, gfield, agent.age(iterations), action, invalid_action_count)
            pygame.display.update()

        clock.tick(fps)
        # Event handle
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            # In-game interactions
            elif event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                # Exit
                if pressed_keys[pygame.K_x]:
                    running = False
                # Pause
                elif pressed_keys[pygame.K_p]:
                    pause = True
                # Resume
                elif pressed_keys[pygame.K_s]:
                    if is_alive:
                        pause = False
                # Start new
                elif pressed_keys[pygame.K_n]:
                    gfield = GameField()
                    agent = Agent(POLICY, gfield.get_player_locality(), born_iteration=iterations)
                    is_alive = True
                    pause = False
                # Decrease speed
                elif pressed_keys[pygame.K_KP_MINUS]:
                    if fps > 0.25:
                        fps /= 2
                # Increase speed
                elif pressed_keys[pygame.K_KP_PLUS]:
                    if fps < 16:
                        fps *= 2

    pygame.quit()
