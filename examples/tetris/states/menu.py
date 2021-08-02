# coding: utf-8

from apeiron import (
    draw, trans,
    pygame, State)

from tetris import states

class Menu(State):
    def handle_keydown_event(self, event):
        if event.key in [pygame.K_p, pygame.K_ESCAPE]:
            return trans.POP()

    def handle_mousebuttondown_event(self, event):
        return trans.SET(states.GameState)

    def draw(self, ctx, interpolation):
        if not getattr(ctx, 'paused', False):
            return draw.clear(self.ctx, (255, 255, 255))

        ctx.state_manager.states[-2].draw(ctx, interpolation)
        draw.rect(ctx, (0, 0, 0), (430, 60, 140,  30), 3)
        ctx.mfont.render_to(
            ctx.screen, (465, 71),
            ' Paused', (0, 0, 0))