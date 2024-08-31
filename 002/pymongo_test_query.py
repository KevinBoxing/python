from pymongo_get_database import get_database

dbname = get_database()

# Retrieve a collection named "user_1_items" from database
collection_name = dbname["user_1_items"]
from pandas import DataFrame
item_details = collection_name.find()
# convert the dictionary objects to dataframe
items_df = DataFrame(item_details)

# see the magic
print(items_df)
# for item in item_details:
#     # This does not give a very readable output
#     #print(item)
#     print(item['item_name'], item['category'])