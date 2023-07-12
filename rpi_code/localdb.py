
import mysql.connector as mariadb
import csv

def mariadb_con():
    mariadb_connection = mariadb.connect(user="root", password="root_password", database="local_data")
    cursor = mariadb_connection.cursor()    
    return mariadb_connection, cursor     

def store_data(reading):
    keys = ", ".join(f"`{key}`" for key in reading.keys())
    values = ", ".join(f"'{reading[key]}'" for key in reading.keys())
    
    mariadb_connection, cursor = mariadb_con()
    sql = f"INSERT INTO `storage_v2`({keys}) VALUES ({values})"
    cursor.execute(sql)
    mariadb_connection.commit()

def extract_to_csv(date_time, rpi_id, room_id):
    file_name = f"{rpi_id}_{room_id}.csv"
    mariadb_connection, cursor = mariadb_con()
    sql = f"""
    SELECT * FROM `storage_v2` 
    WHERE `rpi_id`='{rpi_id}' AND `room_id`='{room_id}' AND `date_time`>'{date_time}'
    """
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    
    with open(file_name, "w") as fp:
        file = csv.writer(fp, lineterminator = "\n")
        file.writerow(column_names)   
        file.writerows(rows)

    return file_name
