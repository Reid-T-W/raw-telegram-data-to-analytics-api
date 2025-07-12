from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto
import asyncio
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def rename_with_id(original_path, message_id):
    dirname, basename = os.path.split(original_path)
    new_name = f"id_{message_id}_{basename}"
    return os.path.join(dirname, new_name)

async def scrape_all_messages(channel_username, total_limit=100, offset_id=0):
    api_id = os.environ.get('TELEGRAM_APP_ID')
    api_hash = os.environ.get('TELEGRAM_APP_HASH')
    client = TelegramClient("session", api_id, api_hash)
    await client.start()
    os.makedirs(channel_username, exist_ok=True)

    offset_id = 0
    all_count = 0
    batch_size = 50

    csv_file = f"{channel_username}/messages.csv"
    with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write CSV header
        writer.writerow(["channel_name", "message_id", "date_posted", "message_text"])

        while all_count < total_limit:
            try:
                messages = await client.get_messages(
                    channel_username,
                    limit=min(batch_size, total_limit - all_count),
                    offset_id=offset_id
                )

                if not messages:
                    break  # No more messages

                for message in messages:
                    if message.text:
                        date_str = message.date.strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([
                            channel_username,
                            message.id,
                            date_str,
                            message.text.replace("\n", " ").strip()
                        ])
                        print(f"all_count {all_count + 1}. date: [{date_str}] message_id: {message.id} offset_id: {offset_id}")
                        all_count += 1

                    if message.media and isinstance(message.media, MessageMediaPhoto):
                      original_path = await message.download_media(file=channel_username + '/')
                      if original_path:
                          new_path = rename_with_id(original_path, message.id)
                          os.rename(original_path, new_path)
                          print(f"Saved image to: {new_path}")
                        # file_path = await message.download_media(file=channel_username + '/')
                        # print(f"Saved image to: {file_path}")

                offset_id = messages[-1].id

            except FloodWaitError as e:
                print(f"FloodWaitError: Sleeping for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(scrape_all_messages("lobelia4cosmetics"))
    asyncio.run(scrape_all_messages("CheMed123"))
    asyncio.run(scrape_all_messages("tikvahpharma"))
    asyncio.run(scrape_all_messages("tenamereja"))
    asyncio.run(scrape_all_messages("HakimApps_Guideline"))