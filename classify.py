import argparse
import os.path
from clean import Cleaner
from count import Counter

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file {} does not exist!".format(arg))
    return arg 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OpsGenie Alert Classifier")
    parser.add_argument('file', type=lambda x: is_valid_file(parser, x),
                        metavar='FILE', help='file to work with')
    parser.add_argument("--clean", nargs='+', dest="clean",
                        help="create a 'clean' file with whitelisted columns a raw file")
    parser.add_argument("--remove", nargs='+', dest="remove",
                        help="Match rows to remove based the 'Message' column")
    parser.add_argument("--count", nargs='?', dest="count", default="all", const="all",
                        help="count of alerts grouped by specified column name (default: count of all)")
    parser.add_argument("--limit", nargs='?', dest="limit", default=20, const=20, type=int,
                        help="limit number of results returned (default: 20)")
    parser.add_argument("--interval", nargs='+', dest="interval",
                        help="Time interval in hours to filter alerts")
    parser.add_argument("--match", nargs='?', dest="match", default=None, const=None,
                        help="Regex match against specified column name for count")
    parser.add_argument("--update-minutes", nargs='?', dest="update_minutes", default=None, const=None,
                        help="Number of minutes between 'CreatedAt' and 'UpdatedAt'")
    args = parser.parse_args()

    if args.clean:
        if not args.file.endswith("raw.csv"):
            parser.error("The file {} does not end with 'raw.csv'".format(args.file))
        Cleaner.clean(args.file, args.clean, args.remove)
    elif args.count:
        Counter.count(args.file, args.count, args.limit, args.interval, args.match, args.update_minutes)