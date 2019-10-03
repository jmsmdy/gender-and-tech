import config
import mysql
import mysql.connector
from mysql.connector import errorcode
from functions import *
import pandas as pd
import numpy as np
import math

# functions for intserting to UN data tables

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
    
    
# functions for inserting to speicial UN data table on abortion laws from 2015    
def get_tuples_special(df):
    """takes a dataframe and returns a list of tuples of each row with relevant columns"""
    tuple_list = []
    for index, row in df.iterrows():
        tup = tuple(row[['Country Name', 'Source Code', 'Revision Year', 'Variable Name', 
                         'Variable Response']])
        tuple_list.append((tup[0], 
                           tup[1], 
                           int(tup[2]) if not math.isnan(tup[2]) else None, 
                           tup[3], 
                           len(tup[4].split(','))
                          ))
    return tuple_list
    
def insert_data_special(table_name, csv_name):
    """ generates and cleans csv data into a pandas data frame, then executes insert inquiry 
    to a pre-existing table (table_name) on AWS """
    cur, cnx = connect_to_db('gender')
    df2 = pd.read_csv(f'Data To Use/{csv_name}.csv')
    # cleaning df to ensure proper types
    df2['Year'] = pd.to_numeric(df2['Revision Year'], errors = 'coerce')
    df2['Value'] = pd.to_numeric(df2['Variable Response'], errors = 'coerce')
    cur.executemany(insert_query(table_name), get_tuples_special(df2))
    cnx.commit()
    cnx.close()    
    
# functions for intserting to Honeypot data table

def insert_more_query(table_name):
    insert_query = f'''INSERT IGNORE INTO {table_name} (
        country,
        total_workforce_millions,
        female_workforce_millions,
        percent_women_workers,
        percent_women_legislators_senior_officials_and_managers,
        percent_women_in_parliament,
        percent_women_in_ministerial_positions,
        overall_workforce_average_wage_USD,
        womens_average_wage_USD,
        gender_pay_gap_percentage,
        tech_workforce_thousands,
        percent_workforce_in_tech,
        female_tech_workforce_thousands,
        percent_women_in_tech,
        percent_difference_of_women_in_workforce_and_women_in_tech,
        female_stem_graduates_percentage,
        tech_average_wage_USD,
        tech_average_wage_for_women_USD,
        gender_pay_gap_in_tech_percentage,
        percent_difference_overall_gender_pay_gap_vs_tech_gender_pay_gap,
        gender_inequality_index,
        gender_pay_gap_2010,
        comparison_of_gender_pay_gap_from_2010_to_2015
        )
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
    return insert_query

def get_more_tuples(df):
    tuple_list = []
    for index, row in df.iterrows():
        tup = (row[1],
               row[2],
               row[3],
               float(row[4][:-1]),
               float(row[5][:-1]),    
               float(row[6][:-1]),
               float(row[7][:-1]),
               row[8],
               row[9],
               float(row[10][:-1]),
               row[11],
               float(row[12][:-1]),
               row[13],
               float(row[14][:-1]),
               float(row[15][:-1]),
               float(row[16][:-1]),
               row[17],
               row[18],
               float(row[19][:-1]),
               float(row[20][:-1]),
               row[21],
               float(row[22][:-1]),
               float(row[23][:-1])
              ) 
        tuple_list.append(tup)
    return tuple_list