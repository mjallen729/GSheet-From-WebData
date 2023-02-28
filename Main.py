# Assign these three variables
spreadsheet = ''  # spreadsheet ID from the URL
workbook = 'available_listings'  # name of the workbook (ie 'Sheet1')
wishlist_link = 'https://www.airbnb.com/wishlists/v/1250433647?s=67&unique_share_id=26a5887d-15af-4bc3-92ef-fa74ea9da81f'  # link to your AirBNB wishlist


from WebScrapers import AirBNBWishlist
from API import GoogleSheets
import pandas as pd

# Checks for updates and serves them to the spreadsheet
def check_for_updates(spreadsheet, workbook_name, link):
    dao = GoogleSheets.DataObject()

    local_data = dao.pull_data(spreadsheet, workbook_name)  # data from Spreadsheet
    server_data = AirBNBWishlist.fetch(link, write= True)  # data from AirBNB server

    print('Checking for changes...')

    try:
        diff = local_data.compare(server_data)

        if len(diff) != 0:
            print('Value change found! [23]')

            # log changes from compare
            try:
                changes = pd.read_csv('./exports/changelog.csv')

            except:
                changes = pd.DataFrame(columns=['Listing','Col','Change (Net)'])

            print('Logging changes...')

            cols = diff.columns.tolist()
            rows = diff.values.tolist()
            listings = diff.index.tolist()

            for l in range(len(listings)):
                for c in range(0, len(cols), 2):
                    # c = (col_name, self/other)
                    data = list()
                    data.append(listings[l] + 1)
                    data.append(cols[c][0])

                    oldval = rows[l][c]
                    newval = rows[l][c + 1]

                    try:
                        float(oldval)
                        float(newval)

                        if str(oldval) != 'nan':
                            net = newval - oldval
                            data.append(net)

                            changes.loc[len(changes)] = data

                    except Exception as e:
                        continue

            changes.to_csv('./exports/changelog.csv', index=False)

        else:
            print('No change found.')
            return

    except:
        print('Structure change found! [67]')

    finally:
        dao.push_data(spreadsheet, workbook_name)
        dao.push_data(spreadsheet, 'describe', './exports/describe_listings.csv')

        try:
            open('./exports/changelog.csv')
            dao.push_data(spreadsheet,'changes','./exports/changelog.csv')

        except Exception as e:
            print('No changelog found!')

check_for_updates(spreadsheet, workbook, wishlist_link)