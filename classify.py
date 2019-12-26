import argparse
import csv
import os.path
from datetime import datetime


def clean(file, clean_columns):
    print ("Cleaning {}".format(file))
    print ("For columns {}".format(clean_columns))

    new_file = file[0:-7] + "clean.csv"

    with open(file, 'r') as raw_file:
        reader = csv.reader(raw_file, delimiter=',')
        headers = next(reader)
        
        indices = get_valid_colum_indices(headers, clean_columns)
        if indices is None:
            print ("invalid column specified for in {}".format(file))
            return

        with open(new_file, 'w') as clean_file:
            writer = csv.writer(clean_file, delimiter=',')
            writer.writerow(clean_columns)
            for row in reader:
                cleaned_row = []
                for i in indices:
                    cleaned_row.append(row[i])
                writer.writerow(cleaned_row)
    print("Done")

def count(file, column, limit, interval):
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        headers = next(reader)
        if column == 'all':
            print("Total number of alerts: {}".format(sum(1 for line in f)))
        
        cols = [column, "CreatedAtDate"] if interval else [column]
        indices = get_valid_colum_indices(headers, cols)
        if indices is None:
            print ("invalid column specified for in {}".format(file))
            return
        
        index = indices[0]
        count_map = {}

        for row in reader:
            if interval:
                if len(interval) != 2:
                    print ("invalid use of --interval, must give 2 values")
                # CreatedAtDate in this format 12/12/12 12:12:12.123-4567
                # cut off the last 9 values to properly parse
                dtime = datetime.strptime(row[indices[1]][0:-9], '%Y/%m/%d %H:%M:%S')
                if dtime.hour < int(interval[0]) or dtime.hour > int(interval[1]):
                    continue
            count_map[row[index]] = count_map.get(row[index], 0) + 1

    alert_list = sorted(count_map.items(),
                        key = lambda kv:(kv[1], kv[0]), 
                        reverse=True)

    for alert, num in alert_list:
        if limit <= 0:
            break
        print("{}: {}".format(alert, num))
        limit -=1
        

def get_valid_colum_indices(full_cols, specified_cols):
    indices = []
    for column in specified_cols:
            # Validate columns to extract
            if column not in full_cols:
                return None
            indices.append(full_cols.index(column))
    return indices

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file {} does not exist!".format(arg))
    return arg 

parser = argparse.ArgumentParser(description="OpsGenie Alert Classifier")
parser.add_argument('file', type=lambda x: is_valid_file(parser, x),
                    metavar='FILE', help='file to work with')
parser.add_argument("--clean", nargs='+', dest="clean", help="clean data from a raw file")
parser.add_argument("--count", nargs='?', dest="count", default="all", const="all",
                    help="count of alerts grouped by specified column name (default: count of all)")
parser.add_argument("--limit", nargs='?', dest="limit", default=20, const=20, type=int,
                    help="limit number of results returned (default: 20)")
parser.add_argument("--interval", nargs='+', dest="interval",
                    help="Time interval in hours to filter alerts")
args = parser.parse_args()

if args.clean:
    if not args.file.endswith("raw.csv"):
        parser.error("The file {} does not end with 'raw.csv'".format(args.file))
    clean(args.file, args.clean)
elif args.count:
    count(args.file, args.count, args.limit, args.interval)