import json
import numpy as np
import os
import pandas as pd
import pickle

from multiprocessing import Pool
from tqdm import tqdm

from data_processing.data_preprocessing_constants import JSON_COUNTS_BY_YEAR, \
    RAW_GAME_LOGS_PATH, EXTRACTED_GAME_LOGS_PATH, SELECTED_YEARS, \
    GAME_LOGS_COUNT, TENHOU_TILE_INDEX, ROUND_NUMBER_SIZE, HONBA_NUMBER_SIZE, \
    DEPOSIT_NUMBER_SIZE, SCORES_SIZE, ONE_SCORE_SIZE, DORA_INDICATORS_SIZE, \
    PRIVATE_TILES_SIZE, SELF_RED_DORA_INDICATORS_SIZE, MELDS_SIZE, \
    ONE_MELD_SIZE, TILES_SIZE

from hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, FIVE_SOU, \
    NORTH, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU


def extract_game_logs_from_json(year):
    with tqdm(desc='Extracting ' + year + ' game logs',
              total=JSON_COUNTS_BY_YEAR[year]) as pbar:
        with open(os.path.join(RAW_GAME_LOGS_PATH, year), 'rb') as fread:
            with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'),
                      'wb') as fwrite:
                for line in fread:
                    js = json.loads(line)
                    for log in js['log']:
                        pickle.dump(log, fwrite)
                    pbar.update(1)


def count_extracted_game_logs(year):
    count = 0
    with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'), 'rb') \
            as fread:
        try:
            while pickle.load(fread):
                count += 1
        except EOFError:
            pass
    return count


def find_max_honba_and_deposit():
    max_honba = 0
    max_honba_year = ''
    max_deposit = 0
    max_deposit_year = ''
    with tqdm(desc='Processing', total=GAME_LOGS_COUNT) as pbar:
        for year in SELECTED_YEARS:
            with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'),
                      'rb') as fread:
                try:
                    while log := pickle.load(fread):
                        if log[0][1] > max_honba:
                            max_honba = log[0][1]
                            max_honba_year = year
                        if log[0][2] > max_deposit:
                            max_deposit = log[0][2]
                            max_deposit_year = year
                        pbar.update(1)
                except EOFError:
                    pass
    return {
        'max_honba': max_honba,
        'max_honba_year': max_honba_year,
        'max_deposit': max_deposit,
        'max_deposit_year': max_deposit_year
    }


def encode_round_number(round_number):
    output = np.empty((34, ROUND_NUMBER_SIZE))
    for bit, val in enumerate(bin(round_number)[2:].zfill(ROUND_NUMBER_SIZE)):
        if val == '1':
            output[:, bit] = 1
        else:
            output[:, bit] = 0
    return output


def encode_honba_number(honba_number):
    output = np.empty((34, HONBA_NUMBER_SIZE))
    for bit, val in enumerate(bin(honba_number)[2:].zfill(HONBA_NUMBER_SIZE)):
        if val == '1':
            output[:, bit] = 1
        else:
            output[:, bit] = 0
    return output


def encode_deposit_number(deposit_number):
    output = np.empty((34, DEPOSIT_NUMBER_SIZE))
    for bit, val in \
            enumerate(bin(deposit_number)[2:].zfill(DEPOSIT_NUMBER_SIZE)):
        if val == '1':
            output[:, bit] = 1
        else:
            output[:, bit] = 0
    return output


def encode_scores(scores):
    output = np.zeros((34, SCORES_SIZE))
    for index, score in enumerate(scores):
        for bit, val in enumerate(bin(score // 100)[2:].zfill(ONE_SCORE_SIZE)):
            if val == '1':
                output[:, index * ONE_SCORE_SIZE + bit] = 1
    return output


def encode_dora_indicator(array, dora_indicators, index):
    if TENHOU_TILE_INDEX[dora_indicators[0]] == RED_FIVE_MAN:
        array[FIVE_MAN, index] = 1
    elif TENHOU_TILE_INDEX[dora_indicators[0]] == RED_FIVE_PIN:
        array[FIVE_PIN, index] = 1
    elif TENHOU_TILE_INDEX[dora_indicators[0]] == RED_FIVE_SOU:
        array[FIVE_SOU, index] = 1
    else:
        array[TENHOU_TILE_INDEX[dora_indicators[0]], index] = 1


def add_tile_to_hand(tile, hand, red_dora_indicators):
    """
    :param tile: Tenhou-encoded integer index of a tile
    :param hand: (34, 4) np.array
    :param red_dora_indicators: (34, 1) np.array
    """
    if TENHOU_TILE_INDEX[tile] == RED_FIVE_MAN:
        index = 0
        while hand[FIVE_MAN, index] != 0:
            index += 1
        hand[FIVE_MAN, index] = 1
        red_dora_indicators[FIVE_MAN] = 1
    elif TENHOU_TILE_INDEX[tile] == RED_FIVE_PIN:
        index = 0
        while hand[FIVE_PIN, index] != 0:
            index += 1
        hand[FIVE_PIN, index] = 1
        red_dora_indicators[FIVE_PIN] = 1
    elif TENHOU_TILE_INDEX[tile] == RED_FIVE_SOU:
        index = 0
        while hand[FIVE_SOU, index] != 0:
            index += 1
        hand[FIVE_SOU, index] = 1
        red_dora_indicators[FIVE_SOU] = 1
    else:
        index = 0
        while hand[tile, index] != 0:
            index += 1
        hand[tile, index] = 1


def encode_start_hand(start_hand):
    hand = np.zeros((34, PRIVATE_TILES_SIZE))
    red_dora_indicators = np.zeros((34, SELF_RED_DORA_INDICATORS_SIZE))
    for tile in start_hand:
        add_tile_to_hand(tile, hand, red_dora_indicators)
    return hand, red_dora_indicators


def can_pon(target_tile, private_tiles):
    """
    :param target_tile: (34, 1) np.array
    :param private_tiles: (34, 4) np.array
    :return: Boolean
    """
    tile = np.where(target_tile == 1)[0][0]
    return np.sum(private_tiles[tile]) + target_tile[tile] >= 3


def can_kan(target_tile, private_tiles):
    """
    :param target_tile: (34, 1) np.array
    :param private_tiles: (34, 4) np.array
    :return: Boolean
    """
    tile = np.where(target_tile == 1)[0][0]
    return np.sum(private_tiles[tile]) + target_tile[tile] == 4


def can_add_kan(target_tile, melds):
    """
    :param target_tile: (34, 1) np.array
    :param melds: (34, 36) np.array
    :return: Boolean
    """
    tile = np.where(target_tile == 1)[0][0]

    for i in range(MELDS_SIZE, step=ONE_MELD_SIZE):
        meld = melds[i:i + TILES_SIZE]
        melded_tiles = np.where(meld == 1)
        if np.all([melded_tiles[0] == np.array([0, 1, 2]),
                   melded_tiles[1] == np.array([tile, tile, tile])]):
            return True

    return False


def can_kita(target_tile, private_tiles):
    """
    :param target_tile: (34, 1) np.array
    :param private_tiles: (34, 4) np.array
    :return: Boolean
    """
    return np.sum(private_tiles[NORTH]) + target_tile[NORTH] > 0


if __name__ == '__main__':
    # assert False  # comment this line to confirm running the scripts

    # Extract game logs from the downloaded JSON objects
    pool = Pool(len(SELECTED_YEARS))
    for year in SELECTED_YEARS:
        pool.apply_async(extract_game_logs_from_json, args=(year,))
    pool.close()
    pool.join()

    # Count the number of extracted game logs
    total = 0
    for year in SELECTED_YEARS:
        count = count_extracted_game_logs(year)
        print(str(count) + ' game logs extracted from ' + year)
        total += count
    print('Total no. of game logs extracted: ' + str(total))

    # Find the maximum honba and deposit numbers
    max_honba_and_deposit_results = find_max_honba_and_deposit()
    for key, val in max_honba_and_deposit_results:
        print(key + ':', val)
