# this demo is modified from the original HippoRAG demo
import os

from hipporag import HippoRAG

def main():

    # Prepare datasets and evaluation
    docs = [
        "Oliver Badman is a politician.",
        "George Rankin is a politician.",
        "Thomas Marwick is a politician.",
        "Cinderella attended the royal ball.",
        "The prince used the lost glass slipper to search the kingdom.",
        "When the slipper fit perfectly, Cinderella was reunited with the prince.",
        "Erik Hort's birthplace is Montebello.",
        "Marina is bom in Minsk.",
        "Montebello is a part of Rockland County."
    ]

    save_dir = 'outputs/demo_llama'  # Define save directory for HippoRAG objects (each LLM/Embedding model combination will create a new subdirectory)
    openai_base_url = os.environ.get('OPENAI_BASE_URL', 'http://localhost:4000/v1')  # OpenAI base URL (for local deployment, e.g., Llama 3.1, GritLM, Contriever)
    llm_model_name = os.environ.get('LLM_MODEL_NAME', 'llama-3.1-70b-instruct')  # LLM model name (Llama, GritLM, or Contriever for now)
    embedding_model_name = os.environ.get('EMBEDDING_MODEL_NAME', 'text-embedding')  # include "text-embedding" in embedding model name for local OpenAi API
    # https://github.com/OSU-NLP-Group/HippoRAG/blob/c0a8b6e27f340d7703d83c48c671d2cb5223d712/src/hipporag/embedding_model/__init__.py#L19

    # Startup a HippoRAG instance
    hipporag = HippoRAG(save_dir=save_dir,
                        llm_base_url=openai_base_url,
                        llm_model_name=llm_model_name,
                        embedding_base_url=openai_base_url,
                        embedding_model_name=embedding_model_name,
                        )

    # Run indexing
    hipporag.index(docs=docs)

    # Separate Retrieval & QA
    queries = [
        "What is George Rankin's occupation?",
        "How did Cinderella reach her happy ending?",
        "What county is Erik Hort's birthplace a part of?"
    ]

    # For Evaluation
    answers = [
        ["Politician"],
        ["By going to the ball."],
        ["Rockland County"]
    ]

    gold_docs = [
        ["George Rankin is a politician."],
        ["Cinderella attended the royal ball.",
         "The prince used the lost glass slipper to search the kingdom.",
         "When the slipper fit perfectly, Cinderella was reunited with the prince."],
        ["Erik Hort's birthplace is Montebello.",
         "Montebello is a part of Rockland County."]
    ]

    print(hipporag.rag_qa(queries=queries,
                                  gold_docs=gold_docs,
                                  gold_answers=answers))

if __name__ == "__main__":
    main()
