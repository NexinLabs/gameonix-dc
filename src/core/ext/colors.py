from random import randint

class Color:
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