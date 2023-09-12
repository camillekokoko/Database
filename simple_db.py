import os

from b_tree import BTree


class SimpleDatabase:
    def __init__(self):
        # before an actual table is loaded, class members are set to None
        
        # a header is a list of column names
        # e.g., ['name', 'id', 'grade']
        self.header = None
        
        # map column name to column index in the header
        self.columns = None
        
        # None if table is not loaded
        # otherwise list b-tree indices corresponding to columns 
        self.b_trees = None

        # rows contains actual data; this is a list of lists
        # specifically, this is a list of rows, where each row
        # is a list of values for each column
        # e.g., if a table with the above header has two rows
        # self.rows can be [['Alice', 'a1234', 'HD'], ['Bob', 'a7654', 'D']]
        self.rows = None

        # name of the loaded table
        self.table_name = None

    def get_table_name(self):
        return self.table_name

    def load_table(self, table_name, file_name):
        # note our DBMS only supports loading one table at a time
        # as we load new table, the old one will be lost
        print(f"loading {table_name} from {file_name} ...")

        if not os.path.isfile(file_name):
            print("File not found")
            return

        # note, you could use a CSV module here, also we don't check
        # correctness of file
        with open(file_name) as f:
            self.header = f.readline().rstrip().split(",")
            self.rows = [line.rstrip().split(",") for line in f]
        self.table_name = table_name
        
        self.columns = {}
        for i, column_name in enumerate(self.header):
            self.columns[column_name] = i
            
        self.b_trees = [None] * len(self.header)
        print("... done!")

    def select_rows(self, table_name, column_name, column_value):
        # modify this code such that row selection uses index if it exists
        # note that our DBMS only supports loading one table at a time

        ## Select rows from the table based on a given column name and value.
        ## Then use the index from B-tree index for that column if it exists.

        ## Check if the table name matches the loaded table.
        if table_name != self.table_name:
            # no such table
            return [], []

        ## Check if the column name exists in the table.
        if column_name not in self.columns:
            # no such column
            return self.header, []

        col_id = self.columns[column_name]

        ## Use B-tree index if it exists for that column, otherwise, use linerar search.
        if self.b_trees[col_id]: #This checks if a binary search tree (b_tree) exists for the given col_id column. A binary search tree is a data structure that allows efficient searching of data.
            search_result = self.b_trees[col_id].search_key(column_value)
            if search_result: 
                selected_rows = [self.rows[i] for i in search_result[0].key_vals[search_result[1]][1]] #This line creates a list of selected rows based on the search result.
            else:
                selected_rows = []
        else:
            selected_rows = [row for row in self.rows if row[col_id] == column_value]
            
        return self.header, selected_rows

    def create_index(self, column_name):

        ## Check if a table is loaded.
        if self.header is None:
            return "No table is loaded."

        ## Check if the column name exists in the table.
        if column_name not in self.columns:
            return f"Column {column_name} does not exist."

        ## Creates a B-tree index for a specified column.
        col_index = self.columns[column_name] #It gets the index of the specified column (col_index) from the self.columns dictionary.

        values = [row[col_index] for row in self.rows] #It extracts all the values from the specified column for each row in the table and stores them in the values list.
        
        self.b_trees[col_index] = BTree() #It initializes a new B-tree (presumably using a class or module named BTree).

        for i, value in enumerate(values): #It iterates through the values list along with their corresponding indices (i) and inserts each value into the B-tree along with its index. This indexing can help in efficient searching and retrieval of data.
            self.b_trees[col_index].insert_key(value, i)
        return f"Index created on column {column_name}."

    def drop_index(self, column_name):

        ## Check if a table is loaded.
        if self.header is None:
            return "No table is loaded."

         ## Check if the column name exists in the table.
        if column_name not in self.columns:
            return f"Column {column_name} does not exist."

        ## Drop the B-tree index
        col_index = self.columns[column_name]
        self.b_trees[col_index] = None

        return f"Index on column {column_name} dropped."

    def get_indexed_columns(self):
        ## Get the names of columns for which a B-tree index exists.
        indexed_columns = []

        for i in range(len(self.b_trees)):
            tree = self.b_trees[i]
            if tree is not None:
                column_name = self.header[i]
                indexed_columns.append(column_name)

        return indexed_columns