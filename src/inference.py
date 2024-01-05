from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain_community.vectorstores import Chroma

def run_inference(text, query):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings()  
    
    docsearch = Chroma.from_texts(
    chunks, embeddings, metadatas=[{"source": i} for i in range(len(chunks))])
    docs = docsearch.similarity_search(query)
    
    template = """
    Use the following pieces of context to answer the question at the end. If you don't find the relevant answer from the input documents, just say I apologize, insufficient data provided, don't try to give a generic answer and also don't try to add extra information which is not present in the input documents.Even if user ask to explain about something which is not present in the input document, don't try to makeup any answer.If you find the appropriate relevant answer describe about it clearly in paragraph wise or in point wise.
    {context}
    {chat_history}
    Human: {human_input}
    Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"], template=template
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")
    chain = load_qa_chain(
        OpenAI(temperature=0), chain_type="stuff", memory=memory, prompt=prompt
    )
    chain({"input_documents": docs, "human_input": query}, return_only_outputs=True)
    # print("CHAIN",chain)
    
    aimessage_content = chain.memory.chat_memory.messages[-1].content
    print(aimessage_content)
    return aimessage_content
    
    
    
    
    
    
    
