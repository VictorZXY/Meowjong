# File directories
HTML_GAME_LOGS_PATH = '../game_logs/html'
GAME_LOG_URLS_PATH = '../game_logs/html\\game_log_urls'
JSON_GAME_LOGS_PATH = '../game_logs\\json'
RAW_GAME_LOGS_PATH = '../game_logs\\json\\raw'
EXTRACTED_GAME_LOGS_PATH = '../game_logs\\json\\extracted'

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
