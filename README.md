# Hw03
# Ebay datascaper
## In this project, I created a file that will take your inputed searchterm, collect the data from the first 10 pages of your search term, and download a dictionary of each item's Name, status, shipping price,item price, & number of items sold onto a json file or a csv file depending on what your input in the command line.  


### Json
For example, if you want to extract the data of the search term: shovel, your input should be

```
python3 ebay-dl.py 'shovel'   
```

if you want to extract the data of the search term: bucket hat, your input should be

```
python3 ebay-dl.py 'bucket hat'   
```

if you want to extract the data of the search term: hat, your input should be

```
python3 ebay-dl.py 'hat'   
```

### CSV

if you want to extract the data of the search term: bike, your input should be

```
python3 ebay-dl.py 'bike' --csv
```

if you want to extract the data of the search term: basket ball, your input should be

```
python3 ebay-dl.py 'basket ball' --csv   
```

if you want to extract the data of the search term: speaker, your input should be

```
python3 ebay-dl.py 'speaker' --csv   
```
