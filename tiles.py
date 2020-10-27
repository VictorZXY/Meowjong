class TilesConverter(object):
    @staticmethod
    def array_to_one_line_string(tiles):
        # Array representation:
        # manzu = 0-9, pinzu = 10-19, souzu = 20-29, honours = 30-36,
        # red dora = 0, 10, 20;
        # One-line string representaion:
        # manzu = m, pinzu = p, souzu = s, honours = z, aka dora = 0,
        # east = 1, south = 2, west = 3, north = 4,
        # haku = 5, hatsu = 6, chun = 7.
        result = ""
        # manzu
        man = ""
        for i in range(1, 10):
            if i == 5:
                man += tiles[0] * '0'
            man += tiles[i] * str(i)
        if man != "":
            result += man + 'm'
        # pinzu
        pin = ""
        for i in range(1, 10):
            if i == 5:
                pin += tiles[10] * '0'
            pin += tiles[10 + i] * str(i)
        if pin != "":
            result += pin + 'p'
        # souzu
        sou = ""
        for i in range(1, 10):
            if i == 5:
                sou += tiles[20] * '0'
            sou += tiles[20 + i] * str(i)
        if sou != "":
            result += sou + 's'
        # honours
        honours = ""
        for i in range(1, 8):
            honours += tiles[29 + i] * str(i)
        if honours != "":
            result += honours + 'z'
        return result

    @staticmethod
    def string_to_37_array(man=None, pin=None, sou=None, honours=None):
        # String representation:
        # east = 1, south = 2, west = 3, north = 4,
        # haku = 5, hatsu = 6, chun = 7, aka dora = 0;
        # Array representation:
        # manzu = 0-9, pinzu = 10-19, souzu = 20-29, honours = 30-36,
        # red dora = 0, 10, 20.
        result = [0] * 37
        for i in man:
            result[int(i)] += 1
        for i in pin:
            result[10 + int(i)] += 1
        for i in sou:
            result[20 + int(i)] += 1
        for i in honours:
            result[29 + int(i)] += 1
        return result

    @staticmethod
    def one_line_string_to_37_array(string):
        # One-line string representaion:
        # manzu = m, pinzu = p, souzu = s, honours = z, aka dora = 0.
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

        return TilesConverter.string_to_37_array(man, pin, sou, honors)


# Tests
if __name__ == "__main__":
    initial_string = "1m2p3s37m0s84p5s41z9s34z"
    correct_string = "137m248p3059s1344z"
    tiles = TilesConverter.one_line_string_to_37_array(initial_string)
    output_string = TilesConverter.array_to_one_line_string(tiles)
    print(output_string)
    print(correct_string)
