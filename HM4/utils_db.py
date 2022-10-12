import sqlite3
import os

from typing import List


def execute_query(query_str: str) -> List:
    """
    function for querying objects from database
    :param query_str: just sql query
    :return: the result of processed query
    """
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    result = cur.execute(query_str).fetchall()
    connection.close()
    return result


def get_filter_customers(city: str, state: str) -> List:
    """
    Execute query to database and returns filtered list
    with certain state and city
    :param city: The name of city
    :param state: The of state
    :return: Only objects with certain state
    and city
    """

    query_sql = '''
                SELECT *
                    FROM customers'''
    if city and state:
        query_sql += f" WHERE City = '{city}' AND State = '{state}';"
    elif city:
        query_sql += f" WHERE City = '{city}';"
    elif state:
        query_sql += f" WHERE State = '{state}';"
    return execute_query(query_sql)


def get_first_name_count():
    query_sql = '''
                    SELECT FirstName, COUNT(FirstName)
                    FROM customers
                    GROUP BY FirstName 
                    ORDER BY COUNT(FirstName) DESC;'''
    return execute_query(query_sql)


def get_total_sum():
    query_str = '''
                SELECT SUM(UnitPrice * Quantity)
                FROM invoice_items;'''
    return execute_query(query_str)


def pretty_print(data):
    result = ''''''
    for item in data:
        result += ' '.join(map(str, item)) + '  ||   '
    return result
