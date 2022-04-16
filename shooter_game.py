#Create your own shooter

from pygame import *
from random import randint

_SCREEN_WIDTH = 800
_SCREEN_HEIGHT = 640
window = display.set_mode(( _SCREEN_WIDTH, _SCREEN_HEIGHT))
clock = time.Clock()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, imagefile, x, y, width, height, speed = 0):
        sprite.Sprite.__init__(self)
        self.image = image.load(imagefile)
        self.image = transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
    def shoot(self):
        x = self.rect.centerx
        y = self.rect.top
        b = Bullet("bullet.png", self.rect.centerx-10, self.rect.y, 20, 20, 5)
        b.rect.centerx = x
        bullets.add(b)

class Enemy(GameSprite):
    def update (self):
        self.rect.y += self.speed
        if self.rect.top > _SCREEN_HEIGHT:
            self.rect.x = randint(0, _SCREEN_WIDTH - self.rect.width)
            self.rect.bottom = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class TextSprite(sprite.Sprite):
    def __init__(self, text, size, color_text, position):
        super().__init__()
        self.text = text
        self.position= position
        self.color = color_text
        self.local_font = font.SysFont('Ariel', size)
        self.image = self.local_font.render(self.text, True, color_text)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def update(self, new_text):
        self.text = new_text
        self.image = self.local_font.render(self.text, True, self.color)

player = Player("rocket.png", _SCREEN_WIDTH/2, _SCREEN_HEIGHT-120, 80, 110, 8)

e1 = Enemy("ufo.png", 600, 0, 80, 80, 4)
background = GameSprite("galaxy.jpg", 0, 0, _SCREEN_WIDTH, _SCREEN_HEIGHT)
game_over = GameSprite("game-over.jpg", 0, 0, _SCREEN_WIDTH, _SCREEN_HEIGHT)
bullets = sprite.Group()
enemies = sprite.Group()
def create_enemy():
    enemy = Enemy("ufo.png", randint(0, _SCREEN_WIDTH - 70), 0, 70, 70, randint(1,5))
    enemies.add(enemy)

should_create_enemies = True
points = 0 
score_counter = TextSprite(text="Points: 0", size=50, color_text=(255, 0, 0), position=(100, 30))
timer_counter = TextSprite(text="Timer: 0", size=50, color_text=(255, 255, 0), position=(550, 30))

press_to_retry = TextSprite(text="Press 'r' to RETRY", size=50, color_text=(255, 255, 0), position=(30, 30))

def intro():
    global should_create_enemies, game_state, points
    if should_create_enemies:
        enemies.empty()
        for i in range(5):
            create_enemy()
        should_create_enemies = False
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                game_state = "PLAY"
                points = 0
                

def play():
    global game_state, points
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key ==K_SPACE:
                player.shoot()
    background.draw(window)
    enemies.update()
    enemies.draw(window)
    bullets.update()
    bullets.draw(window)
    player.update()
    player.draw(window)
    score_counter.draw(window)
    score_counter.update("Points: "+str(points))
    timer_counter.update("Timer: "+str(time.get_ticks()//1000))
    timer_counter.draw(window)

    if sprite.spritecollide(player, enemies, False):
        game_state = "END"
    
    collisions = sprite.groupcollide(enemies,bullets, True, True)
    for c in collisions:
        create_enemy()
        points+=1



def end_screen():
    global should_create_enemies, game_state
    game_over.draw(window)
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_r:
                game_state = "INTRO"
                should_create_enemies = True
    game_over.draw(window)
    press_to_retry.draw(window)


game_state = "INTRO"

game_on = True
while not event.peek(QUIT):
    if game_state == "INTRO":
        intro()
    if game_state == "PLAY":
        play()
    if game_state == "END":
        end_screen()


    display.update()
    clock.tick(60)
