from hand_calculation.tiles import Tiles


class InvalidFormatError(Exception):
    pass


class Meld:
    CHII = 'chii'
    PON = 'pon'
    KAN = 'kan'
    KITA = 'kita'

    type = None
    tiles = None  # 34-array
    called_tile = None  # 34-array
    is_open = True  # for distinguishing between open and closed kan
    who = None
    from_whom = None

    def __init__(self, meld_type=None, tiles=None, called_tile=None,
                 is_open=True, who=None, from_whom=None):
        """
        :param meld_type: One of the constants CHII, PON, KAN, and KITA
        :param tiles: Tiles represented by a 34-array or a one-line string
        :param called_tile: Called tile represented by a 34-array or a
        one-line string
        :param is_open: Boolean, always True except for closed kan
        :param who: The player who makes this meld
        :param from_whom: The player from whom a discarded tile is claimed to
        make this meld
        """
        self.type = meld_type

        if not tiles:
            self.tiles = []
        elif isinstance(tiles, str):
            self.tiles = Tiles.one_line_string_to_array(tiles)
        elif isinstance(tiles, list):
            self.tiles = tiles
        else:
            raise InvalidFormatError

        if not called_tile:
            self.called_tile = []
        elif isinstance(called_tile, str):
            self.called_tile = Tiles.one_line_string_to_array(called_tile)
        elif isinstance(called_tile, list):
            self.called_tile = called_tile
        else:
            raise InvalidFormatError

        self.called_tile = called_tile
        self.is_open = is_open
        self.who = who
        self.from_whom = from_whom

    def __str__(self):
        return 'Type: {}, Tiles: {}'.format(
            self.type, Tiles.array_to_one_line_string(self.tiles))

    def __repr__(self):
        return self.__str__()
