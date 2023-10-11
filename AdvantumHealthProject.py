from square.client import Client
import sqlite3
from sqlite3 import Error
import pandas as pd

#Taking code from Excel to Pandas Dataframe
print("\nConverting Excel to Dataframe")

customers = pd.read_excel(
    '/Users/maxni/Book 1.xlsx', #Name of the file and path
    sheet_name='Customers',                    #Name of the spreadsheet 
    header=0)                                  #1st row is column headers
print(customers)

print("\nInserting the Pandas Dataframe values into SQLITE")
connection = sqlite3.connect('/Users/maxni/sqlite/Atest.db')
customers.to_sql(name = "customers", con = connection, if_exists = "replace", index = False, 
                 dtype = {'Name':'text', 'Email': 'text', 'Age':'real', 'Birthday':'text'})

try:
        client = Client(
        access_token='EAAAEGFw0C8A9NqyXNl2kHv0GwTr1UW57AraQdI6Oi6L1X7aRpI_yfJ9p6QbSe-1',
        environment='sandbox')
except  Exception as err:
        print('error while connecting' + err)
        



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_customers(conn):
    """
    Query all rows in the customer table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customers")

    rows = cur.fetchall()

    for row in rows:
        email = row[1]
        checkCustomers(email, row)
        print(row)
        
def checkCustomers(email, row):
    result = client.customers.search_customers(
        body = {
        "query": {
          "filter": {
            "email_address": {
              "exact": email
                              }
                    }
                 }
                }
            )
    if len(result) > 0:
        print("found")
    else:
        names = row[0].split(" ")
        result = client.customers.create_customer(
        body = {
            "idempotency_key": "59973bb6-75ae-497a-a006-b2490example",
            "given_name": names[0],
            "family_name": names[1],
            "company_name": "Hudson MD Group",
            "email_address": row[1],
            "phone_number": row[2]
                }
                )

        if result.is_success():
            print(result.body)
        elif result.is_error():
            print(result.errors)


def main():
    database = r"C:\Users\maxni\sqlite\Atest.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("2. Query all customers")
        select_all_customers(conn)



main()