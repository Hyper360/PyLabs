import pygame
import random
from Assets import dialogue_and_timer
from csv import reader, writer, DictReader
from datetime import datetime as dt
import os

DT = dialogue_and_timer

header = ['Name', 'Date', 'Time', 'Hits', 'Clicks']
filename = os.path.join(os.path.dirname(__file__), "AimStats", "aimstats.csv")

try:
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        data = list(csv_reader)
        pasthits = [row['Hits'] for row in data]
        pastclicks = [row['Clicks'] for row in data]
        pasttime = [row['Time'] for row in data]
        date = [row['Date'] for row in data]
        names = [row['Name'] for row in data]
except FileNotFoundError:
    date = []
    pasthits = []
    pastclicks = []
    names = []
    pasttime = []
    data = []

    with open(filename, 'w', newline='') as file:
        csv_writer = writer(file)
        csv_writer.writerow(header)

# Above code removed the need for pandas!!
# Credit to ChatGPT!!!

pygame.init()

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hyper's Aimlabs")
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Assets", "PixeloidMono.ttf"), 20)

class Target():
    def __init__(self, screen, x, y, width, height, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def repos(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Border():
    def __init__(self, screen, width, height, thickness):
        self.screen = screen
        self.width = width
        self.height = height
        self.thickness = thickness

        self.b1 = pygame.rect.Rect(0, 0, WIDTH, 1)
        self.b2 = pygame.rect.Rect(0, HEIGHT, WIDTH, 1)
        self.b3 = pygame.rect.Rect(0, HEIGHT, 1, HEIGHT)
        self.b4 = pygame.rect.Rect(WIDTH, 0, 1, HEIGHT)

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.b1)
        pygame.draw.rect(self.screen, (0, 0, 0), self.b2)
        pygame.draw.rect(self.screen, (0, 0, 0), self.b3)
        pygame.draw.rect(self.screen, (0, 0, 0), self.b4)

class JustDrawAlready():
    def __init__(self, surface, y):
        self.surface = surface
        self.y = y

    def draw(self):
        screen.blit(self.surface, (0, self.y))

def search(file, term):
    readers = reader(open(file, 'r'))
    for row in readers:
        if row[0] == term:
            return True
    return False # return None if no match

def write(file, term, col):
    writer = writer(open(file, 'w'))



target = Target(screen, random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 50, 50, (200, 0, 0))
border = Border(screen, WIDTH, HEIGHT, 10)
hit = 0
click = 0
scoreSurface = font.render(str(hit), True, (200, 0, 0))

clicksSurface = font.render(str(click), True, (200, 0, 0))

targetImg = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "crosshair.png"))
targetRect = targetImg.get_rect()

#Finally, stuff copied from POI_lite
input_rect = pygame.Rect((WIDTH/2), 200, 140, 32)
enter_rect = pygame.Rect((WIDTH/2 - 50), (HEIGHT/2 + 150), 140, 32)
user_text = ''
rows = []
rowDraw = []
class Game():
    def __init__(self):
        self.state = 'setup'
        self.nameEntered = False
        self.csvFile = os.path.join(os.path.dirname(__file__), "AimStats", "aimstats.csv")

        self.time_input_rect = pygame.Rect((WIDTH/2), 200, 140, 32)
        self.time_enter_rect = pygame.Rect((WIDTH/2 - 50), (HEIGHT/2 + 150), 140, 32)
        self.time_left = ''
        self.y = 0

    def setup(self):
        screen.fill((200, 200, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    self.time_left += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    self.time_left = self.time_left[:-2]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.time_enter_rect.collidepoint(event.pos):
                    self.time_left = int(self.time_left)
                    self.timer = DT.Timer(self.time_left)
                    self.state = 'game'


        pygame.draw.rect(screen, (0,0,0), self.time_input_rect)
        pygame.draw.rect(screen, (0,200,0), self.time_enter_rect)
        self.time_left_surface = font.render(str(self.time_left), True, (255, 0, 0))
        screen.blit(self.time_left_surface, (self.time_input_rect.x + 5, self.time_input_rect.y))
        self.time_input_rect.width = max(100, (self.time_left_surface.get_width() + 10))
        self.time_input_rect.center = (WIDTH/2, HEIGHT/2)
        self.time_enter_rect.center = (WIDTH/2, self.time_input_rect.centery + 50)

        pygame.display.flip()

    def game(self):
        global hit, click
        screen.fill((200, 200, 200))
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if target.rect.collidepoint(event.pos):
                    target.repos(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 50, 50)
                    hit += 1
                click += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    hit = 0
                    click = 0
                elif event.key == pygame.K_c:
                    self.state = 'highscores'
            mousePos = pygame.mouse.get_pos()
            targetRect.center = mousePos

        self.timer.update(current_time)
        if self.timer.return_exact_time(60) < self.time_left:
            if target.rect.collidelistall([border.b1, border.b2, border.b3, border.b4]):
                target.repos(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 50, 50)

            target.draw()
            border.draw()
            scoreSurface = font.render('Score: ' + str(hit), True, (200, 0, 0))
            clicksSurface = font.render('Clicks: ' + str(click), True, (200, 0, 0))
            timeSurface = font.render('Time:' + str(round(self.time_left - self.timer.return_exact_time(60), 2)), True, (200, 0, 0))

            screen.blit(scoreSurface, (0, 0))
            screen.blit(clicksSurface, (0, 20))
            screen.blit(timeSurface, (0, 40))
            screen.blit(targetImg, targetRect)
        else:
            self.state = 'highscores'
        pygame.display.flip()

    def highscores(self):
        global user_text, pastclicks, pasthits, names, date, rows
        screen.fill((200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if self.nameEntered == False:
                    user_text += event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-2]
                else:
                    if event.key == pygame.K_r:
                        self.state = 'setup'
                        user_text = ''
            if event.type == pygame.MOUSEBUTTONDOWN:
                if enter_rect.collidepoint(event.pos):
                    date.append(str(dt.today().date()))
                    names.append(str(user_text))
                    pasthits.append(hit)
                    pastclicks.append(click)
                    pasttime.append(str(self.time_left))
                    with open(self.csvFile, 'w') as f:
                        writers = writer(f)
                        if os.path.getsize(self.csvFile) == 0:
                            writers.writerow(header)
                        for n in range(len(names)):
                            writers.writerow([names[n], date[n], pasttime[n], pasthits[n], pastclicks[n]])
                        f.close()

                    with open(self.csvFile, 'r') as csvfile:
                        self.reader = reader(csvfile)
                        for row in self.reader:
                            rows.append(row)
                    self.nameEntered = None
                    user_text = ''
                    self.nameEntered = True
                    print(rows)

        if self.nameEntered == False:
            pygame.draw.rect(screen, (0,0,0), input_rect)
            pygame.draw.rect(screen, (0,200,0), enter_rect)
            text_surface = font.render(str(user_text), True, (255, 0, 0))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y))
            input_rect.width = max(100, (text_surface.get_width() + 10))
            input_rect.center = (WIDTH/2, HEIGHT/2)
            enter_rect.center = (WIDTH/2, input_rect.centery + 50)
        elif self.nameEntered == True:
            for row in rows:
                rowDraw.append(JustDrawAlready(font.render(row[0] + " | " + row[1] + " | "  + row[2] + " | "  + row[3] + " | "  + row[4], True, (200, 0, 0)), self.y))
                self.y += 30
            self.nameEntered = None

        for rowSurface in rowDraw:
            rowSurface.draw()

        pygame.display.flip()

    def state_manager(self):
        if self.state == 'setup':
            self.setup()
        if self.state == 'game':
            self.game()
        if self.state == 'highscores':
            self.highscores()
        clock.tick(200)


gamecontroller = Game()
while True:
    gamecontroller.state_manager()
    clock.tick(200)
