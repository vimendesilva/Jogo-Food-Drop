#!/usr/bin/env python2.3
# -*- coding: utf-8 -*-

import os, sys, copy
import getopt
import pygame
from pygame.locals import *
import random as Random

images_dir = os.path.join( "", "imagens" )

cont = 0

class Jogo( pygame.sprite.Sprite ):

    def __init__( self, image, position, speed=None ):
        pygame.sprite.Sprite.__init__( self )
        self.image = image
        if isinstance( self.image, str ):
            self.image = os.path.join( images_dir, self.image )
            self.image = pygame.image.load( self.image )

        self.rect  = self.image.get_rect()
        screen     = pygame.display.get_surface()
        self.area  = screen.get_rect()

        self.set_pos( position )
        self.set_speed( speed or ( 0, 2 ) )

        self.cont = 0
    # __init__()



    def update( self, dt ):
        global cont
        move_speed = ( self.speed[ 0 ] * dt / 16, self.speed[ 1 ] * dt / 16 )
        self.rect  = self.rect.move( move_speed )
        if ( self.rect.left > self.area.right ) or ( self.rect.top > self.area.bottom ) or ( self.rect.right < 0 ):
            print('oi')
            cont += 1
            print(cont)
            if(cont == 3):
            # self.player.get_XP(self.player.get_XP() + 1)
                self.kill()
        if ( self.rect.bottom < - 40 ):
            self.kill()
    # update()



    def get_speed( self ):
        return self.speed
    # get_speed()



    def set_speed( self, speed ):
        self.speed = speed
    # set_speed()



    def get_pos( self ):
        return ( self.rect.center[ 0 ],
                 self.rect.bottom )
    # get_pos()



    def set_pos( self, pos ):
        self.rect.center = ( pos[ 0 ], pos[ 1 ] )
    # get_pos()



    def get_size( self ):
        return self.image.get_size()
    # get_size()




class Ship( Jogo ):
    global cont 
    print(cont)
    def __init__( self, position, lives=0, speed=[ 0, 0 ], image=None ):
        self.acceleration = [ 3, 3 ]
        if not image:
            image = "tomate.png"
        Jogo.__init__( self, image, position, speed )
        self.set_lives( lives )
    # __init__()



    def get_lives( self ):
        return self.lives
    # get_lives()



    def set_lives( self, lives ):
        self.lives = lives
    # set_lives()



    def do_collision( self ):
        if self.get_lives() == 0:
            self.kill()
        else:   
            pass   
            # self.player.get_XP(self.player.get_XP() + 1)
            # self.set_lives( self.get_lives() - 1 )
    # do_collision()



    def is_dead( self ):
        return self.get_lives() == 0
    # is_dead()



    def accel_left( self ):
        speed = self.get_speed()
        self.set_speed( ( speed[ 0 ] - self.acceleration[ 0 ], speed[ 1 ] ) )
    # accel_left



    def accel_right( self ):
        speed = self.get_speed()
        self.set_speed( ( speed[ 0 ] + self.acceleration[ 0 ], speed[ 1 ] ) )
    # accel_right
# Ship



class Amigo( Ship ):
    def __init__( self, position, lives=0, speed=None, image=None ):
        if not image:
            image = "doce.png"
        Ship.__init__( self, position, lives, speed, image )



class Inimigo( Ship ):
    def __init__( self, position, lives=0, speed=None, image=None ):
        if not image:
            image = "tomate.png"
        Ship.__init__( self, position, lives, speed, image )




class Player( Ship ):

    def __init__( self, position, lives=10, image=None ):
        if not image:
            image = "pou.png"
        Ship.__init__( self, position, lives, [ 0, 0 ], image )
        self.set_XP( 0 )
    # __init__()



    def update( self, dt ):
        move_speed = ( self.speed[ 0 ] * dt / 16,
                       self.speed[ 1 ] * dt / 16)
        self.rect  = self.rect.move( move_speed )

        if ( self.rect.right > self.area.right ):
            self.rect.right = self.area.right

        elif ( self.rect.left < 0 ):
            self.rect.left = 0

        if ( self.rect.bottom > self.area.bottom ):
            self.rect.bottom = self.area.bottom

        elif ( self.rect.top < 0 ):
            self.rect.top = 0
    # update()



    def get_pos( self ):
        return ( self.rect.center[ 0 ], self.rect.top )
    # get_pos()



    def get_XP( self ):
        return self.XP
    # get_XP()



    def set_XP( self, XP ):
        self.XP = XP
    # get_XP()
# Player

class PlayerXPStatus:
    """
    Esta classe representa a experiência do usuário
    """
    font    = None
    last_xp = -1
    fgcolor = None
    bgcolor = None
    image   = None

    def __init__( self, player, pos=None, font=None, ptsize=30,
                  fgcolor="0xffff00", bgcolor=None ):
        self.player  = player
        self.fgcolor = pygame.color.Color( fgcolor )
        if bgcolor:
            self.bgcolor = pygame.color.Color( bgcolor )
        self.pos     = pos or [ 0, 0 ]
        self.font    = pygame.font.Font( font, ptsize )

        self.last_rect = None
    # __init__()

    def update( self, dt ):
        pass
    # update()

    def draw( self, screen ):
        text = "XP: % 4d" % self.player.get_XP()
        if self.bgcolor:
            self.image = self.font.render( text, False, self.fgcolor,
                                           self.bgcolor )
        else:
            self.image = self.font.render( text, False, self.fgcolor,
                                           ( 255, 0, 255 ) )
            self.image.set_colorkey( ( 255, 0, 255 ), RLEACCEL )

        self.last_rect = Rect( self.pos, self.image.get_size() )

        screen.blit( self.image, self.pos )

    # draw()


    def clear( self, screen, background ):
        if self.last_rect:
            screen.blit( background, self.last_rect )
    # clear()
# PlayerXPStatus


class PlayerLifeStatus:
    """
    Esta classe representa o contador de vidas do jogador
    """
    player     = None
    pos        = None
    image      = None
    size_image = None
    spacing    = 5
    def __init__( self, player, pos=None, image=None ):
        self.image = image or "vidas.png"
        if isinstance( self.image, str ):
            self.image = os.path.join( images_dir, self.image )
            self.image = pygame.image.load( self.image )

        self.player     = player
        self.pos        = pos or [ 5, 5 ]
        self.size_image = self.image.get_size()
        self.last_rect  = None
    # __init__()



    def update( self, dt ):
        pass
    # update()



    def draw( self, screen ):
        pos = copy.copy( self.pos )
        for i in range( self.player.get_lives() ):
            pos[ 0 ] += self.size_image[ 0 ] + self.spacing
            screen.blit( self.image, pos )

        pos[ 1 ] = self.size_image[ 1 ]
        self.last_rect = Rect( self.pos, pos )
    # draw()


    def clear( self, screen, background ):
        if self.last_rect:
            screen.blit( background, self.last_rect )
    # clear()
# PlayerLifeStatus

class Menu:

    
    image = None
    pos   = None

    def __init__( self, image="tile.png" ):

        if isinstance( image, str ):
            image = os.path.join( images_dir, image )
            image = pygame.image.load( image ).convert()

        self.isize = image.get_size()
        self.pos = [ 0, -1 * self.isize[ 1 ] ]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        w = ( ceil( float( screen_size[ 0 ] ) / self.isize[ 0 ] ) + 1 ) * \
            self.isize[ 0 ]
        h = ( ceil( float( screen_size[ 1 ] ) / self.isize[ 1 ] ) + 1 ) * \
            self.isize[ 1 ]

        back = pygame.Surface( ( w, h ) )

        for i in range( ( back.get_size()[ 0 ] / self.isize[ 0 ] ) ):
            for j in range( ( back.get_size()[ 1 ] / self.isize[ 1 ] ) ):
                back.blit( image, ( i * self.isize[ 0 ], j * self.isize[ 1 ] ) )

        self.image = back
    # __init__()



    def update( self, dt ):
        self.pos[ 1 ] += 1
        if ( self.pos[ 1 ] > 0 ):
            self.pos[ 1 ] -= self.isize[ 1 ]
    # update()



    def draw( self, screen ):
        screen.blit( self.image, self.pos )
    # draw()

class Background:

    image = None
    pos   = None

    def __init__( self, image="tile.png" ):

        if isinstance( image, str ):
            image = os.path.join( images_dir, image )
            image = pygame.image.load( image ).convert()

        self.isize = image.get_size()
        self.pos = [ 0, -1 * self.isize[ 1 ] ]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        w = ( ceil( float( screen_size[ 0 ] ) / self.isize[ 0 ] ) + 1 ) * \
            self.isize[ 0 ]
        h = ( ceil( float( screen_size[ 1 ] ) / self.isize[ 1 ] ) + 1 ) * \
            self.isize[ 1 ]

        back = pygame.Surface( ( w, h ) )

        for i in range( ( back.get_size()[ 0 ] / self.isize[ 0 ] ) ):
            for j in range( ( back.get_size()[ 1 ] / self.isize[ 1 ] ) ):
                back.blit( image, ( i * self.isize[ 0 ], j * self.isize[ 1 ] ) )

        self.image = back
    # __init__()



    def update( self, dt ):
        self.pos[ 1 ] += 1
        if ( self.pos[ 1 ] > 0 ):
            self.pos[ 1 ] -= self.isize[ 1 ]
    # update()



    def draw( self, screen ):
        screen.blit( self.image, self.pos )
    # draw()
# Background




class Game:
    screen      = None
    screen_size = None
    run         = True
    lista       = None
    player      = None
    player_life = None
    player_xp   = None
    background  = None
    tela        = None

    def __init__( self, size, fullscreen ):

        actors = {}
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen       = pygame.display.set_mode( size, flags )
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Jogo' ) #titulo da janela

        self.load_images()
    # init()

    def load_images( self ):
        """
        Lê as imagens necessarias pelo jogo.
        """
        def load_image( filename ):
            img = pygame.image.load( os.path.join( images_dir, filename ) )
            img.set_alpha( None, RLEACCEL ) # disable alpha.
            img.convert()
            img.set_colorkey( ( 255, 0, 255 ), RLEACCEL ) # magenta
            return img
        # load_image()

        #self.image_player        = load_image( "pou.png" )
        self.image_player_status = load_image( "vidas.png" )

    # load_images()



    def handle_events( self ):

        player = self.player

        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key

            #sai do jogo
            if t == QUIT:
                self.run = False

            #o personagem só pode se mover pra direita ou esquerda
            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_RIGHT:
                    player.accel_right()
                elif k == K_LEFT:
                    player.accel_left()
                

            elif t == KEYUP:
                if k == K_LEFT:
                    player.accel_right()
                elif k == K_RIGHT:
                    player.accel_left()
                    
    # handle_events()


    def actors_update( self, dt ):
        #self.background.update( dt ) # atualiza imagem de fundo

        for actor in self.lista.values(): #atualiza lista de personagens caindo
            actor.update( dt )

        self.player_life.update( dt )
        self.player_xp.update( dt )


    def actors_draw( self ):
        self.background.draw( self.screen )
        self.tela.draw( self.screen )

        for actor in self.lista.values():
            actor.draw( self.screen )

        self.player_life.draw( self.screen )
        self.player_xp.draw( self.screen )



    def actor_check_hit( self, actor, lista, action ):
        if   isinstance( actor, pygame.sprite.RenderPlain ):
            hitted = pygame.sprite.groupcollide( actor, lista, 1, 0 )
            for v in hitted.values():
                for o in v:
                    action( o )
            return hitted

        elif isinstance( actor, pygame.sprite.Sprite ):
            if pygame.sprite.spritecollide( actor, lista, 1 ):
                # action()
                self.player.set_XP( self.player.get_XP() + 1 )
            return actor.is_dead()
    # actor_check_hit()



    def actors_act( self ):
        self.actor_check_hit( self.player, self.lista[ "amigos" ], self.player.do_collision )
        self.actor_check_hit( self.player, self.lista[ "inimigos" ], self.player.do_collision )
        if self.player.is_dead():
            self.run = False
            return


    def manage( self ):
        # criando mais "amigos"
        r = Random.randint( 0, 50 )
        x = Random.randint( 200, 600 )
        # x = Random.randint( 1, self.screen_size[ 0 ] / 20 )
        if ( r > ( 40 * len( self.lista[ "amigos" ] ) ) ):
            amigo = Amigo( [ 0, 0 ] )
            size  = amigo.get_size()
            amigo.set_pos( [ x , - size[ 1 ] ] )
            self.lista[ "amigos" ].add( amigo )

        # criando mais "inimigos"
        r = Random.randint( 0, 50 )
        x = Random.randint( 200, 600 )
        if ( r > ( 40 * len( self.lista[ "inimigos" ] ) ) ):
            inimigo = Inimigo( [ 0, 0 ] )
            size  = inimigo.get_size()
            inimigo.set_pos( [ x , - size[ 1 ] ] )
            self.lista[ "inimigos" ].add( inimigo )


    def loop( self ):

        # Criamos o fundo
        self.background = Background( "fundo.png" )

        self.tela = Menu ("azul.png");

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock         = pygame.time.Clock()
        dt            = 16

        pos         = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] ]
        self.player = Player( pos, lives=10  )

        self.player_life = PlayerLifeStatus( self.player, [ 5, 5 ],
                                             image=self.image_player_status )
        self.player_xp   = PlayerXPStatus( self.player,
                                           [ self.screen_size[ 0 ] - 100, 5 ],
                                           fgcolor="0xff0000" )
        self.lista = {
            "amigos" : pygame.sprite.RenderPlain( Amigo( [Random.randint( 200, 600 ), 0] ) ),
            "inimigos" : pygame.sprite.RenderPlain( Inimigo( [Random.randint( 200, 600 ), 0] ) ),
            "player" : pygame.sprite.RenderPlain( self.player ),

            }


        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.actors_update( dt )

            # Faça os atores atuarem
            self.actors_act()

            # Faça a manutenção do jogo, como criar inimigos, etc.
            self.manage()

            # Desenhe para o back buffer
            self.actors_draw()

            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            # print "FPS: %0.2f" % clock.get_fps()
        # while self.run
    # loop()
# Game

class Teste:
    screen      = None
    screen_size = None
    run         = True
    player      = None
    background  = None

    def __init__( self, size, fullscreen ):

        actors = {}
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen       = pygame.display.set_mode( size, flags )
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Jogo' ) #titulo da janela

        self.load_images()
    # init()

    def load_images( self ):
        """
        Lê as imagens necessarias pelo jogo.
        """
        def load_image( filename ):
            img = pygame.image.load( os.path.join( images_dir, filename ) )
            img.set_alpha( None, RLEACCEL ) # disable alpha.
            img.convert()
            img.set_colorkey( ( 255, 0, 255 ), RLEACCEL ) # magenta
            return img
        # load_image()

        #self.image_player        = load_image( "pou.png" )
        # self.image_player_status = load_image( "vidas.png" )

    # load_images()



    def handle_events( self ):

        player = self.player

        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key

            #sai do jogo
            if t == QUIT:
                # self.run = False
                # "fullscreen":  False,
                # "resolution": ( 800, 600 ),
                game = Game( ( 800, 600 ), False )
                game.loop()

            #o personagem só pode se mover pra direita ou esquerda
            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_RIGHT:
                    player.accel_right()
                elif k == K_LEFT:
                    player.accel_left()
                

            elif t == KEYUP:
                if k == K_LEFT:
                    player.accel_right()
                elif k == K_RIGHT:
                    player.accel_left()
                    
    

    def actors_draw( self ):
        self.background.draw( self.screen )
        


    def loop( self ):

        # Criamos o fundo
        self.background = Menu( "azul.png" )

        # self.tela = Menu ("azul.png")

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock         = pygame.time.Clock()
        dt            = 16

        pos         = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] ]
        self.player = Player( pos, lives=10  )

       
        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )

            # Handle Input Events
            self.handle_events()

            # # Atualiza Elementos
            # self.actors_update( dt )

            # # Faça os atores atuarem
            # self.actors_act()

            # # Faça a manutenção do jogo, como criar inimigos, etc.
            # self.manage()

            # Desenhe para o back buffer
            self.actors_draw()

            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            # print "FPS: %0.2f" % clock.get_fps()
        # while self.run
    # loop()
# Game


def usage():
    """
    Imprime informações de uso deste programa.
    """
    prog = sys.argv[ 0 ]
    print "Usage:"
    print "\t%s [-f|--fullscreen] [-r <XxY>|--resolution=<XxY>]" % prog
    print
# usage()



def parse_opts( argv ):

    # Analise a linha de commando usando 'getopt'
    try:
        opts, args = getopt.gnu_getopt( argv[ 1 : ],
                                        "hfr:",
                                        [ "help",
                                          "fullscreen",
                                          "resolution=" ] )
    except getopt.GetoptError:
        # imprime informacao e sai
        usage()
        sys.exit( 2 )

    options = {
        "fullscreen":  False,
        "resolution": ( 800, 600 ), #tamanho tela
        }

    for o, a in opts:
        if o in ( "-f", "--fullscreen" ):
            options[ "fullscreen" ] = True
        elif o in ( "-h", "--help" ):
            usage()
            sys.exit( 0 )
        elif o in ( "-r", "--resolution" ):
            a = a.lower()
            r = a.split( "x" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( "," )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( ":" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue
    # for o, a in opts
    r = options[ "resolution" ]
    options[ "resolution" ] = [ int( r[ 0 ] ), int( r[ 1 ] ) ]
    return options
# parse_opts()



def main( argv ):
    fullpath = os.path.abspath( argv[ 0 ] )
    dir = os.path.dirname( fullpath )
    os.chdir( dir )

    options = parse_opts( argv )
    t = Game( options[ "resolution" ], options[ "fullscreen" ] )
    t.loop()



if __name__ == '__main__':
    main( sys.argv )
