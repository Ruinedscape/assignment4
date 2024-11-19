import maskpass
import pymongo
import mysql.connector

def menu():
    print("\n1) Print tables")
    print("2) Insert data")
    print("3) Delete data")
    print("4) Modify data")
    print("0) Exit")

def connectdb(host_name, user_name, user_password, db_name):
    mySQL_conn = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name
    )
    noSQL_conn = pymongo.MongoClient("mongodb://localhost:27017/")
    
    return mySQL_conn, noSQL_conn

def main():
    mySQL_host_name = "localhost"
    mySQL_user_name = "root"
    mySQL_user_password = maskpass.askpass(mask="*")
    mySQL_db_name = "database4"

    # connecting to databases
    mySQL_conn, noSQL_conn = connectdb(mySQL_host_name, mySQL_user_name, mySQL_user_password, mySQL_db_name)
    cursor = mySQL_conn.cursor() # cursor for mySQL

    # defining noSQL database and collection (table)
    db = noSQL_conn["db1"]
    col = db["orders"]
    
    while True:
        menu()
        menu_input = input("Select what to do: ")

        if menu_input == "1": # printing data
            db_input = input("Choose a database ([1]SQL, [2]noSQL, [3]Both): ")

            if db_input == "1": # printing from mySQL
                cursor.execute("SELECT * FROM database4.customer")
                print("(cid, first_name, last_name, address)")
                for table in cursor.fetchall():
                    print(table)
                            
            elif db_input == "2": # printing from mongoDB
                entries = col.find()
                for entry in entries:
                    print(entry)
                
            elif db_input == "3": # join the tables from both
                all_entries = []

                # appending all entries from customers (mySQL)
                cursor.execute("SELECT * FROM database4.customer")
                for table in cursor.fetchall():
                    all_entries.append(list(table))

                # listing all orders (noSQL)
                order_entries = list(col.find())

                # combining lists where customer ids match
                for customer in all_entries:
                    for order in order_entries:
                        if customer[0] == order["customer_id"]:
                            customer.append(order["_id"])
                
                for entry in all_entries: 
                    print(entry)

        elif menu_input == "2": # inserting data
            db_input = input("Choose a database ([1]SQL, [2]noSQL): ")

            if db_input == "1": # inserting to mySQL
                cid = int(input("Enter the customer id: "))
                first_name = input("Enter the first name: ")
                last_name = input("Enter the last name: ")
                address = input("Enter the address: ")
                new_entry = (cid, first_name, last_name, address)
                
                insert_query = "INSERT INTO database4.customer (cid, first_name, last_name, address) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, new_entry)
                
            elif db_input == "2": # inserting to mongoDB
                order_id = int(input("Enter the order id: "))
                customer_id = int(input("Enter the customer id of the order: "))
                total = int(input("Enter the total of this order: "))
                col.insert_one({"_id": order_id, "customer_id": customer_id, "total": total})
                
        elif menu_input == "3": # deleting data
            db_input = input("Choose a database ([1]SQL, [2]noSQL): ")

            if db_input == "1": # deleting from mySQL
                cid = int(input("Enter the customer id: "))
                delete_query = "DELETE FROM database4.customer WHERE cid = (%s)"
                cursor.execute(delete_query, (cid,))
                
            elif db_input == "2": # deleting from mongoDB
                deleted_order = int(input("Enter the order id of the order to be deleted: "))
                col.delete_one({"_id": deleted_order})
            
        elif menu_input == "4": # modifying data
            db_input = input("Choose a database ([1]SQL, [2]noSQL): ")

            if db_input == "1": # modifying data in mySQL
                modified_customer = int(input("Enter the customer id of the customer to be modified: "))
                new_first_name = input("Enter a new first name: ")
                new_last_name = input("Enter a new last name: ")
                new_address = input("Enter a new address: ")
                modified_entry = (new_first_name, new_last_name, new_address, modified_customer)

                update_query = "UPDATE database4.customer SET first_name = (%s), last_name = (%s), address = (%s) WHERE cid = (%s)"
                cursor.execute(update_query, modified_entry)
                
            elif db_input == "2": # modifying data in mongoDB
                modified_order = int(input("Enter the order id of the order to be modified: "))
                new_customer_id = int(input("Enter a new customer id: "))
                new_total = int(input("Enter a new total: "))
                
                update_query = {"_id": modified_order}
                new_values = {"$set": {"customer_id": new_customer_id, "total": new_total}}
                col.update_one(update_query, new_values)
                
        elif menu_input == "0":
            print("Closing software")
            break

        else:
            print("Unknown input, try again")

    mySQL_conn.commit()
    mySQL_conn.close()
    noSQL_conn.close()
    print("Exiting...")
        
main()
