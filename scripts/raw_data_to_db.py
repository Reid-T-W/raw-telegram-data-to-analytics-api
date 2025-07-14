import csv
import psycopg2

def create_connection():
    # connection establishment
    conn = psycopg2.connect(
        database="telegram-raw-medical-data",
            user='postgres',
            password='test_server',
            host='localhost',
            port= '5432'
    )

    conn.autocommit = True
    return conn

def create_table(conn):
    """ create tables in the PostgreSQL database"""
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

    try:
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # # close communication with the PostgreSQL database server
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()

def post_to_db(reader, conn):
    posts = []
    for data in reader:
        posts.append(data)
    print("lengh of data to post: ", len(posts))
    posts_data = posts[1:]
    cur = conn.cursor()
    cur.executemany("INSERT INTO messages (channel_name, message_id, date_posted, message_text) VALUES(%s,%s,%s, %s)", posts_data)

if __name__ == "__main__":
    # Iterate throught each of the folders in data/raw/telegram_messages
    # Save the folder name in a variable titled telegram_channel_name
    # Open the csv and copy each of the columns to a postgresdb
    # csv_file = f"{channel_username}/messages.csv"
    # csv_file = r"..\data\raw\telegram_messages\CheMed123\messages.csv"
    csv_file = r"..\data\raw\telegram_messages\HakimApps_Guideline\messages.csv"
    # csv_file = r"..\data\raw\telegram_messages\lobelia4cosmetics\messages.csv"
    # csv_file = r"..\data\raw\telegram_messages\tenamereja\messages.csv"
    # csv_file = r"..\data\raw\telegram_messages\tikvahpharma\messages.csv"
    with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        conn = create_connection()
        create_table(conn)
        post_to_db(reader, conn)
