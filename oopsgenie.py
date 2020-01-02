import argparse
import os.path
from clean import Cleaner
from count import Counter, FuzzyCounter

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file {} does not exist!".format(arg))
    return arg 


def main():
    parser = argparse.ArgumentParser(description="OpsGenie Alert Classifier")
    parser.add_argument('file', type=lambda x: is_valid_file(parser, x),
                        metavar='FILE', help='file to work with')
    parser.add_argument("--clean", nargs='+', dest="clean",
                        help="create a 'clean' file with whitelisted columns a raw file")
    parser.add_argument("--remove", nargs='+', dest="remove",
                        help="Match rows to remove based the 'Message' column")
    parser.add_argument("--count", nargs='?', dest="count", default=None, const=None,
                        help="count of alerts grouped by specified column name")
    parser.add_argument("--fuzzy-count", nargs='?', dest="fuzzy_count", default=None, const=None,
                        help="fuzzy count alerts grouped by specified column name")
    parser.add_argument("--limit", nargs='?', dest="limit", default=20, const=20, type=int,
                        help="limit number of results returned (default: 20)")
    parser.add_argument("--interval", nargs='+', dest="interval",
                        help="Time interval in hours to filter alerts")
    parser.add_argument("--match", nargs='?', dest="match", default=None, const=None,
                        help="Regex match against specified column name for count")
    parser.add_argument("--update-minutes", nargs='?', dest="update_minutes", default=None, const=None,
                        help="Number of minutes between 'CreatedAt' and 'UpdatedAt'")
    parser.add_argument("--outfile", nargs='?', dest="outfile", default=None, const=None,
                        help="Optional file to output results of count")
    parser.add_argument("--threshold", nargs='?', dest="threshold", default=90, const=90, type=int,
                        help="Threshold for alert fuzzy match (default: 100 - so 100% match)")
    parser.add_argument("--remove-numbers", nargs='?', dest="remove_numbers", default=False, const=None, type=bool,
                        help="Remove numbers from alias before doing fuzzy matching (default: False). \
                        To be used in conjuction with the fuzzy threshold flag")
    parser.add_argument('--alias-strip-list', type=lambda x: is_valid_file(parser, x),
                        dest='strip_file', help='csv file with a column of values to strip', metavar="FILE")
    args = parser.parse_args()

    if args.clean:
        if not args.file.endswith("raw.csv"):
            parser.error("The file {} does not end with 'raw.csv'".format(args.file))
        Cleaner.clean(args.file, args.clean, args.remove)
    elif args.count:
        counter = Counter()
        counter.count(file=args.file, column=args.count, limit=args.limit, interval=args.interval,
                      match=args.match, update_minutes=args.update_minutes, outfile=args.outfile)
    elif args.fuzzy_count:
        fuzzy_counter = FuzzyCounter()
        fuzzy_counter.count(file=args.file, column=args.fuzzy_count, limit=args.limit, threshold=args.threshold, 
                            remove_numbers=args.remove_numbers, outfile=args.outfile,
                            alias_strip_list=args.strip_file)

if __name__ == "__main__":
    main()