"""
Copyright 2020 Parth Agrawal

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import pygame
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_SPACE
)
import random

pygame.init()

class Player(pygame.sprite.Sprite):
    def load_image(self, image):
        curr_image = pygame.image.load(image)
        curr_image.set_colorkey((0, 0, 0), RLEACCEL)
        curr_image = pygame.transform.scale(curr_image, (100, 100))
        return curr_image

    def __init__(self):
        super(Player, self).__init__()
        self.images_running = []
        self.images_jumping = []
        
        self.ir = 0
        while self.ir < 10:
            self.ir_num = "Player/Run__00" + str(self.ir) + ".png"
            self.images_running.append(self.load_image(self.ir_num))
            self.ir = self.ir + 1

        self.ij = 0
        while self.ij < 10:
            self.ij_num = "Player/Jump__00" + str(self.ij) + ".png"
            self.images_jumping.append(self.load_image(self.ij_num))
            self.ij = self.ij + 1

        self.index_running = 0
        self.image_running = self.images_running[self.index_running]

        self.index_jumping = 0
        self.image_jumping = self.images_jumping[self.index_jumping]

        self.curr_image = self.image_running
        self.rect = pygame.Rect(5, 350, 100, 100)

    def update(self, pressed_keys):
        self.index_running = self.index_running + 1
        if self.index_running >= len(self.images_running):
            self.index_running = 0
        self.image_running = self.images_running[self.index_running]
        self.curr_image = self.image_running

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            self.index_jumping = self.index_jumping + 1
            if self.index_jumping >= len(self.images_jumping):
                self.index_jumping = 0
            self.image_jumping = self.images_jumping[self.index_jumping]
            self.curr_image = self.image_jumping

            self.rect.move_ip(0, -5)
        if not pressed_keys[K_SPACE]:
            if self.rect.top < 350:
                self.rect.move_ip(0, 10)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 750:
            self.rect.right = 750
      

class Zombie(pygame.sprite.Sprite):
    def load_image(self, image):
        curr_image_zombie = pygame.image.load(image)
        curr_image_zombie.set_colorkey((0, 0, 0), RLEACCEL)
        curr_image_zombie = pygame.transform.scale(curr_image_zombie, (100, 100))
        curr_image_zombie = pygame.transform.flip(curr_image_zombie, True, False)
        return curr_image_zombie

    def __init__(self):
        super(Zombie, self).__init__()
        self.images_walking = []
        self.iw = 1
        while self.iw < 11:
            self.iw_str = "Zombie/Walk (" + str(self.iw) + ").png"
            self.images_walking.append(self.load_image(self.iw_str))
            self.iw = self.iw + 1
        self.index_walking = 0
        self.image_walking = self.images_walking[self.index_walking]
        self.curr_image = self.image_walking
        self.rect = pygame.Rect(650, 350, 100, 100)
    
    def update(self):
        self.index_walking = self.index_walking + 1
        if self.index_walking >= len(self.images_walking):
            self.index_walking = 0
        self.image_walking = self.images_walking[self.index_walking]
        self.curr_image = self.image_walking

        self.rect.move_ip(-2.5, 0)

        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(750 + 20, 750 + 100),
                random.randint(0, 200)
            )
        )
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

screen = pygame.display.set_mode([750, 500])
bg = pygame.image.load("Background.png")
bg = pygame.transform.scale(bg, (750, 500))
bg_rect = bg.get_rect()

ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 2000)
ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, random.randint(3000, 5000))

player = Player() 

clouds = pygame.sprite.Group()
zombies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        
        elif event.type == ADDZOMBIE:
            new_zombie = Zombie()
            zombies.add(new_zombie)
            all_sprites.add(new_zombie)        

    clouds.update()
    zombies.update()

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    screen.blit(bg, bg_rect)

    for entity in all_sprites:
        try:
            screen.blit(entity.surf, entity.rect)
        except AttributeError:
            screen.blit(entity.curr_image, entity.rect)

    if pygame.sprite.spritecollideany(player, zombies):
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
