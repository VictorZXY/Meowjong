import csv

if __name__ == '__main__':
    with open('test.txt', 'w') as f:
        f.write('1\n')
        f.write('3\n')
        f.write('5\n')
        f.write('7\n')
        f.write('9\n')

    with open('test.txt', 'r') as f:
        with open('test.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['index', 'label'])
            for index, line in enumerate(f):
                writer.writerow([index + 1, line[:-1]])
