# Documentation for `charz`

## Table of Contents

* [charz](#charz)
* [charz.text](#charz.text)
  * [fill](#charz.text.fill)
  * [flip\_h](#charz.text.flip_h)
  * [flip\_v](#charz.text.flip_v)
  * [fill\_lines](#charz.text.fill_lines)
  * [flip\_lines\_h](#charz.text.flip_lines_h)
  * [flip\_lines\_v](#charz.text.flip_lines_v)
  * [rotate](#charz.text.rotate)
* [charz.\_animation](#charz._animation)
  * [Animation](#charz._animation.Animation)
    * [from\_frames](#charz._animation.Animation.from_frames)
    * [\_\_init\_\_](#charz._animation.Animation.__init__)
    * [get\_smallest\_frame\_dimensions](#charz._animation.Animation.get_smallest_frame_dimensions)
    * [get\_largest\_frame\_dimensions](#charz._animation.Animation.get_largest_frame_dimensions)
  * [AnimationSet](#charz._animation.AnimationSet)
  * [some](#charz._animation.some)
* [charz.\_annotations](#charz._annotations)
  * [Char](#charz._annotations.Char)
* [charz.\_asset\_loader](#charz._asset_loader)
  * [AssetLoaderClassProperties](#charz._asset_loader.AssetLoaderClassProperties)
  * [AssetLoader](#charz._asset_loader.AssetLoader)
* [charz.\_clock](#charz._clock)
  * [Clock](#charz._clock.Clock)
    * [\_\_init\_\_](#charz._clock.Clock.__init__)
    * [delta](#charz._clock.Clock.delta)
    * [tick](#charz._clock.Clock.tick)
* [charz.\_components.\_animated](#charz._components._animated)
  * [AnimatedComponent](#charz._components._animated.AnimatedComponent)
    * [with\_animations](#charz._components._animated.AnimatedComponent.with_animations)
    * [with\_animation](#charz._components._animated.AnimatedComponent.with_animation)
    * [with\_repeat](#charz._components._animated.AnimatedComponent.with_repeat)
    * [add\_animation](#charz._components._animated.AnimatedComponent.add_animation)
    * [play](#charz._components._animated.AnimatedComponent.play)
    * [play\_backwards](#charz._components._animated.AnimatedComponent.play_backwards)
    * [progress\_animation](#charz._components._animated.AnimatedComponent.progress_animation)
* [charz.\_components.\_collision](#charz._components._collision)
  * [Hitbox](#charz._components._collision.Hitbox)
  * [ColliderComponent](#charz._components._collision.ColliderComponent)
    * [with\_hitbox](#charz._components._collision.ColliderComponent.with_hitbox)
    * [get\_colliders](#charz._components._collision.ColliderComponent.get_colliders)
    * [is\_colliding](#charz._components._collision.ColliderComponent.is_colliding)
    * [is\_colliding\_with](#charz._components._collision.ColliderComponent.is_colliding_with)
* [charz.\_components.\_color](#charz._components._color)
  * [ColorComponent](#charz._components._color.ColorComponent)
* [charz.\_components.\_simple\_movement](#charz._components._simple_movement)
  * [SimpleMovementComponent](#charz._components._simple_movement.SimpleMovementComponent)
    * [is\_moving\_left](#charz._components._simple_movement.SimpleMovementComponent.is_moving_left)
    * [is\_moving\_right](#charz._components._simple_movement.SimpleMovementComponent.is_moving_right)
    * [is\_moving\_up](#charz._components._simple_movement.SimpleMovementComponent.is_moving_up)
    * [is\_moving\_down](#charz._components._simple_movement.SimpleMovementComponent.is_moving_down)
    * [get\_movement\_direction](#charz._components._simple_movement.SimpleMovementComponent.get_movement_direction)
    * [update\_movement](#charz._components._simple_movement.SimpleMovementComponent.update_movement)
  * [update\_moving\_nodes](#charz._components._simple_movement.update_moving_nodes)
* [charz.\_components.\_texture](#charz._components._texture)
  * [load\_texture](#charz._components._texture.load_texture)
  * [TextureComponent](#charz._components._texture.TextureComponent)
    * [with\_texture](#charz._components._texture.TextureComponent.with_texture)
    * [with\_unique\_texture](#charz._components._texture.TextureComponent.with_unique_texture)
    * [with\_visibility](#charz._components._texture.TextureComponent.with_visibility)
    * [with\_centering](#charz._components._texture.TextureComponent.with_centering)
    * [with\_z\_index](#charz._components._texture.TextureComponent.with_z_index)
    * [with\_transparency](#charz._components._texture.TextureComponent.with_transparency)
    * [hide](#charz._components._texture.TextureComponent.hide)
    * [show](#charz._components._texture.TextureComponent.show)
    * [is\_globally\_visible](#charz._components._texture.TextureComponent.is_globally_visible)
    * [get\_texture\_size](#charz._components._texture.TextureComponent.get_texture_size)
* [charz.\_engine](#charz._engine)
  * [Engine](#charz._engine.Engine)
    * [run](#charz._engine.Engine.run)
  * [refresh\_screen](#charz._engine.refresh_screen)
  * [tick\_clock](#charz._engine.tick_clock)
* [charz.\_grouping](#charz._grouping)
* [charz.\_non\_negative](#charz._non_negative)
  * [NonNegative](#charz._non_negative.NonNegative)
    * [\_\_init\_\_](#charz._non_negative.NonNegative.__init__)
* [charz.\_prefabs.\_animated\_sprite](#charz._prefabs._animated_sprite)
  * [AnimatedSprite](#charz._prefabs._animated_sprite.AnimatedSprite)
* [charz.\_prefabs.\_label](#charz._prefabs._label)
  * [Label](#charz._prefabs._label.Label)
    * [with\_newline](#charz._prefabs._label.Label.with_newline)
    * [with\_tab\_size](#charz._prefabs._label.Label.with_tab_size)
    * [with\_tab\_char](#charz._prefabs._label.Label.with_tab_char)
    * [with\_tab\_fill](#charz._prefabs._label.Label.with_tab_fill)
    * [with\_text](#charz._prefabs._label.Label.with_text)
    * [text](#charz._prefabs._label.Label.text)
    * [text](#charz._prefabs._label.Label.text)
* [charz.\_prefabs.\_sprite](#charz._prefabs._sprite)
  * [Sprite](#charz._prefabs._sprite.Sprite)
* [charz.\_scene\_tasks](#charz._scene_tasks)
  * [progress\_animations](#charz._scene_tasks.progress_animations)
* [charz.\_screen](#charz._screen)
  * [ScreenClassProperties](#charz._screen.ScreenClassProperties)
  * [Screen](#charz._screen.Screen)
    * [\_\_init\_\_](#charz._screen.Screen.__init__)
    * [on\_startup](#charz._screen.Screen.on_startup)
    * [on\_cleanup](#charz._screen.Screen.on_cleanup)
    * [auto\_resize](#charz._screen.Screen.auto_resize)
    * [auto\_resize](#charz._screen.Screen.auto_resize)
    * [size](#charz._screen.Screen.size)
    * [size](#charz._screen.Screen.size)
    * [is\_using\_ansi](#charz._screen.Screen.is_using_ansi)
    * [get\_actual\_size](#charz._screen.Screen.get_actual_size)
    * [reset\_buffer](#charz._screen.Screen.reset_buffer)
    * [render\_all](#charz._screen.Screen.render_all)
    * [show](#charz._screen.Screen.show)
    * [refresh](#charz._screen.Screen.refresh)
* [charz.\_time](#charz._time)
  * [Time](#charz._time.Time)

<a id="charz"></a>

# Module `charz`

Charz
=====

An object oriented terminal game engine

Includes
--------

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
- `Animation`
- `AnimationSet`
- `Hitbox`
- Functions
- `load_texture`
- Decorators
- `group`
- Enums
- `Group`
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
- Feature dependent
- `SimpleMovementComponent` (when using feature `keyboard`/`all`)

<a id="charz.text"></a>

# Module `charz.text`

Text utility module
===================

Utility for flipping characters/lines. Support for rotating characters

Includes
--------

- `fill`
- `flip_h`
- `flip_v`
- `fill_lines`
- `flip_lines_h`
- `flip_lines_v`
- `rotate`

<a id="charz.text.fill"></a>

## `fill`

```python
def fill(
    line: str,
    *,
    width: int,
    fill_char: Char = " ",
) -> str
```

Fill a single left-justified line with a string of length `1`.

**Arguments**:

- `line` _str_ - Line to be filled.
- `width` _int_ - Maximum width of output string.
- `fill_char` _Char, optional_ - String of length `1` to fill line. Defaults to " ".
  

**Returns**:

- `str` - Line filled with fill character.

<a id="charz.text.flip_h"></a>

## `flip_h`

```python
def flip_h(line: str) -> str
```

Flip a single line horizontally.

Also works with a single character.

**Arguments**:

- `line` _list[str]_ - Content to be flipped.
  

**Returns**:

- `list[str]` - Flipped line or character.

<a id="charz.text.flip_v"></a>

## `flip_v`

```python
def flip_v(line: str) -> str
```

Flip a single line vertically.

Also works with a single character.

**Arguments**:

- `line` _list[str]_ - Content to be flipped.
  

**Returns**:

- `list[str]` - Flipped line or character.

<a id="charz.text.fill_lines"></a>

## `fill_lines`

```python
def fill_lines(
    lines: list[str],
    *,
    fill_char: Char = " ",
) -> list[str]
```

Fill lines with fill character, based on longest line.

Usefull for filling textures, so that it gets a nice rectangular shape.
Good for centering and flipping textures.

**Arguments**:

- `lines` _list[str]_ - Lines to be filled.
- `fill_char` _Char, optional_ - String of length `1` to fill line. Defaults to " ".
  

**Returns**:

- `list[str]` - Rectangular filled lines.

<a id="charz.text.flip_lines_h"></a>

## `flip_lines_h`

```python
def flip_lines_h(lines: list[str]) -> list[str]
```

Flip lines horizontally.

Usefull for flipping textures.

**Arguments**:

- `lines` _list[str]_ - Lines of strings or texture
  

**Returns**:

- `list[str]` - Flipped content

<a id="charz.text.flip_lines_v"></a>

## `flip_lines_v`

```python
def flip_lines_v(lines: list[str]) -> list[str]
```

Flip lines vertically.

Usefull for flipping textures.

**Arguments**:

- `lines` _list[str]_ - Lines of strings or texture.
  

**Returns**:

- `list[str]` - Flipped content.

<a id="charz.text.rotate"></a>

## `rotate`

```python
def rotate(
    char: Char,
    angle: float,
) -> str
```

Return symbol when rotated by angle counter clockwise.

**Arguments**:

- `char` _Char_ - String of length `1` to rotate.
- `angle` _float_ - Counter clockwise rotation in radians.
  

**Returns**:

- `str` - Rotated character or original character.

<a id="charz._animation"></a>

# Module `charz._animation`

<a id="charz._animation.Animation"></a>

## Class `Animation`

```python
class Animation()
```

`Animation` dataclass to represent an animation consisting of multiple frames.

This class allows you to create an animation from a list of frames
using `Animation.from_frames`,
which are lists of strings representing each frame's texture.

It is possible to subclass this dataclass, but its not easy to say
what more functionality should be added to it.

<a id="charz._animation.Animation.from_frames"></a>

### `Animation.from_frames`

```python
@classmethod
def from_frames(
    frames: list[list[str]],
    *,
    reverse: bool = False,
    flip_h: bool = False,
    flip_v: bool = False,
    fill: bool = True,
    fill_char: Char = " ",
    unique: bool = True,
) -> Self
```

Create an `Animation` from a list of frames/textures.

**Arguments**:

- `frames` _list[list[str]]_ - List of frames, where each frame is a list of strings.
- `reverse` _bool, optional_ - Reverse the order of frames. Defaults to False.
- `flip_h` _bool, optional_ - Flip frames horizontally. Defaults to False.
- `flip_v` _bool, optional_ - Flip frames vertically. Defaults to False.
- `fill` _bool, optional_ - Fill in to make shape of frames rectangular. Defaults to True.
- `fill_char` _Char, optional_ - String of length `1` to fill with. Defaults to " ".
- `unique` _bool, optional_ - Whether the frames should be unique instances. Defaults to True.
  

**Returns**:

- `Self` - An instance of `Animation` (or subclass) with the processed frames.
  

**Raises**:

- `ValueError` - If `fill_char` is not of length `1`.

<a id="charz._animation.Animation.__init__"></a>

### `Animation.__init__`

```python
def __init__(
    animation_path: Path | str,
    *,
    reverse: bool = False,
    flip_h: bool = False,
    flip_v: bool = False,
    fill: bool = True,
    fill_char: Char = " ",
) -> None
```

Load an `Animation` given a path to the folder where the animation is stored.

**Arguments**:

- `animation_path` _Path | str_ - Path to folder where animation frames are stored as files.
- `flip_h` _bool, optional_ - Flip frames horizontally. Defaults to False.
- `flip_v` _bool, optional_ - Flip frames vertically. Defaults to False.
- `fill` _bool, optional_ - Fill in to make shape of frames rectangular. Defaults to True.
- `fill_char` _Char, optional_ - String of length `1` to fill with. Defaults to " ".

<a id="charz._animation.Animation.get_smallest_frame_dimensions"></a>

### `Animation.get_smallest_frame_dimensions`

```python
def get_smallest_frame_dimensions() -> Vec2i
```

Get the smallest frame dimensions in the animation.

**Returns**:

- `Vec2i` - A `Vec2i` object containing the width and height of the smallest frame.

<a id="charz._animation.Animation.get_largest_frame_dimensions"></a>

### `Animation.get_largest_frame_dimensions`

```python
def get_largest_frame_dimensions() -> Vec2i
```

Get the largest frame dimensions in the animation.

**Returns**:

- `Vec2i` - A `Vec2i` object containing the width and height of the largest frame.

<a id="charz._animation.AnimationSet"></a>

## Class `AnimationSet`

```python
class AnimationSet(types.SimpleNamespace)
```

`AnimationSet` dataclass to represent a collection of animations.

It is subclassed from `types.SimpleNamespace` to allow dynamic attribute access.

<a id="charz._animation.some"></a>

## `some`

```python
def some(foo: int) -> float
```

Foobar

<a id="charz._annotations"></a>

# Module `charz._annotations`

Custom Annotations for `charz`
------------------------------

This file contains private annotations used across this package.

Whenever there is a "?" comment,
it means a type may or may not implement that field or mixin class.

<a id="charz._annotations.Char"></a>

### `Char`

Signifying `str` of length `1`

<a id="charz._asset_loader"></a>

# Module `charz._asset_loader`

<a id="charz._asset_loader.AssetLoaderClassProperties"></a>

## Class `AssetLoaderClassProperties`

```python
class AssetLoaderClassProperties(type)
```

Workaround to add class properties to `AssetLoader`.

<a id="charz._asset_loader.AssetLoader"></a>

## Class `AssetLoader`

```python
@final
class AssetLoader(metaclass=AssetLoaderClassProperties)
```

`AssetLoader` is a configuration namespace for loading assets.

Paths fields is of type `pathlib.Path`,
and use setters that allow passing either `pathlib.Path` or `str` paths.

`NOTE` Variables have to be set **before** importing *local files* in your project.
It is typical to use `load_texture` or create `Animation` instances
in the class definition when subclassing `Sprite`/`AnimatedSprite`,
which means these configuration variables has to be set before being used.

**Example**:

  
  Configuring `AssetLoader` attributes the correct way:
  
```python
from charz import ..., AssetLoader, ...

AssetLoader.texture_root = "src/sprites"
AssetLoader.animation_root = "src/animations"

from .my_custom_node import ...
```
  

**Attributes**:

- ``texture_root`` - `Path` - Relative path to texture/sprites folder.
- ``animation_root`` - `Path` - Relative path to animations folder.

<a id="charz._clock"></a>

# Module `charz._clock`

<a id="charz._clock.Clock"></a>

## Class `Clock`

```python
class Clock()
```

`Clock` class, with delta time calculation.

Used to sleep for the remaining time of the current frame,
until a new frame should be processed.
An instance of `Clock` is used by the active `Engine`.
If you don't want the clock to sleep, set `fps` to `0`.

**Example**:

  
```python
from charz import Engine, Clock

class MyGame(Engine):
    clock = Clock(fps=12)
```
  TEMPORARY THING:
```python
from os import cool_stuff
```
  

**Attributes**:

- ``fps`` - `NonNegative[float]` - Frames per second. If `0`, it will not sleep.
- ``delta`` - `property[float]` - Read-only attribute for delta time,
  updated on each `tick` call.

<a id="charz._clock.Clock.__init__"></a>

### `Clock.__init__`

```python
def __init__(
    *,
    fps: float = 0,
) -> None
```

Initialize with optional `fps`.

`NOTE` When `fps` is set to `0`, it will **not** do any sleeping,
which means `delta` will be updated and nothing else happens.

**Arguments**:

- `fps` _float, optional_ - Frames per second. Defaults to `0`.

<a id="charz._clock.Clock.delta"></a>

### `Clock.delta`

```python
@property
def delta() -> float
```

Read-only attribute for delta time.

Call `tick` to update and mutate properly.

<a id="charz._clock.Clock.tick"></a>

### `Clock.tick`

```python
def tick() -> None
```

Sleeps for the remaining time to maintain desired `fps`.

<a id="charz._components._animated"></a>

# Module `charz._components._animated`

<a id="charz._components._animated.AnimatedComponent"></a>

## Class `AnimatedComponent`

```python
@group(Group.ANIMATED)
class AnimatedComponent()
```

`AnimatedComponent` mixin class for node.

It provides animation controls,
and enables the node to manage and play animations defined in `AnimationSet`.

**Attributes**:

- ``animations`` - `AnimationSet` - Collection of named animations.
- ``current_animation`` - `Animation | None` - Currently active (or paused) animation.
- ``repeat`` - `bool` - Whether the animation should loop.
- ``is_playing`` - `bool` - Whether the animation is currently playing.
  

**Methods**:

  `add_animation`
  `play`
  `play_backwards`
  `progress_animation`

<a id="charz._components._animated.AnimatedComponent.with_animations"></a>

### `AnimatedComponent.with_animations`

```python
def with_animations(**animations: Animation) -> Self
```

Chained method to add multiple animations.

**Arguments**:

- `animations` _**Animation_ - Named animations as keyword arguments.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._animated.AnimatedComponent.with_animation"></a>

### `AnimatedComponent.with_animation`

```python
def with_animation(
    animation_name: str,
    animation: Animation,
) -> Self
```

Chained method to add a single animation.

**Arguments**:

- `animation_name` _str_ - Name of the animation.
- `animation` _Animation_ - Animation instance to add.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._animated.AnimatedComponent.with_repeat"></a>

### `AnimatedComponent.with_repeat`

```python
def with_repeat(state: bool = True) -> Self
```

Chained method to set the repeat state of the animation.

**Arguments**:

- `state` _bool_ - Whether the animation should repeat. Defaults to `True`.

<a id="charz._components._animated.AnimatedComponent.add_animation"></a>

### `AnimatedComponent.add_animation`

```python
def add_animation(
    animation_name: str,
    animation: Animation,
) -> None
```

Add an animation to the node.

**Arguments**:

- `animation_name` _str_ - Name of the animation.
- `animation` _Animation_ - Animation instance to add.

<a id="charz._components._animated.AnimatedComponent.play"></a>

### `AnimatedComponent.play`

```python
def play(animation_name: str) -> None
```

Play an animation by its name.

**Arguments**:

- `animation_name` _str_ - Name of the animation to play.
  

**Raises**:

- `ValueError` - If the animation with the given name does not exist.

<a id="charz._components._animated.AnimatedComponent.play_backwards"></a>

### `AnimatedComponent.play_backwards`

```python
def play_backwards(animation_name: str) -> None
```

Play an animation in reverse by its name.

**Arguments**:

- `animation_name` _str_ - Name of the animation to play in reverse.
  

**Raises**:

- `ValueError` - If the animation with the given name does not exist.

<a id="charz._components._animated.AnimatedComponent.progress_animation"></a>

### `AnimatedComponent.progress_animation`

```python
def progress_animation() -> None
```

Progress `1` frame of current animation.

Called by a frame task, which is found in `Scene.frame_tasks`.

<a id="charz._components._collision"></a>

# Module `charz._components._collision`

<a id="charz._components._collision.Hitbox"></a>

## Class `Hitbox`

```python
@dataclass(kw_only=True)
class Hitbox()
```

Hitbox dataclass for collision shape data.

**Attributes**:

- ``size`` - `Vec2` - Width and height of the hitbox.
- ``centered`` - `bool` - Whether hitbox is centered around the node's global position.
  Defaults to `False`, meaning the hitbox starts at the node's position,
  and expanding to the right and downwards.
- ``disabled`` - `bool` - Whether collision with node is disabled.
  Defaults to `False`, meaning collision is active on with node.
- ``margin`` - `float` - Inverse margin around the hitbox for collision detection.
  Defaults to `1`, and should not be smaller than `1e-2`.

<a id="charz._components._collision.ColliderComponent"></a>

## Class `ColliderComponent`

```python
@group(Group.COLLIDER)
class ColliderComponent()
```

`ColliderComponent` mixin class for node.

Assign this component to a node to enable collision detection.
All other collider components will then do collision detection against this node,
when `is_colliding` and `get_colliders` is called.

**Attributes**:

- ``hitbox`` - `Hitbox` - The hitbox data for collision detection.
- ``disabled`` - `bool` - Whether the collider is disabled.
  

**Methods**:

  `get_colliders`
  `is_colliding`
  `is_colliding_with`

<a id="charz._components._collision.ColliderComponent.with_hitbox"></a>

### `ColliderComponent.with_hitbox`

```python
def with_hitbox(hitbox: Hitbox) -> Self
```

Chained method to set the hitbox.

**Arguments**:

- `hitbox` _Hitbox_ - The hitbox to set.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._collision.ColliderComponent.get_colliders"></a>

### `ColliderComponent.get_colliders`

```python
def get_colliders() -> list[ColliderNode]
```

Get a list of colliders that this node is colliding with.

This method iterates through all nodes in the `Group.Collider` group and checks
if this node is colliding with any of them.

**Returns**:

- `list[ColliderNode]` - List of colliders that this node is colliding with.

<a id="charz._components._collision.ColliderComponent.is_colliding"></a>

### `ColliderComponent.is_colliding`

```python
def is_colliding() -> bool
```

Check if this node is colliding with any other collider node.

This method iterates through all nodes in the `Group.Collider` group and checks
if this node is colliding with any of them.

**Returns**:

- `bool` - Whether this node is colliding with any other collider node.

<a id="charz._components._collision.ColliderComponent.is_colliding_with"></a>

### `ColliderComponent.is_colliding_with`

```python
def is_colliding_with(collider_node: ColliderNode) -> bool
```

Check if this node is colliding with another collider node.

Uses SAT (Separating Axis Theorem).

`NOTE` Does not yet fully support rotated hitboxes.

**Arguments**:

- `collider_node` _ColliderNode_ - The other collider node to check collision with.
  

**Returns**:

- `bool` - Whether this node is colliding with the other collider node.

<a id="charz._components._color"></a>

# Module `charz._components._color`

<a id="charz._components._color.ColorComponent"></a>

## Class `ColorComponent`

```python
class ColorComponent()
```

`ColorComponent` mixin class for node.

**Attributes**:

- ``color`` - `ColorValue | None` - Optional color value for the node.

<a id="charz._components._simple_movement"></a>

# Module `charz._components._simple_movement`

<a id="charz._components._simple_movement.SimpleMovementComponent"></a>

## Class `SimpleMovementComponent`

```python
@group(Group.MOVEMENT)
class SimpleMovementComponent()
```

`SimpleMovementComponent` mixin class for node.

It provides basic movement functionality for a node,
and allows the node to move in 2D space using the WASD keys.

**Attributes**:

- ``speed`` - `float` - The speed of the node's movement per second (`units/s`).
  Defaults to `16` `units/s`, which is a reasonable speed for most games.
  You can change this value to make the node move faster or slower,
  by overriding this attribute in your node class as a class attribute.
  When `use_delta_time` is `False`, the unit will be `units/frame`.
  Movement direction is normalized when `normalize_movement` is `True`.
- ``use_delta_time`` - `bool` - Whether to use delta time for movement.
  Defaults to `True`; movement will be frame-rate independent.
- ``normalize_movement`` - `bool` - Whether to normalize the movement direction vector.
  Defaults to `True`; movement direction will always have a length of `1`.
  

**Methods**:

  `is_moving_left`
  `is_moving_right`
  `is_moving_up`
  `is_moving_down`
  `get_movement_direction`

<a id="charz._components._simple_movement.SimpleMovementComponent.is_moving_left"></a>

### `SimpleMovementComponent.is_moving_left`

```python
def is_moving_left() -> bool
```

Check if the node is moving left.

Override implementation to change the key used for moving left.

**Returns**:

- ``bool`` - `True` if the node is moving left, `False` otherwise.

<a id="charz._components._simple_movement.SimpleMovementComponent.is_moving_right"></a>

### `SimpleMovementComponent.is_moving_right`

```python
def is_moving_right() -> bool
```

Check if the node is moving right.

Override implementation to change the key used for moving right.

**Returns**:

- ``bool`` - `True` if the node is moving right, `False` otherwise.

<a id="charz._components._simple_movement.SimpleMovementComponent.is_moving_up"></a>

### `SimpleMovementComponent.is_moving_up`

```python
def is_moving_up() -> bool
```

Check if the node is moving up.

Override implementation to change the key used for moving up.

**Returns**:

- ``bool`` - `True` if the node is moving up, `False` otherwise.

<a id="charz._components._simple_movement.SimpleMovementComponent.is_moving_down"></a>

### `SimpleMovementComponent.is_moving_down`

```python
def is_moving_down() -> bool
```

Check if the node is moving down.

Override implementation to change the key used for moving down.

**Returns**:

- ``bool`` - `True` if the node is moving down, `False` otherwise.

<a id="charz._components._simple_movement.SimpleMovementComponent.get_movement_direction"></a>

### `SimpleMovementComponent.get_movement_direction`

```python
def get_movement_direction() -> Vec2
```

Get the movement direction of the node.

This method returns a `Vec2` object representing the direction
of movement based on the current input.

`NOTE` The returned vector is **not** normalized,
meaning it can have a length greater than `1`.

**Returns**:

- ``Vec2`` - Raw direction vector.

<a id="charz._components._simple_movement.SimpleMovementComponent.update_movement"></a>

### `SimpleMovementComponent.update_movement`

```python
def update_movement() -> None
```

Custom update method for the node.

Automatically handles checking for movement input,
and moving the node accordingly.

<a id="charz._components._simple_movement.update_moving_nodes"></a>

## `update_moving_nodes`

```python
def update_moving_nodes(current_scene: Scene) -> None
```

Update moving nodes in the current scene.

<a id="charz._components._texture"></a>

# Module `charz._components._texture`

<a id="charz._components._texture.load_texture"></a>

## `load_texture`

```python
def load_texture(
    texture_path: Path | str,
    *,
    flip_h: bool = False,
    flip_v: bool = False,
    fill: bool = True,
    fill_char: Char = " ",
) -> list[str]
```

Load texture from file.

`NOTE` `AssetLoader.texture_root` will be prepended to `texture_path`.

**Arguments**:

- `texture_path` _Path | str_ - Path to file with texture.
- `flip_h` _bool, optional_ - Flip horizontally. Defaults to `False`.
- `flip_v` _bool, optional_ - Flip vertically. Defaults to `False`.
- `fill` _bool, optional_ - Fill in to make shape rectangular. Defaults to `True`.
- `fill_char` _Char, optional_ - Filler string of length `1` to use. Defaults to `" "`.
  

**Returns**:

- `list[str]` - Loaded texture.
  

**Raises**:

- `ValueError` - If `fill_char` is not of length `1`.

<a id="charz._components._texture.TextureComponent"></a>

## Class `TextureComponent`

```python
@group(Group.TEXTURE)
class TextureComponent()
```

`TextureComponent` mixin class for node.

**Attributes**:

- ``texture`` - `list[str]` - The texture data as a list of lines.
- ``unique_texture`` - `bool` - Whether the texture is unique per instance.
- ``visible`` - `bool` - Visibility state of the node.
- ``centered`` - `bool` - Whether the texture is centered.
- ``z_index`` - `int` - Z-order for rendering.
- ``transparency`` - `Char | None` - Character used to signal transparency.
  

**Methods**:

  `hide`
  `show`
  `is_globally_visible`
  `get_texture_size`

<a id="charz._components._texture.TextureComponent.with_texture"></a>

### `TextureComponent.with_texture`

```python
def with_texture(texture_or_line: list[str] | str | Char) -> Self
```

Chained method to set the texture of the node.

If a string is provided, it is treated as a single line texture.

**Arguments**:

  texture_or_line (list[str] | str | Char):
  Texture data as a list of lines, a single line string, or a character.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._texture.TextureComponent.with_unique_texture"></a>

### `TextureComponent.with_unique_texture`

```python
def with_unique_texture() -> Self
```

Chained method to create unique copy of `texture`, and use that.

Uses `deepcopy` to create the copy.

**Returns**:

- `Self` - Same node instance with a unique texture copy.

<a id="charz._components._texture.TextureComponent.with_visibility"></a>

### `TextureComponent.with_visibility`

```python
def with_visibility(state: bool = True) -> Self
```

Chained method to set the visibility of the node.

**Arguments**:

- `state` _bool, optional_ - Visibility state. Defaults to True.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._texture.TextureComponent.with_centering"></a>

### `TextureComponent.with_centering`

```python
def with_centering(state: bool = True) -> Self
```

Chained method to set whether the texture is centered.

**Arguments**:

- `state` _bool, optional_ - Centering state. Defaults to True.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._texture.TextureComponent.with_z_index"></a>

### `TextureComponent.with_z_index`

```python
def with_z_index(z_index: int) -> Self
```

Chained method to set the z-index for rendering.

**Arguments**:

- `z_index` _int_ - Z-index value.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._texture.TextureComponent.with_transparency"></a>

### `TextureComponent.with_transparency`

```python
def with_transparency(char: Char | None) -> Self
```

Chained method to set the transparency character.

Uses a string of length `1` as transparency character.
If `None` is passed, no transparency is applied,
which means strings with spaces will be rendered on top
of other nodes with texture
(as long as it has a greater z-index or the node is newer).

**Arguments**:

- `char` _Char | None_ - Transparency character or `None`.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._components._texture.TextureComponent.hide"></a>

### `TextureComponent.hide`

```python
def hide() -> None
```

Set the node to be hidden.

<a id="charz._components._texture.TextureComponent.show"></a>

### `TextureComponent.show`

```python
def show() -> None
```

Set the node to be visible.

<a id="charz._components._texture.TextureComponent.is_globally_visible"></a>

### `TextureComponent.is_globally_visible`

```python
def is_globally_visible() -> bool
```

Check whether the node and its ancestors are visible.

**Returns**:

- `bool` - Global visibility.

<a id="charz._components._texture.TextureComponent.get_texture_size"></a>

### `TextureComponent.get_texture_size`

```python
def get_texture_size() -> Vec2i
```

Get the size of the texture.

Computed in O(n*m), where n is the number of lines
and m is the length of the longest line.

**Returns**:

- `Vec2i` - Texture size.

<a id="charz._engine"></a>

# Module `charz._engine`

<a id="charz._engine.Engine"></a>

## Class `Engine`

```python
class Engine(charz_core.Engine)
```

Extended `Engine` for managing scenes, clock, and screen.

It extends the core `Engine` and adds frame tasks
for managing the clock and screen refresh.

The run method is wrapped; to set up the screen,
along side assigning the initial delta time to `Time.delta`.

**Attributes**:

- `clock` _Clock_ - The clock instance for managing frame timing.
- `screen` _Screen_ - The screen instance for rendering output.
  

**Example**:

  
```python
from charz import Engine, Screen, Clock

class MyGame(Engine):
    clock = Clock(fps=8)  # Set frames per second
    screen = Screen(
        width=80,
        height=24,
        initial_clear=True,
    )
```
  
  Could also use a custom `Screen` subclass,
  that could be implemented in `Rust` for better performance

<a id="charz._engine.Engine.run"></a>

### `Engine.run`

```python
def run() -> None
```

Run app/game, which will start the main loop.

The loop will run until `is_running` is set to `False.

This function is also responsible for setting up the `screen`,
which given as an overridden class attribute of `Engine` subclass.

<a id="charz._engine.refresh_screen"></a>

## `refresh_screen`

```python
def refresh_screen(engine: Engine) -> None
```

Call `refresh` on the screen to update the display.

<a id="charz._engine.tick_clock"></a>

## `tick_clock`

```python
def tick_clock(engine: Engine) -> None
```

Tick the clock to update the delta time.

<a id="charz._grouping"></a>

# Module `charz._grouping`

<a id="charz._non_negative"></a>

# Module `charz._non_negative`

<a id="charz._non_negative.NonNegative"></a>

## Class `NonNegative`

```python
class NonNegative(Generic[Number])
```

`NonNegative` descriptor for attributes that must be non-negative.

It is generic, with constraints for `int` and `float` types.

`NOTE` This is only tested on class level attributes, not instance attributes.

**Example**:

  
  This ensures that `delta` is always a non-negative float,
  and raises an error if a negative value is assigned.
  
```python
class Clock:
    delta = NonNegative[float](0)
```
  

**Raises**:

- `TypeError` - If the value is not `int` or `float`.
- `ValueError` - If the value is negative.

<a id="charz._non_negative.NonNegative.__init__"></a>

### `NonNegative.__init__`

```python
def __init__(value: Number) -> None
```

Initialize the descriptor with a non-negative value.

**Arguments**:

- `value` _Number_ - The initial value, must be non-negative.

<a id="charz._prefabs._animated_sprite"></a>

# Module `charz._prefabs._animated_sprite`

<a id="charz._prefabs._animated_sprite.AnimatedSprite"></a>

## Class `AnimatedSprite`

```python
class AnimatedSprite(AnimatedComponent, Sprite)
```

`AnimatedSprite` node with multiple textures packed into animations.

It inherits from `AnimatedComponent` and `Sprite`, allowing it to
play animations defined in its `AnimationSet, while also being a sprite
with a texture, position, rotation, and other visual properties.

**Example**:

  
  The paths are relative to the project root,
  unless an animation directory is set in `AssetLoader`.
  See `Animation` for more options when loading.
  
```python
from charz import AnimatedSprite, AnimationSet, Animation

class MyAnimatedGoblin(AnimatedSprite):
    animations = AnimationSet(
        Idle=Animation("path/to/idle-animation-folder"),
        Attack=Animation("goblin/attack"),
        AttackLeft=Animation("goblin/attack", flip_h=True),
        Flee=Animation("goblin/attack", reverse=True),
    )
```

<a id="charz._prefabs._label"></a>

# Module `charz._prefabs._label`

<a id="charz._prefabs._label.Label"></a>

## Class `Label`

```python
class Label(Sprite)
```

`Label` node to simplify displaying text.

It extends `Sprite` and allows for easy text manipulation.
The text is stored in the `texture` attribute, which is a list of strings.
By using the `text` property, you can easily set and get the text.

How tabs and newlines are handled can be customized with the following attributes:
- `newline`: The character used to separate lines in the text.
Default: `"\n"`
- `tab_size`: The number of characters to use for each tab.
Default: `4`
- `tab_char`: The character to represent a tab.
Default: `"\t"`
- `tab_fill`: The character to use for filling in tabs.
Default: `" "`

**Examples**:

  
  Creating a `Label` instance inside a `Scene.__init__`:
  
```python
import colex
from charz import Scene, Label

class MenuPage(Scene):
    def __init__(self) -> None:
        self.label = Label(
            text="Welcome to the game!\nPress [Enter] to start.",
            color=colex.BLUE,
            centered=True,
        )
```
  
  Creating the `Label` at top level in `Engine.__init__`:
  
```python
import colex
from charz import Engine, Label

class MyGame(Engine):
    def __init__(self) -> None:
        self.label = Label(
            text="Welcome to the game!\nPress [Enter] to start.",
            color=colex.BLUE,
            centered=True,
        )
...
...
game = MyGame()
game.run()
```

<a id="charz._prefabs._label.Label.with_newline"></a>

### `Label.with_newline`

```python
def with_newline(newline: Char) -> Self
```

Chained method to set the newline character.

**Arguments**:

- `newline` _Char_ - Newline character to use.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._prefabs._label.Label.with_tab_size"></a>

### `Label.with_tab_size`

```python
def with_tab_size(tab_size: int) -> Self
```

Chained method to set the tab size.

**Arguments**:

- `tab_size` _int_ - Tab size to use.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._prefabs._label.Label.with_tab_char"></a>

### `Label.with_tab_char`

```python
def with_tab_char(tab_char: Char) -> Self
```

Chained method to set the tab character.

**Arguments**:

- `tab_char` _Char_ - Tab character to use.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._prefabs._label.Label.with_tab_fill"></a>

### `Label.with_tab_fill`

```python
def with_tab_fill(tab_fill: Char) -> Self
```

Chained method to set the tab fill character.

**Arguments**:

- `tab_fill` _Char_ - Tab fill character to use.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._prefabs._label.Label.with_text"></a>

### `Label.with_text`

```python
def with_text(text: str) -> Self
```

Chained method to set the text of the label.

**Arguments**:

- `text` _str_ - Text to set as texture.
  

**Returns**:

- `Self` - Same node instance.

<a id="charz._prefabs._label.Label.text"></a>

### `Label.text`

```python
@property
def text() -> str
```

Get the text of the label.

This replaces tabs with the node's fill character.

**Returns**:

- `str` - The text of the label with tabs replaced by the fill character.

<a id="charz._prefabs._label.Label.text"></a>

### `Label.text`

```python
@text.setter
def text(value: str) -> None
```

Set the text of the label.

This splits the text into lines and replaces tabs with the node's fill character.

**Arguments**:

- `value` _str_ - The text to set as the label's texture.

<a id="charz._prefabs._sprite"></a>

# Module `charz._prefabs._sprite`

<a id="charz._prefabs._sprite.Sprite"></a>

## Class `Sprite`

```python
class Sprite(ColorComponent, TextureComponent, charz_core.Node2D)
```

`Sprite` node to represent a 2D sprite with texture and color.

This is the base class for every node that has a texture and color in 2D space.
Most of the visual nodes will inherit from this class.

**Example**:

  
  Subclassing `Sprite` and overriding class attributes to customize look:
  
```python
import colex
from charz import Sprite

class CustomSprite(Sprite):
    color = colex.RED
    transparency = " "
    centered = True
    texture = [
        "  O",
        "/ | \\",
        " / \\",
    ]
```

<a id="charz._scene_tasks"></a>

# Module `charz._scene_tasks`

<a id="charz._scene_tasks.progress_animations"></a>

## `progress_animations`

```python
def progress_animations(current_scene: Scene) -> None
```

Update animations for all animated nodes in the current scene.

<a id="charz._screen"></a>

# Module `charz._screen`

<a id="charz._screen.ScreenClassProperties"></a>

## Class `ScreenClassProperties`

```python
class ScreenClassProperties(type)
```

Workaround to add class properties to `Screen`.

<a id="charz._screen.Screen"></a>

## Class `Screen`

```python
class Screen(metaclass=ScreenClassProperties)
```

`Screen` class, representing a virtual screen for rendering `ASCII` frames.

An instance of `Screen` is used by the active `Engine`.

`NOTE` Attribute `stream` is defined at *class level*,
which means **all instances will share the same reference**,
unless explicitly overridden.

**Example**:

  
```python
from charz import Engine, Screen

class MyGame(Engine):
    screen = Screen(
        width=80,
        height=24,
        color_choice=Screen.COLOR_CHOICE_AUTO,
    )
```
  

**Attributes**:

- ``stream`` - `FileLike[str]` - Output stream written to.
  Defaults to `sys.stdout`.
- ``buffer`` - `list[list[tuple[Char, ColorValue | None]]]` - Screen buffer,
  where each pixel is stored in a 2D `list`,
  and each pixel is a `tuple` pair of visual character and optional color.
- ``width`` - `NonNegative[int]` - Viewport width in character pixels.
- ``height`` - `NonNegative[int]` - Viewport height in character pixels.
- ``size`` - `property[Vec2i]` - Read-only getter,
  which packs `width` and `height` into a `Vec2i` instance.
- ``auto_resize`` - `property[bool]` - Whether to use terminal size as viewport size.
- ``intial_clear`` - `bool` - Whether to clear terminal on startup.
- ``final_clear`` - `bool` - Whether to clear screen on cleanup.
- ``hide_cursor`` - `bool` - Whether to hide cursor.
- ``transparency_fill`` - `Char` - Character used for transparent pixels..
- ``color_choice`` - `ColorChoice` - How colors are handled.
- ``margin_right`` - `int` - Margin on right side to not draw on.
- ``margin_bottom`` - `int` - Margin under to not draw on.
  
  Hooks:
  `on_startup`
  `on_cleanup`
  

**Methods**:

  `is_using_ansi`
  `get_actual_size`
  `reset_buffer`
  `render_all`
  `show`
  `refresh`

<a id="charz._screen.Screen.__init__"></a>

### `Screen.__init__`

```python
def __init__(
    width: int = 16,
    height: int = 12,
    *,
    auto_resize: bool = False,
    initial_clear: bool = True,
    final_clear: bool = True,
    hide_cursor: bool = True,
    transparency_fill: Char = " ",
    color_choice: ColorChoice = ColorChoice.AUTO,
    stream: FileLike[str] | None = None,
    margin_right: int = 1,
    margin_bottom: int = 1,
) -> None
```

Initialize screen with given width and height.

**Arguments**:

- `width` _NonNegative[int]_ - Viewport width of the screen in characters.
- `height` _NonNegative[int]_ - Viewport height of the screen in characters.
- `auto_resize` _bool_ - Whether to automatically resize the screen,
  based on terminal size. Defaults to `False`.
- `initial_clear` _bool_ - Whether to clear the screen on startup.
  Defaults to `True`.
- `final_clear` _bool_ - Whether to clear the screen on cleanup.
  Defaults to `True`.
- `hide_cursor` _bool_ - Whether to hide the cursor on startup.
  Defaults to `True`.
- `transparency_fill` _Char_ - Character used for transparent pixels.
  Defaults to `" "`.
- `color_choice` _ColorChoice_ - How colors are handled.
  Defaults to `Screen.COLOR_CHOICE_AUTO`.
- `stream` _FileLike[str] | None_ - Output stream.
  Defaults to `sys.stdout`.
- `margin_right` _int_ - Right margin in characters.
  Defaults to `1`.
- `margin_bottom` _int_ - Bottom margin in characters.
  Defaults to `1`.
  

**Raises**:

- `ValueError` - If `transparency_fill` is not a `str` of length `1`.

<a id="charz._screen.Screen.on_startup"></a>

### `Screen.on_startup`

```python
def on_startup() -> None
```

Startup hook.

Called when the screen is being activated.
The logic is seperated into this method,
as only 1 screen (which normally uses `sys.stdout`) can be active at a time.

Multiple screens can be used at the same time,
as long as they use a different type of filehandle (like sockets or files),
though this is not recommended.

<a id="charz._screen.Screen.on_cleanup"></a>

### `Screen.on_cleanup`

```python
def on_cleanup() -> None
```

Cleanup hook.

Called when the screen is being deactivated.
The logic is seperated into this method,
as only 1 screen (which normally uses `sys.stdout`) can be active at a time.

<a id="charz._screen.Screen.auto_resize"></a>

### `Screen.auto_resize`

```python
@property
def auto_resize() -> bool
```

Whether the screen automatically resizes based on terminal size.

**Returns**:

- `bool` - `True` if auto-resizing is enabled, `False` otherwise.

<a id="charz._screen.Screen.auto_resize"></a>

### `Screen.auto_resize`

```python
@auto_resize.setter
def auto_resize(state: bool) -> None
```

Set whether the screen should automatically resize based on terminal size.

**Arguments**:

- `state` _bool_ - `True` to enable auto-resizing, `False` to disable.

<a id="charz._screen.Screen.size"></a>

### `Screen.size`

```python
@property
def size() -> Vec2i
```

Get the size of the screen as a `Vec2i`.

**Returns**:

- `Vec2i` - Width and height of the screen, represented by a `Vec2i`.

<a id="charz._screen.Screen.size"></a>

### `Screen.size`

```python
@size.setter
def size(size: Vec2i) -> None
```

Set the size of the screen.

**Arguments**:

- `size` _Vec2i_ - Width and height, represented by a `Vec2i`.
  

**Raises**:

- `ValueError` - If the size `Vec2i` could not be unpacked into `2`x`int`.

<a id="charz._screen.Screen.is_using_ansi"></a>

### `Screen.is_using_ansi`

```python
def is_using_ansi() -> bool
```

Return whether its using ANSI escape and color codes.

Checks first `.color_choice`. Returns `True` if set to `ALWAYS`,
and `False` if set to `NEVER`.
If set to `AUTO`, check whether a `tty` is detected.

**Returns**:

- `bool` - `True` if using ANSI codes, `False` otherwise.

<a id="charz._screen.Screen.get_actual_size"></a>

### `Screen.get_actual_size`

```python
def get_actual_size() -> Vec2i
```

Get the actual size of the screen based on terminal size.

The `width` and `height` of the screen are just theoretical maximums,
though the real terminal might be smaller than these values.
It also takes into account the right and bottom margins,
which are nice if jittering occurs because of not accurate values
reported by `os.get_terminal_size(...)`.
If `stream` is not set to `sys.stdout`, it will return `width` and `height`.

**Returns**:

- `Vec2i` - Actual size of the screen, adjusted for terminal size and margins.

<a id="charz._screen.Screen.reset_buffer"></a>

### `Screen.reset_buffer`

```python
def reset_buffer() -> None
```

Clear the screen `buffer`.

It will fill the buffer with the transparency fill character,
as well as `None` for the color, per "pixel".

<a id="charz._screen.Screen.render_all"></a>

### `Screen.render_all`

```python
def render_all(nodes: Sequence[Renderable]) -> None
```

Render all nodes provided to the screen buffer.

**Arguments**:

- `nodes` _Sequence[Renderable]_ - Sequence of nodes with `TextureComponent`.
  

**Raises**:

- `ValueError` - If a any node has an invalid transparency character length,
  which is not equal to `1`.

<a id="charz._screen.Screen.show"></a>

### `Screen.show`

```python
def show() -> None
```

Show content of screen buffer.

This will print the formatted frame to the terminal,
if `stream` is set to `sys.stdout`.

<a id="charz._screen.Screen.refresh"></a>

### `Screen.refresh`

```python
def refresh() -> None
```

Refresh the screen, by performing multiple steps.

The steps are:
1. Resize screen if necessary.
2. Reset screen buffer.
3. Render all texture nodes in current scene.
4. Show rendered content in terminal.

<a id="charz._time"></a>

# Module `charz._time`

<a id="charz._time.Time"></a>

## Class `Time`

```python
@final
class Time()
```

`Time` is a class namespace used to store delta time.

`Time.delta` is computed by `Clock`, handled by `Engine` frame task.
`Time.delta` is usually used in `Node.update`,
for syncing movement with real time seconds.

