import pygame
import rocket

pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False


clock = pygame.time.Clock()
rocket = rocket.Rocket(400, 300)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: rocket.increase_speed()
    if pressed[pygame.K_LEFT]: rocket.turn_left()
    if pressed[pygame.K_RIGHT]: rocket.turn_right()

    screen.fill((0, 0, 0))
    rocket.get_next_frame_coordinates()

    screen.blit(rocket.rotated_image, rocket.rotated_rect)
    #pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    pygame.display.flip()
    clock.tick(60)