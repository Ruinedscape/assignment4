import pymongo
import mysql.connector

def setup_mySQLdb():
    connection = mysql.connector.connect( # connecting to mySQL
        host="localhost",
        user="root",
        passwd="" # change this to your password
        )
    cursor = connection.cursor()

    # creating a database called database4
    cursor.execute("CREATE DATABASE database4")
    connection.close()
    cursor.close()

    connection = mysql.connector.connect( # connecting to the database4
        host="localhost",
        user="root",
        passwd="", # change this to your password
        database="database4"
        )
    cursor = connection.cursor()
    
    # creating a table
    create_customer_table = """
    CREATE TABLE database4.customer (
      cid INT PRIMARY KEY,
      first_name VARCHAR(40) NOT NULL,
      last_name VARCHAR(40) NOT NULL,
      address VARCHAR(40)
    );
    """

    cursor.execute(create_customer_table)
    connection.commit()
    
    # populating the table
    pop_customer = """
    INSERT INTO database4.customer VALUES
    (1, 'Aurora', 'Wade', 'Sideway 13'),
    (2, 'Isaac', 'Klein', 'Main Road 23'),
    (3, 'Ruby', 'Page', 'Park Lane 21'),
    (4, 'Joshua', 'Hale', 'Yellow Garden 2');
    """
    
    cursor.execute(pop_customer)
    connection.commit()

def setup_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["db1"] # creating a database
    col = db["orders"] # creating a collection (table)

    orders = [ # populating the collection
        { "_id": 10531, "customer_id": 2, "total": 37},
        { "_id": 10532, "customer_id": 2, "total": 23},
        { "_id": 10533, "customer_id": 4, "total": 60},
        { "_id": 10534, "customer_id": 3, "total": 5},
    ]

    col.insert_many(orders)
    client.close()

setup_mongodb()
setup_mySQLdb()
