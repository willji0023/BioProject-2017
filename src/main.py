# game with repeating time limit that shouldn't be able to exit(so players don't 
# close out of it and lose high scores) unless while the game is running
import pygame, sys, random, time, easygui

pygame.init()                                                            
screen = pygame.display.set_mode([1600,900])
background = pygame.Surface(screen.get_size())
background.fill([255, 255, 255])                                         
clock = pygame.time.Clock()                                              
delay = 1
interval = 5
score = 0
DRONE_Y = 350
GAMETIME = 25
pygame.key.set_repeat(delay, interval)
random.seed(a=None)

# fonts
plainfont = pygame.font.SysFont("monospace", 15)
credit = plainfont.render("William Jin", 1, (0, 0, 0))
boldfont = pygame.font.SysFont("bangers", 35)
normalfont = pygame.font.SysFont("timesnewroman", 70)
LGfunnyfont = pygame.font.SysFont("freestylescript", 40)
hsDisplay = LGfunnyfont.render("High Score", 1, (2, 83, 110))
SMfunnyfont = pygame.font.SysFont("freestylescript", 28)
fancyfont = pygame.font.SysFont("pristina", 150, italic=True)
title = fancyfont.render("The Acidrone", 7, (238, 130, 238))
cursivefont = pygame.font.SysFont("frenchscript", 65, italic=True)
caption = cursivefont.render("...Blackie Fredriks Biology Period 4", 1, (220, 20, 60))
dumbfont = pygame.font.SysFont("comicsans", 20)
joke = dumbfont.render("(of Science)", 1, (0, 0, 0))
easygui.msgbox("To play, move left and right with the arrow keys. Press spacebar to become stationary, but eject a shield to block incoming acid rain, earning points each drop. Catch the mega-acid drop to earn even more points. Rain speed can possibly become stronger or weaker. You have 16 seconds. Good luck!")

# classes
class Drone(pygame.sprite.Sprite):                                        
    def __init__(self, image_file, speed, location):                      
        pygame.sprite.Sprite.__init__(self)     
        self.image = pygame.image.load(image_file)                       
        self.rect = self.image.get_rect()                                
        self.rect.left, self.rect.top = location                         
        self.speed = speed
    def dont_move(self):                                                       
        self.rect.left = self.rect.left
my_drone = Drone('drone.png', [20,0], [600, DRONE_Y])

class Prop(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
my_nature = Prop('na.png', [0, 700])
my_cloud = Prop('clouds.png', [0, -350])

class Acid(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = random.randint(0,1600), random.randint(0, 900)
        self.speed = 0, 20
    def rain(self):
        self.rect.left = self.rect.left + 10
        self.rect.top = self.rect.top + 50
        if self.rect.left > screen.get_width():
            self.rect.left = 0
        if self.rect.top > screen.get_height():
            self.rect.top = 0
            self.rect.left = random.randint(0,1600)

def animate(group, shield):
    for acidrain in group:
        acidrain.rain()
        screen.blit(acidrain.image, acidrain.rect)
    if shield:
        if pygame.sprite.collide_rect(my_drone, megarain):
            global score
            score = score + 100
            acidrain.rect.left = random.randint(0, 1600)
            acidrain.rect.top = 0
        for acidrain in group:
            if pygame.sprite.collide_rect(my_drone, acidrain):
                global score
                score = score + 5
                acidrain.rect.left = random.randint(0, 1600)
                acidrain.rect.top = 0
        
# window for players to leave the game where it is or restart, or for a new player to begin
def gameover(self):
    keep_going = False
    while not keep_going:
        if easygui.boolbox("Restart?", " ", ["Heck yeah!", "How to Play??"]):
            keep_going = True
        else:
            easygui.msgbox("To play, move left and right with the arrow keys. Press spacebar to become stationary, but eject a shield to block incoming acid rain, earning points each drop. Catch the mega-acid drop to earn even more points. Rain speed can possibly become stronger or weaker. You have 16 seconds. Good luck!")

# adding multiple acid drops plus one mega acid           
group = pygame.sprite.Group()
megarain = Acid('megarain.png')
group.add(megarain)
for x in range (0, 16):
    acidrain = Acid('acidrain.png')
    group.add(acidrain)
    
running = True
startup = True
spacePresses = 0
caught = False
spaceRemembered = spacePresses
highscore = 7
highscoreman = "God"

# main while loop
while running:
    screen.blit(background, (0, 0))

    # runs every start to ask for player's name
    while startup:
        name = easygui.enterbox("Hello and welcome. What's your name?")
        if name is None:
            easygui.msgbox("Invalid name dumbie! Try again.")
            continue
        else:
            start_ticks = pygame.time.get_ticks()
            startup = False
    
    # highscores
    currentName = boldfont.render("Hello, "+name, 1, (255, 0, 255))
    currentScore = boldfont.render("Your Score = "+str(score), 1, (0, 0, 0))
    currentHighscore = SMfunnyfont.render(highscoreman+" - "+str(highscore), 1, (2, 83, 110))
    
    animate(group, caught)

    # time
    seconds = (pygame.time.get_ticks()-start_ticks)/1000
    timer = GAMETIME - seconds
    if timer <= 0:
        if score > highscore:
            highscore = score
            highscoreman = name
            win = "goodending.gif"
            ok = easygui.buttonbox("Congratulations, "+name+", on beating the highscore!",
                               "Game Over", ["Woohoo!"], image=win)            
        else:
            lose = "badending.gif"
            ok = easygui.buttonbox("Times up! Good game, "+name,  "Game Over", ["Ok"],
                              image=lose)
        startup = True
        score = 0
        gameover(startup)
    elif timer <= 3:
        currentTimer = normalfont.render(str(timer), 1, (255, 0, 0))
    else:
        currentTimer = normalfont.render(str(timer), 1, (169, 169, 169))
    
    # movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                    
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and spacePresses > spaceRemembered:
                my_drone.rect.left = my_drone.rect.left
            elif event.key == pygame.K_SPACE:
                caught = True
                oldPosition = my_drone.rect.left
                my_drone = Drone('droneshield.png', [0.5,0], [oldPosition -114, DRONE_Y -98])       
                spacePresses = spacePresses + 1
            elif my_drone.rect.left <= screen.get_rect().left and event.key == pygame.K_LEFT:
                my_drone.dont_move()
            elif my_drone.rect.right >= screen.get_rect().right and event.key == pygame.K_RIGHT:
                my_drone.dont_move()
            elif event.key == pygame.K_LEFT and spacePresses > spaceRemembered:
                olderPosition = my_drone.rect.left
                score = score + 5
                my_drone = Drone('drone.png', [0.5,0], [olderPosition + 114, DRONE_Y])  
                my_drone.rect.left = my_drone.rect.left - 20
                caught = False
                spaceRemembered = spacePresses
            elif event.key == pygame.K_RIGHT and spacePresses > spaceRemembered:
                olderPosition = my_drone.rect.left
                score = score + 5
                my_drone = Drone('drone.png', [0.5,0], [olderPosition + 114, DRONE_Y])  
                my_drone.rect.left = my_drone.rect.left + 20
                caught = False
                spaceRemembered = spacePresses
            elif event.key == pygame.K_LEFT:
                my_drone.rect.left = my_drone.rect.left - 20
                score = score + 5             
            elif event.key == pygame.K_RIGHT:
                my_drone.rect.left = my_drone.rect.left + 20
                score = score + 5

    clock.tick(60)
    
    # screen blitting
    screen.blit(title, (200, 200))
    screen.blit(caption, (300, 312))
    screen.blit(joke, (850, 300))
    screen.blit(my_nature.image, my_nature.rect)
    screen.blit(my_cloud.image, my_cloud.rect)
    screen.blit(my_drone.image, my_drone.rect)
    screen.blit(credit, (1470, 700))
    screen.blit(hsDisplay, (1420, 150))
    screen.blit(currentName, (5, 130))
    screen.blit(currentScore, (5, 160))
    screen.blit(currentTimer, (810, 175))
    screen.blit(currentHighscore, (1458, 193))
    pygame.display.flip()
    pygame.display.update()

pygame.quit()

