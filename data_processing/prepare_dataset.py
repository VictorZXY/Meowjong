import json
import os
import pickle

from multiprocessing import Pool
from tqdm import tqdm

from data_processing.data_preprocessing_constants import JSON_COUNTS_BY_YEAR, \
    RAW_GAME_LOGS_PATH, EXTRACTED_GAME_LOGS_PATH, SELECTED_YEARS


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
                        fwrite.write(b'\n')
                    pbar.update(1)


def count_extracted_game_logs(year):
    count = 0
    with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year + '.pickle'), 'rb') \
            as fread:
        for line in fread:
            count += 1
    return count


if __name__ == '__main__':
    assert False  # comment this line to confirm running the scripts

    pool = Pool(len(SELECTED_YEARS))
    for year in SELECTED_YEARS:
        pool.apply_async(extract_game_logs_from_json, args=(year,))
    pool.close()
    pool.join()

    print('Success')

    total = 0
    for year in SELECTED_YEARS:
        count = count_extracted_game_logs(year)
        print(str(count) + ' game logs extracted from ' + year)
        total += count
    print('Total no. of game logs extracted: ' + str(total))
