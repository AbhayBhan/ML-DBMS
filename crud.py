from crud_api import dboperation



def main():
  

    db=input("Enter Database Name : ")
    db = dboperation(db)
    
    while True:
        user_input = input("Enter a command \n 1. Create Table \n 2. Add Data \n 3. get Columns \n 4. Fetch All \n 5. Fetch Where \n 6. Delete Table \n 7. Drop Database \n 8. Exit \n")

        if user_input == "1":
            table_name = input("Enter Table Name : ")
            cols = []
            while True:
                col_name = input("Enter Column Name : ")
                col_datatype = input("Enter Column Datatype : ").upper()
                col_desc = input("Enter Column Description : ")
                cols.append({
                    "name" : col_name,
                    "datatype" : col_datatype,
                    "desc" : col_desc
                })
                if input("Do you want to add more columns? (Y/N) : ").lower() == "n":
                    break
            data = {
                "table_name" : table_name,
                "cols" : cols
            }
            db.createTable(data)
        elif user_input == "2":
            table_name = input("Enter Table Name : ")
            # show table columns here
            try:
                get_cols = db.getColumns(table_name=table_name)
                print('Enter columns data')
                cols = []
                while True:
                    # col_name = input("Enter Column Name : ")
                    cols_value = []
                    for col_name in get_cols:
                        print(col_name[1], end=" ")
                        col_value = input("Value : ")
                        cols_value.append(col_value)
        
                    cols.append(cols_value)
                    if input("Do you want to add more data? (Y/N) : ").lower() == "n":
                        break
                data = {
                    "table_name" : table_name,
                    "cols" : cols
                }

                db.addData(data["table_name"], data["cols"])
            except :
                print("Table Doesn't Exist")

        elif user_input == "3":
            table_name = input("Enter Table Name : ")
            try:
                print(db.getColumns(table_name=table_name))
            except :
                print("Table Doesn't Exist")

        elif user_input == "4":
            try:
                table_name = input("Enter Table Name : ")
                print(db.fetchAll(table_name=table_name))
            except :
                print("Table Doesn't Exist")

        elif user_input == "5":
            table_name = input("Enter Table Name : ")
            data = input("Enter Where Columns : ")
            fromcols=input("Enter Where Clause :  ")
            print(db.fetchWhere(table_name=table_name, data=f"{data} == '{fromcols}'"))

        elif user_input == "6":
            table_name = input("Enter Table Name : ")
            db.deleteTable(table_name=table_name)

        elif user_input == "7":
            db.dropDatabase()
            break

        elif user_input == "8":
            break

        elif user_input == "9": # Not for CUI
            table_name = input("Enter Table Name : ")
            df = db.createDFfromall(table_name=table_name)
            print(df)

        else:
            print("Invalid Input")

if __name__ == "__main__":
    main()

            