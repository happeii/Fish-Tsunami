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
    #bullet cooldown
    Cooldown = 20

    def __init__(self,x,y,hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.image = None
        self.shot = None
        self.shots = []
        self.cooldown_time = 0
    
    def draw(self,Screen):
        Screen.blit(self.image,(self.x,self.y))
        for shot in self.shots:
            shot.draw(screen)

    def move_shots(self, speed, target):
        self.cooldown()
        for shot in self.shots:
            shot.move(speed)
            if shot.off_screen(width):
                self.shots.remove(shot)
            elif shot.collision(target):
                target.hp -= 10
                self.shots.remove(shot)

    def cooldown(self):
        if self.cooldown_time >= self.Cooldown:
            self.cooldown_time = 0
        elif self.cooldown_time > 0:
            self.cooldown_time += 1

    def shoot(self):
        if self.cooldown_time == 0:
            next_shot = Projectile(self.x, self.y, self.shot)
            self.shots.append(next_shot)
            self.cooldown_time = 1

class Player(character):
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.image = player
        self.shot = harpoon
        self.mask = pygame.mask.from_surface(self.image)
        self.max_hp = hp

    def move_shots(self, speed, targets):
        self.cooldown()
        for shot in self.shots:
            shot.move(speed)
            if shot.off_screen(width):
                self.shots.remove(shot)
            else:
                for target in targets:
                    if shot.collision(target):
                        targets.remove(target)
                        self.shots.remove(shot)



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

class Projectile:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, speed):
        self.x += speed

    #delete projectile off screen
    def off_screen(self, width):
        return not (0 < self.x <= width)
    
    #collisions
    def collision(self, target):
        return collide(self,target)

def collide(object1, object2):
    gap_x = object2.x - object1.x
    gap_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (gap_x, gap_y)) != None

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
    projectile_speed = 6


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
        if active_keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_speed)
            enemy.move_shots(-projectile_speed, player)
            if random.randrange(0, 180) == 1:
                enemy.shoot()
            
            if enemy.x < 0:
                lives -= 1
                enemies.remove(enemy)
            
        player.move_shots(projectile_speed, enemies)

        #exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
    

main_loop()