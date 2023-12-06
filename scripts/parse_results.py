import os
import pathlib
import csv


def get_block_id_from_line(line: str):
    split_line = line.strip().split(',')
    assert len(split_line) == 4
    return (split_line[1], split_line[3])


def get_block_lineno_from_line(line: str):
    split_line = line.strip().split(',')
    assert len(split_line) == 8
    return (split_line[1], split_line[-2], split_line[-1])


def get_filepath_from_line(line: str):
    split_line = line.strip().split(',')
    assert len(split_line) == 9
    return split_line[2].strip('"')


def parse_clones():
    res_filepath = pathlib.Path(os.getcwd(), 'results.pairs')
    fields = ['block_id_1', 'block_id_2']
    rows = []
    print(f'reading {res_filepath}...')
    with open(res_filepath, 'r') as res_file:
        for line in res_file.readlines():
            rows.append(get_block_id_from_line(line))
    print(f'finished reading {res_filepath}...')

    print('writing clones.csv...')
    with open('clones.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
    print('finished writing clones.csv...')


def parse_block_stats():
    stats_dir = pathlib.Path(os.getcwd(), 'file_block_stats')

    fields = ['filepath', 'block_id', 'block_begin', 'block_end']
    rows = []

    # parse file stats
    for stats_file in os.listdir(stats_dir):
        i_filepath = pathlib.Path(stats_dir, stats_file)
        print(f'reading {i_filepath}...')
        with open(i_filepath, 'r') as i_file:
            last_filepath = ""
            for line in i_file.readlines():
                if line.startswith('f'):
                    last_filepath = get_filepath_from_line(line)
                elif line.startswith('b'):
                    (block_id, block_begin, block_end) = get_block_lineno_from_line(line)
                    rows.append([last_filepath, block_id, block_begin, block_end])
        print(f'finished reading {i_filepath}...')

    print('writing stats.csv...')
    with open('stats.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
    print('finished writing stats.csv...')


if __name__ == "__main__":
    parse_block_stats()
    parse_clones()
