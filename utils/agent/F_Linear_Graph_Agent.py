from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from utils.security.F_prompt_injection import injection_node
from utils.security.F_anonymizer import anonymize_node
from langgraph.graph import END, StateGraph


class GraphState(TypedDict):
	question: str
	context: str
	answer: str
	is_safe: str


class Linear_Graph_Agent:
	def __init__(self, searcher, model_name="llama3.2"):
		self.searcher = searcher
		self.llm = OllamaLLM(model=model_name)

		self.template = """You are a compassionate, professional maternal health assistant.
        Answer the patient's query using ONLY the provided medical context.
        If the context does not contain the answer, explicitly say: "I cannot provide a safe answer based on the medical guidelines available to me."
        Always recommend consulting an obstetrician for severe symptoms.

        MEDICAL CONTEXT:
        {context}

        PATIENT QUERY:
        {question}

        ANSWER:"""
		self.prompt = PromptTemplate(
			template=self.template, input_variables=["context", "question"]
		)

		self.app = self._build_graph()

	def retrieve_node(self, state: GraphState) -> GraphState:
		q = state["question"]

		top_k = self.searcher.search(q, top_k=3)
		contexto_recuperado = "\n\n".join(top_k["documents"][0])

		state["context"] = contexto_recuperado
		return state

	def generate_node(self, state: GraphState) -> GraphState:
		chain = self.prompt | self.llm | StrOutputParser()

		out = chain.invoke({"context": state["context"], "question": state["question"]})

		state["answer"] = out
		return state

	def security_node(self, state: GraphState) -> GraphState:
		q = state["question"]
		is_safe = injection_node(self.llm, q)
		state["is_safe"] = is_safe
		if is_safe == "no":
			state["answer"] = "Security Alert: Malicious prompt detected."
		return state

	def anonymize_query_node(self, state: GraphState) -> GraphState:
		q = state["question"]
		safe_query = anonymize_node(q)
		state["question"] = safe_query
		return state

	def route_after_security(self, state: GraphState) -> str:
		if state.get("is_safe") == "no":
			return "end"
		else:
			return "anonymize"

	def _build_graph(self):
		g = StateGraph(GraphState)

		g.add_node("security", self.security_node)
		g.add_node("anonymize", self.anonymize_query_node)
		g.add_node("retrieve", self.retrieve_node)
		g.add_node("generate", self.generate_node)

		g.set_entry_point("security")

		g.add_conditional_edges(
			"security",
			self.route_after_security,
			{
				"end": END,
				"anonymize": "anonymize",
			},
		)

		g.add_edge("anonymize", "retrieve")
		g.add_edge("retrieve", "generate")
		g.add_edge("generate", END)

		return g.compile()

	def run(self, query: str):
		inputs = {"question": query, "context": "", "answer": "", "is_safe": ""}
		final_state = self.app.invoke(inputs)
		return final_state["answer"]
