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

    def addData(self, table_name, data) :
        if(self.table_exists(table_name=table_name)) :
            print("The Table Exists")
        else :
            print("The Table Doesn't Exists")
            

    def print(self) :
        self.cursor.execute(f'SELECT * FROM {self.database_name}')
        return self.cursor.fetchall()
    
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
print(db.print())
db.addData(table_name="books",data=data)

db.close()