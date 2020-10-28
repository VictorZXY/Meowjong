# tiles
ONE_MAN = 0
TWO_MAN = 1
THREE_MAN = 2
FOUR_MAN = 3
FIVE_MAN = 4
SIX_MAN = 5
SEVEN_MAN = 6
EIGHT_MAN = 7
NINE_MAN = 8
ONE_PIN = 9
TWO_PIN = 10
THREE_PIN = 11
FOUR_PIN = 12
FIVE_PIN = 13
SIX_PIN = 14
SEVEN_PIN = 15
EIGHT_PIN = 16
NINE_PIN = 17
ONE_SOU = 18
TWO_SOU = 19
THREE_SOU = 20
FOUR_SOU = 21
FIVE_SOU = 22
SIX_SOU = 23
SEVEN_SOU = 24
EIGHT_SOU = 25
NINE_SOU = 26
EAST = 27
SOUTH = 28
WEST = 29
NORTH = 30
HAKU = 31
HATSU = 32
CHUN = 33

# manzu
MANZU = [ONE_MAN, TWO_MAN, THREE_MAN, FOUR_MAN, FIVE_MAN, SIX_MAN,
         SEVEN_MAN, EIGHT_MAN, NINE_MAN]

# pinzu
PINZU = [ONE_PIN, TWO_PIN, THREE_PIN, FOUR_PIN, FIVE_PIN, SIX_PIN,
         SEVEN_PIN, EIGHT_PIN, NINE_PIN]

# souzu
SOUZU = [ONE_SOU, TWO_SOU, THREE_SOU, FOUR_SOU, FIVE_SOU, SIX_SOU,
         SEVEN_SOU, EIGHT_SOU, NINE_SOU]

# terminals: 1 and 9
TERMINALS = [ONE_MAN, NINE_MAN, ONE_PIN, NINE_PIN, ONE_SOU, NINE_SOU]

# winds, dragons and honours
WINDS = [EAST, SOUTH, WEST, NORTH]
DRAGONS = [HAKU, HATSU, CHUN]
HONOURS = WINDS + DRAGONS

# yao-chuu-hai: terminals and honours
YAO_CHUU = TERMINALS + HONOURS

# red dora count
RED_DORA_COUNT = 4
