import pygame
import time
import random

pygame.font.init()

#game settings
width = 1000
height = 700
fps = 60

#colors
black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)

screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()



#images
background = pygame.transform.scale(pygame.image.load("assets/bg.png"),(width,height))
player = pygame.transform.scale(pygame.image.load("assets/harpoon boat.png"),(90,30))
harpoon = pygame.transform.scale(pygame.image.load("assets/harpoon.png"),(60,20))
fish = pygame.transform.scale(pygame.image.load("assets/8-bit fish.png"),(70,70))
fish_bullet = pygame.transform.scale(pygame.image.load("assets/temp fish bullet.png"),(50,10))



class character():
    def __init__(self,x,y,hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.image = None
        self.shot = None
        self.shots = []
        self.cooldown = 0
    
    def draw(self,Screen):
        Screen.blit(self.image,(self.x,self.y))

class Player(character):
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.image = player
        self.shot = harpoon
        self.mask = pygame.mask.from_surface(self.image)
        self.max_hp = hp

class Enemy(character):
    UNITS = {
        "atkfish": (fish, fish_bullet)
     }
    def __init__(self, x, y, unit, hp=100):
        super().__init__(x, y, hp)
        self.image,self.shot = self.UNITS[unit]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, speed):
        self.x -= speed

def main_loop():
    running = True
    score = 0
    wave = 0
    lives = 3
    main_text = pygame.font.SysFont('freesansbold',40)
    player_speed = 5
    player = Player(100,400)
    enemies = []
    enemy_speed = 2
    wave_size = 5

    def update_screen():
        screen.blit(background,(0,0))
        score_text=main_text.render(f'SCORE: {score}',True,(255,255,255))
        wave_text=main_text.render(f'WAVE: {wave}',True,(255,255,255))
        lives_text=main_text.render(f'LIVES: {lives}',True,(255,255,255))
        screen.blit(score_text,(10,10))
        screen.blit(lives_text,(800,10))
        screen.blit(wave_text,(10,40))
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)


        pygame.display.update


    while running:
        timer.tick(fps)
        update_screen()
        
        #waves
        if len(enemies) == 0:
            wave += 1
            wave_size += 5
            for i in range (wave_size):
                enemy = Enemy(random.randrange(width + 100, width + 1000),
                            random.randrange(100, height - 100),
                            random.choice(["atkfish"]))
                enemies.append(enemy)

        #movement
        active_keys = pygame.key.get_pressed()
        if active_keys[pygame.K_a] and player.x - player_speed > 0:
            player.x -= player_speed
        if active_keys[pygame.K_d] and player.x + player_speed + 100 < width:
            player.x += player_speed
        if active_keys[pygame.K_w] and player.y - player_speed > 0:
            player.y -= player_speed
        if active_keys[pygame.K_s] and player.y + player_speed + 40 < height:
            player.y += player_speed

        for enemy in enemies:
            enemy.move(enemy_speed)

        #exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
    

main_loop()