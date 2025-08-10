import csv

class DataSaver:
    def __init__(self):
        pass

    def save_to_csv(self, data):
        # Split the result into lines
        lines = data.strip().splitlines()

        # Save to CSV
        with open(r"src\data\raw\extracted_llm_data.csv", "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["channel_name", "message_id", "intent", "product_name"])
            for line in lines:
                row = line.strip().split(",", maxsplit=3)
                writer.writerow(row)

data_saver = DataSaver()