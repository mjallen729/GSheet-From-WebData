import gspread
from gspread_dataframe import set_with_dataframe
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

class DataObject:
    def __init__(self) -> None:
        self.cred = Credentials.from_service_account_file('../keys/service-acct.json',
                                                        scopes= scopes)
        self.gc = gspread.authorize(self.cred)
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
    
    def push_data(self, spreadsheet_key, worksheet_name):
        sheet = self.gc.open_by_key(spreadsheet_key)
        notebook = sheet.worksheet(worksheet_name)

        df = pd.read_csv('../exports/available_listings.csv')
        df = df.drop(df.columns[0], axis=1)
        set_with_dataframe(worksheet= notebook, dataframe= df, include_index= False,
                           include_column_header= True, resize= True)
        
        
        df2 = get_as_dataframe(notebook)
        print(df2)

if __name__ == '__main__':
    test = DataObject()
    test.push_data('1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk', 'remote')