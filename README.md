## OpsGenie Alert Classifier
Helpful functions for analyzing an export of OpsGenie alerts and collecting useful data on them.

### Functions
* Clean *(--clean _cloumn1_ _column2_ _..._)*
  * Specify rows from a *raw.csv file into a *clean.csv file
* Count *(--count _column_)*
  * Count the number of alerts matching a specified column name (default Alias). If no column is specified, return the total count of alerts
* Limit *(--limit _limit_)*
  * Limit the number of results returned, ordered by count highest to lowest
* Time Interval Filtering *(--interval _hour1_ _hour2_)*
  * An interval to filter the "CreatedAtDate" hour of each alert. This can be added to count.
* Keyword matching *(--match _keyword_)*
  * A keyword to filter the specified --count column against
* Minutes between update *(--update-minutes _minutes_)*
  * A filter matching alerts that update within x minutes (between "CreatedAt" and "UpdatedAt" timestamps)

### Future functionality
* TBD

### Running
This requires Python3
```
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```


Example usage:
- Clean alert-data-raw.csv to only include the columns "Alias", "Message", and "Teams"
```
python classify.py alert-data-raw.csv --clean Alias Message Teams
```

- Get a count of all alerts
```
python classify.py alert-data-raw.csv --count
```

- Get a count of alerts grouped by the column "Alias"
```
python classify.py alert-data-raw.csv --count Alias
```

- Get a count of all alerts grouped by the column "Alias" that are created between the hours of 04 and 13 (UTC)
```
python classify.py alert-data-raw.csv --count Alias --interval 4 13
```

- Get a count of all alerts grouped by the column "Alias" that match the keyword "gdpr"
```
python classify.py alert-data-raw.csv --count Alias --match gdpr
```

- Get a count of all alerts grouped by the column "Alias" that updated within 5 minutes of creation
```
python classify.py alert-data-tier1-raw.csv --count Alias --update-minutes 5
```