import colex  # Color constants and styling
import keyboard  # For taking key inputs
from charz import *


class Player(Sprite):
    _SPEED: int = 4  # Defining local constant
    color = colex.RED  # In reality just a string, like "\x1b[31m" for red
    centered = True  # Apply sprite centereing - Handled by `charz`
    texture = [  # A texture may be defined as a class variable, of type `list[str]`
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
    screen = Screen(auto_resize=True)
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
