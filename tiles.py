from tile_constants import ONE_MAN, FIVE_MAN, ONE_PIN, FIVE_PIN, ONE_SOU, \
    FIVE_SOU, EAST, RED_DORA_COUNT


class TilesConverter(object):
    @staticmethod
    def array_to_one_line_string(tiles):
        # Array representation:
        # manzu = 0-8, pinzu = 9-17, souzu = 18-26, honours = 27-33,
        # red dora count as 4;
        # One-line string representaion:
        # manzu = m, pinzu = p, souzu = s, honours = z, red dora = 0,
        # east = 1, south = 2, west = 3, north = 4,
        # haku = 5, hatsu = 6, chun = 7.
        result = ""
        # manzu
        man = ""
        for i in range(1, 10):
            if i == 5:
                man += (tiles[FIVE_MAN] // RED_DORA_COUNT) * '0'
                man += (tiles[FIVE_MAN] % RED_DORA_COUNT) * '5'
            else:
                man += tiles[ONE_MAN + i - 1] * str(i)
        if man != "":
            result += man + 'm'
        # pinzu
        pin = ""
        for i in range(1, 10):
            if i == 5:
                pin += (tiles[FIVE_PIN] // RED_DORA_COUNT) * '0'
                pin += (tiles[FIVE_PIN] % RED_DORA_COUNT) * '5'
            else:
                pin += tiles[ONE_PIN + i - 1] * str(i)
        if pin != "":
            result += pin + 'p'
        # souzu
        sou = ""
        for i in range(1, 10):
            if i == 5:
                sou += (tiles[FIVE_SOU] // RED_DORA_COUNT) * '0'
                sou += (tiles[FIVE_SOU] % RED_DORA_COUNT) * '5'
            else:
                sou += tiles[ONE_SOU + i - 1] * str(i)
        if sou != "":
            result += sou + 's'
        # honours
        honours = ""
        for i in range(1, 8):
            honours += tiles[EAST + i - 1] * str(i)
        if honours != "":
            result += honours + 'z'
        return result

    @staticmethod
    def string_to_34_array(man=None, pin=None, sou=None, honours=None):
        # String representation:
        # east = 1, south = 2, west = 3, north = 4,
        # haku = 5, hatsu = 6, chun = 7, red dora = 0;
        # Array representation:
        # manzu = 0-8, pinzu = 9-17, souzu = 18-26, honours = 27-33,
        # red dora count as 4;
        result = [0] * 34
        for i in man:
            if i == '0':
                result[FIVE_MAN] += RED_DORA_COUNT
            else:
                result[ONE_MAN + int(i) - 1] += 1
        for i in pin:
            if i == '0':
                result[FIVE_PIN] += RED_DORA_COUNT
            else:
                result[ONE_PIN + int(i) - 1] += 1
        for i in sou:
            if i == '0':
                result[FIVE_SOU] += RED_DORA_COUNT
            else:
                result[ONE_SOU + int(i) - 1] += 1
        for i in honours:
            result[EAST + int(i) - 1] += 1
        return result

    @staticmethod
    def one_line_string_to_34_array(string):
        # One-line string representaion:
        # manzu = m, pinzu = p, souzu = s, honours = z, red dora = 0.
        man = ""
        pin = ""
        sou = ""
        honors = ""

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

        return TilesConverter.string_to_34_array(man, pin, sou, honors)


# Tests
if __name__ == "__main__":
    print("Test 1:")
    initial_string = "1m2p3s37m0s84p5s41z9s34z"
    correct_string = "137m248p3059s1344z"
    tiles = TilesConverter.one_line_string_to_34_array(initial_string)
    output_string = TilesConverter.array_to_one_line_string(tiles)
    print("output string:  " + output_string)
    print("correct string: " + correct_string)

    print("Test 2:")
    initial_string = "1m3s37m0s5s41z9s34z"
    correct_string = "137m3059s1344z"
    tiles = TilesConverter.one_line_string_to_34_array(initial_string)
    output_string = TilesConverter.array_to_one_line_string(tiles)
    print("output string:  " + output_string)
    print("correct string: " + correct_string)
