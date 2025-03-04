import pymysql
import json

# Name:Xiangyi Zeng
# UNI:xz2727

def run_q(cnx, q, args, fetch=False):
    """
    Method to run queries on your AWS MySQL Database.
    This is similar to the connection between your jupyter notebook and AWS in HW1.

    Implementation for this method is provided.

    :param cnx: Connection to database
    :param q: The query string
    :param args: Any arguments passed
    :param fetch: Whether the query needs to return data
    :return: Result from query, if applicable
    """
    cursor = cnx.cursor()
    if args is not None:
        print("Q = "+q % args)
    else:
        print("Q =", q)
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

class ColumnDefinition:
    """
    Represents a column definition in the CSV Catalog.

    Implementation for ColumnDefinition is provided.
    """

    # Allowed types for a column. We are keeping it simple(r) for this assignment.
    column_types = ("text", "number")

    def __init__(self, column_name, column_type="text", not_null=False):
        """
        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types, defaults to text
        :param not_null: True or False, whether the column can have NULL fields or not.
        """

        if column_name == None:
            print("Issue!!")
            raise ValueError('You must have a column name!!')
        else:
            self.column_name = column_name

        if column_type in self.column_types:
            self.column_type = column_type
        else:
            print("Issue!")
            raise ValueError('That column type is not accepted. Please try again.')

        if type(not_null)==type(True):
            self.not_null = not_null
        else:
            print("Issue!")
            raise ValueError('The not_null column must be either True or False! Please try again.')


    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        """
        :return: A JSON object, not a string, representing the column and it's properties.
        """
        result = {
            "column_name": self.column_name,
            "column_type": self.column_type,
            "not_null": self.not_null
        }
        return result

class IndexDefinition:
    """
    Represents the definition of an index.

    Implementation for IndexDefinition is provided.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, index_name, index_type, column_names):
        """
        :param index_name: Name for index. Must be unique name for table.
        :param index_type: Valid index type.
        """
        self.index_name = index_name
        if index_type not in IndexDefinition.index_types:
            raise ValueError("Not the right index type")
        if len(column_names) == 0:
            raise ValueError("Must have an associate column name")

        self.index_type = index_type

        # column_names must always be initialized in proper order because of how we load/create indexes
        self.column_names = column_names

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        result = {
            "index_name": self.index_name,
            "type": self.index_type,
            "columns": self.column_names
        }
        return result

class TableDefinition:
    """
    Represents the definition of a table in the CSVCatalog.

    You must complete the remainder of TableDefinition
    """

    def __init__(self, t_name=None, csv_f=None, column_definitions=None, index_definitions=None, cnx=None,
                 load=False):

        """
        Initialization method. Implementation is provided.

        :param t_name: Name of the table.
        :param csv_f: Full path to a CSV file holding the data.
        :param column_definitions: List of column definitions to use from file. Cannot contain invalid column name.
            May be just a subset of the columns.
        :param index_definitions: List of index definitions. Column names must be valid.
        :param cnx: Database connection to use. If None, create a default connection.
        :param load: Whether you are creating a new TableDefinition or loading a preexisting one.
        """
        self.cnx = cnx
        self.table_name = t_name
        self.columns = None
        self.indexes = None


        if not load:

            if t_name is None or csv_f is None:
                raise ValueError("Table and file must both have a name")

            # We will assume that the file does exist in the proper location
            # Feel free to add additional error checking here though


            self.file_name = csv_f
            self.save_core_definition()

            if column_definitions is not None:

                for c in column_definitions:
                    self.add_column_definition(c)

            if index_definitions is not None:
                for idx in index_definitions:
                    self.define_index(idx.index_name, idx.column_names, idx.index_type)

        else:
            # All three methods you must implement.
            self.load_core_definition()
            self.load_columns()
            self.load_indexes()

    def load_columns(self):
        """
        Method to query the metadata table and update self.columns with ColumnDefinitions stored

        :return: Nothing
        """
        # ************************ TO DO ***************************
        print("Running load columns")
        q = "select * from csvcolumns where table_name = %s"
        result = run_q(self.cnx, q, (self.table_name,), fetch=True)
        self.columns = []
        for row in result:
            new_col = ColumnDefinition(row['column_name'], row['type'], bool(row['not_null']))
            self.columns.append(new_col)
    def load_indexes(self):
        """
        This is a trickier and lengthier method to implement. Keep track of your data structures.
        A general outline is provided for guidance.

        This method requires you to get the index information from the csvindexes table in AWS and create the necessary IndexDefinition

        :return:
        """
        # Get the data from csvindexes
        # Make an empty dictionary to store index data temporarily
        # Go through the data in csvindexes
            # Append indexes that have not been seen yet
            # Add the new column to the index if the index name has been seen before

        # For all the indexes in the temporary index dictionary
            # Ensure that the columns are ordered according to the index order
            # Create a new IndexDefinition object for each index
            # Append the new IndexDefinition to self.indexes

        # ************************ TO DO ***************************
        print("Running load indexes")
        q = "select * from csvindexes where table_name = %s order by index_name,index_order"

        result = run_q(self.cnx, q, (self.table_name, ), fetch=True)
        self.indexes = {}

        for row in result:
            tmp_index = self.indexes.get(row['index_name'], None)
            if tmp_index is None:
                tmp_index = IndexDefinition(row['index_name'], row['type'], [row['column_name']])
                self.indexes[row['index_name']] = tmp_index
            else:
                # add the column name according to index_order
                tmp_index.column_names.append(row['column_name'])
    def load_core_definition(self):
        """
        Loads a TableDefinition by querying the metadata tables in AWS
        Hint: look at save_core_definition below for some guidance

        :return: Nothing
        """
        # ************************ TO DO ***************************

        print("Running load core definition")
        q = "select * from csvtables where table_name = %s"
        result = run_q(self.cnx, q, (self.table_name,), fetch=True)
        self.file_name = result[0]['path']

    def save_core_definition(self):
        """
        Implementation is provided for save_core_definition(self).

        :return: Nothing
        """
        print("Running save core definition")
        q = "insert into csvtables values(%s, %s)"
        result = run_q(self.cnx, q, (self.table_name, self.file_name), fetch=True)

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def add_column_definition(self, c):
        """
        Add a column definition to self.columns.

        Implementation is provided for add_column_definition(self, c).
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        #SQL will throw the error if table integrity is not kept and a column with a duplicate
        print("adding column")
        q = "insert into csvcolumns values(%s, %s, %s, %s)"
        result = run_q(self.cnx, q, (self.table_name, c.column_name, c.column_type, c.not_null), fetch=True)
        if self.columns is None:
            self.columns = []
        self.columns.append(c)

    def get_column(self, cn):
        """
        Returns a column of the current table so that it can be deleted from the columns list
        Helper method for drop_column_definition(self, cn).

        Implementation is provided for get_column(self, cn).
        :param cn: name of the column you are trying to get.
        :return: Column if found or None
        """
        for col in self.columns:
            if col.column_name == cn:
                return col

        print("Column '" + cn + "' not found")
        return


    def drop_column_definition(self, cn):
        """
        Remove from definition and catalog tables.
        :param cn: Column name (string)
        :return: Returns nothing, removes from the columns list
        """
        print("dropping column")
        column_to_drop = self.get_column(cn)
        if column_to_drop is not None:
            self.columns.remove(column_to_drop)
            self.drop_col_in_sql(cn) # You must implement this function
            print("Column '" + cn + "' has been dropped!")

        return

    def drop_col_in_sql(self, cn):
        """
        Deletes the row in sql for the given column.
        THINK: What does this mean for the indexes that depend on this column?)
        Method should be 2 lines only.

        :param cn: Column name (string)
        :return: Returns nothing, executes SQL query
        """
        # ************************ TO DO ***************************
        q = "delete from csvcolumns where table_name = %s and column_name  = %s"
        run_q(self.cnx, q, (self.table_name, cn))
        return
    def to_json(self):
        """
        Implementation is provided for to_json(self)
        :return: A JSON representation of the table and it's elements.
        """
        result = {
            "table_name": self.table_name,
            "file_name" : self.file_name
        }

        if self.columns is not None:
            result['columns'] = []
            for c in self.columns:
                result['columns'].append(c.to_json())

        if self.indexes is not None:
            result['indexes'] = []
            for _, idx in self.indexes.items():
                result['indexes'].append(idx.to_json())
        return result


    def save_index_definition(self, i_name, cols, type):
        """
        Performs the insert into the the csvindexes table using a query and the run_q method
        Is a helper method for define_index(self, index_name, columns, type="index") method below.

        Implementation is provided for save_index_definition.
        :param i_name: name of the index
        :param cols: columns the index is defined on
        :param type: type of index
        :return: Does not return anything.
        """

        q = "insert into csvindexes (table_name, column_name, type, index_name, index_order) " + \
            " values(%s, %s, %s, %s, %s)"
        for i in range(0, len(cols)):
            v = (self.table_name, cols[i], type, i_name, str(i))
            result = run_q(self.cnx, q, v, fetch=False)

    def define_index(self, index_name, columns, type="INDEX"):
        """
        Define or replace and index definition.
        Should update the self.indexes variable.

        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param type: One of the valid index types.
        :return: Returns nothing
        """
        # ************************ TO DO ***************************
        print("adding index")
        self.save_index_definition(index_name, columns, type)
        if self.indexes is None:
            self.indexes = {}
            self.indexes['index_name'] = IndexDefinition(index_name, type, columns)
        self.indexes['index_name'] = IndexDefinition(index_name, type, columns)
    def get_index(self, ind_name):
        """
        Gets the IndexDefinition matching the name, if exists.
        Prints "Index [ind_name] not found" and returns None if index is not found.

        :param ind_name: name of the index you are trying to get.
        :return: Returns the index, if found
        """
        # ************************ TO DO ***************************
        if self.indexes.get(ind_name) is not None:
            return self.indexes[ind_name]
        else:
            print("Index "+ind_name+" not found")
            return None
    def drop_index(self, index_name):
        """
        Remove an index from the metadata and the list of indexes associated with the table

        :param index_name: Name of index to remove (str)
        :return: Returns nothing.
        """
        # ************************ TO DO ***************************
        if self.indexes.get(index_name) is not None:
            del self.indexes[index_name]
            self.drop_indx_in_sql(index_name)
            print("Index "+index_name+" has been dropped!")
        return
    def drop_indx_in_sql(self, index_name):
        """
        Helper method for drop_index.
        Deletes the row for the given index in SQL.

        Implementation is provided for drop_indx_in_sql.
        :param index_name: name of index to remove (str)
        :return: Returns nothing.
        """
        q = "DELETE FROM csvindexes WHERE table_name = '" + self.table_name + "' and index_name = '" + index_name + "'"
        result = run_q(self.cnx, q, None, fetch=False)


    def describe_table(self):
        """
        Simply wraps to_json()

        Implementation is provided for describe_table
        :return: JSON representation.
        """
        result = self.to_json()
        return result



class CSVCatalog:
    """
    Implementation for class CSVCatalog is provided.
    """

    def __init__(self, dbhost="localhost", dbport=3306,
                  dbuser="root", dbpw="zxy3221915",  db="CSVCatalog",debug_mode=None):
        self.cnx = pymysql.connect(
            host=dbhost,
            port=dbport,
            user=dbuser,
            password=dbpw,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __str__(self):
        pass

    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        result = TableDefinition(table_name, file_name, cnx=self.cnx)
        return result

    def drop_table(self, table_name):

        q = "DELETE FROM csvtables WHERE table_name = '" + table_name + "'"
        result = run_q(self.cnx, q, None, fetch=True)
        print("Table '" + table_name + "' was dropped")

    def get_table(self, table_name):
        """
        Returns a previously created table.
        :param table_name: Name of the table.
        :return:
        """
        result = TableDefinition(table_name, load=True, cnx=self.cnx)
        return result


