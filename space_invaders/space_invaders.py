import pygame, sys, random
from pygame.locals import*
 
pygame.init()
 
MAX_SHOTS = 0

size = width, height = 720, 720

WHITE = (255,255,255)
BLACK = (0,0,0)
SCREENRECT = Rect(0, 0, width, height)
 
FPS = 24 # frames per second setting
fpsClock = pygame.time.Clock()
 
# set up the window
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space Invaders!')

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 1
        self.image = pygame.image.load('middle_alien_1.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.midtop = (.5 * width, .8 * height)
        self.x = self.rect.midtop[0]
        self.y = self.rect.midtop[1]
        print(self.rect)

    def move(self, speed):
        self.rect.midtop = (self.rect.midtop[0] + speed, self.rect.midtop[1])
        if not SCREENRECT.contains(self):
            self.rect = self.rect.clamp(SCREENRECT)

    def gunpos(self):
        return self.rect.midtop[0], self.rect.midtop[0]
 
class Alien(pygame.sprite.Sprite):
    images = []
    animcycle = 12
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health = 15
        self.image = pygame.image.load('middle_alien_1.png')
        self.image = pygame.transform.scale(self.image, (35,35))
        self.speed = 2
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.x = self.rect.midtop[0]
        self.y = self.rect.midtop[1]
        self.collision = False

    def update(self):
        self.rect.midtop = (self.rect.midtop[0] + self.speed, self.rect.midtop[1])
        
    def step_down(self):
        self.rect.top = self.rect.bottom + 1

    def direction_change(self):
        self.speed = -self.speed
        
class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.jpg')
        self.image = pygame.transform.scale(self.image, (5,15))
        self.speed = -20
        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y)
    def update(self):
        self.rect.midtop = (self.rect.midtop[0], self.rect.midtop[1] + self.speed)

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.Font(None, 72)
        self.color = Color('white')
        self.update()
        self.rect = self.image.get_rect().move(200,650)
 
    def update(self):
        text = "Score : " + str(self.score)
        self.image = self.font.render(text, 0, self.color)

class AlienShot(pygame.sprite.Sprite):
    def __init__(self, alien):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.jpg')
        self.image = pygame.transform.scale(self.image, (5,15))
        self.speed = 20
        self.rect = self.image.get_rect()
        self.rect.midtop = (alien.rect.midtop[0] + 10, alien.rect.midtop[1])
    def update(self):
        self.rect.midtop = (self.rect.midtop[0], self.rect.midtop[1] + self.speed)

def music(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1, 0.0)
 
def main():
    music("Rush_-_Tom_Sawyer.wav")
    player_group = pygame.sprite.GroupSingle()
    player = Player()
    player_group.add(player)
    score = Score()
    shots = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    alien_shots = pygame.sprite.Group()
    
    won = False
    lost = False
    game_over = False

    a=0
    speed = 0
    alien_speed = 5
    total_score = 0
    alien_jump = 40
     
    x_spacing = 40
    y_spacing = 35

    for y in range(5):
        for x in range(12):
            aliens.add(Alien(x_spacing * x + 25, y_spacing * y))

    background = pygame.Surface(screen.get_size()).convert()
 
    while not game_over:
        sprites = pygame.sprite.RenderPlain((player, shots, aliens, alien_shots, score))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speed = -8
                if event.key == pygame.K_RIGHT:
                    speed = 8 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    speed = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_SPACE] and len(shots) <= MAX_SHOTS:
            shots.add(Shot(player.rect.midtop[0], player.rect.midtop[1]))

        for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
            total_score += 1

        for alien in pygame.sprite.groupcollide(player_group, aliens, 1, 1).keys():
            total_score += 1

        for shot in shots:
            if not SCREENRECT.contains(shot.rect):
                shots.remove(shot)

        for shot in alien_shots:
            if not SCREENRECT.contains(shot.rect):
                alien_shots.remove(shot)
            if shot.rect.colliderect(player.rect):
                lost = True
                game_over = True

        if not player_group:
            lost = True
            game_over = True
        alien_number = random.randint(0, len(aliens.sprites()) -1)
        alien_shooter = aliens.sprites()[alien_number]

        if len(alien_shots) < MAX_SHOTS + 1:
            alien_shots.add(AlienShot(alien_shooter))

        for alien in aliens:
            if not SCREENRECT.contains(alien.rect) and alien.rect.midtop[0] > width:
                for alien1 in aliens:
                    alien1.speed = -alien1.speed
                    alien1.rect.midtop = (alien1.rect.midtop[0] - 2, alien1.rect.midtop[1] + alien_jump)
            elif not SCREENRECT.contains(alien.rect) and alien.rect.midtop[0] < 0:
                for alien1 in aliens:
                    alien1.speed = -alien1.speed
                    alien1.rect.midtop = (alien1.rect.midtop[0] + 2, alien1.rect.midtop[1] + alien_jump)
    
        score.score = total_score  
        player.move(speed)
        screen.blit(background,(0,0))
        sprites.update()
        sprites.draw(screen)
        pygame.display.update()
        fpsClock.tick(FPS)

        if not aliens:
            won = True
            game_over = True

    if lost == True:
        death = "GAME OVER: SCORE - " + str(total_score)
        font = pygame.font.Font(None, 72)
        text = font.render(death, 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery
        screen.blit(text, textpos)
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit

    if won == True:
        death = "CONGRADULATIONS! SCORE - " + str(total_score)
        font = pygame.font.Font(None, 72)
        text = font.render(death, 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery
        screen.blit(text, textpos)
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit

if __name__ == "__main__":
    main()