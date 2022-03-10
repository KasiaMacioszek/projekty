#grafika + dźwięk: kenney.nl - licencja w folderze needed

#importujemy wszystko, co jest potrzebne
import pygame
import os
import random
from pygame.math import Vector2



#wprowadzamy zmienne, które będą potrzebne
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'Asteroids'
ASTEROIDS = ['meteorGrey_big3.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png']
ASTEROIDS_POS = [(SCREEN_HEIGHT, random.randint(0, SCREEN_WIDTH)), (random.randint(0, SCREEN_WIDTH), 0),
                 (random.randint(0, SCREEN_HEIGHT), SCREEN_WIDTH)]
level = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def loadImage(name, useColorKey=False):
    """function to load an image,
    atributes: name - image name, useColorKey = False
    returns an image
    """
    fullname = os.path.join('needed', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if useColorKey == True:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def loadSound(name):
    """Function to load sound
    atributes: name - sound name
    returns sound"""
    soundname = os.path.join('needed', name)
    sound = pygame.mixer.Sound(soundname)
    return sound

#klasa Statku
#////////////

class ShipPlayer(pygame.sprite.Sprite):
    """Player class, has all atributes from pygame sprite"""
    def __init__(self, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)):
        """initializing a player ship with starting position in the middle"""
        super(ShipPlayer, self).__init__()
        self.image = loadImage('playerShip1_red.png', True)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.original_image = self.image
        self.rect = self.image.get_rect(center = pos)
        self.position = Vector2(pos)
        self.direction = Vector2(0, -1)
        self.speed = 0
        self.angle = 0
        self.angle_change = 0
    def update(self):
        """updating the position and direction of the ship"""
        if self.angle_change != 0:
            self.direction.rotate_ip(self.angle_change)
            self.angle += self.angle_change
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.direction * self.speed
        self.rect.center = self.position

        if self.rect.left < 0:
            self.rect.move_ip(SCREEN_WIDTH, 0)
            self.position = self.rect.center
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.move_ip(-SCREEN_WIDTH, 0)
            self.position = self.rect.center
        elif self.rect.top < 0:
            self.rect.move_ip(0, SCREEN_HEIGHT)
            self.position = self.rect.center
        elif self.rect.bottom > SCREEN_HEIGHT-100:
            self.rect.move_ip(0, -SCREEN_HEIGHT)
            self.position = self.rect.center


#klasa laseru
#////////////

class ShipBullet(pygame.sprite.Sprite):
    """Player laser class, has all atributes from pygame sprite"""
    def __init__(self, startpos=(0, 0), direction=(0, 0), angle=0):
        """initializing a laser
        atributes: start position, direction, angle of rotation"""
        super(ShipBullet, self).__init__()
        self.image = loadImage('laserRed03.png', True)
        self.image = pygame.transform.scale(self.image, (5, 20))
        self.original_image = self.image
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect()
        self.rect.midtop = startpos + direction
        self.direction = Vector2(direction)
        self.speed = 7

    def update(self):
        """updates for the class"""
        if self.rect.bottom >= SCREEN_WIDTH or self.rect.bottom >= SCREEN_HEIGHT or self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.midtop += self.direction * self.speed

#klasa asteroid
#//////////////

class Asteroids(pygame.sprite.Sprite):
    """asteroids class, has all atributes from pygame sprite"""
    def __init__(self, counter=0, startpos=(0, 0)):
        """initializing an asteroid
        atributes: couter - size of an asteroid, startpos - start position"""
        super(Asteroids, self).__init__()
        self.counter = counter
        self.image = loadImage(ASTEROIDS[self.counter], True)
        self.original_image = self.image
        #self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.speed = 1
        self.rect.midtop = startpos
        x = random.uniform(-3, 3)
        y = random.uniform(-3, 3)
        self.direction = Vector2(x, y)
        if self.direction == Vector2(0, 0):
            self.direction = Vector2(1, -1)
    def update(self):
        """updates for asteroid class"""
        x = random.uniform(-3, 3)
        y = random.uniform(-3, 3)
        vec = Vector2(x, y)
        if vec == Vector2(0, 0):
            vec = Vector2(1, -1)
        self.rect.midtop += self.direction * self.speed
        if self.rect.right < 0:
            self.rect.move_ip(SCREEN_WIDTH, 0)
            self.rect.midtop = self.rect.center
            self.direction = vec
        if self.rect.left > SCREEN_WIDTH:
            self.rect.move_ip(-SCREEN_WIDTH, 0)
            self.midtop = self.rect.center
            self.direction = vec
        if self.rect.top < 0:
            self.rect.move_ip(0, SCREEN_HEIGHT)
            self.midtop = self.rect.center
            self.direction = vec
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.move_ip(0, -SCREEN_HEIGHT)
            self.midtop = self.rect.center
            self.direction = vec

#Klasa tablicy wyników
#\\\\\\\\\\\\\\\\\\\\\

class scoreBoard(pygame.sprite.Sprite):
    """Class for the score board, has all atributes from pygame sprite"""
    def __init__(self):
        """initializing the board"""
        super(scoreBoard, self).__init__()
        self.score = 0
        self.level = 1
        self.lives = 3
        self.text = "Score: " + str(self.score) + "       Level: " + str(self.level) + "     lives: " + str(self.lives)
        self.font = pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 30)
        self.image = self.font.render(self.text, 1, WHITE)
        self.rect = self.image.get_rect()
    def update(self, score, level, lives):
        """updating the score
        atributes: actual score level and remaining lives"""
        self.score = score
        self.level = level
        self.lives = lives
        self.text = "Score = " + str(self.score) + "        Level: " + str(self.level) + "     lives: " + str(self.lives)
        self.image = self.font.render(self.text, 1, WHITE)
        self.rect = self.image.get_rect()



#Funkcja tworząca wyznaczoną liczbę asteroid
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def createAsteroids(level):
    """Function to create the right amount of asteroids
    atributes: level"""
    AsteroidsSprites = pygame.sprite.RenderPlain()
    for i in range(level+2):
        if i >= 3:
            i = i % 3
        AsteroidsSprites.add(Asteroids(0, ASTEROIDS_POS[i]))
    return AsteroidsSprites


#klasa przycisku
#\\\\\\\\\\\\\\\
class Button(object):
    """class for the buttons"""
    def __init__(self, x, y, width, height, text, textcolor, backgroundcolor):
        """initializing the class
        atributes:
        x, y - placing the button on the screen
        width, height - size of the button
        text - text on the button
        textcolor, backgroundcolor - colors of the button"""
        super(Button).__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = textcolor
        self.background = backgroundcolor
        self.angle = 0
    def check(self):
        """Function to check if the mouse position is on the button"""
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def draw(self, screen):
        """function to draw the button on the screen given as an atribute"""
        pygame.draw.rect(screen, self.background, (self.rect), 0)
        draw_text_center(self.text, pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), screen, self.x+(self.width/2), self.y+(self.height/2), self.text_color)
        pygame.draw.rect(screen, self.text_color, self.rect, 5)


def save_score(score):
    """function to save the score to file"""
    score = str(score)
    with open(os.path.join('needed', 'scores.txt'), 'r') as infile:
        content = infile.read()
    with open(os.path.join('needed', 'scores.txt'), 'w') as outfile:
        outfile.write(content+score+'$')

def top_score():
    """function to pick three best scores"""
    with open(os.path.join('needed', 'scores.txt'), 'r') as infile:
        scores = infile.read()
        scores = scores.split('$')
        s=[]
        for i in range(len(scores)-1):
            s.append(int(scores[i]))
        max1 = max(s)
        s = list(filter((max1).__ne__, s))
        max2 = max(s)
        s = list(filter((max2).__ne__, s))
        max3 = max(s)
        s = list(filter((max3).__ne__, s))
        return max1, max2, max3

def game_over(screen, score):
    """function to run when game is over
    atributes: screen, score to save and display for user"""
    click = False
    while True:
        background = loadImage('4.png')
        screen.blit(background, (0, 0))
        draw_text('GAME OVER', pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), WHITE, screen,
                  SCREEN_WIDTH / 2, 100)
        draw_text('Your score: ' + str(score), pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), WHITE,
                  screen, SCREEN_WIDTH / 2, 300)
        save_score(score)
        button1 = Button(SCREEN_WIDTH / 2 - 200, 500, 400, 50, 'try again', WHITE, BLACK)
        button1.draw(screen)
        button2 = Button(SCREEN_WIDTH / 2 - 100, 600, 200, 50, 'Back', WHITE, BLACK)
        button2.draw(screen)
        if button1.check():
            if click:
                game_loop(screen)
        if button2.check():
            if click:
                main_menu(screen)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


#Funkcja wywołująca program
#\\\\\\\\\\\\\\\\\\\\\\\\\\\

def game_loop(screen):
    """function with the game loop, containing all the actions
    and sprite collisions in, atribute: screen to display"""
    livecount = 3
    level = 1
    score = 0

    background_img = loadImage('4.png')
    screen.blit(background_img, (0,0))

    ShipSprite = pygame.sprite.RenderPlain()
    Ship = ShipPlayer((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    ShipSprite.add(Ship)
    BulletSprites = pygame.sprite.RenderPlain()

    AsteroidsSprites = createAsteroids(level)

    asteroidFX = loadSound('phaserDown2.ogg')
    laserFX = loadSound('laser7.ogg')
    shipFX = loadSound('pepSound1.ogg')
    levelUpFX = loadSound('phaserUp2.ogg')

    scoreboardSprite = pygame.sprite.RenderPlain()
    scoreboardSprite.add(scoreBoard())
    scoreboardSprite.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()
    RUNNING = True
    while RUNNING:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Ship.angle_change = 3
                elif event.key == pygame.K_LEFT:
                    Ship.angle_change = -3
                elif event.key == pygame.K_UP:
                    Ship.speed = 2
                elif event.key == pygame.K_SPACE:
                    BulletSprites.add(ShipBullet(Ship.position, Ship.direction, Ship.angle))
                    laserFX.play()
                elif event.key == pygame.K_p:
                    pygame.time.delay(5000)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    Ship.angle_change = 0
                elif event.key == pygame.K_LEFT:
                    Ship.angle_change = 0
        ShipSprite.update()
        BulletSprites.update()
        AsteroidsSprites.update()

        for hit in pygame.sprite.groupcollide(scoreboardSprite, BulletSprites, 0, 1):
            pass

        for hit in pygame.sprite.groupcollide(scoreboardSprite, ShipSprite, 0, 0):
            ShipSprite.update()

        for asteroid in AsteroidsSprites:
            hit = pygame.sprite.spritecollide(asteroid, scoreboardSprite, 0)
            if hit:
                AsteroidsSprites.remove(asteroid)
                asteroid1 = Asteroids(asteroid.counter, (0, SCREEN_WIDTH))
                AsteroidsSprites.add(asteroid1)


        for hit in pygame.sprite.groupcollide(ShipSprite, AsteroidsSprites, 0, 0):
            livecount -= 1
            scoreboardSprite.update(score, level, livecount)
            scoreboardSprite.clear(screen, background_img)
            scoreboardSprite.draw(screen)
            shipFX.play()
            if livecount == 0:
                game_over(screen, score)

            else:
                for ship in ShipSprite:
                    ship.kill()
                Ship = ShipPlayer()
                ShipSprite.add(Ship)
                for asteroid in AsteroidsSprites:
                    if asteroid.rect == (SCREEN_WIDTH/2, SCREEN_HEIGHT/2):
                        asteroid.rect.move_ip(SCREEN_WIDTH, random.randint(SCREEN_HEIGHT))
                        AsteroidsSprites.update()

        for asteroid in AsteroidsSprites:
            hit = pygame.sprite.spritecollide(asteroid, BulletSprites, 1)
            if hit:
                asteroidFX.play()
                AsteroidsSprites.remove(asteroid)
                if asteroid.counter == 0:
                    AsteroidsSprites.add(Asteroids(1, asteroid.rect.midtop))
                    AsteroidsSprites.add(Asteroids(1, asteroid.rect.midtop))
                    score += 10
                    scoreboardSprite.update(score, level, livecount)
                    scoreboardSprite.clear(screen, background_img)
                    scoreboardSprite.draw(screen)
                    pygame.display.flip()
                elif asteroid.counter == 1:
                    AsteroidsSprites.add(Asteroids(2, asteroid.rect.midtop))
                    AsteroidsSprites.add(Asteroids(2, asteroid.rect.midtop))
                    score += 20
                    scoreboardSprite.update(score, level, livecount)
                    scoreboardSprite.clear(screen, background_img)
                    scoreboardSprite.draw(screen)
                    pygame.display.flip()
                else:
                    pass

        if len(AsteroidsSprites) == 0 and livecount != 0:
            level += 1
            levelUpFX.play()
            scoreboardSprite.update(score, level, livecount)
            scoreboardSprite.clear(screen, background_img)
            scoreboardSprite.draw(screen)
            AsteroidsSprites = createAsteroids(level)
            livecount = 3

        ShipSprite.clear(screen, background_img)
        BulletSprites.clear(screen, background_img)
        AsteroidsSprites.clear(screen, background_img)

        ShipSprite.draw(screen)
        BulletSprites.draw(screen)
        AsteroidsSprites.draw(screen)

        pygame.display.flip()



def draw_text_center(text, font, screen, x, y, color):
    """function to display the text and know where the center of it is
    atributes:
    text, font - text as a string, font as pygame font (with size)
    screen - screen to be displayed on
    x, y, color - placing the text and it's color"""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    screen.blit(textobj, textrect)

def draw_text(text, font, color, surface, x, y):
    """function to display the text and know where the center of it is
    atributes:
    text, font - text as a string, font as pygame font (with size)
    color - text color (in rgb)
    surface - screen to be displayed on
    x, y, - placing the text"""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.midtop = (x, y)
    surface.blit(textobj, textrect)

def best_score(screen):
    """function that shows the best scores on screen given as atribute"""
    click = False
    while True:
        background = loadImage('4.png')
        screen.blit(background, (0, 0))
        draw_text_center('the best score:', pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), screen, SCREEN_WIDTH / 2, 200, WHITE)
        score = top_score()
        draw_text_center('1. '+str(score[0]), pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), screen, SCREEN_WIDTH / 2, 300, WHITE)
        draw_text_center('2. ' + str(score[1]), pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), screen, SCREEN_WIDTH / 2, 400, WHITE)
        draw_text_center('3. ' + str(score[2]), pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50), screen, SCREEN_WIDTH / 2, 500, WHITE)
        button = Button(SCREEN_WIDTH / 2 - 100, 600, 200, 50, 'back', WHITE, BLACK)
        button.draw(screen)
        if button.check():
            if click:
                main_menu(screen)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()

def rules(screen):
    """function to display the rules of the game on the screen given as an atribute"""
    click = False
    while True:
        background = loadImage('4.png')
        screen.blit(background, (0, 0))
        draw_text_center('welcome to asteroids game', pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 35), screen, SCREEN_WIDTH / 2, 100, WHITE)
        draw_text_center("don't let the asteroids kill your spaceship", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 200, WHITE)
        draw_text_center("be faster than they are,", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 250, WHITE)
        draw_text_center("use the arrows to rotate the ship", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 300, WHITE)
        draw_text_center("use the top arrow to start your engine", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 350, WHITE)
        draw_text_center("and fly through the space", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 400, WHITE)
        draw_text_center("press space to shoot with a laser", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 450, WHITE)
        draw_text_center("and smash asteroids before they smash you", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 500, WHITE)
        draw_text_center("if you want a few seconds break just press p",pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2,550, WHITE)
        button = Button(SCREEN_WIDTH / 2 - 100, 600, 200, 50, 'back', WHITE, BLACK)
        button.draw(screen)
        if button.check():
            if click:
                main_menu(screen)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def about_me(screen):
    """function to display informations about the author of the game on the screen given as an atribute"""
    click = False
    while True:
        background = loadImage('4.png')
        screen.blit(background, (0, 0))
        draw_text_center('welcome to my first game', pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 35), screen, SCREEN_WIDTH / 2, 50, WHITE)
        draw_text_center("I created a clone of the asteroids game", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 100, WHITE)
        draw_text_center("it took me a while to make it", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 150, WHITE)
        draw_text_center("but i had a lot of fun doing this", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 200, WHITE)
        draw_text_center("hope you'll also like it and have fun playing", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 250, WHITE)
        draw_text_center("if you do or have any comments", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 300, WHITE)
        draw_text_center("feel free to e-mail me or find me on facebook", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 350, WHITE)
        draw_text_center("my e-mail: kasiamacioszek1201@gmail.com", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 400, WHITE)
        draw_text_center("me: Kasia Macioszek", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 450, WHITE)
        draw_text_center("graphic credits to kenney.nl", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 500, WHITE)
        draw_text_center("special thanks to my boyfriend who helped me", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 550, WHITE)
        draw_text_center("by giving both the idea and mental support", pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 25), screen, SCREEN_WIDTH / 2, 600, WHITE)
        button = Button(SCREEN_WIDTH / 2 - 100, 700, 200, 50, 'back', WHITE, BLACK)
        button.draw(screen)
        if button.check():
            if click:
                main_menu(screen)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def main_menu(screen):
    """function to display the main menu of the game on the screen given as an atribute"""
    click = False
    while True:
        font = pygame.font.Font(os.path.join('needed', 'androidnation.ttf'), 50)
        background = loadImage('4.png')
        screen.blit(background, (0, 0))
        draw_text('main menu', font, WHITE, screen, SCREEN_WIDTH/2, 100)
        button1 = Button(SCREEN_WIDTH/2-225, 200, 450, 50, 'start game', WHITE, BLACK)
        button1.draw(screen)
        button2 = Button(SCREEN_WIDTH/2-250, 300, 500, 50, 'How to play', WHITE, BLACK)
        button2.draw(screen)
        button3 = Button(SCREEN_WIDTH/2-225, 400, 450, 50, 'Best score', WHITE, BLACK)
        button3.draw(screen)
        button4 = Button(SCREEN_WIDTH/2-350, 500, 700, 50, 'About the author', WHITE, BLACK)
        button4.draw(screen)
        button5 = Button(SCREEN_WIDTH/2-100, 600, 200, 50, 'quit', WHITE, BLACK)
        button5.draw(screen)
        if button1.check():
            if click:
                game_loop(screen)
        if button2.check():
            if click:
                rules(screen)
        if button3.check():
            if click:
                best_score(screen)
        if button4.check():
            if click:
                about_me(screen)
        if button5.check():
            if click:
                pygame.quit()
                quit()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
def main():
    """main function to initialize the window"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    main_menu(screen)

if __name__ == "__main__":
    main()
    pygame.quit()