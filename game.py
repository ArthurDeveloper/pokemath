import pygame
import random
import time

# Initializing pygame
pygame.init()

class Game:
    def __init__(self):
        self.level = 0
        self.score = 0

        # Reads high score from high_score.txt
        with open('high_score.txt') as f:
            self.high_score = int(f.read())

        self.setup()

    # Setting up all variables
    def setup(self):
        self.screen = pygame.display.set_mode((640, 680))
        self.bg = (0, 100, 100)

        with open('max_random.txt', 'r') as f:
            def clamp(val, min, max):
                if val < min:
                    val = min
                if val > max:
                    val = max

                return val

            contents = f.read().split('\n') 
            self.max_random_a = clamp(int(contents[0]), 0, 9)
            self.max_random_b = clamp(int(contents[1]), 0, 9)
            self.numbers = [0, 0, 0]

        # The pokeball is the hidden square
        self.pokeball_idx = random.randint(0, 1) if self.level < 6 else random.randint(0, 2)
        
        self.a = random.randint(0, self.max_random_a)
        self.b = random.randint(0, self.max_random_b)
        with open('op.txt', 'r') as f:
            # Can be +, -, : or x
            self.operation = f.read().strip() 

        match self.operation:
            case '+':
                self.c = self.a + self.b
            case '-':
                while self.a < self.b:
                    self.a = random.randint(0, self.max_random_a)
                    self.b = random.randint(0, self.max_random_b)
                self.c = self.a - self.b
            case ':':
                while self.a < self.b or self.a == 0 or self.b == 0 or self.a % self.b != 0:
                    self.a = random.randint(0, self.max_random_a)
                    self.b = random.randint(0, self.max_random_b)

                self.c = self.a // self.b
            case 'x':
                while self.a < self.b or self.a == 0 or self.b == 0 or self.a % self.b != 0:
                    self.a = random.randint(0, self.max_random_a)
                    self.b = random.randint(0, self.max_random_b)

                self.c = self.a * self.b
        

        self.numbers = [self.a, self.b, self.c]

        self.squares = [pygame.image.load(f'res/square_{i if i <= 9 else 9}.png') for i in self.numbers]                          

        self.squares[self.pokeball_idx] = pygame.image.load('res/pokeball.png')

        self.font = pygame.font.Font("res/PublicSans-VariableFont_wght.ttf", 128)
        # The number the user is typing, u'' makes it null
        self.typed_number = u''

        self.has_tried = False
        self.correct = False         

        with open('times.txt', 'r') as f:
            # Gets all the times and removes \n's (linebreaks)
            self.times = [v.strip() for v in f.read().split('\n')]
            # Seeings if the numbers are valid and replacing them with other values if they ain't valid
            def validate(v):
                try:
                    millis = int(v)*1000
                    if millis <= 0:
                        millis = 0
                    return millis
                except:
                    return 15000

            for idx, time in enumerate(self.times):
                self.times[idx] = validate(time)


        if self.level > 0:
            self.initial_time = self.time = self.times[self.level]
        else:
            # Using same time as level one for level zero
            self.initial_time = self.time = self.times[0]

        print(f'{self.a}, {self.b}, {self.c}')


      
    def change_high_score(self, new_hs):
        self.high_score = new_hs
        with open('high_score.txt', 'w') as f:
            f.write(str(new_hs))


    def loop(self):
        running = True
        game_over = False
        clock = pygame.time.Clock()
        while running:
            clock.tick()

            if game_over:
                # Shows game over message
                self.screen.fill(self.bg)
                font = pygame.font.Font('res/PublicSans-VariableFont_wght.ttf', 96)
                game_over_txt = font.render('GAME OVER!', True, (255, 0, 0))
                self.screen.blit(game_over_txt, (640/2-280, 660/2-70))
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                continue


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # If the player typed a number, show it, otherwise, if the player typed return,
                    # submit, otherwise, if the player typed backspace, remove a number, otherwise,
                    # do nothing
                    try:
                        int(event.unicode)    
                        self.typed_number += event.unicode
                    except ValueError:
                        if event.key == pygame.K_RETURN:
                            self.has_tried = True
                            match self.pokeball_idx:
                                case 0:
                                    if int(self.typed_number) == self.a:
                                        self.correct = True
                                    else:
                                        self.correct = False
                                case 1:
                                    if int(self.typed_number) == self.b:
                                        self.correct = True
                                    else:
                                        self.correct = False
                                case 2:
                                    if int(self.typed_number) == self.c:
                                        self.correct = True
                                    else:
                                        self.correct = False


                        elif event.key == pygame.K_BACKSPACE:
                            idx = len(self.typed_number)-1
                            self.typed_number = self.typed_number[:idx] + self.typed_number[idx+1:]

                   

            # Rendering squares
            self.screen.fill(self.bg)
            for square in self.squares:
                index = self.squares.index(square)
                if (index == 2):
                    break
                self.screen.blit(square, 
                    (640/2-177/2-175 if index == 0 else 640/2+177/2, 
                     228)
                )

            self.screen.blit(self.squares[2], (
                640/2-177/2, 100
            ))

            # Drawing the number the user typed
            self.font.size('32')
            font_img = self.font.render(self.typed_number, True, (255, 255, 255))
            self.screen.blit(font_img, (640/2-30, 470))

            # Drawing some advices
            small_font = pygame.font.Font('res/PublicSans-VariableFont_wght.ttf', 32)
            font_img = small_font.render('Press Enter to submit', True, (255, 255, 255))
            self.screen.blit(font_img, (640/2-150, 620))

            # Rendering small ui elements (score , high score and level)
            ui_font = pygame.font.Font("res/PublicSans-VariableFont_wght.ttf", 32)
            
            font_img = ui_font.render(f'Your score: {self.score}', True, (255, 255, 255))
            self.screen.blit(font_img, (0, 60))

            font_img = ui_font.render(f'High score: {self.high_score}', True, (255, 255, 255))
            self.screen.blit(font_img, (450, 0))

            font_img = ui_font.render(f'Function: {self.operation}', True, (255, 255, 255))
            self.screen.blit(font_img, (450, 60))

            # Checking if the user wrote the correct answer
            if self.has_tried:
                if self.correct:
                    font_img = small_font.render('CORRECT !', True, (0, 230, 50))
                    self.screen.blit(font_img, (640/2-50, 640))
                    pygame.display.flip()
                    # Reseting the screen and changing the score (and level if needed)
                    time.sleep(1)
                    self.score += 1
                    # Level up if player is not on level 10 yet
                    if self.score % 10 == 0 and self.level < 10:
                        self.level += 1

                    # Changing high score if it has been beaten
                    self.change_high_score(self.score)

                    self.setup()

                else:
                    font_img = small_font.render('FOUT !', True, (255, 0, 0))
                    self.screen.blit(font_img, (640/2-50, 640))
                    pygame.display.flip()
                    # Reseting the screen and ending the game
                    time.sleep(1)
                    game_over = True

            font_img = small_font.render(f'Level: {self.level}', True, (255, 255, 255))
            self.screen.blit(font_img, (20, 20))

            self.time -= clock.get_rawtime()

            timer_rect = pygame.Rect(0, 400, 700*(self.time/self.initial_time), 20)

            pygame.draw.rect(self.screen, (255, 0, 0), timer_rect)

            if self.time <= 0:
                game_over = True
                continue

            pygame.display.flip()

Game().loop()
