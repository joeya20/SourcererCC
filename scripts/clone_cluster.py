from argparse import ArgumentParser
import re
import os
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pathlib

re_pattern = r"(?P<proj_id_1>[0-9]+),(?P<block_id_1>[0-9]+),(?P<proj_id_2>[0-9]+),(?P<block_id_2>[0-9]+)"
clusters = dict()


def get_snippet(filepath, snippet_start, snippet_end):
    with open(filepath[str(filepath).find('.zip/')+5:]) as src:
        lines = src.readlines()
        return "\n".join(lines[int(snippet_start)-1:int(snippet_end)]).strip()


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


def parse_block_stats():
    stats_dir = pathlib.Path(os.getcwd(), 'file_block_stats')

    fields = ['filepath', 'block_id', 'block_begin', 'block_end', 'snippet']
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
                    snippet = get_snippet(last_filepath, block_begin, block_end)
                    rows.append([last_filepath, block_id, block_begin, block_end, snippet])
        print(f'finished reading {i_filepath}...')

    print('writing stats.csv...')
    with open('output/stats.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
    print('finished writing stats.csv...')


def process_csv(df=None):
    if df is None:
        df = pd.read_csv('out.csv', index_col=0)
    else:
        print(df.describe())
        ax = sns.countplot(df, x='len')
        ax.set_yscale('log')
        plt.tight_layout()
        plt.show()
        print(df.nlargest(5, 'len'))


def gen_csv(filepath: str):
    with open(filepath, 'r') as ifile:
        while True:
            line = ifile.readline()
            if not line:   # break on EOF
                break
            match = re.match(re_pattern, line)
            if match is None:
                raise ValueError(f'invalid line: {line}')
            groups = match.groupdict()
            for item in groups.values():
                if item is None:
                    raise ValueError(f'invalid line: {line}')

            # create directed graph
            # this is necessary because not all clone pairs will necessarily
            # have matching clones
            block_id_1 = int(groups['block_id_1'])
            block_id_2 = int(groups['block_id_2'])
            if block_id_1 in clusters:
                clusters[block_id_1].add(block_id_2)
            else:
                clusters[block_id_1] = set([block_id_2])
            if block_id_2 in clusters:
                clusters[block_id_2].add(block_id_1)
            else:
                clusters[block_id_2] = set([block_id_1])

    tmp_list = []
    for k, v in clusters.items():
        clone_class = [k] + list(v)
        clone_class.sort()
        tmp_list.append(str(clone_class))
    print(tmp_list[0])
    df = pd.DataFrame(zip(tmp_list), columns=['clones'])
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df['len'] = df['clones'].apply(lambda x: len(json.loads(x)))
    df.to_csv('out.csv')
    return df


def main():
    arg_parser = ArgumentParser("Clone Cluster")
    arg_parser.add_argument('--path', '-p', action='store', type=str, default='results.pairs')
    args = arg_parser.parse_args()
    filepath = args.path
    if not os.path.isfile(filepath):
        raise ValueError('Invalid results.pair path')
    df = gen_csv(filepath)
    process_csv(df)


if __name__ == '__main__':
    main()
