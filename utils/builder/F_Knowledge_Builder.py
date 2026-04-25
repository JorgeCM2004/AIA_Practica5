from pathlib import Path

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from tqdm import tqdm


class Knowledge_Builder:
	def __init__(self):
		self.base_dir = Path(__file__).parent.parent.parent
		self.data_path = self.base_dir / "data" / "ghana_maternal_health.csv"
		self.db_path = self.base_dir / "chroma_db"

		self.client = chromadb.PersistentClient(path=str(self.db_path))

		self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
			model_name="all-MiniLM-L6-v2"
		)

		self.collection = self.client.get_or_create_collection(
			name="maternal_health_knowledge", embedding_function=self.embedding_fn
		)

	def build(self, force_build=False):
		if force_build:
			try:
				self.client.delete_collection(name="maternal_health_knowledge")
			except ValueError:
				pass

			self.collection = self.client.create_collection(
				name="maternal_health_knowledge", embedding_function=self.embedding_fn
			)
		else:
			if self.collection.count() > 0:
				return

		df = pd.read_csv(self.data_path)

		documents = []
		metadatas = []
		ids = []

		for index, row in df.iterrows():
			pregunta = str(row["Question"]).strip()
			respuesta = str(row["Answer"]).strip()

			texto_completo = (
				f"Patient Symptom/Query: {pregunta}\nMedical Action: {respuesta}"
			)

			documents.append(texto_completo)
			metadatas.append({"question": pregunta, "answer": respuesta})
			ids.append(f"clinical_case_{index}")

		batch_size = 5000

		for i in tqdm(
			range(0, len(documents), batch_size),
			desc="Indexando vectores",
			unit="batch",
		):
			end_idx = min(i + batch_size, len(documents))

			self.collection.add(
				documents=documents[i:end_idx],
				metadatas=metadatas[i:end_idx],
				ids=ids[i:end_idx],
			)
