import sys
import time
import pygame
import random
import json as js


width = 600
height = 600
white_color = (255, 255, 255)

pygame.init()

# цвета ввода имени игрока
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

FONT = pygame.font.Font(None, 32)

fontObj = pygame.font.Font('freesansbold.ttf', 85)
textSurfaceObj = fontObj.render('BREAK OUT!', True, (255, 255, 0), (0, 0, 0))
textRectObj = textSurfaceObj.get_rect()
textRectObj.topleft = (30, 150)

fontObj1 = pygame.font.Font('freesansbold.ttf', 35)
textSurfaceObj1 = fontObj1.render('Введите имя', True, (100, 100, 100))
textRectObj1 = textSurfaceObj1.get_rect()
textRectObj1.topleft = (30, 250)

clock11 = pygame.time.Clock()

a1 = -610
b1 = -610
a2 = -550
b2 = -530
a3 = -550
b3 = -330
v = 200


class Button:
    # кнопки "Завершение игры" и "Продолжение игры"
    def __init__(self):
         self.button1 = pygame.Rect(70, 400, 250, 75)
         self.button2 = pygame.Rect(300, 400, 250, 75)

    def draw_but(self):
        table = ["Продолжить игру", "Закончить игру"]
        pygame.draw.rect(screen, [0, 255, 0], self.button1)
        pygame.draw.rect(screen, [255, 0, 0], self.button2)
        for i in range(2):
            fontObj = pygame.font.Font('freesansbold.ttf', 20)
            textSurfaceObj = fontObj.render(table[i], True, (0, 0, 0))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.topleft = (80 + 250 * i, 430)
            screen.blit(textSurfaceObj, textRectObj)


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('ball.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = self.WIDTH / 2
        self.rect.centery = self.HEIGHT / 2
        self.speed = [3, 3]

    def update(self):
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        elif self.rect.right >= self.WIDTH or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        self.rect.move_ip(self.speed)


def fill(surface, color):
    # функция заливки картинки определенным цветом
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


class Brick(pygame.sprite.Sprite):
    def __init__(self, position, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('brick_yellow.png')
        if color == 'red':
            fill(self.image, pygame.Color("red"))
        elif color == 'white':
            fill(self.image, pygame.Color("white"))
        elif color == 'ord':
            fill(self.image, pygame.Color("yellow"))
        elif color == 'pink':
            fill(self.image, pygame.Color("pink"))

        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.color = color


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('platform.png')
        self.image = pygame.transform.scale(self.image, (120, 10))
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.midbottom = (self.WIDTH / 2, self.HEIGHT - 20)
        self.speed = [0, 0]

    def update(self, event):
        # перемещения платформы
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-10, 0]
        elif event.key == pygame.K_RIGHT and self.rect.right < self.WIDTH:
            self.speed = [10, 0]
        else:
            self.speed = [0, 0]
        self.rect.move_ip(self.speed)


class Wall(pygame.sprite.Group):
    def __init__(self, number_of_bricks, width):
        self.b = number_of_bricks
        pygame.sprite.Group.__init__(self)
        pos_x = 30
        pos_y = 70

        # разные цвета от которых зависят дополнительные функции
        cols = []
        # красный - увеличение скорости шарика
        cols += ["red"] * 10
        # белый - уменьшение размеров платформы
        cols += ["white"] * 10
        # желтые - дают 10 баллов к счету
        cols += ["yellow"] * 30
        # обычные платформы, за каждую платформу дается 1 балл к счету
        cols += ["ord"] * 99
        # розовые дают дополнительные жизни
        cols += ["pink"] * 2
        random.shuffle(cols)

        for i in range(number_of_bricks):
            color = cols[i]
            brick = Brick((pos_x, pos_y), color)
            self.add(brick)
            pos_x += brick.rect.width
            i += 1
            if i % 13 == 0 and i < 91:
                pos_x = 30
                pos_y += brick.rect.height
            if i == 91 or i == 102 or i == 113:
                pos_x = 70
                pos_y += brick.rect.height
            if i == 124 or i == 133 or i == 142:
                pos_x = 110
                pos_y += brick.rect.height


class Json:
    # раабота с файлом с таблицей результатов
    def __init__(self, path=''):
        self.path = path
        json_data = open(path, 'rb')
        self.connection = js.load(json_data)
        json_data.close()
        self.list = []
        for i in range(1, 4):
            self.list.append(self.connection["Table"][0]["00"+str(i)])

    def write_tojson(self,  Name, Score):

        for i in range(len(self.list)):
           if Score > int(self.list[i][0]["Score"]):
               self.list.insert(i, [{'Name': Name, 'Score': str(Score)}])
               if len(self.list) > 3:
                   del self.list[3]
               break

        write_message = \
            {
                'Table': [
                    {
                     '001':
                     [
                        {
                         'Name': self.list[0][0]["Name"],
                         'Score': self.list[0][0]["Score"]
                        }
                     ],
                     '002':
                     [
                        {
                         'Name': self.list[1][0]["Name"],
                         'Score': self.list[1][0]["Score"]
                        }
                     ],
                     '003':
                     [
                        {
                         'Name': self.list[2][0]["Name"],
                         'Score': self.list[2][0]["Score"]
                        }
                     ]
                    }
                ]

            }

        with open(self.path, 'w') as file:
            js.dump(write_message, file, indent=2, ensure_ascii=False)
        file.close()


class InputBox:
    # ввод имени игрока
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYUP:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += pygame.key.name(event.key)
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def game_over():
    # заставка "Game Over"
    global a1, a2, a3, b1, b2, b3

    if a1 < 0:
        con = v * clock.tick() / 1000
    else:
        screen.fill((0, 0, 0))
        con = 0
        a1 = -610
        b1 = -610
        a2 = -550
        b2 = -530
        a3 = -550
        b3 = -330
        return False

    a1 += con
    b1 += con
    a2 += con
    b2 += con
    a3 += con
    b3 += con

    pygame.draw.rect(screen, (0, 0, 0), (a1, b1, 620, 620))

    font = pygame.font.Font(None, 200)
    text1 = font.render("GAME", 1, (255, 0, 0))
    screen.blit(text1, (a2, b2))

    font2 = pygame.font.Font(None, 200)
    text2 = font2.render("OVER", 1, (255, 0, 0))
    screen.blit(text2, (a3, b3))

    pygame.display.flip()
    return True


def show_score(score):
    font_score = pygame.font.SysFont('Consolas', 20)
    text_score = font_score.render(str(score).zfill(5), True, white_color)
    text_score_rect = text_score.get_rect()
    text_score_rect.topleft = [32, 30]

    font_title = pygame.font.SysFont('Consolas', 25)
    text_title = font_title.render('SCORE', True, white_color)
    text_title_rect = text_title.get_rect()
    text_title_rect.topleft = [10, 10]

    screen.blit(text_score, text_score_rect)
    screen.blit(text_title, text_title_rect)


def show_lives(lives):
    font = pygame.font.SysFont('Consolas', 25)
    text = font.render(str(lives), True, white_color)
    text_rect = text.get_rect()
    text_rect.topleft = [width - 60, 15]

    heart = pygame.image.load('heart.png')
    heart_rect = heart.get_rect()
    heart_rect.topright = [width - 10, 10]

    screen.blit(text, text_rect)
    screen.blit(heart, heart_rect)


def print_table():
    # печать таблицы результатов(3 лучших результата)
    table = ""

    for i in range(3):
        table = json_work.list[i][0]["Score"] + " "
        table += json_work.list[i][0]["Name"]

        fontObj = pygame.font.Font('freesansbold.ttf', 20)
        textSurfaceObj = fontObj.render(table, True, (255, 255, 0))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (150, 100 + 50*i)
        screen.blit(textSurfaceObj, textRectObj)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
pygame.key.set_repeat(30)
json_work = Json('settings.json')

input_box1 = InputBox(30, 290, 140, 32)
enter = False
Nameof = None


def start_game():
    # начало и продолжение игры
    ball = Ball(width, height)
    paddle = Paddle(width, height)
    wall = Wall(151, width)
    Game = True
    score = 0
    lives = 7

    waiting = True
    global enter, Nameof

    while Game:
        clock.tick(60)

        while not enter:
                for event in pygame.event.get():
                    input_box1.handle_event(event)

                input_box1.update()

                screen.fill((30, 30, 30))

                input_box1.draw(screen)

                screen.blit(textSurfaceObj, textRectObj)
                screen.blit(textSurfaceObj1, textRectObj1)
                pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Nameof = input_box1.text
                        enter = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                paddle.update(event)
                if waiting and event.key == pygame.K_SPACE:
                    waiting = False
                    if ball.rect.centerx < width / 2:
                        ball.speed = [3, -3]
                    else:
                        ball.speed = [-3, -3]

        if waiting:
            ball.rect.midbottom = paddle.rect.midtop
        else:
            ball.update()

        if pygame.sprite.collide_rect(ball, paddle):
            ball.speed[1] = -ball.speed[1]

        collided_list = pygame.sprite.spritecollide(ball, wall, False)
        if collided_list:
            brick = collided_list[0]
            cx = ball.rect.centerx
            if cx < brick.rect.left or cx > brick.rect.right:
                ball.speed[0] = -ball.speed[0]
            else:
                ball.speed[1] = -ball.speed[1]

            if brick.color == 'red':
                if ball.speed[0] > 0:
                    ball.speed[0] += 0.4
                    ball.speed[1] -= 0.4
                else:
                    ball.speed[0] -= 0.4
                    ball.speed[1] += 0.4

            elif brick.color == 'white':
                z = paddle.image.get_rect()[2] - 10
                if z >= 60:
                    paddle.image = pygame.transform.scale(paddle.image,
                                                          (z, 10))
                    paddle.rect[2] = z
                else:
                    paddle.image = pygame.image.load('images/platform.png')
                    paddle.image = pygame.transform.scale(paddle.image,
                                                          (120, 10))
                    paddle.rect[2] = 120

            elif brick.color == 'yellow':
                score += 10

            elif brick.color == 'pink':
                lives += 1

            wall.remove(brick)
            wall.b -= 1
            if wall.b == 0:
                wall = Wall(151, width)
            score += 1
        else:
            collided_list = pygame.sprite.spritecollide(ball, wall, False)

        if ball.rect.top > height:
            lives -= 1
            waiting = True

        screen.fill((0, 0, 0))
        show_score(score)
        show_lives(lives)

        screen.blit(ball.image, ball.rect)
        screen.blit(paddle.image, paddle.rect)
        wall.draw(screen)
        pygame.display.flip()

        if lives <= 0:
            Game = False
            json_work.write_tojson(Nameof, score)

    while not Game:
        value = game_over()
        if value:
            pass
        else:
            return


def cont_game():
    button = Button()
    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            print_table()
            button.draw_but()
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button.button1.collidepoint(mouse_pos):
                    return True
                if button.button2.collidepoint(mouse_pos):
                    return False


Play = True
while Play:
    start_game()
    Play = cont_game()
