from src.BaseDataTable import BaseDataTable
import copy
import logging
import json
import os
import pandas as pd
import csv

pd.set_option("display.width", 256)
pd.set_option('display.max_columns', 20)


class CSVDataTable(BaseDataTable):
    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """
    _rows_to_print = 10
    _no_of_separators = 2

    def __init__(self, table_name, connect_info, key_columns, debug=True, load=True, rows=None):

        """
        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        self._data = {
            "table_name": table_name,
            "connect_info": connect_info,
            "key_columns": key_columns,
            "debug": debug
        }

        self._key_columns = key_columns

        self._logger = logging.getLogger()

        self._logger.debug("CSVDataTable.__init__: data = " + json.dumps(self._data, indent=2))

        if rows is not None:
            self._rows = copy.copy(rows)
        else:
            self._rows = []
            self._load()

    def __str__(self):

        result = "CSVDataTable: config data = \n" + json.dumps(self._data, indent=2)

        no_rows = len(self._rows)
        if no_rows <= CSVDataTable._rows_to_print:
            rows_to_print = self._rows[0:no_rows]
        else:
            temp_r = int(CSVDataTable._rows_to_print / 2)
            rows_to_print = self._rows[0:temp_r]
            keys = self._rows[0].keys()

            for i in range(0, CSVDataTable._no_of_separators):
                tmp_row = {}
                for k in keys:
                    tmp_row[k] = "***"
                rows_to_print.append(tmp_row)

            rows_to_print.extend(self._rows[int(-1 * temp_r) - 1:-1])

        df = pd.DataFrame(rows_to_print)
        result += "\nSome Rows: = \n" + str(df)

        return result

    def _add_row(self, r):
        if self._rows is None:
            self._rows = []
        self._rows.append(r)

    def _load(self):

        dir_info = self._data["connect_info"].get("directory")
        file_n = self._data["connect_info"].get("file_name")
        full_name = os.path.join(dir_info, file_n)

        with open(full_name, "r") as txt_file:
            csv_d_rdr = csv.DictReader(txt_file)
            for r in csv_d_rdr:
                self._add_row(r)

        self._logger.debug("CSVDataTable._load: Loaded " + str(len(self._rows)) + " rows")

    def save(self):
        """
        Write the information back to a file.
        :return: None
        """
        fn = self._data["connect_info"].get("directory") + "/" + self._data["connect_info"].get("file_name")
        with open(fn, "w") as csvfile:
            self.columns = self._rows[0].keys()
            csvw = csv.DictWriter(csvfile, self.columns)
            csvw.writeheader()
            for r in self._rows:
                csvw.writerow(r)

    def get_key_column(self):
        pkey = self._data.get("key_columns")
        return pkey

    @staticmethod
    def _project(row, field_list):

        result = {}

        if field_list is None:
            return row

        for f in field_list:
            result[f] = row[f]

        return result

    @staticmethod
    def matches_template(row, template):

        result = True
        if template is not None:
            for k, v in template.items():
                if v != row.get(k, None):
                    result = False
                    break

        return result

    def find_by_primary_key(self, key_fields, field_list=None):
        """
        Finds and returns the records that match the primary key
        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        :param field_list: A subset of the fields of the record to return.
        :return: None, or a dictionary containing the requested fields for the record identified
            by the key.
        """

        dictionary = dict(zip(self.get_key_column(), key_fields))

        # What method can you use?
        for r in reversed(self.get_rows()):
            if CSVDataTable.matches_template(r, dictionary):
                return CSVDataTable._project(r, field_list)
        return None

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None):
        """
        Finds the record that matches the template.
        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
        :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A list containing dictionaries. A dictionary is in the list representing each record
            that matches the template. The dictionary only contains the requested fields.

        """
        result = []

        for r in reversed(self.get_rows()):
            if CSVDataTable.matches_template(r, template):
                new_r = CSVDataTable._project(r, field_list)
                result.append(new_r)

        return result

    def delete_by_key(self, key_fields):
        """
        Deletes the record that matches the key.
        :param key_fields: List of value for the key fields.
        :return: A count of the rows deleted.
        """

        # HINT: Create a dictionary of values/a template for key fields, then call a method you wrote
        row_to_remove = self.find_by_primary_key(key_fields)
        if row_to_remove is not None:
            self.get_rows().remove(row_to_remove)
            return str(1)+' '+"row deleted"
        else:
            return str(0)+' '+"row deleted"

    def delete_by_template(self, template):
        """
        Deletes the record that matches the template
        :param template: Template to determine rows to delete.
        :return: Number of rows deleted.
        """
        counter = 0

        # Iterate through rows, if matches, remove the row
        for r in reversed(self.get_rows()):
            if CSVDataTable.matches_template(r, template):
                self.get_rows().remove(r)
                counter += 1

        return str(counter)+' '+"rows deleted"

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of value for the key fields.
        :param new_values: A dict of field:value to set for updated row.
        :return: Number of rows updated.
        """

        # HINT: Create a dictionary of values/a template for key fields, then call a method you wrote
        key_test = []
        do_test = False
        row_to_update = self.find_by_primary_key(key_fields)
        if row_to_update is None:
            return str(0)+' '+"row updated"
        # check primary key duplicate
        pkey_list = self.get_key_column()
        for i in range(len(pkey_list)):
            if new_values.get(pkey_list[i]) is not None and new_values.get(pkey_list[i]) != key_fields[i]:
                key_test.append(new_values.get(pkey_list[i]))
                do_test = True
            else:
                key_test.append(key_fields[i])

        if do_test:
            test_row = self.find_by_primary_key(key_test)
            if test_row is not None:
                raise Exception("can't update with duplicated primary key")
        # update the row
        for k, v in new_values.items():
            row_to_update[k] = v

        return str(1)+' '+"row updated"

    def update_by_template(self, template, new_values):
        """
        :param template: Template for rows to match.
        :param new_values: New values to set for matching fields.
        :return: Number of rows updated.
        """

        # Iterate through rows, if matches, update the row... what should you check first?
        counter = 0
        do_update = False
        # check duplicate primary key first
        for row in reversed(self.get_rows()):
            if self.matches_template(row, template):
                do_update = True
                key_test = []
                do_test = False
                for column in self.get_key_column():
                    if new_values.get(column) is not None and row[column] != new_values.get(column):
                        key_test.append(new_values[column])
                        do_test = True
                    else:
                        key_test.append(row[column])
                    if do_test:
                        test_row = self.find_by_primary_key(key_test)
                        if test_row is not None:
                            raise Exception("can't update with duplicated primary key")

        # update
        if do_update:
            for row in reversed(self.get_rows()):
                if self.matches_template(row, template):
                    for k, v in new_values.items():
                        row[k] = v
                        counter += 1
        return str(counter)+' '+"rows updated"

    def insert(self, new_record):
        """
        Inserts a new record
        :param new_record: A dictionary representing a row to add to the set of records.
        :return: None
        """

        # HINT: Append a new_record... what should you check first?
        key_test = []
        for column in self.get_key_column():
            key_test.append(new_record[column])
        if self.find_by_primary_key(key_test) is not None:
            raise Exception("can't insert with duplicated primary key")
        else:
            self.get_rows().append(new_record)
        return
        
    def get_rows(self):
        return self._rows
