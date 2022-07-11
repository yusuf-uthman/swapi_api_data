import requests
from sqlalchemy import create_engine
import requests
# from starwardob import starwardob

# import postgres db credentials fron config file
# password = config.password
# user = config.user
# db = config.db
# port = config.port
# host = config.host

# credentials and variables from github secret
port     = int(os.environ.get("HEROKU_DEMO_PG_PORT"))
schema   = os.environ.get("HEROKU_DEMO_PG_SCHEMA")
table    = os.environ.get("HEROKU_DEMO_PG_TABLE")
password = os.environ.get("HEROKU_DEMO_PG_PASS")
user     = os.environ.get("HEROKU_DEMO_PG_USER")
db       = os.environ.get("HEROKU_DEMO_PG_DB")
host     = os.environ.get("HEROKU_DEMO_PG_HOST")

# # create a connection to postgres database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
conn   = engine.raw_connection()
cursor = conn.cursor()

#variables
# schema  = 'api_schema'
# table = 'swapi_data'

# main function that calls all other functions
def process_api_data(schema, table):
    create_schema(schema)
    drop_table(schema, table)
    create_table(schema, table)
    truncate_table(schema, table)
    insert_data = extract_insert(schema, table)
    query_data = query_db(schema, table)
    if len(insert_data) == len(query_data):
        print(f"""Data count from api and database are {len(insert_data)} and {len(query_data)} respectively. Operation successfull!""")
    else:
        print("""Incomplete data transfer!""")

# create schema function
def create_schema(schema):
    cursor.execute(f""" CREATE SCHEMA IF NOT EXISTS {schema}; """)
    conn.commit()

# create table function
def create_table(schema, table):
    cursor.execute(f"""   
    CREATE TABLE IF NOT EXISTS {schema}.{table}(
                    id SERIAL primary key not null
                    ,name        varchar(200)
                    ,height      varchar(50)
                    ,mass        varchar(50)
                    ,hair_color   varchar(200)
                    ,skin_color   varchar(200)
                    ,eye_color    varchar(200)
                    ,birth_year   varchar(200)
                    ,age          int                    
                    ,gender       varchar(200)
                    ,homeworld    varchar(200)
                    ,films        int
                    ,species      varchar(200)
                    ,vehicles     int
                    ,starships    int
                    ,created      Timestamp
                    ,edited       Timestamp
                    ,url          varchar(200)
                    ,insert_date date DEFAULT now()
                        )
    """)
    conn.commit()

# truncate table function
def truncate_table(schema, table):
    cursor.execute(f""" TRUNCATE TABLE {schema}.{table}; """)
    conn.commit()

# drop table 
def drop_table(schema, table):
    cursor.execute(f""" DROP TABLE IF EXISTS {schema}.{table} CASCADE; """)
    conn.commit()    

# query database function
def query_db(schema, table):
    cursor.execute(f""" select * from {schema}.{table} """)
    db_api_data = []
    for rec in cursor.fetchall():
        db_api_data.append(rec)
    return db_api_data

# function that converts to logical year
def star_war_age(year):
    if (year != 'unknown' and year != "n/a"):
        age = starwardob.StarwarDOB(year).age
    else:
        age = year
    return age

# function to remove unwanted character in a record
def clean_str(data):   
    data = str(data)
    clean_data = data.replace(",",'')
    return clean_data

# extract and insert data function
def extract_insert(schema, table):
    url = "https://swapi.dev/api/people/"
    api_data_list  = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for rec in data['results']:
                rec_list = [
                    rec['name'],
                    rec['height'],
          clean_str(rec['mass']),    
                    rec['hair_color'],
                    rec['skin_color'],
                    rec['eye_color'],
                    rec['birth_year'],
       star_war_age(rec['birth_year']),                    
                    rec['gender'],
                    rec['homeworld'],
                len(rec['films']),
                    rec['species'],
                len(rec['vehicles']),
                len(rec['starships']),
                    rec['created'],
                    rec['edited'],
                    rec['url'],
                ]
                api_data_list.append(rec_list)
        url  = response.json()['next']
    #insert data into the database    
    for rec in api_data_list:
        cursor.execute(f""" 
              insert into {schema}.{table}(name, height, mass, hair_color, skin_color, eye_color, birth_year, age, gender, homeworld,
              films, species, vehicles, starships, created, edited, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", rec)
        conn.commit()
    return api_data_list

# run main function that calls other functions
if __name__ == '__main__':
    process_api_data(schema, table)

# close cursor and connection
cursor.close()
conn.close()
print('postgres db connection closed ')
