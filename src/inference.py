#inference.py

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
# from langchain.callbacks import get_openai_callback

def run_inference(text, query):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    #train_model
    knowledge_base = FAISS.from_texts(chunks, embeddings)


    docs = knowledge_base.similarity_search(query)

    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=docs, question=query)

    return response
