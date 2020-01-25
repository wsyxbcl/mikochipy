#!/usr/bin/python3
import argparse
from pathlib import Path

import pandas as pd

def main(path, cycle):
    df = pd.read_excel(path, sheet_name=3, usecols=[1, 3, 6, 7])
    df_filtered = df.loc[(df['状态']=="恒流放电") & (df['循环']==10)]
    aimed_v_c = df_filtered.iloc[:, 2:]
    aimed_v_c.to_csv(path.with_suffix('').as_posix()+'_cycle{}_v_c.csv'.format(cycle),
                     header=False, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="extract V and C of one cycle")
    parser.add_argument(dest='data_path', type=Path, 
                        help="Path of the aimed .xlsx file")
    parser.add_argument('-c', '--cycle', dest='cycle',metavar='#cycle', 
                        required=True, type=int, help="Aimed number of cycle (int)")
    args = parser.parse_args()
    main(args.data_path, args.cycle)