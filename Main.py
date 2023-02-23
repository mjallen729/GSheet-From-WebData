import Crawler
from API import GoogleSheets
import pandas as pd

# Runs hourly to check for updates and serve them to the spreadsheet
def check_for_updates(spreadsheet, workbook_name):
    dao = GoogleSheets.DataObject()

    local_data = dao.pull_data(spreadsheet, workbook_name)
    server_data = Crawler.fetch(write= True)

    diff =1 #local_data.compare(server_data)

    if diff != 0:
        print('Change found!')
        dao.push_data(spreadsheet, workbook_name)

spreadsheet = '1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk'
workbook = 'remote'
check_for_updates(spreadsheet, workbook)