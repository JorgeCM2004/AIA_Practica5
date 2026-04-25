import json
from pathlib import Path

import kagglehub
import pandas as pd


class Data_Downloader:
	def __init__(self):
		self.data_dir = Path(__file__).parent.parent.parent / "data"

	def download(self):
		dataset_path = kagglehub.dataset_download(
			"ghanaairesnet/ghana-maternal-health-q-and-a-dataset-ga-english",
			force_download=True,
		)
		downloaded_folder = Path(dataset_path)

		self.data_dir.mkdir(parents=True, exist_ok=True)
		final_csv_path = self.data_dir / "ghana_maternal_health.csv"

		json_files = list(downloaded_folder.rglob("*.json"))
		all_dataframes = []
		for json_file in json_files:
			with open(json_file, "r", encoding="utf-8") as f:
				raw_data = json.load(f)

			if isinstance(raw_data, dict) and "qa_pairs" in raw_data:
				df_temp = pd.json_normalize(raw_data["qa_pairs"])
			else:
				df_temp = pd.json_normalize(raw_data)

			df_temp = df_temp[["question_english", "answer"]]
			df_temp.columns = ["Question", "Answer"]
			all_dataframes.append(df_temp)

		master_df = pd.concat(all_dataframes, ignore_index=True)

		master_df.to_csv(final_csv_path, index=False, encoding="utf-8")
