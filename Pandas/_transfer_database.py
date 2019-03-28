# _transfer_database.py
# Author: John Paximadis, 
  Co-Founder of IEC Infrared Systems, LLC
#==============================================================================
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import argparse
import json
import os
import pandas as pd
import pymssql
import sqlite3

#==============================================================================
def delete_sqlite_db (filename):
    """ Delete the specified SQLite database file. """
    
    if os.path.isfile(filename):
        print("Deleting existing SQLite database '%s'..." % (filename))
        os.remove(filename)

def create_macola_db_connection (server, database, user, password):
    """ Create a connection to the specified Macola database. """
    
    print("Creating Macola DB connection...")
    return pymssql.connect(server, user, password, database)

def create_sqlite_db_connection (filename):
    """ Create a connection to the specified SQLite database. """
    
    print("Creating SQLite DB connection...")
    return sqlite3.connect(filename)

def copy_db_table_bmprdstr_sql (mssql_conn, sqlite_conn):
    """ Copy a subset of fields from Macola's BOM structure table (bmprdstr) to 
    the local SQLite instance. """
    
    print("Copying select fields from table bmprdstr_sql...")
    sql = "SELECT item_no, seq_no, comp_item_no, alt_item_no, qty_per_par FROM bmprdstr_sql;"
    df = pd.read_sql(sql, mssql_conn)
    df.to_sql("bmprdstr_sql", sqlite_conn, index=False)

def copy_db_table_imitmidx_sql (mssql_conn, sqlite_conn):
    """ Copy a subset of fields from Macola's item master table (imitmidx) to 
    the local SQLite instance. """
    
    print("Copying select fields from table imitmidx_sql...")
    sql = "SELECT item_no, item_desc_1, item_desc_2 FROM imitmidx_sql;"
    df = pd.read_sql(sql, mssql_conn)
    df.to_sql("imitmidx_sql", sqlite_conn, index=False)

def copy_db_table_iminvloc_sql (mssql_conn, sqlite_conn):
    """ Copy a subset of fields from Macola's inventory location table (iminvloc) to 
    the local SQLite instance. """
    
    print("Copying select fields from table iminvloc_sql...")
    sql = "SELECT item_no, loc, avg_cost, last_cost FROM iminvloc_sql;"
    df = pd.read_sql(sql, mssql_conn)
    df.to_sql("iminvloc_sql", sqlite_conn, index=False)

def create_sqlite_indices (sqlite_conn):
    """ For efficiency purposes, index the sqlite database tables. """
    
    print("Creating SQLite table indices...")
    cur = sqlite_conn.cursor()
    cur.execute("CREATE UNIQUE INDEX bmprdstr_idx ON bmprdstr_sql (item_no, seq_no);")
    cur.execute("CREATE UNIQUE INDEX imitmidx_idx ON imitmidx_sql (item_no);")
    cur.execute("CREATE UNIQUE INDEX iminvloc_idx ON iminvloc_sql (item_no, loc);")

#==============================================================================
def main (config_file_name):
    """ Application main. """

    # Load the JSON configuration file.
    with open(config_file_name) as json_file:  
        config = json.load(json_file)

    # Create a connection to the Macola MS-SQL database.
    macola_conn = create_macola_db_connection(
        config["macola_db_server"],
        config["macola_db_database"],
        config["macola_db_user"],
        config["macola_db_password"]
    )

    # Delete the current SQLite database (if it exists), and then create a
    # connection to a new instance.
    delete_sqlite_db(config["sqlite_db_file"])
    sqlite_conn = create_sqlite_db_connection(config["sqlite_db_file"])
    
    # Copy select fields from select Macola tables to the local SQLite instance.
    copy_db_table_bmprdstr_sql(macola_conn, sqlite_conn)
    copy_db_table_imitmidx_sql(macola_conn, sqlite_conn)
    copy_db_table_iminvloc_sql(macola_conn, sqlite_conn)

    # Create indices for the local SQLite instance.
    create_sqlite_indices(sqlite_conn)

#==============================================================================
if __name__ == "__main__":
    
    # Configure an argument parser, and then execute it.
    parser = argparse.ArgumentParser(description="Create a local SQLite database " \
        "as a subset of a specified Macola database.")
    
    default_config_file = "./CONFIG.json"
    parser.add_argument("-c", "--config_file",
        help="JSON configuration file (default: '%s')" % (default_config_file), 
        default=default_config_file)
    
    args = parser.parse_args()

    # Execute the application.
    main(args.config_file)

    print("Done.")
    
