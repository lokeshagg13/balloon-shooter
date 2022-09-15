import pygame

pygame.init()

#######################################

# Colors

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (55, 55, 55)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Fonts

label_font = pygame.font.Font('Plaguard-ZVnjx.otf', 80)
medium_font = pygame.font.Font('Plaguard-ZVnjx.otf', 40)

########################

# Game elements orientation and coordinates

game_panel_coords = (350, 100)
game_panel_dims = (600, 500)
game_panel_top_y = game_panel_coords[1]
game_panel_bottom_y = game_panel_coords[1] + game_panel_dims[1]
game_title_coords = (500, 30)

#########################

# Game parameters

game_title = 'Shoot It'
balloon_speed = 5
gun_speed = 5
bullet_speed = balloon_speed * 10
max_bullets = 10
bullets = []


#########################

# Game Methods

def create_balloon():
    balloon = pygame.image.load('balloon.gif')
    balloon = pygame.transform.scale(balloon, (40, 80))
    balloon_rect = balloon.get_rect()
    balloon_rect.top = game_panel_top_y
    balloon_rect.left = game_panel_coords[0] + 10
    return (balloon, balloon_rect)


def create_gun():
    gun = pygame.image.load('gun.png')
    gun = pygame.transform.scale(gun, (80, 60))
    gun_rect = gun.get_rect()
    gun_rect.top = game_panel_top_y
    gun_rect.right = game_panel_coords[0] + game_panel_dims[0] - 10
    return (gun, gun_rect)


def create_bullet(x, y):
    bullet = pygame.image.load('bullet.png')
    bullet = pygame.transform.scale(bullet, (50, 25))
    bullet_rect = bullet.get_rect()
    bullet_rect.top = y
    bullet_rect.right = x
    bullets.append((bullet, bullet_rect))
    return (bullet, bullet_rect)

def move_all_bullets():
    for bullet_info in bullets:
        bullet_rect = bullet_info[1]
        if bullet_rect.left > balloon_rect.right + bullet_speed:
            bullet_rect.left -= bullet_speed

def check_bullet_position():
    wasted_bullets_idx = []
    for bullet_idx, bullet_info in enumerate(bullets):
        if bullet_rect.left <= balloon_rect.right + 5:
            if bullet_rect.top >= balloon_rect.top - 5 and bullet_rect.bottom <= balloon_rect.bottom + 5:
                return "WON"
            else:
                wasted_bullets_idx.append(bullet_idx)
    for idx in wasted_bullets_idx:
        del bullets[idx]
    return "RUNNING"

#########################

# Initialise game environment

infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h - 50

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(game_title)

balloon, balloon_rect = create_balloon()
gun, gun_rect = create_gun()
bullet, bullet_rect = create_bullet(100, 100, 1)

##########################

# Game Loop

fps = 60
timer = pygame.time.Clock()

run = True
while run:
    timer.tick(60)
    screen.fill(black)

    game_title = label_font.render('SHOOT IT', True, white)
    screen.blit(game_title, (game_title_coords[0], game_title_coords[1]))

    pygame.draw.rect(screen, gray, [game_panel_coords[0], game_panel_coords[1], game_panel_dims[0], game_panel_dims[1]],
                     1, 5)

    screen.blit(gun, gun_rect)

    if balloon_rect.top < game_panel_top_y or balloon_rect.bottom > game_panel_bottom_y:
        balloon_speed = -balloon_speed
    balloon_rect.update([balloon_rect.left, balloon_rect.top + balloon_speed, balloon_rect.width, balloon_rect.height])
    screen.blit(balloon, balloon_rect)
    screen.blit(bullet, bullet_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and gun_rect.bottom < game_panel_bottom_y:
        gun_rect.top += gun_speed
    elif keys[pygame.K_UP] or keys[pygame.K_w] and gun_rect.top > game_panel_top_y:
        gun_rect.top -= gun_speed
    if keys[pygame.K_SPACE] and len(bullets) < 10:
        new_bullet = create_bullet(gun_rect.left, (gun_rect.top + gun_rect.bottom) / 2)


    pygame.display.flip()

pygame.quit()
