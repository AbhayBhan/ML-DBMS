from flask import Blueprint,render_template,redirect,url_for,request,flash
import os
from os.path import isfile, join
from crud_api import dboperation

views=Blueprint('views',__name__)


@views.route('')
def home():
    return render_template("home.html")

@views.route('/database-list')
def database_list():
    try:
        databases_path = 'databases'
        database_list = os.listdir(databases_path)
        if database_list:
            database_list = [database.split('.')[0] for database in database_list if isfile(join(databases_path, database))]
    except:
        database_list = []
    
    print(database_list)

    return render_template("database_list.html",database_list=database_list)

@views.route('/create-database',methods=['GET','POST'])
def create_database():
    if request.method == 'POST':
        dbname = request.form['dbname']

        databases_path = 'databases'
        database_list = os.listdir(databases_path)
        database_list = [database.split('.')[0] for database in database_list if isfile(join(databases_path, database))]

        if dbname in database_list:
            flash(f'{dbname} is already exists',category='error')
            print('already exists')
        else:
            dboperation(dbname)
            flash(f'{dbname} is created successfully',category='success')
            return redirect(url_for('views.database_list'))
    return render_template("create_update_database.html")   



@views.route('/update-database/<string:database_name>')
def update_database(database_name):
    try:
        databases_path = 'databases'
        database_list = os.listdir(databases_path)
        database_list = [database.split('.')[0] for database in database_list if isfile(join(databases_path, database))]
        if database_name in database_list:
            dboperation(database_name)
            flash(f'{database_name} is updated successfully',category='success')
    except:
        flash(f'{database_name} is not updated',category='error')
    return render_template("create_update_database.html")

@views.route('/delete-database/<string:database_name>')
def delete_database(database_name):
    try:
        databases_path = 'databases'
        database_list = os.listdir(databases_path)
        database_list = [database.split('.')[0] for database in database_list if isfile(join(databases_path, database))]
        if database_name in database_list:
            os.remove(f'databases/{database_name}.db')
            flash(f'{database_name} is deleted successfully',category='success')
    except:
        flash(f'{database_name} is not deleted',category='error')
    return redirect(url_for('views.database_list'))

@views.route('/<string:database_name>/table-list')
def table_list(database_name):
    try:
        print(database_name)
        db = dboperation(database_name)
        table_list = db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_list = [table[0] for table in table_list]
    except:
        table_list = []
    return render_template("table_list.html",database_name=database_name,table_list=table_list)

@views.route('/<string:database_name>/create-table',methods=['GET','POST'])
def create_table(database_name):
    if request.method == 'POST':
        table_name = request.form['table_name']
        col_name = request.form.getlist('col_name')
        col_datatype = request.form.getlist('col_datatype')
        col_desc = request.form.getlist('col_desc')

        cols = []
        for i in range(len(col_name)):
            cols.append({
                    "name" : col_name,
                    "datatype" : col_datatype,
                    "desc" : col_desc
                })
        data = {
                "table_name" : table_name,
                "cols" : cols
            }
        db = dboperation(database_name)
        db.createTable(data)
        flash(f'{table_name} is created successfully',category='success')
        return redirect(url_for('views.table_list',database_name=database_name))
    return render_template("create_update_table.html",database_name=database_name)


