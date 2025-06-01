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

Add to project with `keyboard` feature:

```bash
pip install charz[keyboard]
```

or

```bash
rye add charz --features keyboard
```

Copy this code into the entry point (`main.py` or `__init__.py`)

```python
import colex              # Color constants and styling
import keyboard           # For taking key inputs
from charz import *       # Module can be imported as namespace: "import charz"


class Player(Sprite):
    SPEED: int = 4     # Defining constant
    color = colex.RED  # In reality just a string, like "\x1b[31m" for red
    centered = True    # Apply sprite centereing - Handled by `charz`
    texture = [        # A texture may be defined as a class variable, of type `list[str]`
        "  O",
        "/ | \\",
        " / \\",
    ]

    def update(self) -> None:  # This method is called every frame
        if keyboard.is_pressed("a"):
            self.position.x -= self.SPEED * Time.delta
        if keyboard.is_pressed("d"):
            self.position.x += self.SPEED * Time.delta
        if keyboard.is_pressed("s"):
            self.position.y += self.SPEED * Time.delta
        if keyboard.is_pressed("w"):
            self.position.y -= self.SPEED * Time.delta


class Game(Engine):
    fps = 12
    screen = Screen(
        auto_resize=True,
        initial_clear=True,
    )

    def __init__(self) -> None:
        Camera.current.mode = Camera.MODE_CENTERED
        self.player = Player(position=Vec2(10, 5))
    
    def update(self) -> None:
        if keyboard.is_pressed("q"):
            self.is_running = False
        if keyboard.is_pressed("e"):
            self.player.queue_free()  # `Engine` will drop reference to player
            # NOTE: Player reference is still kept alive by `App`, but it won't be updated


if __name__ == "__main__":
    game = Game()
    game.run()
```

`Note`: If using `rye`, replace:

```python
if __name__ == "__main__":
```

with

```python
def main() -> None:
```

## Rational

This project is heavily inspired by the `Godot Game Engine`.

## Includes

- Annotations
  - `ColorValue`  (from package `colex`)
  - `Self`        (from standard `typing` or from package `typing-extensions`)
- Math (from package `linflex`)
  - `lerp`
  - `sign`
  - `clamp`
  - `move_toward`
  - `Vec2`
  - `Vec2i`
  - `Vec3`
- Submodules
  - `text`
    - `fill`
    - `flip_h`
    - `flip_v`
    - `fill_lines`
    - `flip_lines_h`
    - `flip_lines_v`
    - `rotate`
- Framework
  - `Engine`
  - `Clock`
  - `Screen`
  - `Scene`
- Datastructures
  - `AnimationSet`
  - `Hitbox`
- Functions
  - `load_texture`
- Decorators
  - `group`
- Enums
  - `Group`
- Singletons
  - `Time`
  - `AssetLoader`
- Components
  - `TransformComponent`
  - `TextureComponent`
  - `ColorComponent`
  - `AnimatedComponent`
  - `ColliderComponent`
- Nodes
  - `Node`
  - `Node2D`
  - `Camera`
  - `Sprite`
  - `Label`
  - `AnimatedSprite`
- Feature dependent\*
  - `SimpleMovementComponent`

\*: Feature dependent imports requires explicit import statements as they are lazy loaded:

```python
# Example when using star import, with feature dependent import
from charz import *
from charz import SimpleMovementComponent
```

## Regarding testing

Tests for `charz` are currently manual and only somewhat implemented. The plan is to use `pytest`, however, it's hard to make work since `charz` is meant for long-running tasks, including IO.

## Versioning

This project will use `semantic versioning` after reaching release `0.1.0`. Consider any dev increment to be a breaking change. It is adviced to pin `charz` using `==` in your `pyproject.toml`, until release `0.1.0`.

## License

MIT
