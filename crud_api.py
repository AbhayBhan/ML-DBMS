import sqlite3
import pandas as pd
import os

class dboperation :
    def __init__(self,name) :
        self.database_name = name
        self.conn = sqlite3.connect('databases/'+name+".db")
        self.cursor = self.conn.cursor()

    def table_exists(self, table_name) :
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor.fetchone() is not None
    

    def createTable(self, table_data) :
        columns = []
        table_name = table_data["table_name"];

        for col in table_data["cols"]:
            col_name = col["name"]
            col_datatype = col["datatype"]
            columns.append(f"{col_name} {col_datatype}")

        result_string = ", ".join(columns)

        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {result_string}
            )'''

        self.cursor.execute(query)
        self.create_ml_info_table(table_name=table_name, data=table_data)

        print("Created Table")

        self.conn.commit()


    def create_ml_info_table(self, table_name, data) : 
        ml_table = table_name + '_ml_info'
        query = f"CREATE TABLE IF NOT EXISTS {ml_table} ( col_name TEXT, col_desc TEXT )"
        self.cursor.execute(query)

        for col in data['cols']:
            col_name = col["name"]
            col_desc = col["desc"]
            # self.addData(ml_table,[col_name,col_desc])
            self.addData_in_info_table(ml_table,[col_name,col_desc])
        
        print("ML InfoTable Created.")

        self.conn.commit()

    def getColumns(self, table_name):
        if self.table_exists(table_name=table_name):
            self.cursor.execute(f'PRAGMA table_info({table_name})')
            columns_info = self.cursor.fetchall()
            return columns_info
        else:
            print("The Table Doesn't Exist")

    def addData(self, table_name, data):
        if self.table_exists(table_name=table_name):
            for obj in data:
                placeholders = ','.join(['?'] * len(obj))
                query = f'INSERT INTO {table_name} VALUES ({placeholders})'
                
                self.cursor.execute(query, obj)
                self.conn.commit()
            print("Data added successfully")
        else:
            print("The Table Doesn't Exist")


    def addData_in_info_table(self, table_name, data):
        if self.table_exists(table_name=table_name):
            placeholders = ','.join(['?'] * len(data))
            query = f'INSERT INTO {table_name} VALUES ({placeholders})'
            self.cursor.execute(query, data)
            self.conn.commit()
            print("Data added successfully")
        else:
            print("The Table Doesn't Exist")
    

    def fetchAll(self, table_name) :
        self.cursor.execute(f'SELECT * FROM {table_name}')
        return self.cursor.fetchall()
    
    def fetchWhere(self, table_name, data, fromcols=None) :
        if self.table_exists(table_name=table_name) :
            if fromcols is not None: 
                cols = ','.join(fromcols)
                self.cursor.execute(f'SELECT {cols} FROM {table_name} WHERE {data}')
                return self.cursor.fetchall()
            else :
                self.cursor.execute(f'SELECT * FROM {table_name} WHERE {data}')
                return self.cursor.fetchall()
        else : 
            print("The Table Doesn't Exist")
        
    def createDFfromall(self, table_name) :
        if self.table_exists(table_name=table_name) : 
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.conn)
            return df
        else : 
            print("The Table Doesn't Exist")

    def deleteTable(self, table_name) : 
        if self.table_exists(table_name=table_name) :
            conf = input("Do you really want to remove this table? (Y/N) : ")
            if conf.lower() == "y" :
                self.cursor.execute(f'DROP TABLE {table_name}')
                self.cursor.execute(f'DROP TABLE {table_name}_ml_info')
                self.conn.commit()
                print(f"Table {table_name} has been removed.")
            else :
                print("Operation Aborted.")
        else : 
            print("The Table Doesn't Exist")

    def dropDatabase(self) : 
        self.close()
        dbname = self.database_name+".db"
        if os.path.exists(dbname) : 
            conf = input("Do you really want to drop this database? (Y/N) : ")
            if conf.lower() == "y" :
                os.remove(dbname)
                print("Dropped Database.")
            else : 
                print("Dropping Aborted.")
        else : 
            print("Unable to perform deletion.")
    
    def close(self) :
        self.conn.close()


# db = dboperation("books")


# data = {
#     "table_name" : "books",
#     "cols" : [{
#         "name" : "Book_Name",
#         "datatype" : "TEXT",
#         "desc" : "Names of the Books"
#     },{
#         "name" : "Author",
#         "datatype" : "TEXT",
#         "desc" : "Authors of the books"
#     },{
#         "name" : "Copies",
#         "datatype" : "INTEGER",
#         "desc" : "Copies Made of the books"
#     }]
# }


if __name__ == "__main__" :
    pass
    # db.createTable(data)
    # print(db.fetchAll("books"))
    # db.addData(table_name="books",data=['To Kill a Mockingbird', 'Abc', 12])
    # print(db.fetchWhere(table_name="books", data="Book_Name == 'To Kill a Mockingbird'"))
    # print(db.getColumns(table_name="books"))
    # print(db.fetchAll("books_ml_info"))
    # db.close()
    # db.dropDatabase()
