# Tips when Creating with `charz`

This document aims to give useful tips. It will also showcase some handy examples.

## Terms

- `node`: An entity or game object that either exists in the world (like a sprite or point) or theoretical (like a timer node)
- `component`: A class used to extend nodes
- `MRO chain`: Method resolution order, when calling a chain of super methods (like `__new__`)

## Composition using inherited components

In `charz`, nodes are often composed using `components`.
