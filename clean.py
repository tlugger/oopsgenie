import csv
from utils import get_valid_colum_indices

class Cleaner():

    def clean(file, clean_columns, remove):
        print ("Cleaning {}".format(file))
        print ("For columns {}".format(clean_columns))

        new_file = file[0:-7] + "clean.csv"

        with open(file, 'r') as raw_file:
            reader = csv.reader(raw_file, delimiter=',')
            headers = next(reader)

            col_count = len(clean_columns)

            if remove:
                clean_columns.append("Message")
            
            indices = get_valid_colum_indices(headers, clean_columns)
            if indices is None:
                print ("invalid column specified for in {}".format(file))
                return

            with open(new_file, 'w') as clean_file:
                writer = csv.writer(clean_file, delimiter=',')
                writer.writerow(clean_columns)
                for row in reader:
                    if remove:
                        blacklisted = False
                        for r in remove:
                            if r in row[indices[-1]]:
                                blacklisted = True
                        if blacklisted:
                            continue
                    cleaned_row = []
                    for i in range(col_count):
                        cleaned_row.append(row[indices[i]])
                    writer.writerow(cleaned_row)
        print("Done")