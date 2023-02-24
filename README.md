# Vacation-Planner
Using google sheets API, Pandas, and Selenium to create auto-updating spreadsheet with AirBNB rental data.

## Installation
`git clone` the repo and `cd` to the directory.

`pip install -r requirements.txt` to install the dependencies. I highly recommend using a python virtual environment-- find out how to do so here: https://docs.python.org/3/tutorial/venv.html

You then need to create a service account in Google Cloud, share your Google Sheets document with it, and get your credentials file. I followed this tutorial (steps 1-3): https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0

NOTE: Once you get your service account credentials file, rename it `credentials.json` and put it in the `keys` folder.

## Usage
In `main.py`: change `spreadsheet` to the spreadsheet ID. It'll be in the URL: docs.google.com/spreadsheets/d/{SHEET ID}/...

Change `workbook` to the name of your workbook.

Finally, set `wishlist_link` to a link to your AirBNB Wishlist.

Now you're good to go-- just run `main.py`
