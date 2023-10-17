import pygame
import rocket
import bullet

pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False


clock = pygame.time.Clock()
rocket = rocket.Rocket(400, 300)
active_bullets = []
fire_right_now = False

def fire(active_bullets, rocket):
    if len(active_bullets) < 5:
        active_bullets.append(bullet.Bullet(rocket.rotated_rect.centerx,
                                                 rocket.rotated_rect.centery, rocket.rotation_angle))



def update_bullets(active_bullets):
    far_bullets = []
    for i in range(len(active_bullets)):
        if active_bullets[i].is_far_enough():
            far_bullets.append(i)
        else:
            active_bullets[i].update(screen)
    for i in far_bullets:
        del active_bullets[i]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: rocket.increase_speed()
    if pressed[pygame.K_LEFT]: rocket.turn_left()
    if pressed[pygame.K_RIGHT]: rocket.turn_right()
    if pressed[pygame.K_SPACE]: fire(active_bullets, rocket)

    screen.fill((0, 0, 0))
    rocket.get_next_frame_coordinates()
    update_bullets(active_bullets)

    screen.blit(rocket.rotated_image, rocket.rotated_rect)
    #pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    pygame.display.flip()
    clock.tick(60)

