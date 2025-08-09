import time
import os
from openai import OpenAI
from src.helper.data_loader import data_loader as data_loader_instance
from src.helper.data_saver import data_saver as data_saver_instance

client = OpenAI(
    base_url="https://api.cohere.ai/compatibility/v1",
    api_key=os.environ.get('COHOR_API_KEY'),
)

def extract_intent(text):
    """
    Test
    """
    prompt = f"""
    You will be given multiple lines of data, each on a new line. Each line consists of three columns: the first column is the Telegram channel name, the second column is the message ID, and the third column is the actual message.

    Your task is to:
    1. Identify the **main intent** of the third column (the message).
    2. If the intent is **ProductPromotion**, identify the name of the main product being promoted.
    3. Choose **only one intent** from the following list for each message:

    - ProductPromotion
    - HealthTip
    - GeneralAnnouncement
    - CustomerServiceInfo
    - Reminder
    - Other

    Now, for each line of input, return a corresponding output line in the **exact same order**, formatted strictly like this:
    
    <channel_name>,<message_id>,<intent>,<product_name_or_dash>
    
    If the intent is not **ProductPromotion**, use `-` in place of the product name.

    **Return only the output lines** (no explanations, no bullet points, no extra text, no markdown, no numbering).

    Messages:
    {text}
    """


    
    completion = client.chat.completions.create(
        model="command-a-03-2025",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content


if __name__ == '__main__':
    # Example input
    # loader = data_loader_instance.load_data_by_channel("HakimApps_Guideline")
    # loader = data_loader_instance.load_data_by_channel("CheMed123")
    # loader = data_loader_instance.load_data_by_channel("lobelia4cosmetics")
    # loader = data_loader_instance.load_data_by_channel("tenamereja")
    loader = data_loader_instance.load_data_by_channel("tikvahpharma")
    api_call_count = 0
    max_calls_before_pause = 5

    for batch in loader: 
        lines = batch
        # print(lines)
        extracted_data = extract_intent(lines)
        print(extracted_data)
        data_saver_instance.save_to_csv(extracted_data)

        # Increment API call counter
        api_call_count += 1

        # After every 20 API calls, wait 60 seconds
        if api_call_count % max_calls_before_pause == 0:
            print(f"Reached {max_calls_before_pause} API calls. Waiting for 1 minute...")
            time.sleep(60)

