import CSVCatalog
import json

# Example test, you will have to update the connection info
# Implementation Provided
def create_table_test():
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    cat.create_table("Batting", "./Data/Batting.csv")
    t = cat.get_table("Batting")
    print("Table = ", t)
    cat.create_table("People", "./Data/People.csv")
    t = cat.get_table("People")
    print("Table = ", t)
    cat.create_table("Appearances", "./Data/Appearances.csv")
    t = cat.get_table("Appearances")
    print("Table = ", t)
#create_table_test()

def drop_table_test():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    cat.drop_table("People")
    cat.drop_table("Batting")
    cat.drop_table("Appearances")



#drop_table_test()

def add_column_test():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table("Batting")
    col1 = CSVCatalog.ColumnDefinition('playerID', 'text', not_null=True)
    col2 = CSVCatalog.ColumnDefinition('yearID', 'number', not_null=True)
    col3 = CSVCatalog.ColumnDefinition('stint', 'number', not_null=True)
    t.add_column_definition(col1)
    t.add_column_definition(col2)
    t.add_column_definition(col3)
    print("Table =", t)
    t = cat.get_table("People")
    col1 = CSVCatalog.ColumnDefinition('playerID', 'text', not_null=True)
    col2 = CSVCatalog.ColumnDefinition('birthYear', 'number', not_null=False)
    t.add_column_definition(col1)
    t.add_column_definition(col2)
    print("Table =", t)
    t = cat.get_table("Appearances")
    col1 = CSVCatalog.ColumnDefinition('playerID', 'text', not_null=True)
    col2 = CSVCatalog.ColumnDefinition('yearID', 'number', not_null=True)
    col3 = CSVCatalog.ColumnDefinition('teamID', 'number', not_null=True)
    t.add_column_definition(col1)
    t.add_column_definition(col2)
    t.add_column_definition(col3)
    print("Table =", t)
    
    



#add_column_test()

# Implementation Provided
# Fails because no name is given
def column_name_failure_test():
    cat = CSVCatalog.CSVCatalog()
    col = CSVCatalog.ColumnDefinition(None, "text", False)
    t = cat.get_table("Batting")
    t.add_column_definition(col)

#column_name_failure_test()

# Implementation Provided
# Fails because "canary" is not a permitted type
def column_type_failure_test():
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    col = CSVCatalog.ColumnDefinition("bird", "canary", False)
    t = cat.get_table("Batting")
    t.add_column_definition(col)

#column_type_failure_test()

# Implementation Provided
# Will fail because "happy" is not a boolean
def column_not_null_failure_test():
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    col = CSVCatalog.ColumnDefinition("name", "text", "happy")
    t = cat.get_table("Batting")
    t.add_column_definition(col)

#column_not_null_failure_test()


def add_index_test():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('Batting')
    t.define_index('primary_key', ['playerID', 'yearID', 'stint'], 'PRIMARY')
    print("Table =", t)
    t = cat.get_table('People')
    t.define_index('primary_key', ['playerID'], 'PRIMARY')
    print("Table =", t)
    t = cat.get_table('Appearances')
    t.define_index('primary_key', ['yearID', 'teamID', 'playerID'], 'PRIMARY')
    print("Table =", t)
#add_index_test()


def col_drop_test():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('Batting')
    t.drop_column_definition('playerID')
    t = cat.get_table('Batting')
    print("Table =", t)
    t = cat.get_table('People')
    t.drop_column_definition('birthYear')
    t = cat.get_table('People')
    print("Table =", t)
    t = cat.get_table('Appearances')
    t.drop_column_definition('teamID')
    t = cat.get_table('Appearances')
    print("Table =", t)
#col_drop_test()

def index_drop_test():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('Batting')
    t.drop_index('primary_key')
    print('Table =', t)
    t = cat.get_table('Appearances')
    t.drop_index('primary_key')
    print('Table =', t)
#index_drop_test()

# Implementation provided
def describe_table_test():
    cat = CSVCatalog.CSVCatalog()
    t = cat.get_table("Batting")
    desc = t.describe_table()
    print("DESCRIBE Batting = \n", json.dumps(desc, indent = 2))
    t = cat.get_table("people")
    desc = t.describe_table()
    print("DESCRIBE People = \n", json.dumps(desc, indent=2))
    t = cat.get_table("Appearances")
    desc = t.describe_table()
    print("DESCRIBE Appearances = \n", json.dumps(desc, indent=2))

#describe_table_test()

