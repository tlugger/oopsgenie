import csv
from datetime import datetime
from utils import get_valid_colum_indices


class Counter:

    def count(file, column, limit, interval, match, update_minutes):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            if column == 'all':
                print("Total number of alerts: {}".format(sum(1 for line in f)))
            
            cols = [column, "CreatedAtDate"] if interval else [column]
            if update_minutes:
                cols.extend(["CreatedAt", "UpdatedAt"])
            indices = get_valid_colum_indices(headers, cols)
            if indices is None:
                print ("invalid column specified for in {}".format(file))
                return
            
            index = indices[0]
            count_map = {}

            for row in reader:
                if match:
                    if match not in row[index]:
                        continue
                if update_minutes:
                    ms_to_update = float(row[indices[-1]]) - float(row[indices[-2]])
                    min_to_update = ms_to_update/1000/60
                    if min_to_update > int(update_minutes):
                        continue
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