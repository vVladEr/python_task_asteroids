import pygame
import gameObjectsLogic

pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False
a = screen.get_rect().width


clock = pygame.time.Clock()
objects = gameObjectsLogic.GameObjectsLogic(screen)
rocket = objects.rocket

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: rocket.increase_speed()
    if pressed[pygame.K_LEFT]: rocket.turn_left()
    if pressed[pygame.K_RIGHT]: rocket.turn_right()
    if pressed[pygame.K_SPACE]: objects.fire()

    screen.fill((0, 0, 0))
    rocket.get_next_frame_coordinates()
    objects.update_bullets()
    objects.update_asteroids()
    objects.bullet_hit_asteroid()
    done = objects.rocket_hit_asteroid()



    pygame.display.flip()
    clock.tick(60)

