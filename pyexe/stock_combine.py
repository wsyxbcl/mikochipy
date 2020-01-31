# import datetime
import os
import re
from pathlib import Path

import pandas as pd

from dir_walker import walker

aimed_path - ""
saved_filename = "" # save to excel by default

working_path = Path(aimed_path)

for i, (filename, subdir) in enumerate(walker(working_path, pattern=re.compile('.*?.txt'))):
    print("reading "+filename)
    with open(Path(subdir).joinpath(Path(filename)), 'r') as fp:
    head = fp.readline()
    stock_name = head[7:11]
    print(stock_name)
    # Skip first two lines and the last line
    data_csv = pd.read_csv(Path(subdir).joinpath(Path(filename)), skiprows=2, header=None, encoding='gbk')[:-1]
    # extract the first and the 5th column
    data_csv = data_csv.loc[:, [0, 4]]
    # data_csv.columns = ['date', filename[:-4]]
    data_csv_t = data_csv.transpose()
    header_date = data_csv_t.iloc[0]
    data_csv_t = data_csv_t[1:]
    data_csv_t.columns = header_date
    data_csv_t['stock'] = filename[:-4]
    data_csv_t['name'] = stock_name

    cols = data_csv_t.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_csv_t = data_csv_t[cols]
    if i == 0:
        data_csv_all = data_csv_t
    else:
        data_csv_all = data_csv_all.append(data_csv_t, ignore_index=True, sort=False)

data_csv_all.to_excel(working_path.joinpath(Path(saved_filename)))
