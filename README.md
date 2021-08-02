# apeiron
raw pygame is not nice. there will be minimal activity as i'll work on this whenever i feel like. relevant docs about the implementation: [amethyst/concepts/state](https://book.amethyst.rs/stable/concepts/state.html#state), [tetra/ContextBuilder](https://docs.rs/tetra/0.5.6/tetra/struct.ContextBuilder.html)

```python
# coding: utf-8

from apeiron import (
    draw, trans, pygame,
    State, ContextBuilder)

class PausedState(State):
    def handle_keydown_event(self, event):
        if event.key in [pygame.K_p, pygame.K_ESCAPE]:
            return trans.POP()

        return trans.NONE()

    def draw(self, ctx, interpolation):
        draw.clear(ctx, (255, 255, 255))
        draw.rect(ctx, (0, 0, 0), self.ctx.rect)

class MainState(State):
    def on_start(self):
        self.ctx.pos  = [0, 0]
        self.ctx.rect = pygame.Rect(0, 0, 10, 10)

    def handle_keydown_event(self, event):
        return {
            pygame.K_p     : trans.PUSH(PausedState),
            pygame.K_s     : trans.SET(PausedState),
            pygame.K_ESCAPE: trans.POP()
        }.get(event.key, trans.NONE())

    def update(self, ctx, dt):
        if ctx.rect.x > ctx.config['size'][0]:
            ctx.pos = [0, 0]

        ctx.pos[0] += 100 * dt
        ctx.pos[1] += 100 * dt
        ctx.rect.update(ctx.pos, (10, 10))

    def draw(self, ctx, interpolation):
        draw.clear(ctx, (0, 0, 0))
        draw.rect(ctx, (255, 255, 255), ctx.rect)

if __name__ == '__main__':
    ContextBuilder('?', 400, 400) \
        .grab_mouse(False) \
        .resizable(True) \
        .step(120) \
        .fps(75) \
        .build() \
        .run(MainState)
```
