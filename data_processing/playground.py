import json
import pickle

if __name__ == '__main__':
    with open('../game_logs\\json\\raw\\2009', 'rb') as fread:
        line = fread.readline()
        j = json.loads(line)
        with open('test', 'wb') as fwrite:
            for log in j['log']:
                pickle.dump(log, fwrite)
                fwrite.write(b'\n')

    with open('test','rb') as f:
        for line in f:
            result = pickle.loads(line)
            print(result)
