import os
import pygame as pg
import sys
import math

def load_png(name):
    fullname = os.path.join(name)
    try:
        image = pg.image.load(fullname)
        if image.get_alpha == None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()

class Cannonball(pg.sprite.Sprite):

    def __init__(self, xvel, yvel):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("cannonball.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.xvel = xvel
        self.yvel = yvel
        self.allx = []
        self.ally = []

    def update(self):
        position = self.physics(self.rect)
        self.rect = position
        self.allx.append(self.rect.centerx)
        self.ally.append(self.rect.centery)
        if self.rect.centery >= 800:
            self.rect.centery = 800
            self.xvel = 0
            self.yvel = 0
            global velx, vely
            velx.text = str(self.stats()[0] * 100 // 1 / 2000)
            vely.text = str(self.stats()[1] * 100 // 1 / 2000)

    def physics(self, rect):
        self.yvel += 9.8 / 20
        return rect.move((self.xvel / 20), (self.yvel / 20))
    
    def stats(self):
        return ((max(self.allx) - min(self.allx)) / 20, (max(self.ally) - min(self.ally)) / 20)

    def fire(self, xv, yv):
        self.allx = []
        self.ally = []
        self.rect.x = cannon.rect.x + 80
        self.rect.y = cannon.rect.y
        self.xvel = xv * 20
        self.yvel = yv * 20

class Cannon(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("cannon.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
    
    def create_ball(self, xv, yv):
        global ball
        ball.fire(xv, yv)

class Stand (pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("cannonstand.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()

class Button(pg.sprite.Sprite):

    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(name)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()

    def press_action():
        return None

class Launch(Button):
    
    def __init__(self):
        super().__init__("launch.png")

    def press_action(self):
        global lvel, lang
        cannon.create_ball(int(lvel.text) * math.cos(math.radians(int(lang.text))), int(lvel.text) * -1 * math.sin(math.radians(int(lang.text))))

class TextBox(pg.Rect):
    def __init__(self, xpos, ypos, text):
        pg.Rect.__init__(self, xpos, ypos, 200, 100)
        self.color_passive = pg.Color("azure3")
        self.color_active = pg.Color("aquamarine")
        self.color = self.color_passive
        self.text = text
        self.active = False

    def correction(self):
        try:
            j = int(self.text)
            j + 1
        except ValueError:
            self.text == 'Error'

def main():
    pg.init()
    screen = pg.display.set_mode((1600, 900))
    pg.display.set_caption("Projectile Motion Simulation")

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((135, 206, 235))

    screen.blit(background, (0, 0))
    f = pg.image.load("floor.png")
    screen.blit(f, (0, 800))
    pg.display.flip()

    base_font = pg.font.Font(None, 32)

    global cannon
    cannon = Cannon()
    stand = Stand()
    cannon.rect.x = 100
    cannon.rect.y= 740
    stand.rect.x = cannon.rect.x
    stand.rect.y = cannon.rect.y + 30

    global ball
    ball = Cannonball(0, 0)
    ball.rect.centerx = 800
    ball.rect.centery = 800

    global launch
    launch = Launch()
    launch.rect.x = 300
    launch.rect.y = 800

    global lvel, lang
    lvel = TextBox(1350, 50, "10")
    lang = TextBox(1350, 200, "45")
    global velx, vely
    velx = TextBox(1350, 350, "0")
    vely = TextBox(1350, 500, "0")
    active = None

    standsprite = pg.sprite.RenderPlain(stand)
    cannonsprite = pg.sprite.RenderPlain(cannon)
    ballsprite = pg.sprite.RenderPlain(ball)
    launchsprite = pg.sprite.RenderPlain(launch)

    clock = pg.time.Clock()

    while True:
        clock.tick(20)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            position = pg.mouse.get_pos()

            if event.type == pg.MOUSEBUTTONUP:
                if launch.rect.collidepoint(position):
                    if ball.yvel == 0 and ball.xvel == 0:
                        launch.press_action()
                if lvel.collidepoint(position):
                    if ball.yvel == 0 and ball.xvel == 0:
                        lvel.active = True
                        lvel.color = lvel.color_active
                        lang.active = False
                        lang.color = lang.color_passive
                        lang.correction()
                        active = lvel
                if lang.collidepoint(position):
                    if ball.yvel == 0 and ball.xvel == 0:
                        lang.active = True
                        lang.color = lang.color_active
                        lvel.active = False
                        lvel.color = lvel.color_passive
                        lvel.correction()
                        active = lang
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    active.text = active.text[:-1]
                elif event.key == pg.K_KP_ENTER:
                    active.correction()
                    active = None
                else:
                    active.text += event.unicode

        screen.blit(background, ball.rect)
        screen.blit(background, cannon.rect)
        screen.blit(background, stand.rect)
        screen.blit(f, (0, 800))

        if ball.xvel != 0 and ball.yvel != 0:
            ball.update()
            velx.text = str((ball.xvel * 100 // 1) / 2000)
            vely.text = str((ball.yvel * 100 // 1) / 2000)

        for l in (lvel, lang, velx, vely):
            pg.draw.rect(screen, l.color, l)
            text_surface = base_font.render(l.text, True, (0, 0, 0))
            screen.blit(text_surface, (l.x + 5, l.y + 5))
            text_surface = base_font.render("m/s", True, (0,0,0)) if l != lang else base_font.render("degrees", True, (0,0,0))
            if ball.xvel == 0 and ball.yvel == 0 and (l == velx or l == vely):
                text_surface = base_font.render("m", True, (0,0,0))
            screen.blit(text_surface, (l.x + 100, l.y + 5))

        text_surface = base_font.render("Launch Velocity", True, (0,0,0))
        screen.blit(text_surface, (lvel.x + 5, lvel.y + 50))
        text_surface = base_font.render("Launch Angle", True, (0,0,0))
        screen.blit(text_surface, (lang.x + 5, lang.y + 50))  
        text_surface = base_font.render("X Velocity", True, (0,0,0)) if (ball.xvel != 0 and ball.yvel != 0) else base_font.render("Distance Traveled", True, (0,0,0))
        screen.blit(text_surface, (velx.x + 5, velx.y + 50))
        text_surface = base_font.render("Y Velocity", True, (0,0,0)) if (ball.xvel != 0 and ball.yvel != 0) else base_font.render("Max Height", True, (0,0,0))
        screen.blit(text_surface, (vely.x + 5, vely.y + 50))

        cannonsprite.update()        
        cannonsprite.draw(screen)
        standsprite.update()
        standsprite.draw(screen)
        launchsprite.update()
        launchsprite.draw(screen)
        ballsprite.update()
        ballsprite.draw(screen)
        pg.display.flip()

if __name__ == '__main__': main()


