from evaluation.hand_calculation import ONE_MAN, FIVE_MAN, SEVEN_MAN, ONE_PIN, \
    FIVE_PIN, SEVEN_PIN, ONE_SOU, FIVE_SOU, SEVEN_SOU, EAST, RED_DORA_VALUE


class Tiles:
    @staticmethod
    def tiles_count(tiles):
        count = 0
        for index, num in enumerate(tiles):
            if index == FIVE_MAN or index == FIVE_PIN or index == FIVE_SOU:
                count += (num // RED_DORA_VALUE) + (num % RED_DORA_VALUE)
            else:
                count += num
        return count

    @staticmethod
    def is_shuntsu(tiles):
        """
        Determine whether the given tiles form a shuntsu.
        :param tiles: a 34-array
        :return: Boolean
        """
        if Tiles.tiles_count(tiles) == 3:
            indices = Tiles.array_to_indices(tiles)
            if len(indices) == 3 \
                    and (ONE_MAN <= indices[0] <= SEVEN_MAN
                         or ONE_PIN <= indices[0] <= SEVEN_PIN
                         or ONE_SOU <= indices[0] <= SEVEN_SOU):
                return indices[0] == indices[1] - 1 == indices[2] - 2
        return False

    @staticmethod
    def is_koutsu(tiles):
        """
        Determine whether the given tiles form a koutsu.
        :param tiles: a 34-array
        :return: Boolean
        """
        if Tiles.tiles_count(tiles) == 3:
            indices = Tiles.array_to_indices(tiles)
            if len(indices) == 3:
                return indices[0] == indices[1] == indices[2]
        return False

    @staticmethod
    def is_kantsu(tiles):
        """
        Determine whether the given tiles form a kantsu.
        :param tiles: a 34-array
        :return: Boolean
        """
        if Tiles.tiles_count(tiles) == 4:
            indices = Tiles.array_to_indices(tiles, count_red_dora=True)
            if len(indices) == 4:
                return indices[0] == indices[1] == indices[2] == indices[3]
        return False

    @staticmethod
    def is_pair(tiles):
        """
        Determine whether the given tiles form a pair.
        :param tiles: a 34-array
        :return: Boolean
        """
        if Tiles.tiles_count(tiles) == 2:
            indices = Tiles.array_to_indices(tiles)
            if len(indices) == 2:
                return indices[0] == indices[1]
        return False

    @staticmethod
    def array_to_indices(tiles, start_index=0, end_index=33,
                         count_red_dora=False):
        """
        Convert a 34-array tiles into a list of array indices, counting only
        within the specified interval.
        :param tiles: Input tiles represented by a 34-array
        :param start_index: Start index of the interval (inclusive)
        :param end_index: End index of the interval (inclusive)
        :return: A list of integer array indices
        """
        indices = []
        for index in range(start_index, end_index + 1):
            if tiles[index] > 0:
                if count_red_dora \
                        and (index == FIVE_MAN or index == FIVE_PIN
                             or index == FIVE_SOU):
                    indices.extend([index] * (tiles[index] // RED_DORA_VALUE
                                              + tiles[index] % RED_DORA_VALUE))
                else:
                    indices.extend([index] * tiles[index])
        return indices

    @staticmethod
    def indices_to_array(indices):
        # Array representation:
        # manzu = 0-8, pinzu = 9-17, souzu = 18-26, honours = 27-33,
        # red dora is not taken into count in this method.
        result = [0] * 34
        for index in indices:
            result[index] += 1
        for index in [FIVE_MAN, FIVE_PIN, FIVE_SOU]:
            if result[index] == 4:
                result[index] = 7
        return result

    @staticmethod
    def array_to_one_line_string(tiles):
        # Array representation:
        # manzu = 0-8, pinzu = 9-17, souzu = 18-26, honours = 27-33,
        # red dora count as 4;
        # One-line string representaion:
        # manzu = m, pinzu = p, souzu = s, honours = z, red dora = 0,
        # east = 1, south = 2, west = 3, north = 4,
        # haku = 5, hatsu = 6, chun = 7.
        result = ''

        # manzu
        man = ''
        for i in range(1, 10):
            if i == 5:
                man += (tiles[FIVE_MAN] // RED_DORA_VALUE) * '0'
                man += (tiles[FIVE_MAN] % RED_DORA_VALUE) * '5'
            else:
                man += tiles[ONE_MAN + i - 1] * str(i)
        if man != '':
            result += man + 'm'

        # pinzu
        pin = ''
        for i in range(1, 10):
            if i == 5:
                pin += (tiles[FIVE_PIN] // RED_DORA_VALUE) * '0'
                pin += (tiles[FIVE_PIN] % RED_DORA_VALUE) * '5'
            else:
                pin += tiles[ONE_PIN + i - 1] * str(i)
        if pin != '':
            result += pin + 'p'

        # souzu
        sou = ''
        for i in range(1, 10):
            if i == 5:
                sou += (tiles[FIVE_SOU] // RED_DORA_VALUE) * '0'
                sou += (tiles[FIVE_SOU] % RED_DORA_VALUE) * '5'
            else:
                sou += tiles[ONE_SOU + i - 1] * str(i)
        if sou != '':
            result += sou + 's'

        # honours
        honours = ''
        for i in range(1, 8):
            honours += tiles[EAST + i - 1] * str(i)
        if honours != '':
            result += honours + 'z'

        return result

    @staticmethod
    def string_to_array(man='', pin='', sou='', honours=''):
        # String representation:
        # east = 1, south = 2, west = 3, north = 4,
        # haku = 5, hatsu = 6, chun = 7, red dora = 0;
        # Array representation:
        # manzu = 0-8, pinzu = 9-17, souzu = 18-26, honours = 27-33,
        # red dora count as 4.
        result = [0] * 34

        # manzu
        for i in man:
            if i == '0':
                result[FIVE_MAN] += RED_DORA_VALUE
            else:
                result[ONE_MAN + int(i) - 1] += 1

        # pinzu
        for i in pin:
            if i == '0':
                result[FIVE_PIN] += RED_DORA_VALUE
            else:
                result[ONE_PIN + int(i) - 1] += 1

        # souzu
        for i in sou:
            if i == '0':
                result[FIVE_SOU] += RED_DORA_VALUE
            else:
                result[ONE_SOU + int(i) - 1] += 1

        # honours
        for i in honours:
            result[EAST + int(i) - 1] += 1

        return result

    @staticmethod
    def one_line_string_to_array(string):
        # One-line string representaion:
        # manzu = m, pinzu = p, souzu = s, honours = z, red dora = 0.
        man = ''
        pin = ''
        sou = ''
        honors = ''

        split_start = 0

        for index, i in enumerate(string):
            if i == 'm':
                man += string[split_start: index]
                split_start = index + 1
            if i == 'p':
                pin += string[split_start: index]
                split_start = index + 1
            if i == 's':
                sou += string[split_start: index]
                split_start = index + 1
            if i == 'z':
                honors += string[split_start: index]
                split_start = index + 1

        return Tiles.string_to_array(man, pin, sou, honors)
