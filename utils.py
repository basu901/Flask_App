import sqlite3, json, requests

from urllib.request import pathname2url
from enum import Enum

class Constants(Enum):
    DRINK_NAME_API = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s="

    #dispalys a random cocktail
    DRINK_RANDOM_API = "www.thecocktaildb.com/api/json/v1/1/random.php"
    
    API_DRINK_NAME = "strDrink"
    API_DRINK_INSTR = "strInstructions"
    API_DRINK_IMAGE = "strDrinkThumb"
    API_DRINK_GLASS = "strGlass"

def data_population(path_to_db):
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(path_to_db))
        conn = sqlite3.connect(dburi,uri=True)
    except sqlite3.OperationalError:
        create_database(path_to_db)
    #Populate the data here to fill the object using SQLAlchemy

def create_database(path_to_db):
    conn = sqlite3.connect(path_to_db)
    columns = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "dname VARCHAR UNIQUE NOT NULL",
        "instructions VARCHAR NOT NULL",
        "glass VARCHAR",
        "image BLOB"
    ]
    create_table_cmd = f"CREATE TABLE IF NOT EXISTS cocktails ({','.join(columns)})"
    conn.execute(create_table_cmd)
    populate_data(conn)


def populate_data(conn):
    url = Constants.DRINK_NAME_API.value
    drink_list = ["margarita","mojito","whiskey sour","martini"]
    for drink in drink_list:
        #You need to iterate through all the items over the drinks in a drink type list
        new_url = f"{url}{drink}"
        response = requests.get(new_url)
        payload = response.json()["drinks"]
        for item in payload:
            dname = item[Constants.API_DRINK_NAME.value]
            instructions = item[Constants.API_DRINK_INSTR.value]
            glass = item[Constants.API_DRINK_GLASS.value]
            image = item[Constants.API_DRINK_IMAGE.value]
            to_print = f"{dname},{instructions}{glass},{image}\n"
            print(to_print)
            #specifying column values to prevent primary key insertion error
            insert_table_cmd = "INSERT INTO cocktails(dname,instructions,glass,image) VALUES (?,?,?,?)"
            conn.execute(insert_table_cmd,[dname,instructions,glass,image])
    conn.commit()

