#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import annotations
import builtins
from collections import namedtuple
from enum import IntEnum
from typing import List, Tuple, Union, overload

Position = namedtuple("Position", ["x", "y"])

handler_names = [
    "key_pressed",
    "key_released",
    "key_typed",
    "mouse_clicked",
    "mouse_double_clicked",
    "mouse_dragged",
    "mouse_moved",
    "mouse_pressed",
    "mouse_released",
    "mouse_wheel",
]


class MouseButtonEnum(IntEnum):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3


class MouseButton:
    """An abstraction over a set of mouse buttons.

    :param buttons: list of mouse buttons pressed at the same time.

    """

    def __init__(self, buttons: List[str]):
        button_names = {
            MouseButtonEnum.LEFT: "LEFT",
            MouseButtonEnum.RIGHT: "RIGHT",
            MouseButtonEnum.MIDDLE: "MIDDLE",
        }
        self._buttons = buttons
        self._button_names = (
            [button_names[bt] for bt in self._buttons] if self._buttons else ""
        )

    @property
    def buttons(self):
        return self._button_names

    def __eq__(self, other):
        if isinstance(other, str):
            button_map = {
                "CENTER": MouseButtonEnum.MIDDLE,
                "MIDDLE": MouseButtonEnum.MIDDLE,
                "LEFT": MouseButtonEnum.LEFT,
                "RIGHT": MouseButtonEnum.RIGHT,
            }
            return button_map.get(other.upper(), -1) in self._buttons
        return self._buttons == other._buttons

    def __neq__(self, other):
        return self != other

    def __repr__(self):
        fstr = ", ".join(self.buttons)
        return f"MouseButton({fstr})"

    __str__ = __repr__


class Key:
    """A higher level abstraction over a single key.

    :param name: The name of the key; ENTER, BACKSPACE, etc.

    :param text: The text associated with the given key. This
        corresponds to the symbol that will be "typed" by the given
        key.

    """

    def __init__(self, name: str, text: str = ""):
        self.name = name.upper()
        self.text = text

    def __eq__(self, other: Union[Key, str]):
        if isinstance(other, str):
            return other in [self.name, self.text]
        return self.name == other.name and self.text == other.text

    def __neq__(self, other):
        return self != other

    def __str__(self):
        return self.text if self.text.isalnum() else self.name

    def __repr__(self):
        return f"Key({self.name})"


class Event:
    """A generic sketch event.

    :param modifers: The set of modifiers held down at the time of the
        event.
    :type modifiers: str list

    :param pressed: If the key/button is held down when the event
        occurs.
    :type pressed: bool

    """

    def __init__(self, raw_event, active: bool = False):
        self._modifiers: List[str] = [k.name for k in raw_event.modifiers]
        self._active = active

        self._raw = raw_event
        """
        _raw: VispyEvent, SkiaPseudoEvent
            This holds the raw event generated by the backend 
        """

    @property
    def modifiers(self):
        return self._modifiers

    @property
    def pressed(self):
        return self._active

    def is_shift_down(self) -> bool:
        """Was shift held down during the event?

        :returns: True if the shift-key was held down.

        """
        return "Shift" in self._modifiers

    def is_ctrl_down(self) -> bool:
        """Was ctrl (command on Mac) held down during the event?

        :returns: True if the ctrl-key was held down.

        """
        return "Control" in self._modifiers

    def is_alt_down(self) -> bool:
        """Was alt held down during the event?

        :returns: True if the alt-key was held down.

        """
        return "Alt" in self._modifiers

    def is_meta_down(self) -> bool:
        """Was the meta key (windows/option key) held down?

        :returns: True if the meta-key was held down.

        """
        return "Meta" in self._modifiers

    def _update_builtins(self):
        pass


class KeyEvent(Event):
    @overload
    def __init__(self, key: Union[str, Key], pressed: bool):
        """Encapsulates information about a key event.

        :param key: The key associated with this event.

        :param pressed: Specifies whether the key is held down or not.

        """
        ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._raw.key is not None:
            self.key = Key(self._raw.key.name, self._raw.text)
        else:
            self.key = Key("UNKNOWN")

    def _update_builtins(self):
        builtins.key_is_pressed = self.pressed
        builtins.key = self.key if self.pressed else None


class MouseEvent(Event):
    @overload
    def __init__(
        self,
        x: int,
        y: int,
        position: Tuple[int, int],
        change: Tuple[int, int],
        scroll: Tuple[int, int],
        count: int,
        button: MouseButton,
    ):
        """A class that encapsulates information about a mouse event.

        :param x: The x-position of the mouse in the window at the time of
            the event.

        :param y: The y-position of the mouse in the window at the time of
            the event.

        :param position: Position of the mouse in the window at the time
            of the event.

        :param change: the change in the x and y directions (defaults to
            (0, 0))

        :param scroll: the scroll amount in the x and y directions
            (defaults to (0, 0)).

        :param count: amount by which the mouse whell was dragged.

        :param button: Button information at the time of the event.

        """
        ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x, y = self._raw.pos
        x = max(min(builtins.width, x), 0)
        y = max(min(builtins.height, builtins.height - y), 0)
        dx, dy = self._raw.delta

        self.x = max(min(builtins.width, x), 0)
        self.y = max(min(builtins.height, builtins.height - y), 0)

        self.position = Position(x, y)

        # TODO: scroll should be renamed as delta
        # https://p5js.org/reference/#/p5/mouseWheel
        self.scroll = Position(int(dx), int(dy))

        self.count = self.scroll.y
        self.button = MouseButton(
            self._raw.buttons + [self._raw.button] if self._raw.button else []
        )

    def _update_builtins(self):
        builtins.pmouse_x = builtins.mouse_x
        builtins.pmouse_y = builtins.mouse_y
        builtins.mouse_x = self.x
        builtins.mouse_y = self.y
        builtins.mouse_is_pressed = self._active
        builtins.mouse_button = self.button
        builtins.moved_x = builtins.mouse_x - builtins.pmouse_x
        builtins.moved_y = builtins.mouse_y - builtins.pmouse_y

    def __repr__(self):
        press = "pressed" if self.pressed else "not-pressed"
        return f"MouseEvent({press} at {self.position})"

    __str__ = __repr__
