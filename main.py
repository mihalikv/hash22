import os
from collections import Counter, OrderedDict
import numpy as np
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = ['test']
input_files = [os.path.join(dir_path, 'input', '{}.txt'.format(file_name)) for file_name in file_names]
output_files = [os.path.join(dir_path, 'output', '{}.out'.format(file_name)) for file_name in file_names]


def process(input_file_path, output_file_path):
    output_file = open(output_file_path, 'w')

    with open(input_file_path) as input_file:
        print(input_file.readlines())

    output_file.write('test')
    output_file.close()


def main():
    for index, input_file_path in enumerate(input_files):
        process(input_file_path, output_files[index])


if __name__ == "__main__":
    main()