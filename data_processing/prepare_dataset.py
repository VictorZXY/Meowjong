import json
import os
import pickle

from multiprocessing import Pool
from tqdm import tqdm

TOTAL_JSON_COUNT = 603416
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
JSON_GAME_LOGS_PATH = '../game_logs\\json'
RAW_GAME_LOGS_PATH = '../game_logs\\json\\raw'
EXTRACTED_GAME_LOGS_PATH = '../game_logs\\json\\extracted'
SELECTED_YEARS = ['2009', '2010', '2011', '2012', '2013', '2014', '2015',
                  '2016', '2017', '2018', '2019', '2020']


def extract_game_logs_from_json(year):
    with tqdm(desc='Extracting ' + year + ' game logs',
              total=JSON_COUNTS_BY_YEAR[year]) as pbar:
        with open(os.path.join(RAW_GAME_LOGS_PATH, year), 'rb') as fread:
            with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year), 'wb') \
                    as fwrite:
                for line in fread:
                    js = json.loads(line)
                    for log in js['log']:
                        pickle.dump(log, fwrite)
                        fwrite.write(b'\n')
                    pbar.update(1)


def count_extracted_game_logs(year):
    count = 0
    with open(os.path.join(EXTRACTED_GAME_LOGS_PATH, year), 'rb') as fread:
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
