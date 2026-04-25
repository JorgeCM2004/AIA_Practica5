from utils import Data_Downloader, Hybrid_Searcher, Knowledge_Builder
from utils.agent import Tools_Graph_Agent


def main():
	downloader = Data_Downloader()
	downloader.download()

	builder = Knowledge_Builder()
	builder.build(force_build=False)

	searcher = Hybrid_Searcher()

	rag_system = Tools_Graph_Agent(searcher=searcher, model_name="llama3.2")

	query = input("Question: ")

	while query.strip() != "/bye":
		respuesta = rag_system.run(query)

		print(respuesta)

		query = input("Question: ")


if __name__ == "__main__":
	main()
