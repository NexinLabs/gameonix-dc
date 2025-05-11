



from random import randint

class Color:
    """
    A class containing predefined color constants for use in Discord embeds and messages.
    Each color is represented as a hexadecimal integer value.
    Attributes:
        BLURPLE (int): Discord's signature blue-purple color (0x7289da).
        GREYPLE (int): A greyish-purple color (0x99aab5).
        DARK_GRAY (int): Dark gray color (0x546e7a).
        DARK_THEME (int): Color matching Discord's dark theme (0x36393F).
        LEIGHT_GREEN (int): Light grayish green color (0x979c9f).
        DARK_RED (int): Dark red color (0x992d22).
        RED (int): Pure red color (0xff0000).
        DARK_ORANGE (int): Dark orange color (0xa84300).
        ORANGE (int): Orange color (0xe67e22).
        DARK_GOLD (int): Dark gold color (0xc27c0e).
        GOLD (int): Gold color (0xf1c40f).
        MAGENDA (int): Magenta color (0xe91e63).
        PURPLE (int): Purple color (0x9b59b6).
        DARK_BLUE (int): Dark blue color (0x206694).
        BLUE (int): Pure blue color (0x0000ff).
        GREEN (int): Pure green color (0x00ff00).
        DARK_GREEN (int): Dark green color (0x1f8b4c).
        PINK (int): Pink color (0xff0066).
        TEAL (int): Teal color (0x1abc9c).
        CYAN (int): Cyan color (0x1abc9c).
        DARK_TEAL (int): Dark teal color (0x11806a).
        YELLOW (int): Pure yellow color (0xffff00).
    Methods:
        random(colorRange: int = 0xFFFFFF) -> int: Returns a random color value within the specified range.
    """
    
    BLURPLE = 0x7289da
    GREYPLE = 0x99aab5
    DARK_GRAY = 0x546e7a
    DARK_THEME = 0x36393F
    LEIGHT_GREEN = 0x979c9f
    DARK_RED = 0x992d22
    RED = 0xff0000
    DARK_ORANGE = 0xa84300
    ORANGE = 0xe67e22
    DARK_GOLD = 0xc27c0e
    GOLD = 0xf1c40f
    MAGENDA = 0xe91e63
    PURPLE = 0x9b59b6
    DARK_BLUE = 0x206694
    BLUE = 0x0000ff
    GREEN = 0x00ff00
    DARK_GREEN = 0x1f8b4c
    PINK = 0xff0066
    TEAL = 0x1abc9c
    CYAN = 0x1abc9c
    DARK_TEAL = 0x11806a
    YELLOW = 0xffff00

    @staticmethod
    def random(colorRange: int = 0xFFFFFF):
        return randint(0, colorRange)