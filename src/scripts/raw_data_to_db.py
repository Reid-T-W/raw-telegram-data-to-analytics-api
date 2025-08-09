import csv
import psycopg2

def create_connection():
    # connection establishment
    conn = psycopg2.connect(
        database="telegram-raw-medical-data-v2",
            user='postgres',
            password='test_server',
            host='localhost',
            port= '5432'
    )

    conn.autocommit = True
    return conn

def create_table(conn, type):
    """ create tables in the PostgreSQL database depending on the type given"""
    if type == 'messages':
        
        command = (
            """
            CREATE TABLE messages (
                id SERIAL PRIMARY KEY,
                channel_name VARCHAR(255) NOT NULL,
                message_id VARCHAR(255) NOT NULL,
                date_posted VARCHAR(255) NOT NULL,
                message_text VARCHAR(5000) NOT NULL
            )
            """
        )
    elif type == 'llm_extracts':
        command = (
            """
            CREATE TABLE llm_extracts_for_messages (
                id SERIAL PRIMARY KEY,
                channel_name VARCHAR(255) NOT NULL,
                message_id VARCHAR(255) NOT NULL,
                intent VARCHAR(255) NOT NULL,
                product_name VARCHAR(5000) NULL
            )
            """
        )
    
    try:
        cur = conn.cursor()
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def post_to_db(reader, conn, type):
    if type == 'messages':
        posts = []
        for data in reader:
            posts.append(data)
        print("lengh of data to post: ", len(posts))
        posts_data = posts[1:]
        cur = conn.cursor()
        cur.executemany("INSERT INTO messages (channel_name, message_id, date_posted, message_text) VALUES(%s,%s,%s, %s)", posts_data)
    elif type == 'llm_extracts':
        extracts = []
        for data in reader:
            extracts.append(data)
        print("lengh of data to post: ", len(extracts))
        extracts_data = extracts[1:]
        cur = conn.cursor()
        cur.executemany("INSERT INTO llm_extracts_for_messages (channel_name, message_id, intent, product_name) VALUES(%s,%s,%s,%s)", extracts_data)

if __name__ == "__main__":
    message_locations = [
        r"src\data\raw\telegram_messages\CheMed123\messages.csv",
        r"src\data\raw\telegram_messages\HakimApps_Guideline\messages.csv",
        r"src\data\raw\telegram_messages\lobelia4cosmetics\messages.csv",
        r"src\data\raw\telegram_messages\tenamereja\messages.csv",
        r"src\data\raw\telegram_messages\tikvahpharma\messages.csv"
    ]

    # Populating data into message table
    conn = create_connection()
    create_table(conn, 'messages')
    
    for location in message_locations:
        csv_file = location
        with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            post_to_db(reader, conn, 'messages')
    
    # Populating data into llm_extracts_for_messages table
    create_table(conn, 'llm_extracts')
    csv_file = r"src\data\raw\extracted_llm_data.csv"
    with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        post_to_db(reader, conn, 'llm_extracts')



    # # Iterate throught each of the folders in data/raw/telegram_messages
    # # Save the folder name in a variable titled telegram_channel_name
    # # Open the csv and copy each of the columns to a postgresdb
    # # csv_file = f"{channel_username}/messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\CheMed123\messages.csv"
    # csv_file = r"..\data\raw\telegram_messages\HakimApps_Guideline\messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\lobelia4cosmetics\messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\tenamereja\messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\tikvahpharma\messages.csv"

