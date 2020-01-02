## OpsGenie Alert Classifier
Helpful functions for analyzing an export of OpsGenie alerts and collecting useful data on them.

### Functions
* Clean **(--clean _cloumn1_ _column2_ _..._)**
    * Specify rows from a *raw.csv file into a *clean.csv file
    * Remove **(--remove _keyword1_ _keyword2_ _..._)**
        * A keyword to filter each cleaned row against. Matches on any value in the 'Message' column.
* Count **(--count _column_)**
    * Count the number of alerts matching a specified column name. Passing a column name of "all" will return the total count of alerts
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
* Fuzzy Count **(--fuzzy-count _column_)**
    * Count the number of alerts for a specified column name using fuzzy matching.
    * Threshold **(--threshold _threshold_)**
        * A threshold of tolerance for fuzzy matching on your --fuzzy-count. This is based on Levenshtein Distance; Default to 90.
    * Remove Numbers **(--remove-numbers _boolean_)**
        * Remove numbers from the alert alias before performing fuzzy matching in --count. This defaults to False and should be used in conjunction with the fuzzy threshold flag.
    * Alias Strip List File **(--alias-strip-list _csv_)**
        * Remove strings from the alert alias before performing matching in --fuzzy-count. Input for this flag is a csv without headers that contains a single column of strings to strip out of the alias (e.g. server names).


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

Usage Examples:
```bash
# Clean alert-data-raw.csv to only include the columns "Alias", "CreatedAtDate", and "Teams" (creates alert-data-clean.csv)
python oopsgenie.py alert-data-raw.csv --clean Alias CreatedAtDate Teams

# Clean alert-data-raw.csv to only include the column "Alias", "CreatedAtDate", and "Teams" but exclude any message containing "staging"
python oopsgenie.py alert-data-raw.csv --clean Alias CreatedAtDate Teams --remove staging

# Get a count of all alerts
python oopsgenie.py alert-data-raw.csv --count

# Get a count of alerts grouped by the column "Alias"
python oopsgenie.py alert-data-raw.csv --count Alias

# Get a count of alerts grouped by the column "Alias" with server names stripped out
python oopsgenie.py alert-data-raw.csv --count Alias --alias-strip-list server_names.csv

# Get a count of alerts grouped by the column "Alias" and with a fuzzy matching threshold of 80%
python oopsgenie.py alert-data-raw.csv --fuzzy-count Alias --threshold 80

# Get a count of alerts grouped by the column "Alias" and with a fuzzy matching threshold of 90% and numbers removed from the alias before the fuzzy matching
python oopsgenie.py alert-data-raw.csv --fuzzy-count Alias --threshold 90 --remove-numbers True

# Get a count of all alerts grouped by the column "Alias" that are created between the hours of 04 and 13 (UTC)
python oopsgenie.py alert-data-raw.csv --count Alias --interval 4 13

# Get a count of all alerts grouped by the column "Alias" that match the keyword "gdpr"
python oopsgenie.py alert-data-raw.csv --count Alias --match gdpr

# Get a count of all alerts grouped by the column "Alias" that updated within 5 minutes of creation
python oopsgenie.py alert-data-raw.csv --count Alias --update-minutes 5

# Get a count of alerts grouped by the column "Alias" and store in a file named "alias-count.csv
python oopsgenie.py alert-data-raw.csv --count Alias --outfile alias-count.csv
```
