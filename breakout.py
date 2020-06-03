# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:19:05 2018

@author: tdpco
"""

import sys
import time
import pygame
import random
import matplotlib.pyplot as plt

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }


def get_ball_speed():
    '''
    Method to Get Ball Speed countinously increasing with time
    '''
    return int(time.time() - start_time) / 1000


class StartGame():

    def main(self, init_bat_speed=10, xspeed_init=10,
             yspeed_init=10, max_lives=3, score=0):
        '''
        Method to initialize all the values
        '''
        global start_time
        global number_of_matches_won
        number_of_matches_won = 0
        start_time = time.time()
        bgcolour = pygame.image.load("background.jpg")
        size = width, height = 620, 480
        pygame.init()
        pygame.display.set_caption('Breakout')
        screen = pygame.display.set_mode(size)
        bat = pygame.image.load("paddle.jpg").convert()
        batrect = bat.get_rect()
        ball = pygame.image.load("ball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballrect = ball.get_rect()
        wall = Brick()
        wall.build_level(width)
        batrect = batrect.move((width / 2) - (batrect.right / 2), height-30)
        ballrect = ballrect.move(width / 2, height / 2)
        xspeed = xspeed_init
        yspeed = yspeed_init
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 30)
        pygame.mouse.set_visible(0)
        bat_speed = init_bat_speed
        while 1:
            clock.tick(500)

            # Enabling Events to close the Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            # Checking if bat has hit the ball
            if ballrect.bottom >= batrect.top \
                and ballrect.bottom <= batrect.bottom \
                and ballrect.right >= batrect.left \
                    and ballrect.left <= batrect.right:
                    yspeed = -yspeed

            # Move Ball increaing Speed with Time
            if xspeed < 0:
                xspeed = xspeed - get_ball_speed()
            else:
                xspeed = xspeed + get_ball_speed()
            if yspeed < 0:
                yspeed = yspeed - get_ball_speed()
            else:
                yspeed = yspeed + get_ball_speed()
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed
            if ballrect.top < 0:
                yspeed = -yspeed

            # Move Bat with input speed from one end to other
            # print("Current Bat Speed : %s and Bat Rect %s" % (bat_speed,batrect))
            bat_speed = xspeed
            batrect = batrect.move(bat_speed, 0)
            # Checking if bat hit the wall
            if batrect.left < 0 or batrect.right > width:
                bat_speed = -bat_speed
            # print("Width %s and Bat Right %s"%(width,batrect.right))
            # check if ball has gone past bat - lose a life
            if ballrect.top > height:
                lives -= 1
                xspeed = xspeed_init
                yspeed = yspeed_init
                if random.random() > 0.5:
                    xspeed = -xspeed
                ballrect.center = width * random.random(), height / 3
                batrect = bat.get_rect()
                batrect = batrect.move((width / 2) - (batrect.right / 2), height-30)
                if lives == 0:
                    game_over = pygame.font.Font(None, 80)\
                        .render("Game Over", True, (0, 128, 128), bgcolour)
                    game_over_rect = game_over.get_rect()
                    game_over_rect = game_over_rect.move(
                            width / 2 - (game_over_rect.center[0]), height / 3)
                    screen.blit(game_over, game_over_rect)
                    pygame.display.flip()
                    return(score)

            # Checking if ball has hit any wall
            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed
            if xspeed > 0 and ballrect.right > width:
                xspeed = -xspeed

            # Checking if bat has hit any wall
            if batrect.left < 0 and bat_speed < 0:
                bat_speed = -bat_speed
            if bat_speed > 0 and batrect.right > width:
                bat_speed = -bat_speed

            # If bircks are hit Delete the Brick
            index = ballrect.collidelist(wall.brickrect)
            if index != -1:
                if ballrect.center[0] > wall.brickrect[index].right \
                        or ballrect.center[0] < wall.brickrect[index].left:
                    xspeed = -xspeed
                else:
                    yspeed = -yspeed
                wall.brickrect[index:index + 1] = []
                score += 10

            # Displaying Score on Screen
            screen.blit(bgcolour, (0, 0))
            scoretext = pygame.font.Font(None, 40)\
                .render("Score : " + str(score), True, (0, 128, 128), bgcolour)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(scoretextrect.left + 5, 0)
            screen.blit(scoretext, scoretextrect)

            batspeedtext = pygame.font.Font(None, 40)\
                .render("Bat Speed : " + str(abs(bat_speed)),
                        True, (0, 128, 128), bgcolour)
            batspeedtextrect = batspeedtext.get_rect()
            batspeedtextrect = batspeedtextrect.move(
                    batspeedtextrect.right + (width/3 - 10), 0)
            screen.blit(batspeedtext, batspeedtextrect)

            for i in range(0, len(wall.brickrect)):
                screen.blit(wall.brick, wall.brickrect[i])

            # If there is no bricks left on Screen Declare Player winner
            if wall.brickrect == []:
                number_of_matches_won += 1
                winner = pygame.font.Font(None, 80)\
                    .render("You Won", True, (0, 128, 128), bgcolour)
                winnerrect = winner.get_rect()
                winnerrect = winnerrect.move(
                        width / 2 - (winnerrect.center[0]), height / 3)
                screen.blit(winner, winnerrect)
                pygame.display.flip()
                return(score)

            screen.blit(ball, ballrect)
            screen.blit(bat, batrect)
            pygame.display.flip()


class Brick():
    '''
    Class For defining Bricks
    '''
    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left
        self.brickheight = brickrect.bottom - brickrect.top

    def build_level(self, width):
        xpos = 0
        ypos = 60
        gap = 5
        adj = 0
        self.brickrect = []
        for i in range(0, 44):
            if xpos > width:
                adj = 0
                xpos = -adj
                ypos += self.brickheight
            self.brickrect.append(self.brick.get_rect())
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength + gap


def draw_histogram_one_variable(final_score, given_label):
    plt.hist(final_score, alpha=0.5, label=given_label)
    plt.title('Score Histogram for Breakout - %s' % given_label, fontdict=font)
    plt.xlabel('Score', fontdict=font)
    plt.ylabel('Number of Games', fontdict=font)
    plt.xscale('linear')
    plt.yscale('linear')
    plt.legend(loc='upper left',
               facecolor='wheat',
               shadow=True,
               title="Match Description",
               labelspacing=1,
               fontsize='large',
               bbox_to_anchor=(1.02, 1),
               borderaxespad=0,
               labels=['Number of Matches = %s' % len(final_score),
                       'Total Score = %s' % sum(final_score)
                       ])
    plt.subplots_adjust(right=0.8)
    plt.show()


if __name__ == '__main__':
    # Value Can be changed to set properties of game
    # xspeed_init = 50
    # yspeed_init = 50
    # max_lives = 3
    # score = 0
    number_of_games = 100
    final_score = []
    startgame = StartGame()
    for i in range(0, number_of_games):
        print("Playing Game For - %s " % str(i+1))
        final_score.append(startgame.main())
    # Result for bat speed 10
    draw_histogram_one_variable(final_score,
                                'Paddle Speed Increasing With Time')
