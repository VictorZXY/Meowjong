from evaluation.hand_calculation.tile_constants import ONE_MAN, TWO_MAN, \
    THREE_MAN, FOUR_MAN, FIVE_MAN, SIX_MAN, SEVEN_MAN, EIGHT_MAN, NINE_MAN, \
    ONE_PIN, TWO_PIN, THREE_PIN, FOUR_PIN, FIVE_PIN, SIX_PIN, SEVEN_PIN, \
    EIGHT_PIN, NINE_PIN, ONE_SOU, TWO_SOU, THREE_SOU, FOUR_SOU, FIVE_SOU, \
    SIX_SOU, SEVEN_SOU, EIGHT_SOU, NINE_SOU, EAST, SOUTH, WEST, NORTH, HAKU, \
    HATSU, CHUN, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU

# File directories
HTML_GAME_LOGS_PATH = '../game_logs/html'
GAME_LOG_URLS_PATH = '../game_logs/html/game_log_urls'
JSON_GAME_LOGS_PATH = '../game_logs/json'
RAW_GAME_LOGS_PATH = '../game_logs/json/raw'
EXTRACTED_GAME_LOGS_PATH = '../game_logs/json/extracted'
DATASET_PATH = '../dataset'

# For downloading game logs from Tenhou.net
SELECTED_YEARS = ['2009', '2010', '2011', '2012', '2013', '2014', '2015',
                  '2016', '2017', '2018', '2019', '2020']
SANMA_EAST_PATTERN = '-00b1-'
SANMA_SOUTH_PATTERN = '-00b9-'
URL_PATTERN = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             + 'Chrome/86.0.4240.198 Safari/537.36'

# For multiprocessing
CPU_COUNT = 8

# Dataset statistics
HTML_COUNT = 4241
TOTAL_URL_COUNT = TOTAL_JSON_COUNT = 603416
URL_COUNTS_BY_YEAR = {
    '2009': 21976,
    '2010': 38105,
    '2011': 50984,
    '2012': 60627,
    '2013': 48407,
    '2014': 54314,
    '2015': 51171,
    '2016': 47718,
    '2017': 51872,
    '2018': 57674,
    '2019': 62341,
    '2020': 58227
}
JSON_COUNTS_BY_YEAR = {
    '2009': 21976,
    '2010': 38105,
    '2011': 50984,
    '2012': 60627,
    '2013': 48407,
    '2014': 54314,
    '2015': 51171,
    '2016': 47718,
    '2017': 51872,
    '2018': 57674,
    '2019': 62341,
    '2020': 58227
}
GAME_LOGS_COUNT = 5434685
GAME_LOGS_COUNTS_BY_YEAR = {
    '2009': 198686,
    '2010': 344889,
    '2011': 461839,
    '2012': 546674,
    '2013': 432572,
    '2014': 486993,
    '2015': 461631,
    '2016': 431151,
    '2017': 466831,
    '2018': 519067,
    '2019': 560674,
    '2020': 523678
}
MAX_HONBA = 15
MAX_HONBA_YEAR = '2016'
MAX_DEPOSIT = 7
MAX_DEPOSIT_YEAR = '2010'

# Tenhou tiles encoding to Meowjong tiles encoding
TENHOU_TILE_INDEX = {
    # manzu
    11: ONE_MAN,
    12: TWO_MAN,
    13: THREE_MAN,
    14: FOUR_MAN,
    15: FIVE_MAN,
    16: SIX_MAN,
    17: SEVEN_MAN,
    18: EIGHT_MAN,
    19: NINE_MAN,
    # pinzu
    21: ONE_PIN,
    22: TWO_PIN,
    23: THREE_PIN,
    24: FOUR_PIN,
    25: FIVE_PIN,
    26: SIX_PIN,
    27: SEVEN_PIN,
    28: EIGHT_PIN,
    29: NINE_PIN,
    # souzu
    31: ONE_SOU,
    32: TWO_SOU,
    33: THREE_SOU,
    34: FOUR_SOU,
    35: FIVE_SOU,
    36: SIX_SOU,
    37: SEVEN_SOU,
    38: EIGHT_SOU,
    39: NINE_SOU,
    # honours
    41: EAST,
    42: SOUTH,
    43: WEST,
    44: NORTH,
    45: HAKU,
    46: HATSU,
    47: CHUN,
    # red dora
    51: RED_FIVE_MAN,
    52: RED_FIVE_PIN,
    53: RED_FIVE_SOU
}

# Dataset encodings
TARGET_TILE_SIZE = 1
TILES_SIZE = 4
SELF_RED_DORA_SIZE = 1
MELDS_SIZE = 36
KITA_SIZE = 4
DISCARDS_SIZE = 30
DORA_INDICATORS_SIZE = 4
RIICHI_PLAYERS_SIZE = 18
SCORES_SIZE = 44
ROUND_NUMBER_SIZE = 4
HONBA_NUMBER_SIZE = 4
DEPOSIT_NUMBER_SIZE = 4
SELF_WIND_SIZE = 1
TOTAL_COLUMNS_SIZE = 365
TOTAL_FEATURES_COUNT = 12410

ONE_SCORE_SIZE = 11
TURN_NUMBER_SIZE = 5
ONE_MELD_SIZE = 9
MELDS_COUNT = 4

RIICHI_STATUS_SIZE = 1
ONE_RIICHI_PLAYER_SIZE = 6
OTHER_PLAYERS_COUNT = 3
