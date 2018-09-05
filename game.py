#! -*- coding: utf-8 -*-
import os
import pygame
from pygame.locals import *
import random as Random
import pygame.mixer

from food import Food
from pou import Pou, PlayerXPStatus, PlayerLifeStatus
from pygame.mixer import Sound

class Background:

    image = None
    pos   = None

    def __init__(self, image):

        # image = "./imagens/fundo.png"
        image = pygame.image.load(image).convert()

        self.isize  = image.get_size()
        self.pos    = [0, -1 * self.isize[1]]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        w = (ceil(float(screen_size[0]) / self.isize[0]) + 1) * self.isize[0]
        h = (ceil(float(screen_size[1]) / self.isize[1]) + 1) * self.isize[1]

        back = pygame.Surface((w, h))

        for i in range((back.get_size()[0] / self.isize[0])):
            for j in range((back.get_size()[1] / self.isize[1])):
                back.blit(image, (i * self.isize[0], j * self.isize[1]))

        self.image = back 

    def update(self, dt):
        self.pos[1] += 1
        if (self.pos[1] > 0):
            self.pos[1] -= self.isize[1]

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class Game:
    screen      = None
    screen_size = None
    run         = True
    menu_open   = True
    list        = None
    player      = None
    player_life = None
    player_xp   = None
    background  = None
    img         = None
    som_acerto  = None
    som_erro    = None
    fim         = False
    nivel       = 20


    def __init__(self, size):

        actors = {}
        pygame.init()
        flags = DOUBLEBUF

        self.screen      = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Food Drop') #titulo da janela

        self.load_images()
        #inicializa a biblioteca de som
        pygame.mixer.init()
        #criando objetos de som
        self.som_acerto = pygame.mixer.Sound(os.path.join('snd','mtem.wav'))
        self.som_acerto.set_volume(0.5)

        self.som_erro = pygame.mixer.Sound(os.path.join('snd','game_over.wav'))
        self.som_erro.set_volume(0.5) 


    def load_images(self):
        """
        Lê as imagens necessarias pelo jogo.
        """
        def load_image(filename):
            img = pygame.image.load(os.path.join("imagens", filename))
            img.set_alpha(None, RLEACCEL) # disable alpha.
            img.convert()
            img.set_colorkey(( 255, 0, 255), RLEACCEL) # magenta
            return img

        #self.image_player        = load_image( "pou.png" )
        self.image_player_status = load_image("vidas.png")

    def handle_events(self):

        player = self.player

        for event in pygame.event.get():
            t = event.type
            if t in (KEYDOWN, KEYUP):
                k = event.key

            #sai do jogo
            if t == QUIT:
                self.run = False
                exit(0)

            # o personagem só pode se mover pra direita ou esquerda
            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                    exit(0)
                elif k == K_RIGHT:
                    player.accel_right()
                elif k == K_LEFT:
                    player.accel_left()
                elif k == K_SPACE and self.menu_open:
                    self.menu_open = False

            elif t == KEYUP:
                if   k == K_LEFT:
                    player.accel_right()
                elif k == K_RIGHT:
                    player.accel_left()

    def actors_update(self, dt):
        #self.background.update( dt ) # atualiza imagem de fundo

        for actor in self.list.values(): #atualiza lista de personagens caindo
            actor.update(dt)

        self.player_life.update(dt)
        self.player_xp.update(dt)

    def actors_draw(self):
        self.background.draw(self.screen)
        # self.tela.draw(self.screen)

        for actor in self.list.values():
            actor.draw(self.screen)

        self.player_life.draw(self.screen)
        self.player_xp.draw(self.screen)

    def actor_check_hit(self, actor, list, action):
        if isinstance(actor, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(actor, list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o)
            return hitted

        elif isinstance(actor, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(actor, list, 1):
                if(self.nivel >= 5):
                    if(self.player.get_XP() % 10 == 0):
                        self.nivel = self.nivel - 1
                self.player.set_XP(self.player.get_XP() + 1)
                #reproduz o som de acerto
                self.som_acerto.play()
            return actor.is_dead()

    def actors_act( self ):
        self.actor_check_hit(self.player, self.list["food"], self.player.do_collision)

        if self.player.is_dead():
            self.menu_open = True 
            self.fim = True
            self.nivel = 20
            self.som_erro.play()
            return

    def food_check_pos(self):

        for sprite in self.list["food"].sprites():
            if sprite.is_lost():
                self.list["food"].remove(sprite)
                self.player.set_lives(self.player.get_lives() -1)

    def manage(self):
        # criando mais "foods"
        r = Random.randint( 0, 60 )
        x = Random.randint( 200, 600 )
        # print(r, len(self.list["food"]))
        if (r > (self.nivel * len(self.list["food"]))): # parametro 10 muda a quantidade de comidas
            food = Food([0, 0])
            size  = food.get_size()
            food.set_pos([x , - size[1]])
            self.list["food"].add(food)

    def menu(self):
        self.background = Background('./imagens/menu.png')
        self.background.draw(self.screen)

        img = pygame.image.load("imagens/teste_pou.png").convert_alpha() 
        img = pygame.transform.scale(img, (400, 410))
        self.screen.blit(img, (200, 115))

        if(self.fim):
            self.font = pygame.font.Font(None, 50)
            self.write_on_screen(u'GAME OVER', (0, 0, 0), (290, 60))

            self.font = pygame.font.Font(None, 50)
            self.write_on_screen(u'Pontuação: % 4d' % self.player.get_XP(), (0, 0, 0), (280, 100))
                
            self.font = pygame.font.Font(None, 30)
            self.write_on_screen(u'Pressione <SPACE> para recomeçar!', (0, 0, 0), (235, 560))
        else:          
            self.font = pygame.font.Font(None, 50)
            self.write_on_screen(u'FOOD DROP', (0, 0, 0), (290, 60))

            self.font = pygame.font.Font(None, 30)
            self.write_on_screen(u'Pressione <SPACE> para começar!', (0, 0, 0), (235, 560))


    def write_on_screen(self, text_out, color, position):
		text = self.font.render(text_out, 0, color)
		text_rect = text.get_rect()
		text_rect.move_ip(position)
		self.screen.blit(text, text_rect)

    def loop( self ):

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock         = pygame.time.Clock()
        dt            = 16

        while self.run and self.menu_open:
            clock.tick(1000 / dt)
            
            self.menu()

            self.handle_events()

            pygame.display.flip()


        # Inicia o jogo 

        # Criamos o fundo
        self.background = Background('./imagens/menu.png')

        pos         = [self.screen_size[0] / 2, self.screen_size[1]]
        self.player = Pou(pos, lives=10)

        self.player_life = PlayerLifeStatus(self.player, [5, 5], image=self.image_player_status)
        self.player_xp   = PlayerXPStatus(self.player, [self.screen_size[0] - 100, 5], fgcolor="0xff0000")
        
        self.list = {
            "food"  : pygame.sprite.RenderPlain(Food([Random.randint(200, 600), 0])),
            "player" : pygame.sprite.RenderPlain(self.player),
        }

        # assim iniciamos o loop principal do programa
        while self.run and not self.menu_open:
            clock.tick(1000 / dt)

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.actors_update(dt)

            self.food_check_pos()

            # Faça os atores atuarem
            self.actors_act()

            # Faça a manutenção do jogo, como criar inimigos, etc.
            self.manage()

            # Desenhe para o back buffer
            self.actors_draw()        

            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()


if __name__ == '__main__':
    pygame.mixer.init()
    #importa o arquivo de música de fundo
    pygame.mixer.music.load(os.path.join('snd','Goofy-Mischief.mp3'))
    #informa quantas vezes a música deve tocar seguidamente (-1 reproduz infinitamente)
    pygame.mixer.music.play(-1)
    #define o volume que a música deve reproduzir
    pygame.mixer.music.set_volume(0.5)
    game = Game((800, 600))
    while True:
        game.loop()