import sqlite3

class dboperation :
    def __init__(self,name) :
        self.database_name = name
        self.conn = sqlite3.connect(name+".db")
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

        print("Created Table")

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

    def deleteTable(self, table_name) : 
        if self.table_exists(table_name=table_name) :
            conf = input("Do you really want to remove this table? (Y/N) : ")
            if conf == "Y" :
                self.cursor.execute(f'DROP TABLE {table_name}')
                self.conn.commit()
                print(f"Table {table_name} has been removed.")
            else :
                print("Operation Aborted.")
        else : 
            print("The Table Doesn't Exist")
    
    def close(self) :
        self.conn.close()


db = dboperation("books")
data = {
    "table_name" : "books",
    "cols" : [{
        "name" : "Book_Name",
        "datatype" : "TEXT"
    },{
        "name" : "Author",
        "datatype" : "TEXT"
    },{
        "name" : "Copies",
        "datatype" : "INTEGER"
    }]
}

db.createTable(data)
# print(db.fetchAll("books"))
db.addData(table_name="books",data=['To Kill a Mockingbird', 'Abc', 12])
print(db.fetchWhere(table_name="books", data="Book_Name == 'To Kill a Mockingbird'"))
# print(db.getColumns(table_name="books"))
db.close()