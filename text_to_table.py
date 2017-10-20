import argparse
import sqlite3

import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--format', choices=['excel', 'sqlite'], required=True)
    parser.add_argument('--output')

    args = parser.parse_args()
    filename = args.output

    df = pd.read_csv(args.input, sep='|')

    if args.format == 'excel':
        if filename is None:
            filename = 'output.xlsx'
        writer = pd.ExcelWriter(filename)
        df.to_excel(writer, 'Sheet1')
        writer.save()

    if args.format == 'sqlite':
        if filename is None:
            filename = 'output.sqlite3'
        df.to_sql('result', sqlite3.connect(filename), if_exists='replace')
