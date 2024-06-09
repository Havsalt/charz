from __future__ import annotations as _annotations


class Texture:
    visible: bool = True

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
