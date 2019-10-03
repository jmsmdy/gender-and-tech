from statsmodels.formula.api import ols
import statsmodels.api as sm
import config
import mysql
import mysql.connector
from mysql.connector import errorcode
from functions import *
from SQL_functions import *
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# SQL Querying for Analysis
def get_data(query):
    """ creates a data frame from the queried data """
    cur, cnx = connect_to_db('gender')
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [i[0] for i in cur.description]
    cnx.close()
    return df

def get_attributes_query(attribute_1, attribute_table_1, attribute_2, 
                         attribute_table_2 = 'women_in_tech'):
    """ returns a query to select and join desired data from 2 different tables """
    query1 = f'''SELECT a.country , a.{attribute_1[0]} as {attribute_1[1]},
                                    w.{attribute_2[0]} as {attribute_2[1]}
                FROM gender.{attribute_table_1} as a
                INNER JOIN gender.{attribute_table_2} as w ON w.country = a.country;'''
    return query1


# Modeling functions
def anova_table_and_summary(df, dep_var, ind_var):
    anova_test = ols(f'{dep_var}~{ind_var}',data=df).fit() 
    print(anova_test.summary())
    anova_table = sm.stats.anova_lm(anova_test, typ=2)
    print(pd.DataFrame(anova_table))