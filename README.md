## OpsGenie Alert Classifier
Helpful functions for analyzing an export of OpsGenie alerts and collecting useful data on them.

### Functions
* Clean **(--clean _cloumn1_ _column2_ _..._)**
    * Specify rows from a *raw.csv file into a *clean.csv file
    * Remove **(--remove _keyword1_ _keyword2_ _..._)**
        * A keyword to filter each cleaned row against. Matches on any value in the 'Message' column.
* Count **(--count _column_)**
    * Count the number of alerts matching a specified column name (default all alerts in csv). If no column is specified, return the total count of alerts
    * Limit **(--limit _limit_)**
        * Limit the number of results returned, ordered by count highest to lowest
    * Time Interval Filtering **(--interval _hour1_ _hour2_)**
        * An interval to filter the "CreatedAtDate" hour of each alert. This can be added to count.
    * Keyword matching **(--match _keyword_)**
        * A keyword to filter the specified --count column against
    * Minutes between update **(--update-minutes _minutes_)**
        * A filter matching alerts that update within x minutes (between "CreatedAt" and "UpdatedAt" timestamps)
    * Output file **(--outfile _filename_)**
        * A file to output the results of --count
    * Fuzzy Threshold **(--fuzzy-threshold _threshold_)**
        * A threshold of tolerance for fuzzy matching on your --count. This is based on Levenshtein Distance; If you don't set this parameter, it will default to perfect matches. 
    * Remove Numbers **(--remove-numbers _boolean_)**
        * Remove numbers from the alert alias before performing fuzzy matching in --count. This defaults to False and should be used in conjunction with the fuzzy threshold flag.
    * Alias Strip List File **(--alias-strip-list _csv_)**
        * Remove strings from the alert alias before performing matching in --count. Input for this flag is a csv without headers that contains a single column of strings to strip out of the alias (e.g. server names).


**Note:** `limit`, `interval`, `match` and `outfile` can all be chained to filter results of `count`. If `outfile` is specified `limit` is ignored.

### Future functionality
* TBD

### Running
This requires Python3
```
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```


Example usage:
- Clean alert-data-raw.csv to only include the columns "Alias", "CreatedAtDate", and "Teams" (creates alert-data-clean.csv)
```
python main.py alert-data-raw.csv --clean Alias CreatedAtDate Teams
```

- Clean alert-data-raw.csv to only include the column "Alias", "CreatedAtDate", and "Teams" but exclude any message containing "staging"
```
python main.py alert-data-raw.csv --clean Alias CreatedAtDate Teams --remove staging
```

- Get a count of all alerts
```
python main.py alert-data-raw.csv --count
```

- Get a count of alerts grouped by the column "Alias"
```
python main.py alert-data-raw.csv --count Alias
```

- Get a count of alerts grouped by the column "Alias" with server names stripped out
```
python main.py alert-data-raw.csv --count Alias --alias-strip-list server_names.csv
```

- Get a count of alerts grouped by the column "Alias" and with a fuzzy matching threshold of 90%
```
python main.py alert-data-raw.csv --count Alias --fuzzy-threshold 90
```

- Get a count of alerts grouped by the column "Alias" and with a fuzzy matching threshold of 90% and numbers removed from the alias before the fuzzy matching
```
python main.py alert-data-raw.csv --count Alias --fuzzy-threshold 90 --remove-numbers True
```

- Get a count of all alerts grouped by the column "Alias" that are created between the hours of 04 and 13 (UTC)
```
python main.py alert-data-raw.csv --count Alias --interval 4 13
```

- Get a count of all alerts grouped by the column "Alias" that match the keyword "gdpr"
```
python main.py alert-data-raw.csv --count Alias --match gdpr
```

- Get a count of all alerts grouped by the column "Alias" that updated within 5 minutes of creation
```
python main.py alert-data-raw.csv --count Alias --update-minutes 5
```

- Get a count of alerts grouped by the column "Alias" and store in a file named "alias-count.csv
```
python main.py alert-data-raw.csv --count Alias --outfile alias-count.csv
```