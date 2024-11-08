"""
A script for testing the RAG Chatbot using a LlamaIndex Workflow
"""

import sys
from pathlib import Path


from llama_index.utils.workflow import draw_all_possible_flows

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from workflows.rag import RAGWorkflow

# uncomment the following to generate workflow visualization
draw_all_possible_flows(RAGWorkflow, filename="rag_workflow.html")

# test the workflow by uncommenting the code below and running the following command:
# python -m workflows.rag

# async def main():
#     w = RAGWorkflow()
#     result = await w.run(query="贾宝玉的父亲对他有什么看法？")
#     print(result)


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
