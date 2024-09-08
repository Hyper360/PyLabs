import pygame

# Yessir, a copy of the same Dialogue and timer module used in HFC !!!

class DialogueCharacter():
    def __init__(self, screen, x, y, file):
        self.x = x
        self.y = y
        self.screen = screen
        self.file = pygame.image.load(file)
        self.file_rect = self.file.get_rect()
        self.file_rect.x = self.x
        self.file_rect.y = self.y
    
    def change_image(self, new_image):
        self.file = pygame.image.load(new_image)
        self.file_rect = self.file.get_rect()
        self.file_rect.x = self.x
        self.file_rect.y = self.y
    
    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.file_rect.x = self.x
        self.file_rect.y = self.y
    
    def change_image_size(self, width, height):
        self.file = pygame.transform.scale(self.file, (width, height))
        self.file.convert()
        self.file_rect = self.file.get_rect()

    def draw(self):
        self.screen.blit(self.file, self.file_rect)

class Timer():
    def __init__(self, time):
        self.called = pygame.time.get_ticks()
        self.time = time
        self.signal = False

        # For return time
        self.ticker = 0
        self.seconds = 0
    
    def reset(self, current_time):
        self.signal = False
        self.called = current_time
        self.ticker = 0
        self.seconds = 0
    
    def return_time(self, fps):
        if self.ticker < fps:
            self.ticker += 1
        elif self.ticker >= fps:
            self.seconds += 1
            self.ticker = 0
        
        return self.seconds

    def return_exact_time(self, fps):
        self.ticker += 1
        self.seconds = self.ticker/fps

        return self.seconds

    def update(self, current_time):
        if current_time - self.called >= self.time:
            self.signal = True
            self.called = current_time