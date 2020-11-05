from functools import reduce

from hand_calculation.hand_divider import HandDivider
from hand_calculation.tiles import Tiles

if __name__ == '__main__':
    hand_divider = HandDivider()
    tiles = Tiles.string_to_array(man='123', pin='123', sou='123',
                                  honours='11222')
    result = hand_divider.divide_hand(tiles)
    indices = [Tiles.array_to_indices(item) for item in result[0]]
    flattened = reduce(lambda x, y: x + y, indices)
    flattened_array = Tiles.indices_to_array(flattened)

    print(Tiles.array_to_one_line_string(tiles))
    print(Tiles.array_to_one_line_string(flattened_array))

    a = [1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1]
    print(reduce(lambda x, y: x * y, a))
