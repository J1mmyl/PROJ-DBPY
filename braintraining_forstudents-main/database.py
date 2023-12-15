"""
Author      : Jimmy LAM
Date        : 24.11.2023
Version     : v1
"""
import mysql.connector
import datetime
import pathlib
import csv

var = []

# identifiants mysql
config = {
  'user': 'root',
  'host': '127.0.0.1',
  'database': 'mygame',
  'raise_on_warnings': True,
  'autocommit': True,
  'buffered': True
}

# start connection
mydb = mysql.connector.connect(**config)

def save_game(results):
    sql="INSERT INTO results (pseudo,date_hour,during,exercise,nb_ok,nb_trials) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor = mydb.cursor()
    cursor.execute(sql, (results[0], results[1],results[2],results[3],results[4],results[5]))
    cursor.close()

def get_database_infos(pseudo):
    infos = []
    cursor = mydb.cursor()
    if pseudo:
        sql = "SELECT id FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        ids = cursor.fetchall()
        infos.append(ids)
    
        sql = "SELECT pseudo FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        pseudos = cursor.fetchall()
        infos.append(pseudos)

        sql = "SELECT date_hour FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        date_hours = cursor.fetchall()
        infos.append(date_hours)

        sql = "SELECT during FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        durings = cursor.fetchall()
        infos.append(durings)

        sql = "SELECT exercise FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        exercises = cursor.fetchall()
        infos.append(exercises)

        sql = "SELECT nb_ok FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        nboks = cursor.fetchall()
        infos.append(nboks)

        sql = "SELECT nb_trials FROM results WHERE pseudo LIKE %s"
        cursor.execute(sql, (pseudo,))
        nbtrials = cursor.fetchall()
        infos.append(nbtrials)

    else:
        sql = "SELECT id FROM results"
        cursor.execute(sql)
        ids = cursor.fetchall()
        infos.append(ids)

        sql="SELECT pseudo FROM results"
        cursor.execute(sql)
        pseudos = cursor.fetchall()
        infos.append(pseudos)

        sql = "SELECT date_hour FROM results"
        cursor.execute(sql)
        date_hours = cursor.fetchall()
        infos.append(date_hours)

        sql = "SELECT during FROM results"
        cursor.execute(sql)
        durings = cursor.fetchall()
        infos.append(durings)

        sql = "SELECT exercise FROM results"
        cursor.execute(sql)
        exercises = cursor.fetchall()
        infos.append(exercises)

        sql = "SELECT nb_ok FROM results"
        cursor.execute(sql)
        nboks = cursor.fetchall()
        infos.append(nboks)

        sql = "SELECT nb_trials FROM results"
        cursor.execute(sql)
        nbtrials = cursor.fetchall()
        infos.append(nbtrials)

        print("INFO :" + str(infos))
    cursor.close()
    return infos
