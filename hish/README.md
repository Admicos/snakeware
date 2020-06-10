# hish: the Highly Improved SHell

hish is a Python shell for tinkerers.

## Features

- Free movement on the entire screen
- Execution of arbitrary lines

## Usage

Start with the built-in command:

```python
>>> hish
```

or start manually:

```python
>>> from hish import HISH
>>> HISH().run()
```

- Arrow keys to move around
- Enter to execute current line

## Known Issues

- Blocks (function contents, ifs, etc) cannot be edited and ran after the first
  time
    - Entire blocks themselves, (assuming they haven't scrolled out of view or
      overridden by output) should work properly

- Some special keys might not be handled well

## Planned Features

- Text selection, copy, cut, paste
- Manual scrolling
    - Currently the window will only scroll when it reaches the end

## Dependencies

- (n)curses
