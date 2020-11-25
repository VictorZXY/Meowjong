import os
import re
import requests

from multiprocessing import Pool
from tqdm import tqdm

from data_processing.data_preprocessing_constants import HTML_COUNT, \
    HTML_GAME_LOGS_PATH, SELECTED_YEARS, GAME_LOG_URLS_PATH, URL_PATTERN, \
    SANMA_EAST_PATTERN, SANMA_SOUTH_PATTERN, URL_COUNTS_BY_YEAR, \
    RAW_GAME_LOGS_PATH, USER_AGENT, CPU_COUNT


def extract_urls_from_html_logs():
    # year_urls_counts = {}
    # for year in SELECTED_YEARS:
    #     year_urls_counts[year] = 0
    # total_urls_count = 0

    with tqdm(desc='Extracting URLs', total=HTML_COUNT) as pbar:
        for dirpath, dirnames, files in os.walk(HTML_GAME_LOGS_PATH):
            for year in SELECTED_YEARS:
                if year in dirpath:
                    with open(os.path.join(GAME_LOG_URLS_PATH, year + '.txt'),
                              'w') as fwrite:
                        for file_name in files:
                            if file_name.endswith('.html'):
                                with open(os.path.join(dirpath, file_name), 'r',
                                          encoding='utf-8') as fread:
                                    file_contents = fread.read()
                                    urls = re.findall(URL_PATTERN,
                                                      file_contents,
                                                      re.I | re.S | re.M)
                                    for url in urls:
                                        if SANMA_EAST_PATTERN in url \
                                                or SANMA_SOUTH_PATTERN in url:
                                            fwrite.write(url.replace(
                                                'tenhou.net/0/',
                                                'tenhou.net/6/') + '\n')
                                            # year_urls_counts[year] += 1
                                            # total_urls_count += 1
                                    pbar.update(1)

    print('Extracting URLs finished.\n')
    # for year in SELECTED_YEARS:
    #     print(year + ' URLs count: ' + str(year_urls_counts[year]))
    # print('Total URLs count: ' + str(total_urls_count) + '\n')


def download_json_from_urls(year):
    with tqdm(desc='Downloading ' + year + ' JSON objects',
              total=URL_COUNTS_BY_YEAR[year]) as pbar:
        with open(os.path.join(GAME_LOG_URLS_PATH, year + '.txt'), 'r') \
                as fread:
            with open(os.path.join(RAW_GAME_LOGS_PATH, year), 'wb') as fwrite:
                for line in fread:
                    referer_link = line.replace('\n', '')
                    url = referer_link.replace('tenhou.net/6/?log=',
                                               'tenhou.net/5/mjlog2json.cgi?')
                    headers = {
                        'User-Agent': USER_AGENT,
                        'Referer': referer_link
                    }
                    response = requests.get(url, headers=headers)
                    fwrite.write(response.content + b'\n')
                    pbar.update(1)


def download_2011_json_from_urls(index):
    # This was explicitly written due to the 2011 JSON objects were not fully
    # downloaded at the first run.
    with tqdm(desc='Downloading JSON objects from 2011_' + str(index) + '.txt',
              total=URL_COUNTS_BY_YEAR['2011'] // CPU_COUNT) as pbar:
        with open(os.path.join(GAME_LOG_URLS_PATH,
                               '2011_' + str(index) + '.txt'), 'r') as fread:
            with open(os.path.join(RAW_GAME_LOGS_PATH, '2011_' + str(index)),
                      'wb') as fwrite:
                for line in fread:
                    referer_link = line.replace('\n', '')
                    url = referer_link.replace('tenhou.net/6/?log=',
                                               'tenhou.net/5/mjlog2json.cgi?')
                    headers = {
                        'User-Agent': USER_AGENT,
                        'Referer': referer_link
                    }
                    response = requests.get(url, headers=headers)
                    fwrite.write(response.content + b'\n')
                    pbar.update(1)


if __name__ == '__main__':
    assert False  # comment this line to confirm running the scripts

    # Original code
    extract_urls_from_html_logs()

    pool = Pool(len(SELECTED_YEARS))
    for year in SELECTED_YEARS:
        pool.apply_async(download_json_from_urls, args=(year,))
    pool.close()
    pool.join()

    # This was explicitly written due to the 2011 JSON objects were not fully
    # downloaded at the first run.
    with open(os.path.join(GAME_LOG_URLS_PATH, '2011' + '.txt'), 'r') \
            as fread:
        for index in range(CPU_COUNT):
            with open(os.path.join(GAME_LOG_URLS_PATH,
                                   '2011_' + str(index) + '.txt'), 'w') \
                    as fwrite:
                for count in range(URL_COUNTS_BY_YEAR['2011'] // CPU_COUNT):
                    line = fread.readline()
                    fwrite.write(line)
    print('Finished extracting 2011 URLs.\n')

    pool = Pool(CPU_COUNT)
    for index in range(CPU_COUNT):
        pool.apply_async(download_2011_json_from_urls, args=(index,))
    pool.close()
    pool.join()

    # This was used to merge the 2011 JSON sub-files into a single file.
    with open(os.path.join(RAW_GAME_LOGS_PATH, '2011'), 'wb') as fwrite:
        for index in range(CPU_COUNT):
            with open(os.path.join(RAW_GAME_LOGS_PATH, '2011_' + str(index)),
                      'rb') as fread:
                content = fread.read()
                fwrite.write(content)

    # Testing whether all JSON objects are successfully downloaded
    for year in SELECTED_YEARS:
        with open(os.path.join(RAW_GAME_LOGS_PATH, year), 'rb') as fread:
            json_count = 0
            for line in fread:
                json_count += 1
            assert json_count == URL_COUNTS_BY_YEAR[year]

    print('Success')
