import csv
import tiktoken


class DataLoader:
    def __init__(self):
        self.available_channels = [
            "CheMed123",
            "HakimApps_Guideline",
            "lobelia4cosmetics",
            "tenamereja",
            "tikvahpharma",
        ]

        self.channel_locations = {
            "CheMed123": r"src\data\raw\telegram_messages\CheMed123\messages.csv",
            "HakimApps_Guideline": r"src\data\raw\telegram_messages\HakimApps_Guideline\messages.csv",
            "lobelia4cosmetics" : r"src\data\raw\telegram_messages\lobelia4cosmetics\messages.csv",
            "tenamereja": r"src\data\raw\telegram_messages\tenamereja\messages.csv",
            "tikvahpharma": r"src\data\raw\telegram_messages\tikvahpharma\messages.csv"
        }

    def load_data_by_channel(self, channel_name):
        """
        Loads a telegram's channel data from csv
        """
        max_tokens = 128000
        total_token = 0
        token_upper_limit = (max_tokens/2) - 20000
        lines=""

        if channel_name not in self.available_channels:
            raise Exception(f"Channel does not exist, available channels are {self.available_channels}")
        
        channel_location = self.channel_locations.get(channel_name)
        print(f"Loading data for channel, {channel_name}")
        print(f"CSV location for {channel_name} is {channel_location}")
        csv_file = channel_location
        # # csv_file = r"..\data\raw\telegram_messages\lobelia4cosmetics\messages.csv"
        # # csv_file = r"..\data\raw\telegram_messages\tenamereja\messages.csv"
        # # csv_file = r"..\data\raw\telegram_messages\tikvahpharma\messages.csv"
        with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            # Removing first row (column titles)
            first_row = next(reader, None)

            for data in reader:
                line = f"{data[0]},{data[1]},{data[3]}"
                lines += "\n" + line
                tokens = self.estimate_no_of_tokens(lines)

                if tokens >= 1000:
                    print("Tokeeeeeeeeeeeeeeeeeeeeeens: ", tokens)
                    yield lines
                    lines=""

    def estimate_no_of_tokens(self, data):
        """
        Estimates the number of tokens for a given text
        """
        encoding = tiktoken.encoding_for_model("gpt-4")
        num_tokens = len(encoding.encode(data))
        return num_tokens
        

data_loader = DataLoader()