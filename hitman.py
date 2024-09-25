import sys
import cfg
import math
import random
import pygame
from modules import *

def initGame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Bunny Hitman")

    game_images ={}
    for key, value in cfg.IMAGE_PATH.items():
        if isinstance(value, list):
            images = []
            for item in value: images.append(pygame.image.load(item))
            game_images[key] = images
        else:
            game_images[key] = pygame.image.load(value)
    
    game_sounds = {}                         
    for key, value in cfg.AUDIO.items():
        if key != 'moonlight':
            game_sounds[key] = pygame.mixer.Sound(value)
    return screen, game_images, game_sounds

def StartInterface(screen, game_images):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 105, 180), (0, 0, cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1]))
    pygame.draw.rect(screen, (0, 0, 255), (cfg.SCREENSIZE[0]//2, 0, cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1]))

    bunny_1 = game_images['rabbit']
    bunny_2 = game_images['rabbit_2']
    screen.blit(bunny_1, (100, 200))
    screen.blit(bunny_2, (400, 200))
    font = pygame.font.Font(None, 50)
    select = font.render("Select a character:", True, (0, 255, 0))
    srect = select.get_rect()
    srect.midtop = (cfg.SCREENSIZE[0] // 2, 40)
    screen.blit(select, srect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 300 and 100 <= mouse_pos[1] <= 300:
                    return 1
                elif 400 <= mouse_pos[0] <= 600 and 100 <= mouse_pos[1] <= 300:
                    return 2
        
        pygame.display.update()

def main():
    screen, game_images, game_sounds = initGame()

    pygame.mixer.music.load(cfg.AUDIO['moonlight'])
    pygame.mixer.music.play(-1, 0, 0)

    font = pygame.font.Font(None, 24)
    sleceted_bunny, running, exitcode = StartInterface(screen, game_images), True, False
    if sleceted_bunny == 1:
        bunny = BunnySprite(image=game_images.get('rabbit'), position=[100, 100])
    elif sleceted_bunny == 2:
        bunny = BunnySprite(image=game_images.get('rabbit_2'), position=[100, 100])
    
    acc_record = [0., 0.]
    healthvalue = 194
    arrow_sprites_group = pygame.sprite.Group()
    badguy_sprites_group = pygame.sprite.Group()

    badguy = EnemySprite(images=game_images['badguy'], position=(640, 100))
    badguy_sprites_group.add(badguy)

    badtimer = 100
    badtimer1 = 0

    font = pygame.font.Font(None, 30)
    start_text = font.render("Press 'SPACE' to start the game.", True, (200, 25, 50))
    start_rect = start_text.get_rect()
    start_rect.midbottom = (cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] - 50)
    start_game = False
    blink_timer = 0

    clock = pygame.time.Clock()

    while not start_game:
        screen.fill(0)
        start_image = game_images['start']
        image_width, image_height = start_image.get_rect().size
        aspect_ratio = image_width / image_height
    
        if aspect_ratio > 1:
            new_image_width = screen.get_width()
            new_image_height = int(new_image_width / aspect_ratio+54)
        else:
            new_image_height = screen.get_height()
            new_image_width = int(new_image_height * aspect_ratio)
    
        scaled_image = pygame.transform.scale(start_image, (new_image_width, new_image_height))
    
        screen.blit(scaled_image, ((screen.get_width() - new_image_width) // 2, (screen.get_height() - new_image_height) // 2))

        if blink_timer % 30 < 15:
            screen.blit(start_text, start_rect)
        pygame.display.update()
        blink_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_game = True

    while running:
        
        screen.fill(0)
        for x in range(cfg.SCREENSIZE[0]//game_images['grass'].get_width()+1):
            for y in range(cfg.SCREENSIZE[1]//game_images['grass'].get_height()+1):
                screen.blit(game_images['grass'], (x*100, y*100))
        for i in range(4): screen.blit(game_images['castle'], (0, 30+105*i))
        
        countdown_text = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0, 0, 0))
        countdown_rect = countdown_text.get_rect()
        countdown_rect.topright = [635, 5]
        screen.blit(countdown_text, countdown_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_sounds['shoot'].play()
                acc_record[1] +=1
                mouse_pos = pygame.mouse.get_pos()
                angle = math.atan2(mouse_pos[1] - (bunny.rotated_position[1]+32), mouse_pos[0] - (bunny.rotated_position[0]+26))
                arrow = ArrowSprite(game_images.get('arrow'), (angle, bunny.rotated_position[0]+32, bunny.rotated_position[1]+26))
                arrow_sprites_group.add(arrow)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            bunny.move(cfg.SCREENSIZE, 'up')
        elif key_pressed[pygame.K_s]:
            bunny.move(cfg.SCREENSIZE, 'down')
        elif key_pressed[pygame.K_a]:
            bunny.move(cfg.SCREENSIZE, 'left')
        elif key_pressed[pygame.K_d]:
            bunny.move(cfg.SCREENSIZE, 'right')
        
        for arrow in arrow_sprites_group:
            if arrow.update(cfg.SCREENSIZE):
                arrow_sprites_group.remove(arrow)
        
        if badtimer == 0:
            badguy = EnemySprite(game_images['badguy'], position=(640, random.randint(50, 430)))
            badguy_sprites_group.add(badguy)
            badtimer=100-(badtimer1*2)
            badtimer1 = 20 if badtimer1>=20 else badtimer1+2
        badtimer -= 1

        for badguy in badguy_sprites_group:
            if badguy.update():
                game_sounds['hit'].play()
                healthvalue -= random.randint(4, 8)
                badguy_sprites_group.remove(badguy)

        for arrow in arrow_sprites_group:
            for badguy in badguy_sprites_group:
                if pygame.sprite.collide_mask(arrow, badguy):
                    game_sounds['enemy'].play()
                    arrow_sprites_group.remove(arrow)
                    badguy_sprites_group.remove(badguy)
                    acc_record[0] += 1

        arrow_sprites_group.draw(screen)
        badguy_sprites_group.update()
        badguy_sprites_group.draw(screen)

        bunny.draw(screen, pygame.mouse.get_pos())

        screen.blit(game_images.get('healthbar'), (5, 5))

        for i in range(healthvalue):
            screen.blit(game_images.get('health'), (i+8, 8))

        if pygame.time.get_ticks() >= 90000 or healthvalue <= 0:
            if healthvalue > 0:
                running, exitcode, game_win = False, True, True
            else:
                running, exitcode, game_win = False, True, False   
        
        clock.tick(cfg.FPS)

        accuracy = acc_record[0]/acc_record[1]*100 if acc_record[1] > 0 else 0
        accuracy = '%.2f' % accuracy

        if exitcode:
            if game_win:
                screen.blit(game_images.get('youwin'), (0, 0))
            else:
                screen.blit(game_images.get('gameover'), (0, 0))

        pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()