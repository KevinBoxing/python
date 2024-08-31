# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database

dbname = get_database()

# Create a new collection
collection_name = dbname["user_1_items"]

# Create an index on the collection
category_index = collection_name.create_index("category")