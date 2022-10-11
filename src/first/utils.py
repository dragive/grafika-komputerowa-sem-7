import enum

from src.first.tools.AbstractTool import AbstractTool
from src.first.tools.LineTool import LineTool
from src.first.tools.OvalTool import OvalTool
from src.first.tools.PickTool import PickTool
from src.first.tools.RectangleTool import RectangleTool


class Tools(enum.Enum):
    PICK: type(AbstractTool) = PickTool
    LINE: type(AbstractTool) = LineTool
    OVAL: type(AbstractTool) = OvalTool
    SQUARE: type(AbstractTool) = RectangleTool


class Buttons(enum.Enum):
    LEFT_BUTTON = '<Button-1>'
    MIDDLE_BUTTON = '<Button-2>'
    RIGHT_BUTTON = '<Button-3>'
    LEFT_BUTTON_MOTION = '<B1-Motion>'
    MOTION = '<Motion>'
    MIDDLE_BUTTON_MOTION = '<B2-Motion>'
    RIGHT_BUTTON_MOTION = '<B3-Motion>'
    LEFT_BUTTON_DOUBLE = '<Double-Button-1>'
    MIDDLE_BUTTON_DOUBLE = '<Double-Button-2>'
    RIGHT_BUTTON_DOUBLE = '<Double-Button-3>'
