import csv
import os
import re
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
    elif type == "messages_images":
        command = (
            """
            CREATE TABLE messages_images (
                id SERIAL PRIMARY KEY,
                channel_name VARCHAR(255) NOT NULL,
                message_id VARCHAR(255) NOT NULL,
                has_image BOOLEAN NOT NULL
            )
            """
        )
    elif type == "image_items":
        command = (
            """
            CREATE TABLE image_items (
                id SERIAL PRIMARY KEY,
                channel_name VARCHAR(255) NOT NULL,
                message_id VARCHAR(255) NOT NULL,
                item VARCHAR(255) NULL
            )
            """
        )
    try:
        cur = conn.cursor()
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def post_to_db(reader=None, conn=None, type=None, messages_with_images = None, channel_name=None, all_yolo_detections=None):
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
    elif type == "messages_images":
        for message_id in messages_with_images:
            cur = conn.cursor()
            cur.execute("INSERT INTO messages_images (channel_name, message_id, has_image) VALUES(%s, %s,%s)", (channel_name, message_id, True))
    elif type == "image_items":
        for yolo_detection in all_yolo_detections:
            cur = conn.cursor()
            # print("yolo detection: ", yolo_detection)
            cur.execute("INSERT INTO image_items (channel_name, message_id, item) VALUES(%s, %s, %s)", (yolo_detection[0], yolo_detection[1], yolo_detection[2]))  


if __name__ == "__main__":
    # message_locations = [
    #     r"src\data\raw\telegram_messages\CheMed123\messages.csv",
    #     r"src\data\raw\telegram_messages\HakimApps_Guideline\messages.csv",
    #     r"src\data\raw\telegram_messages\lobelia4cosmetics\messages.csv",
    #     r"src\data\raw\telegram_messages\tenamereja\messages.csv",
    #     r"src\data\raw\telegram_messages\tikvahpharma\messages.csv"
    # ]

    # image_directories = [
    #     r"src\data\raw\telegram_messages\CheMed123",
    #     r"src\data\raw\telegram_messages\HakimApps_Guideline",
    #     r"src\data\raw\telegram_messages\lobelia4cosmetics",
    #     r"src\data\raw\telegram_messages\tenamereja",
    #     r"src\data\raw\telegram_messages\tikvahpharma"
    # ]

    # # Populating data into message table
    conn = create_connection()
    # create_table(conn, 'messages')
    
    # for location in message_locations:
    #     csv_file = location
    #     with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
    #         reader = csv.reader(csvfile)
    #         post_to_db(reader, conn, 'messages')
    
    # # Populating data into llm_extracts_for_messages table
    # create_table(conn, 'llm_extracts')
    # csv_file = r"src\data\raw\extracted_llm_data.csv"
    # with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
    #     reader = csv.reader(csvfile)
    #     post_to_db(reader, conn, 'llm_extracts')

    # # Populating data on images
    # create_table(conn, 'messages_images')

    # messages_with_images = []
    # for directory in image_directories:
    #     # Extract channel name
    #     channel_name = os.path.basename(directory).split('\\')[-1]
    #     for entry in os.scandir(directory):  
    #         if entry.is_file():
    #             print(entry.path)
    #             entries = os.path.basename(entry.path).split('_')  
    #             if len(entries) > 1:
    #                 messages_with_images.append(entries[1])
    #     post_to_db(conn=conn, type='messages_images', messages_with_images=messages_with_images, channel_name=channel_name)
    #     messages_with_images = []

    # Populating yolo data
    # Create table
    create_table(conn, 'image_items')
    all_yolo_detections = []
    # Read data from excel
    csv_file = r"src\data\raw\yolo_detctions.csv"
    with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for data in reader:
            # print(data)
            # channel_name = os.path.basename(data[0]).split('/')[-1]
            channel_name = os.path.basename(os.path.dirname(data[0]))
            message_id = os.path.basename(data[0]).split('_')[1]
            if len(data) > 0:
                detections = data[1].split(',')
                for record in detections:
                    data_to_insert = [channel_name, message_id, record]
                    all_yolo_detections.append(data_to_insert)
    post_to_db(conn=conn, type='image_items', all_yolo_detections=all_yolo_detections)
    # print(all_yolo_detections)


            # posts.append(data)


    # for directory in image_directories:
    #     # Extract channel name
    #     channel_name = os.path.basename(directory).split('\\')[-1]
    #     for entry in os.scandir(directory):  
    #         if entry.is_file():
    #             print(entry.path)
    #             entries = os.path.basename(entry.path).split('_')  
    #             if len(entries) > 1:
    #                 message_id = entries[1]






    # # Iterate throught each of the folders in data/raw/telegram_messages
    # # Save the folder name in a variable titled telegram_channel_name
    # # Open the csv and copy each of the columns to a postgresdb
    # # csv_file = f"{channel_username}/messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\CheMed123\messages.csv"
    # csv_file = r"..\data\raw\telegram_messages\HakimApps_Guideline\messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\lobelia4cosmetics\messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\tenamereja\messages.csv"
    # # csv_file = r"..\data\raw\telegram_messages\tikvahpharma\messages.csv"

