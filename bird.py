import pygame
from random import randint

# TODO: replay/death screen
# TODO: show score not in console but on screen

pygame.init()
width, height = 1500, 1100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_COLOR = (34, 139, 34)
SKY_BLUE = (135, 206, 235)
POOPY_BROWN = (139, 69, 19)
ground_rect = pygame.Rect(0, height - 150, width, 150) 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("flappy tappy i am not happy")

font = pygame.font.Font(None, 50) 
pre_screen_text = font.render("press button to start", True, BLACK)
text_rect = pre_screen_text.get_rect(center=(width // 2, height // 2))

class Flappy(pygame.Rect):
    score = 0
    def __init__(self, x, y, width=40, height=40):
        super().__init__(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load("C:\\Users\\juliu\OneDrive\\Documents\\pywork\\birdy\\ABIRDAJAJAJAJ.png"), (80, 65)) # change to correct file location
        self.dy = 0  
        self.gravity_strength = 1  
        self.jump_strength = -16.3
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, self.rect.width - 25, self.rect.height - 30)

    def draw_bird(self):
        #pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        screen.blit(self.image, self)
    def update(self):
        self.dy += self.gravity_strength  
        self.y += self.dy  
        
        self.rect.x = self.x + 15
        self.rect.y = self.y + 16

        if self.y > ground_rect.y - self.height:  # floor
            return quit() # die
        elif self.y < 0:  # ceiling
            self.y = 0
            self.dy = 0

    def jump(self):
        self.dy = self.jump_strength

    def give_hitbox(self):
        #pygame.draw.rect(screen, WHITE, self.rect) 
        return self.rect

    def update_score(self):
        self.score += 1
        print(self.score)

class Pipe(pygame.Rect):
    gap = 200
    pipes = []
    def __init__(self, x=width, y=height, width=135, height=0):
        super().__init__(x, y, width, height)
        self.dx = -5

    def create_pipe_pair(self):
        self.x = width - self.width
        self.height = height - randint(300, height)
        upper_pipe = pygame.Rect(self.x, 0, self.width, self.height)
        lower_pipe = pygame.Rect(self.x, self.height + self.gap, self.width, height)
        self.pipes.append(lower_pipe)
        self.pipes.append(upper_pipe)

    def draw_pipes(self):
        for pipe in self.pipes:
            pygame.draw.rect(screen, PIPE_COLOR, pipe)
            pygame.draw.rect(screen, BLACK, pipe, 2)

    def move_pipes(self):
        for pipe in self.pipes: # pipes stores (x, y, width, height) as a tuple
            pipe.x += self.dx

def detect_collision(pipe_list, player_rect):
    for pipe in pipe_list:
        if pipe.colliderect(player_rect):
            return True
    else:
        return False

def has_passed_pipe(pipe_list, player_rect):
    global passed_pipes
    for pipe in pipe_list[0::2]:
        if pipe[0] <= player_rect.x and pipe not in passed_pipes:
            passed_pipes.append(pipe)
            return True 
    else:
        return False

bird = Flappy(200, height // 2 - 200)
clock = pygame.time.Clock()

running = True
pre_screen = True
skip_first_pipe_creation = True # i have NO IDEA how to fix the bug of first pipe being a wall othjerwise
pipey = Pipe()
pipey.create_pipe_pair()
frame_count = 0
passed_pipes = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if pre_screen:
                pre_screen = False  
            else:
                bird.jump() 

    if pre_screen:
        screen.fill(SKY_BLUE)
        screen.blit(pre_screen_text, text_rect)
        pygame.display.flip()
        continue  # basicalyl a whiole loop here

    screen.fill(SKY_BLUE)  
    bird.update() 
    bird.draw_bird()  

    if frame_count % 80 == 0:
        if skip_first_pipe_creation:
            skip_first_pipe_creation = False
        else:
            pipey.create_pipe_pair()
    pipey.draw_pipes()  
    pipey.move_pipes()

    frame_count += 1
    if detect_collision(pipey.pipes, bird.rect):
        running = False # die
    
    if has_passed_pipe(pipey.pipes, bird.rect) == True:
        bird.update_score()

    clock.tick(60)

    # draw the ground
    pygame.draw.rect(screen, POOPY_BROWN, ground_rect)
    pygame.draw.rect(screen, BLACK, ground_rect, 2)
    bird.give_hitbox()
    pygame.display.flip()  

pygame.quit()
