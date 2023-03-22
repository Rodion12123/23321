
from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None,36)

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = 'bullet.png' 

score = 0 
lost = 0


window = display.set_mode((700,500))
display.set_caption("Космос")
back=transform.scale(image.load("galaxy.jpg"),(700,500))

clock = time.Clock()
FPS = 61


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.player_speed
            if keys[K_RIGHT] and self.rect.x < WIGTH - 80:
                self.rect.x += self.player_speed
                
                    
class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed

        if self.rect.y > win_height:
            
            self.rect.x = randint(80, win_width - 80)
            self.rect.x = 0
            lost += 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (15,15))
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
    


win_width = 900
win_height = 700
FPS = 60
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
clock = time.Clock()


ship = Player(img_hero, 5, win_height - 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1,3))
    monsters.add(monster)
bullets = sprite.Group()

finish = False


run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
        if not finish:
            window.blit(background, (0,0))
            text = font2.render("Счет::" + str(score), 1, (255,255,255))
            window.blit(text,(10,20))
            text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10,50))
            ship.update()
            monsters.update()
            bullets.update()

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                monster 

            display.update()
            clock.tick(FPS)
