# Charz

An object oriented terminal game engine

## Installation

Install using either `pip` or `rye`:

```bash
pip install charz[all]
```

```bash
rye add charz --features all
```

If you don't need the `keyboard` package, simply use:

```bash
pip install charz
```

```bash
rye add charz
```

## Getting started

```python
import colex              # Color constants and styling
import keyboard           # For taking key inputs
from charz import *       # Module can be imported as namespace: "import charz"


class Player(Sprite):
    _SPEED: int = 4    # Defining local constant
    color = colex.RED  # In reality just a string, like "\x1b[31m" for red
    centered = True    # Apply sprite centereing - Handled by `charz`
    texture = [        # A texture may be defined as a class variable, of type `list[str]`
        "  O",
        "/ | \\",
        " / \\",
    ]

    def update(self, delta: float) -> None:  # This method is called every frame
        if keyboard.is_pressed("a"):
            self.position.y -= self._SPEED * delta
        if keyboard.is_pressed("d"):
            self.position.y += self._SPEED * delta
        if keyboard.is_pressed("s"):
            self.position.y += self._SPEED * delta
        if keyboard.is_pressed("w"):
            self.position.y -= self._SPEED * delta


class Game(Engine):
    fps = 12
    screen = Screen(auto_resize = True)
    clear_console = True

    def __init__(self) -> None:
        Camera.current.mode = Camera.MODE_CENTERED
        self.player = Player(position=Vec2(10, 5))
    
    def update(self, _delta: float) -> None:
        if keyboard.is_pressed("q"):
            self.is_running = False
        if keyboard.is_pressed("e"):
            self.player.queue_free()  # `Engine` will drop reference to player
            # NOTE: Player reference is still kept alive by `App`, but it won't be updated


if __name__ == "__main__":
    game = Game()
    game.run()
```

## Rational

This project is heavily inspired by the `Godot Game Engine`.

## Includes

- Annotations
  - `ColorValue`
- Math
  - `lerp`
  - `sign`
  - `clamp`
  - `Vec2`
  - `Vec2i`
  - `Vec3`
- Modules
  - `text`
    - `fill`
    - `flip_h`
    - `flip_v`
    - `fill_lines`
    - `flip_lines_h`
    - `flip_lines_v`
    - `rotate`
  - `colex`    (Dependency)
  - `keyboard` (Optional dependency)
- Framework
  - `Engine`
  - `Clock`
  - `DeltaClock`
  - `Screen`
- Datastructures
  - `AnimationSet`
  - `Hitbox`
- Functions
  - `load_texture`
- Components
  - `Transform`
  - `Texture`
  - `Color`
  - `Animated`
  - `Collider`
- Nodes
  - `Camera`
  - `Node`
  - `Node2D`
  - `Sprite`
  - `Label`
  - `AnimatedSprite`

## Regarding testing

Tests for `charz` are currently manual and only somewhat implemented. Until I find a testing tool I like, things will be manual, just so I know if the critical parts work.

**NOTE**: Tests cannot be run from `current working directory` at the moment! I'll just monkeypatch it to run on my machine *-famose last words*.

## Versioning

This project will use `semantic versioning` after reaching release `0.1.0`. Consider any patch bump before that to be a breaking change. It is adviced to pin `charz` using `==` in your `pyporject.toml`, until release `0.1.0`.

## License

MIT
