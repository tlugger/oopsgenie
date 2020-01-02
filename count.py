import csv
from datetime import datetime
from utils import get_valid_colum_indices
from fuzzywuzzy import fuzz


class Counter(object):

    def count(self, file, column, limit, interval, match, update_minutes, outfile):
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
        
        return self.format_output(count_map, column, outfile, limit)

    @classmethod
    def format_output(self, count_map, column, outfile, limit, fuzzy=False):
        
        alert_list = sorted(count_map.items(), 
                            key = lambda kv:(kv[1], kv[0]), 
                            reverse=True)

        if not outfile:
            for alert, num in alert_list:
                if limit <= 0:
                    break
                print("{}: {}".format(alert, num))
                limit -=1
        else:
            output_file = 'fuzzy-' + outfile if fuzzy else outfile
            with open(output_file, 'w') as out:
                writer = csv.writer(out, delimiter=',')
                writer.writerow([column, "Count"])
                for row in alert_list:
                    writer.writerow(row)
            print("Done")

class FuzzyCounter(Counter):

    def count(self, file, column, limit, threshold, remove_numbers, outfile, alias_strip_list):
        strip_list = []
        if alias_strip_list:
            with open(alias_strip_list, 'rt', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                values_to_strip = list(csv_reader)
                strip_list = [item[0] for item in values_to_strip] 

        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)

            indices = get_valid_colum_indices(headers, [column])
            if indices is None:
                print ("invalid column specified for in {}".format(file))
                return
            
            index = indices[0]
            count_map = {}

            for row in reader:
                for strip in strip_list:
                    if strip in row[1]: 
                        row[1] = row[1].replace(strip, "")
                        break
                count_map[row[index]] = count_map.get(row[index], 0) + 1

        # if the fuzzy threshold is set to 100% match, we can skip this
        # O Notation murdering step
        if threshold < 100:
            # Get a list of the keys in the count_map
            # Then see if any are a fuzzy match
            count_map = self.count_fuzzy_matches(count_map, threshold, remove_numbers)

        return self.format_output(count_map, column, outfile, limit, fuzzy=True)

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
                            count_map[key] = count_map[key] + count_map[alert_key]
                            skip_list.append(alert_key)
        for skip in skip_list:
            if count_map.get(skip):
                del count_map[skip]

        return count_map