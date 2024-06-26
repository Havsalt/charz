from __future__ import annotations as _annotations

from typing import (
    Generator as _Generator,
    Any as _Any
)

from ._annotations import (
    NodeType as _NodeType,
    TextureNode as _TextureNode
)


class Texture:
    _texture_instances: dict[int, _TextureNode] = {}

    @classmethod
    def iter_texture_nodes(cls) -> _Generator[_TextureNode, None, None]:
        yield from cls._texture_instances.values()
    
    def __new__(cls: type[_NodeType], *args: _Any, **kwargs: _Any) -> _NodeType:
        instance = super().__new__(cls, *args, **kwargs) # type: _TextureNode  # type: ignore[reportAssignmentType]
        Texture._texture_instances[instance.uid] = instance
        instance.texture = []
        return instance # type: ignore
    
    texture: list[str]
    visible: bool = True

    def with_texture(self, texture_or_line: list[str] | str, /):
        if isinstance(texture_or_line, str):
            self.texture = [texture_or_line]
            return self
        self.texture = texture_or_line
        return self

    def as_visible(self, state: bool = True, /):
        self.visible = state
        return self
    
    def hide(self) -> None:
        self.visible = False
    
    def show(self) -> None:
        self.visible = True

    def is_globally_visible(self) -> bool: # global visibility
        """Checks whether the node and its ancestors are visible

        Returns:
            bool: global visibility
        """
        if not self.visible:
            return False
        parent = self.parent # type: ignore
        while parent != None:
            if not isinstance(parent, Texture):
                return True
            if not parent.visible:
                return False
            parent = parent.parent # type: ignore
        return True
    
    def free(self: _TextureNode) -> None:
        del Texture._texture_instances[self.uid]
        super().free()
