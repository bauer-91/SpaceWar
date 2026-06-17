import random
import sys
from builtins import print

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import EVENT_ENEMY, EVENT_ENEMY_SHOT
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('background1-'))
        self.entity_list.append(EntityFactory.get_entity('player'))
        self.timeout = 20000
        pygame.time.set_timer(EVENT_ENEMY, random.randint(500, 2000))
        pygame.time.set_timer(EVENT_ENEMY_SHOT, 2000)

    def run(self):
        pygame.mixer_music.load(f'asset/level1.wav')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if ent.name == 'player':
                    self.level_text(14, f'Player - Health:{ent.health}', (0, 255, 200), (10, 15))
                    self.level_text(14, f'Player - Score:{ent.score}', (0, 255, 200), (10, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    self.entity_list.append(EntityFactory.get_entity('enemy'))
                    pygame.time.set_timer(
                        EVENT_ENEMY,
                        random.randint(500, 2000)
                    )
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for ent in self.entity_list:
                            if isinstance(ent, Player):
                                self.entity_list.append(ent.shoot())
                                break
                if event.type == EVENT_ENEMY_SHOT:
                    for ent in self.entity_list:
                        if isinstance(ent, Enemy):
                            self.entity_list.append(ent.shoot())

            self.level_text(14, f'LEVEL 1', (0, 255, 200), (10, 5))

            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Pixelify Sans Bold", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color)
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
