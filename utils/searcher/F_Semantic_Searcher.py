from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


class Semantic_Searcher:
	def __init__(self):
		self.base_dir = Path(__file__).parent.parent.parent
		self.db_path = self.base_dir / "chroma_db"

		self.client = chromadb.PersistentClient(path=str(self.db_path))

		self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
			model_name="all-MiniLM-L6-v2"
		)

		self.collection = self.client.get_collection(
			name="maternal_health_knowledge", embedding_function=self.embedding_fn
		)

	def search(self, user_query, top_k=3):
		return self.collection.query(query_texts=[user_query], n_results=top_k)
