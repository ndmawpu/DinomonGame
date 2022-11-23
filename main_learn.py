from random import choice, randint
import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        paimon_run = pygame.image.load('assets/paimon/sticker_6.png').convert_alpha()
        paimon_run = pygame.transform.smoothscale(paimon_run,(100,100))
        paimon_lose = pygame.image.load('assets/paimon/sticker_21.png').convert_alpha()
        paimon_lose = pygame.transform.smoothscale(paimon_lose,(100,100))

        self.paimon_frame = [paimon_run,paimon_lose]
        self.paimon_index = 0 
        self.image = self.paimon_frame[self.paimon_index]
        self.rect = self.image.get_rect(midbottom = (100,379))
        self.paimon_fall = 0

    def player_input(self):
        if game_active:
            keys = pygame.key.get_pressed()
            if keys [pygame.K_SPACE] and self.rect.bottom >= 379:
                self.paimon_fall = -20

    def paimon_animation_state(self):
        if game_active:
            self.paimon_index = 0
            self.image = self.paimon_frame[self.paimon_index]
        else:
            self.paimon_index = 1
            self.image = self.paimon_frame[self.paimon_index]

    def gravity (self):
        if game_active:
            self.paimon_fall += 1
            self.rect.y += self.paimon_fall
            if self.rect.bottom > 379 : self.rect.bottom = 379

    def update (self):
        self.paimon_animation_state()
        self.gravity()
        self.player_input()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type) :
        super().__init__()        
        if type == 'slime':
            slime1 = pygame.image.load('assets/slime/slime.png').convert_alpha()
            slime1 = pygame.transform.smoothscale(slime1,(97,51))
            slime2 = pygame.image.load('assets/slime/slime1.png').convert_alpha()
            slime2 = pygame.transform.smoothscale(slime2,(97,51))
            self.frames = [slime1,slime2]
            y_pos = 259

        elif type == 'snail':
            snail1 = pygame.image.load('assets/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('assets/snail/snail2.png').convert_alpha()
            self.frames = [snail1,snail2]
            y_pos = 379

        elif type == 'fly':
            fly1 = pygame.image.load('assets/fly/fly1.png').convert_alpha()
            fly2 = pygame.image.load('assets/fly/fly2.png').convert_alpha()
            self.frames = [fly1,fly2]
            y_pos = 259
        else :
            grass = pygame.image.load('assets/grass.png').convert_alpha()
            self.frames = [grass]
            y_pos = 379

        self.animation_index = 0
        self.image = self.frames[self.animation_index]        
        self.rect = self.image.get_rect (midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames) : self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100 : 
            self.kill()

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, True):
        obstacle.empty()
        return False 
    else: return True

def floor_animation():
    screen.blit(floor,(floor_x_pos,379))
    screen.blit(floor,(floor_x_pos + 768, 379))

def display_time():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score = current_time
    score_surf = text_font.render(f'score: {score}', True, 'white')
    score_surf_rect = score_surf.get_rect(center = (384,50))
    screen.blit(score_surf,score_surf_rect)

def display_color():
    color1 = pygame.Color(115,90,123,48)
    color2 = pygame.Color(247,191,194,97)
    color3 = pygame.Color(175,139,165,69)
    color4 = pygame.Color(69,41,70,27)
    
    color1_suf = pygame.Surface((20,20))
    color2_suf = pygame.Surface((20,20))
    color3_suf = pygame.Surface((20,20))
    color4_suf = pygame.Surface((20,20))
    
    color1_suf.fill (color1)
    color2_suf.fill (color2)
    color3_suf.fill (color3)
    color4_suf.fill (color4)

    screen.blit(color1_suf,(5,5))
    screen.blit(color2_suf,(30,5))
    screen.blit(color3_suf,(55,5))
    screen.blit(color4_suf,(80,5))

pygame.init()
pygame.display.set_caption('ehe')
screen = pygame.display.set_mode((768,432))
clock = pygame.time.Clock()
game_active = False
start_time = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()

bg = pygame.image.load('assets/background/background2.jpg').convert()
bg = pygame.transform.smoothscale(bg,(768,432))

text_font = pygame.font.Font ('assets/font/TTF/dogicapixelbold.ttf',15)
text_font1 = pygame.font.Font ('assets/font/TTF/dogicapixelbold.ttf',65)
text_surface = text_font.render('dinomon',True, (255,255,255))
text_surface_rect = text_surface.get_rect( topright = (766,5))

paimon_lines = text_font.render('I\'m here to satisfy your Paimonal needs',True, "white")
paimon_lines_rect = paimon_lines.get_rect (center = (384,320))

paimon_intro = pygame.image.load('assets/paimon/sticker_29.png').convert_alpha()
paimon_intro = pygame.transform.smoothscale(paimon_intro,(200,200))
paimon_intro_rect = paimon_intro.get_rect(center = (384,216))

intro_lines = text_font.render('Press SPACE to start', True , 'white')
intro_lines_rect = intro_lines.get_rect (center = (384,112))

lose_lines = text_font1.render('YOU LOSE', True, 'white')
lose_lines_rect = lose_lines.get_rect(center = (384,162))

floor = pygame.image.load('assets/floor1.png').convert_alpha()
floor = pygame.transform.scale(floor,(768,103))
floor_x_pos = 0

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  :
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == obstacle_timer :
                obstacle.add(Obstacle(choice(['grass', 'grass', 'slime', 'snail', 'fly'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)
            
    if game_active:
        screen.blit(bg,(0,0))
        obstacle.draw(screen)
        obstacle.update()
        player.draw(screen)
        player.update()

        pygame.draw.rect(screen, (69,41,70,27), text_surface_rect,0,8)
        screen.blit(text_surface,text_surface_rect)
        display_time()
        display_color()
        floor_animation()

        floor_x_pos -= 7
        if floor_x_pos <= -768: floor_x_pos = 0
        game_active = collision_sprite()
    else:
        if start_time == 0:
            screen.fill('pink')
            screen.blit(paimon_intro,paimon_intro_rect)
            screen.blit(paimon_lines,paimon_lines_rect)
            screen.blit(intro_lines,intro_lines_rect)
        else:
            
            player.clear(screen, bg)
            player.draw(screen)
            player.update()
            start_time = int(pygame.time.get_ticks() / 100)
            screen.blit(lose_lines, lose_lines_rect)
            screen.blit(intro_lines,intro_lines_rect)             
    pygame.display.update()
    clock.tick(60)