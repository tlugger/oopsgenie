import csv
from datetime import datetime
from utils import get_valid_colum_indices
from fuzzywuzzy import fuzz


class Counter(object):

    def count(self, file, column, limit, interval, match, fuzzy_thresh, remove_numbers, update_minutes, outfile):
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

                current_count = count_map.get(row[index], 0)
                if current_count != 0:
                    current_count = current_count.get('count')
                count_map[row[index]] = {"count": (current_count + 1), "fuzzy": False}

        # if the fuzzy threshold is set to 100% match, we can skip this
        # O Notation murdering step
        if fuzzy_thresh < 100:
            # Get a list of the keys in the count_map
            # Then see if any are a fuzzy match
            count_map = self.count_fuzzy_matches(count_map, fuzzy_thresh, remove_numbers)

        alert_list = sorted(count_map.items(), 
                            reverse=True)

        if not outfile:
            for alert, num in alert_list:
                if limit <= 0:
                    break
                print("{}: {}".format(alert, num))
                limit -=1
        else:
            with open(outfile, 'w') as out:
                writer = csv.writer(out, delimiter=',')
                writer.writerow([column, "Count", "Includes Fuzzy Matches"])
                for row in alert_list:
                    row_to_write = (row[0], row[1].get("count"), row[1].get("fuzzy"))
                    writer.writerow(row_to_write)
            print("Done")

    @classmethod
    def count_fuzzy_matches(self, count_map, fuzzy_thresh, remove_numbers):
        alert_keys = list(count_map.keys())
        skip_list = []
        for key, val in count_map.items():
            if key not in skip_list:
                for alert_key in alert_keys:
                    if remove_numbers:
                        new_key = ''.join([i for i in key if not i.isdigit()])
                        new_alert_key = ''.join([i for i in alert_key if not i.isdigit()])
                    else:
                        new_key = key
                        new_alert_key = alert_key
                    fuzzy_match_ratio = fuzz.ratio(new_key, new_alert_key) 
                    if fuzzy_match_ratio >= fuzzy_thresh:
                        if key != alert_key:
                            count_map[key] = {"count": (count_map[key]['count'] + count_map[alert_key]['count']), "fuzzy": True}
                            skip_list.append(alert_key)
        for skip in skip_list:
            if count_map.get(skip):
                del count_map[skip]

        return count_map
