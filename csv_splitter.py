import csv
from os import path, listdir, rename, remove


def split(filehandler, delimiter=',', row_limit=10000,
    output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    """
    Splits a CSV file into multiple pieces.

    A quick bastardization of the Python CSV library.

    Arguments:

        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.

    Example usage:

        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));

    """
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = path.join(
         output_path,
         output_name_template  % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = path.join(
               output_path,
               output_name_template  % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


f_names = []
for f_name in listdir("."):
    if 'idle_' in f_name:
        f_names.append(f_name)

for f_name in f_names:
    print('Working on {}.'.format(f_name))
    split(open(f_name, 'r'))
    for o_name in listdir("."):
        if 'output_' in o_name:
            rename(o_name, o_name.replace('output', f_name[:-4]))
    remove(f_name)
