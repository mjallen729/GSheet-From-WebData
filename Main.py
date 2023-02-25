from WebScrapers import AirBNBWishlist
from API import GoogleSheets
import pandas as pd

# Run hourly to check for updates and serve them to the spreadsheet
def check_for_updates(spreadsheet, workbook_name, link):
    dao = GoogleSheets.DataObject()

    local_data = dao.pull_data(spreadsheet, workbook_name)  # data from Spreadsheet
    server_data = AirBNBWishlist.fetch(link, write= True)  # data from AirBNB server

    print('Checking for changes...')

    try:
        diff = local_data.compare(server_data)

        if len(diff) != 0:
            print('Value change found!')

            # log changes from compare
            try:
                changes = pd.read_csv('./exports/changelog.csv').drop(0, axis=1)

            except:
                changes = pd.DataFrame(columns=['Listing','Col','Change'])

            cols = diff.columns.tolist()
            rows = diff.values.tolist()
            listings = diff.index.tolist()

            for l in range(len(listings)):
                for c in range(0, len(cols), 2):
                    # c = (col_name, self/other)
                    data = list()
                    data.append(listings[l])
                    data.append(cols[c][0])

                    oldval = rows[l][c]
                    newval = rows[l][c + 1]

                    try:
                        float(oldval)
                        float(newval)

                        if str(oldval) != 'nan':
                            net = newval - oldval
                            data.append(net)

                            changes.loc[l] = data

                    except Exception as e:
                        continue

            changes.to_csv('./exports/changelog.csv')

        else:
            print('No change found.')

    except:
        print('Structure change found! (error thrown)')

    finally:
        dao.push_data(spreadsheet, workbook_name)
        #dao.push_data(spreadsheet,'changes','./exports/changelog.csv')

spreadsheet = '1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk'
workbook = 'available_listings'
wishlist_link = 'https://www.airbnb.com/wishlists/v/1250433647?s=67&unique_share_id=26a5887d-15af-4bc3-92ef-fa74ea9da81f'

check_for_updates(spreadsheet, workbook, wishlist_link)