import config
import mysql
import mysql.connector
from mysql.connector import errorcode
from functions import *
import pandas as pd
import numpy as np
import math

def insert_query(table_name):
    """ calls SQL query to insert country, subgroup, year, unit, value into pre-existing table """
    insert_query = f"""
    INSERT IGNORE INTO {table_name} 
    (country, subgroup, year, unit, value)
    VALUES 
    (%s, %s, %s, %s, %s)
    """
    return insert_query
    
def get_tuples(df):
    """takes a dataframe and returns a list of tuples of each row with relevant columns"""
    tuple_list = []
    for index, row in df.iterrows():
        tup = tuple(row[['Country or Area', 'Subgroup', 'Year', 'Unit', 'Value']])
        tuple_list.append((tup[0], 
                           tup[1], 
                           int(tup[2]) if not math.isnan(tup[2]) else None, 
                           tup[3], 
                           int(tup[4]) if not math.isnan(tup[4]) else None
                          ))
    return tuple_list


def insert_data(table_name, csv_name):
    """ generates and cleans csv data into a pandas data frame, then executes insert inquiry 
    to a pre-existing table (table_name) on AWS """
    cur, cnx = connect_to_db('gender')
    df = pd.read_csv(f'Data To Use/{csv_name}.csv')
    # cleaning df to ensure proper end point
    stop = df.loc[df['Country or Area'] == 'fnSeqID'].index[0]
    df2 = df.iloc[0:stop]
    # cleaning df to ensure proper types
    df2['Year'] = pd.to_numeric(df2['Year'], errors = 'coerce')
    df2['Value'] = pd.to_numeric(df2['Value'], errors = 'coerce')
    cur.executemany(insert_query(table_name), get_tuples(df2))
    cnx.commit()
    cnx.close()