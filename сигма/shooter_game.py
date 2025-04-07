from pygame import *
import random

win_widht = 700
win_height = 500

window = display.set_mode((win_widht, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load('galaxy.jpg'), (win_widht, win_height))

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 70:
            self.rect.x += self.speed 

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_widht:
            self.rect.y = 0
            self.rect.x = randint(80, win_widht - 80)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_widht:
            self.rect.y = 0
            self.rect.x = random.randint(80, win_widht - 80)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (30, 30))
     
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

spacecraft = Player('rocket.png', 350, 420, 10)

bullets = sprite.Group()  
monstres = sprite.Group()
asteroids = sprite.Group()


for i in range(7):
    monster = Enemy('ufo.png', random.randint(0, 650), -60, random.randint(3, 6))
    monstres.add(monster)

for i in range(2):
    asteroid = Asteroid('asteroid.png',random.randint(0, 650), -60, random.randint(1, 5))
    asteroids.add(asteroid)

score = 0

font.init()
font1 = font.SysFont('Arial', 36)
text_loser = font1.render('ТЫ ПРОООООООООООООИГРАЛ!!!',1,(255,0,0))
text_vin = font1.render('ТЫ ВЫЫЫЫЫЫЫГРААЛАЛАЛЛА!!!',1,(0,255,0))
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False 
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet = Bullet('bullet.png', spacecraft.rect.x, spacecraft.rect.y,  10)
                bullets.add(bullet)


    window.blit(background, (0, 0))

    spacecraft.update()
    spacecraft.reset()

    monstres.update()
    monstres.draw(window)

    asteroids.update()
    asteroids  .draw(window)

    bullets.update()
    bullets.draw(window)


    collisions = sprite.groupcollide(monstres , bullets, True, True)
    for collision in collisions:
        score += 1
        monster = Enemy('ufo.png', random.randint(0, 635), -60, random.randint(1, 5))
        monstres.add(monster)

    for monster in monstres:
        if monster.rect.y > win_height:
            lost += 1
            monster.rect.y = 0
            monster.rect.x = random.randint(0, 650)


    if lost >= 10 or sprite.spritecollide(spacecraft, monstres, False) or sprite.spritecollide(spacecraft, asteroids, False):
        window.blit(text_loser, (200,200))
        display.update()
        run = False        
    if score >= 100:
        window.blit(text_vin, (200,200))
        display.update()
        run = False


    text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    text_score = font1.render("Счет: " + str(score), 1, (255, 255, 255))
    
    window.blit(text_score, (10, 10))
    window.blit(text_lose, (10, 50))


    display.update()
    clock.tick(FPS)