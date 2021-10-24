import CSVTable
import CSVCatalog
import json
import csv


# Must clear out all tables in CSV Catalog schema before using if there are any present
# Please change the path name to be whatever the path to the CSV files are
# First methods set up metadata!! Very important that all of these be run properly

# Only need to run these if you made the tables already in your CSV Catalog tests
# You will not need to include the output in your submission as executing this is not required
# Implementation is provided
def drop_tables_for_prep():
    cat = CSVCatalog.CSVCatalog()
    cat.drop_table("people")
    cat.drop_table("batting")
    cat.drop_table("appearances")


# drop_tables_for_prep()

# Implementation is provided
# You will need to update these with the correct path
def create_lahman_tables():
    cat = CSVCatalog.CSVCatalog()
    cat.create_table("people", "./Data/NewPeople.csv")
    cat.create_table("batting", "./Data/NewBatting.csv")
    cat.create_table("appearances", "./Data/NewAppearances.csv")


# create_lahman_tables()


# Note: You can default all column types to text
def update_people_columns():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('people')
    with open(t.file_name) as f:
        data = [datum for datum in csv.reader(f, delimiter=",")]
    headers = data[0]
    for header in headers:
        if header == 'playerID':
            new_col = CSVCatalog.ColumnDefinition(header, 'text', not_null=True)
        else:
            new_col = CSVCatalog.ColumnDefinition(header, 'text')
        t.add_column_definition(new_col)


# update_people_columns()

def update_appearances_columns():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('appearances')
    with open(t.file_name) as f:
        data = [datum for datum in csv.reader(f, delimiter=",")]
    headers = data[0]
    for header in headers:
        if header == 'yearID' or header == 'teamID' or header == 'playerID':
            new_col = CSVCatalog.ColumnDefinition(header, 'text', not_null=True)
        else:
            new_col = CSVCatalog.ColumnDefinition(header, 'text')
        t.add_column_definition(new_col)


# update_appearances_columns()

def update_batting_columns():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('batting')
    with open(t.file_name) as f:
        data = [datum for datum in csv.reader(f, delimiter=",")]
    headers = data[0]
    for header in headers:
        if header == 'yearID' or header == 'stint' or header == 'playerID':
            new_col = CSVCatalog.ColumnDefinition(header, 'text', not_null=True)
        else:
            new_col = CSVCatalog.ColumnDefinition(header, 'text')
        t.add_column_definition(new_col)


# update_batting_columns()

# Add primary key indexes for people, batting, and appearances in this test
def add_index_definitions():
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('people')
    t.define_index('playerID', ['playerID'], 'PRIMARY')
    t = cat.get_table('batting')
    t.define_index('playerID', ['playerID', 'yearID', 'stint'], 'PRIMARY')
    t = cat.get_table('appearances')
    t.define_index('yearID', ['yearID', 'teamID', 'playerID'], 'PRIMARY')


# add_index_definitions()


def test_load_info():
    table = CSVTable.CSVTable("batting")
    print(table.__description__.file_name)


# test_load_info()

def test_get_col_names():
    table = CSVTable.CSVTable("people")
    names = table.__get_column_names__()
    print('The column names are: ', names)


# test_get_col_names()

def add_other_indexes():
    """
    We want to add indexes for common user stories
    People: nameLast, nameFirst
    Batting: teamID
    Appearances: None that are too important right now
    :return:
    """
    # ************************ TO DO ***************************
    cat = CSVCatalog.CSVCatalog(
        dbhost="localhost",
        dbport=3306,
        dbuser="root",
        dbpw="zxy3221915",
        db="CSVCatalog")
    t = cat.get_table('people')
    t.define_index('name', ['nameLast', 'nameFirst'], 'INDEX')
    t = cat.get_table('batting')
    t.define_index('teamID', ['teamID'], 'INDEX')


# add_other_indexes()

def load_test():
    people_table = CSVTable.CSVTable("people")
    print(people_table)


# load_test()


def dumb_join_test():
    batting_table = CSVTable.CSVTable("batting")
    appearances_table = CSVTable.CSVTable("appearances")
    result = batting_table.dumb_join(appearances_table, ["playerID", "yearID"], {"playerID": "baxtemi01"},
                                     ["playerID", "yearID", "teamID", "AB", "H", "G_all", "G_batting"])
    print(result)


# dumb_join_test()


def get_access_path_test():
    batting_table = CSVTable.CSVTable("batting")
    template = ["teamID", "playerID", "yearID"]
    index_result, count = batting_table.__get_access_path__(template)
    print(index_result)
    print(count)


# get_access_path_test()

def sub_where_template_test():
    # ************************ TO DO ***************************
    batting_table = CSVTable.CSVTable("people")
    res = batting_table.__get_sub_where_template__({"nameFirst": "David", 'teamID': 'CHA'})
    print('The where_template is : {"nameFirst": "David","teamID":"CHA"}')
    print('The sub_where_template is: ', end='')
    print(res)


# sub_where_template_test()


def test_find_by_template_index():
    # ************************ TO DO ***************************
    batting_table = CSVTable.CSVTable("batting")
    res = batting_table.__find_by_template_index__({'yearID': '1965', 'teamID': 'ML1'}, 'teamID',
                                                   ['playerID', 'yearID', 'teamID', 'lgID'])
    print('find_by_template_index of template:{"yearID":"1965","teamID":"ML1"}, index: "teamID"')
    print(res)


# test_find_by_template_index()

def smart_join_test():
    # ************************ TO DO ***************************
    batting_table = CSVTable.CSVTable("batting")
    appearances_table = CSVTable.CSVTable("appearances")
    result = batting_table.__smart_join__(appearances_table, ["playerID", "yearID"], {"playerID": "baxtemi01"},
                                          ["playerID", "yearID", "teamID", "AB", "H", "G_all", "G_batting"])
    print(result)


# smart_join_test()

def test():
    drop_tables_for_prep()
    create_lahman_tables()
    update_people_columns()
    update_appearances_columns()
    update_batting_columns()
    add_index_definitions()
    add_other_indexes()
    print("===============================")
    smart_join_test()

# test()
