import argparse
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain.embeddings import OllamaEmbeddings

from langchain.llms import Ollama 
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def main():
    parser= argparse.ArgumentParser(description="Filter out URL arguments. ")
    parser.add_argument('--url', type=str, default='http://example.com', required=True, help= "The URL to filter ")

    
    args = parser.parse_args()
    url = args.url 
    print(f"URL: {url}")
    
    loader = WebBaseLoader(url)
    data = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap= 100)
    all_splits = text_splitter.split_documents(data)
    print(f"Split into {len(all_splits)} chunks")
    
    vectorstore = Chroma.from_documents(documents= all_splits,embedding= GPT4AllEmbeddings() )
    
    
    print(f"Loaded {len(data)} documents")
    
    from langchain import hub
    
    QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")
    
    
    llm = Ollama(model="phi3",
                 verbose = True,
                 callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))
    
    print(f"Loaded model: {llm.model}")
    
    from langchain.chains import RetrievalQA
    
    qa_chain = RetrievalQA.from_chain_type(
        llm, 
        retriever = vectorstore.as_retriever(), 
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )
    
    
    question = f"According to {url} When did Hassan Nasrallah die?"
    result = qa_chain({"query": question})
    
    print(result)
    
if __name__ == "__main__":
    main()