"""

csv_table_tests.py

"""

from src.CSVDataTable import CSVDataTable

import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
data_dir = os.path.abspath("../data/Baseball")


def tests_people():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }
    people = CSVDataTable("People", connect_info, ["playerID"])
    try:

        print()
        print("find_by_primary_key(): Known Record")
        print(people.find_by_primary_key(["aardsda01"]))

        print()
        print("find_by_primary_key(): Unknown Record")
        print(people.find_by_primary_key((["cah2251"])))

        print()
        print("find_by_template(): Known Template")
        template = {"nameFirst": "David", "nameLast": "Aardsma", "nameGiven": "David Allan"}
        print(people.find_by_template(template))

        # Please complete code IN THE SAME FORMAT to test when the rest of methods pass or fail
        # HINT HINT: Don't forget about testing the primary key integrity constraints!!
        # For these tests, think to yourself: When should this fail? When should this pass?

        print()
        print("find_by_template(): UnKnown Template")
        template = {"nameFirst": "David", "nameLast": "Aardsma", "playerID": "cah2251"}
        print(people.find_by_template(template))

        print()
        print("delete_by_key(): Known Record")
        print(people.delete_by_key(["aardsda01"]))

        print()
        print("delete_by_key(): UnKnown Record")
        print(people.delete_by_key(["cah2251"]))

        print()
        print("delete_by_template(): Known Template")
        template = {"birthMonth": "9", "birthCountry": "USA"}
        print(people.delete_by_template(template))

        print()
        print("delete_by_template(): UnKnown Template")
        template = {"nameFirst": "David", "nameLast": "Aardsma", "playerID": "cah2251"}
        print(people.delete_by_template(template))

        print()
        print("update_by_key(): Known Record,no duplicate primary key")
        print(people.update_by_key(["abreujo02"], {"weight": 250, "height": 80}))

        print()
        print("update_by_key(): UnKnown Record,no duplicate primary key")
        print(people.update_by_key(["cah2251"], {"weight": 250, "height": 80}))

        print()
        print("update_by_template(): Known Template,no duplicate primary key")
        template = {"nameFirst": "David", "birthCountry": "USA"}
        print(people.update_by_template(template, {"weight": 210, "height": 72}))

        print()
        print("update_by_template(): UnKnown Template,no duplicate primary key")
        template = {"nameFirst": "David", "nameLast": "Aardsma", "playerID": "cah2251"}
        print(people.update_by_template(template, {"weight": 210, "height": 72}))

        print()
        print("insert(): no duplicate primary key")
        print(people.insert({'playerID': 'cah2251', 'birthYear': '1901', 'birthMonth': '11', 'birthDay': '17',
                             'birthCountry': 'USA', 'birthState': 'NY', 'birthCity': 'Denver', 'deathYear': '',
                             'deathMonth': '', 'deathDay': '', 'deathCountry': '', 'deathState': '', 'deathCity': '',
                             'nameFirst': 'David', 'nameLast': 'littlewood', 'nameGiven': 'amen', 'weight': '225',
                             'height': '75', 'bats': 'R', 'throws': 'R', 'debut': '1921-04-06', 'finalGame': '1941-08-23',
                             'retroID': 'aardd007', 'bbrefID': 'aardsda07'}
                            ))
        try:
            print()
            print("update_by_key(): Known Record,duplicate primary key")
            print(people.update_by_key(["actama99"], {"weight": 250, "height": 80, "playerID": "poolha01"}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("update_by_key(): UnKnown Record,duplicate primary key")
            print(people.update_by_key(["aaa2251"], {"weight": 250, "height": 80, "playerID": "poolha01"}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("update_by_template(): Known Template,duplicate primary key")
            template = {"nameFirst": "Bobby", "nameLast": "Abreu", "nameGiven": "Bob Kelly"}
            print(people.update_by_template(template, {"weight": 210, "height": 72, "playerID": "poolha01"}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("update_by_template(): UnKnown Template,duplicate primary key")
            template = {"nameFirst": "David", "nameLast": "Aardsma", "playerID": "cah2251"}
            print(people.update_by_template(template, {"weight": 210, "height": 72, "playerID": "poolha01"}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("insert(): duplicate primary key")
            print(people.insert({'playerID': 'adamsjo02', 'birthYear': '1901', 'birthMonth': '11', 'birthDay': '17',
                                 'birthCountry': 'USA', 'birthState': 'NY', 'birthCity': 'Denver', 'deathYear': '',
                                 'deathMonth': '', 'deathDay': '', 'deathCountry': '', 'deathState': '',
                                 'deathCity': '',
                                 'nameFirst': 'David', 'nameLast': 'littlewood', 'nameGiven': 'amen', 'weight': '225',
                                 'height': '75', 'bats': 'R', 'throws': 'R', 'debut': '1921-04-06',
                                 'finalGame': '1941-08-23',
                                 'retroID': 'aardd007', 'bbrefID': 'aardsda07'}
                                ))
        except Exception as e:
            print("An error occurred:", e)

    except Exception as e:
        print("An error occurred:", e)


def tests_batting():
    # Do the same tests for the batting table, so you can ensure your methods work for a table with a composite primary key
    # Replace this line with your tests
    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }
    batting = CSVDataTable("Batting", connect_info, ["playerID", "yearID", "stint"])
    try:

        print()
        print("find_by_primary_key(): Known Record")
        print(batting.find_by_primary_key(["abercda01", "1871", "1"]))

        print()
        print("find_by_primary_key(): Unknown Record")
        print(batting.find_by_primary_key((["cah2251", "1888", "1"])))

        print()
        print("find_by_template(): Known Template")
        template = {"G": "25", "AB": "118", "R": "30"}
        print(batting.find_by_template(template))

        # Please complete code IN THE SAME FORMAT to test when the rest of methods pass or fail
        # HINT HINT: Don't forget about testing the primary key integrity constraints!!
        # For these tests, think to yourself: When should this fail? When should this pass?

        print()
        print("find_by_template(): UnKnown Template")
        template = {"G": "24", "AB": "110", "playerID": "cah2251"}
        print(batting.find_by_template(template))

        print()
        print("delete_by_key(): Known Record")
        print(batting.delete_by_key(["abercda01", "1871", "1"]))

        print()
        print("delete_by_key(): UnKnown Record")
        print(batting.delete_by_key(["cah2251", "1888", "1"]))

        print()
        print("delete_by_template(): Known Template")
        template = {"yearID": "1939", "G": "20"}
        print(batting.delete_by_template(template))

        print()
        print("delete_by_template(): UnKnown Template")
        template = {"yearID": "1990", "G": "12", "playerID": "cah2251"}
        print(batting.delete_by_template(template))

        print()
        print("update_by_key(): Known Record,no duplicate primary key")
        print(batting.update_by_key(["glennjo01", "1871", "1"], {"G": 16, "AB": 110, "yearID": 1888}))

        print()
        print("update_by_key(): UnKnown Record,no duplicate primary key")
        print(batting.update_by_key(["cah2251", "1888", "1"], {"G": 25, "AB": 80}))

        print()
        print("update_by_template(): Known Template,no duplicate primary key")
        template = {"teamID": "COL", "yearID": "1995"}
        print(batting.update_by_template(template, {"CS": 0, "BB": 0}))

        print()
        print("update_by_template(): UnKnown Template,no duplicate primary key")
        template = {"yearID": "1990", "G": "12", "playerID": "cah2251"}
        print(batting.update_by_template(template, {"CS": 1, "BB": 2}))

        print()
        print("insert(): no duplicate primary key")
        print(batting.insert({'playerID': 'aaaacda01', 'yearID': '1996', 'stint': '2', 'teamID': 'TRO', 'lgID': 'NA',
                              'G': '10', 'AB': '4', 'R': '0', 'H': '0', '2B': '0', '3B': '0', 'HR': '0', 'RBI': '0',
                              'SB': '0', 'CS': '0', 'BB': '0', 'SO': '0', 'IBB': '', 'HBP': '', 'SH': '', 'SF': '',
                              'GIDP': '0'}))
        try:
            print()
            print("update_by_key(): Known Record,duplicate primary key")
            print(batting.update_by_key(["carleji01", "1871", "1"], {"playerID": "forceda01", "G": 34, "AB": 100}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("update_by_key(): UnKnown Record,duplicate primary key")
            print(batting.update_by_key(["cah2251", "1888", "1"], {"G": 25, "AB": 80, "playerID":
                                        "flynncl01", "yearID": "1871"}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("update_by_template(): Known Template,duplicate primary key")
            template = {"teamID": "COL", "yearID": "1995"}
            print(batting.update_by_template(template, {"A": 10, "height": 72, "playerID": "aceveju01"}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("update_by_template(): UnKnown Template,duplicate primary key")
            template = {"yearID": "1990", "G": "12", "playerID": "cah2251"}
            print(batting.update_by_template(template, {"A": 21, "height": 72, "playerID": "aguilri01", "stint": 1}))
        except Exception as e:
            print("An error occurred:", e)

        try:
            print()
            print("insert(): duplicate primary key")
            print(batting.insert({'playerID': 'kohlehe01', 'yearID': '1871', 'stint': '1', 'teamID': 'TRO', 'lgID': 'NA',
                              'G': '10', 'AB': '4', 'R': '0', 'H': '0', '2B': '0', '3B': '0', 'HR': '0', 'RBI': '0',
                              'SB': '0', 'CS': '0', 'BB': '0', 'SO': '0', 'IBB': '', 'HBP': '', 'SH': '', 'SF': '',
                              'GIDP': '0'}
                                ))
        except Exception as e:
            print("An error occurred:", e)

    except Exception as e:
        print("An error occurred:", e)


tests_people()
tests_batting()

