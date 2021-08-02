# coding: utf-8

from threading import Timer
from apeiron import (
    draw, trans,
    pygame, State)

import pygame.freetype

from tetris import states
from tetris.logic import Shape
from tetris.logic import Board

pygame.freetype.init()

kevent = [pygame.event.custom_type(), 15] #   key event
bevent = [pygame.event.custom_type(), 5 ] # board event

colors = [
    (240,   0,   3), # ZShape
    (  1, 240,   0), # SShape
    (158,   1, 239), # TShape
    (240, 160,   1), # LShape
    (  1, 216, 215), # LineShape
    (  0,   0, 240), # SquareShape
    (  0,   0, 240), # MirroredLShape
]

class Game(State):
    def on_start(self):
        pygame.time.set_timer(bevent[0], 1000 // bevent[1])

        self.block = pygame.Rect(200, 20, 20, 20)
        self.ctx.board = Board()
        self.ctx.mfont = pygame.freetype.SysFont('monospace', 13)

    def on_stop(self):
        pygame.time.set_timer(kevent[0], 0)
        pygame.time.set_timer(bevent[0], 0)

    def on_pause(self):
        self.on_stop()
        self.ctx.paused = True

    def on_resume(self):
        pygame.time.set_timer(bevent[0], 1000 // bevent[1])
        self.ctx.paused = False

    def handle_quit_event(self, event):
        pygame.quit(); exit(0)

    def handle_bevent_event(self, event): # called by on_userevent_event
        if self.ctx.board.is_game_finished:
            return trans.POP()

        self.ctx.board.one_line_down()

    def handle_kevent_event(self, event): # called by on_userevent_event
        shape = self.ctx.board.shape
        pkeys = pygame.key.get_pressed()

        dx, dy = {
            pkeys[pygame.K_DOWN ]: ( 0, 1),
            pkeys[pygame.K_LEFT ]: (-1, 0),
            pkeys[pygame.K_RIGHT]: ( 1, 0)
        }.get(1, (0, 0))

        self.ctx.board.move(shape, shape.x + dx, shape.y + dy)

    def handle_userevent_event(self, event):
        func = {
            bevent[0]: self.handle_bevent_event,
            kevent[0]: self.handle_kevent_event
        }.get(event.type, lambda *a, **k: None)

        return func(event)

    def handle_keyup_event(self, event):
        if event.key in [pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            pygame.time.set_timer(kevent[0], 0)

    def handle_keydown_event(self, event):
        shape = self.ctx.board.shape

        if event.key == pygame.K_SPACE:
            self.ctx.board.hard_drop()

        elif event.key == pygame.K_p:
            return trans.PUSH(states.MenuState)

        elif event.key in [pygame.K_z, pygame.K_x, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            shape, dx, dy = {
                pygame.K_z    : (shape.rotate( 1),  0, 0),
                pygame.K_x    : (shape.rotate(-1),  0, 0),
                pygame.K_DOWN : (           shape,  0, 1),
                pygame.K_LEFT : (           shape, -1, 0),
                pygame.K_RIGHT: (           shape,  1, 0)
            }.get(event.key)

            self.ctx.board.move(shape, shape.x + dx, shape.y + dy)

            if event.key not in [pygame.K_z, pygame.K_x]:
                Timer(kevent[1] / 1000, pygame.time.set_timer, (kevent[0], 1000 // kevent[1])).start()

    def draw(self, ctx, interpolation):
        draw.clear(ctx, (238, 238, 238))

        for (x, y) in ctx.board.shape.coords:
            draw.rect(
                ctx,
                colors[ctx.board.shape.shape],
                self.block.move(
                    (x + ctx.board.shape.x) * self.block.width,
                    (y + ctx.board.shape.y) * self.block.height))

        for y in range(ctx.board.BOARD_H):
            for x in range(ctx.board.BOARD_W):
                if (shape := ctx.board.get_shape(x, y)) is not None:
                    draw.rect(
                        ctx,
                        colors[shape],
                        self.block.move(x * self.block.width, y * self.block.height))

                draw.rect(
                    ctx,
                    (202, 202, 202),
                    self.block.move(x * self.block.width, y * self.block.height), 1)

        draw.rect(ctx, (0, 0, 0), (200, 20, 200, 480), 3)
        draw.rect(ctx, (0, 0, 0), (430, 20, 140,  30), 3)
        ctx.mfont.render_to(
            ctx.screen, (465, 31),
            f'Score: {ctx.board.score}', (0, 0, 0))