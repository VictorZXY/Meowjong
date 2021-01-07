import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--input', action='store', type=str, required=True)
my_parser.add_argument('--id', action='store', type=int, required=True)

args = my_parser.parse_args()
print(args.input)
