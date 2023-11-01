import pygame
import gameObjectsLogic

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False


pygame.font.init()
f = pygame.font.SysFont('arial', 48)


clock = pygame.time.Clock()
objects = gameObjectsLogic.GameObjectsLogic(screen)
rocket = objects.rocket

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        rocket.increase_speed()
    if pressed[pygame.K_LEFT]:
        rocket.turn_left()
    if pressed[pygame.K_RIGHT]:
        rocket.turn_right()
    if pressed[pygame.K_SPACE]:
        objects.fire()

    screen.fill((0, 0, 0))
    rocket.get_next_frame_coordinates()
    score_text = f.render(f"{rocket.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    objects.update()
    if not done:
        done = objects.rocket_destroyed
    pygame.display.flip()
    clock.tick(60)

