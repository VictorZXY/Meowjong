import json
import os
import re
import requests

from multiprocessing import Process
from progress.bar import IncrementalBar

HTML_COUNT = 4241
HTML_GAME_LOGS_PATH = '../game_logs/html'
GAME_LOG_URLS_PATH = '../game_logs/html\\game_log_urls'
JSON_GAME_LOGS_PATH = '../game_logs\\json'
RAW_GAME_LOGS_PATH = '../game_logs\\json\\raw'
SANMA_EAST_PATTERN = '-00b1-'
SANMA_SOUTH_PATTERN = '-00b9-'
SELECTED_YEARS = ['2009', '2010', '2011', '2012', '2013', '2014', '2015',
                  '2016', '2017', '2018', '2019', '2020']
URL_PATTERN = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             + 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             + 'Chrome/86.0.4240.198 Safari/537.36'


def extract_urls_from_html_logs():
    year_urls_counts = {}
    for year in SELECTED_YEARS:
        year_urls_counts[year] = 0
    total_urls_count = 0

    with IncrementalBar('Extracting URLs', max=HTML_COUNT) as bar:
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
                                            year_urls_counts[year] += 1
                                            total_urls_count += 1
                                    bar.next()

    for year in SELECTED_YEARS:
        print(year + ' URLs count: ' + str(year_urls_counts[year]))
    print('Total URLs count: ' + str(total_urls_count))
    return year_urls_counts


def download_json_from_urls(year, year_urls_counts):
    with IncrementalBar('Downloading ' + year + ' game logs',
                        max=year_urls_counts[year]) as bar:
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
                    bar.next()
    print('Finished downloading ' + year + ' game logs')


if __name__ == '__main__':
    try:
        year_urls_counts = extract_urls_from_html_logs()

        process_list = []
        for year in SELECTED_YEARS:
            p = Process(target=download_json_from_urls,
                        args=(year, year_urls_counts))
            p.start()
            process_list.append(p)
        for p in process_list:
            p.join()

        print('Success')
    except Exception as e:
        print(e)
