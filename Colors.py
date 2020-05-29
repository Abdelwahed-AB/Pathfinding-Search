from enum import Enum
from pygame import Color

RGB = Color

class ColorCode(Enum):
    WHITE = RGB(255, 255, 255)
    LIGHT_GRAY = RGB(238, 238, 238)
    GRAY = RGB(125, 125, 125)
    DARK_GRAY = RGB(78, 78, 78)
    BLACK = RGB(17, 17, 17)
    LIGHTER_GREEN = RGB(59, 224, 56)
    GREEN = RGB(47, 219, 54)
    LIGHTER_RED = RGB(230, 53, 41)
    RED = RGB(227, 42, 42)
    BLUE = RGB(20, 94, 238)
    ORANGE = RGB(245, 153, 58)
    YELLOW = RGB(233, 221, 52)
    BG_COLOR = RGB(38, 38, 38)
