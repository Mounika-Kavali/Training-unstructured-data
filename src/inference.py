from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain.llms import OpenAI
from langchain_community.vectorstores import Chroma

def run_inference(text, query):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings()  
    
    docsearch = Chroma.from_texts(chunks, embeddings, metadatas=[{"source": i} for i in range(len(chunks))])
    docs = docsearch.similarity_search(query)
    
    template = """
    Use the following pieces of context to answer the question at the end. 
    
   
    If user question does not match to any context in the input documents then strictly just say- I appolozise, insufficient data provided.Never try to give a generic answer from the internet and also don't try to add extra information which is not present in the input documents.Even if user ask to explain about something which is not present in the input document, don't try to makeup any answer.
    
    If you find the relevant answer from the input documents to the user question then  describe about it clearly.If user does not given a proper question format just consider it as a complete question and find its relevant answer from the input documents and explain in detail about the given question.

    
    {context}
    chat_history: {chat_history}
    Human: {human_input}
    Chatbot:"""


    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"], template=template
    )


    llm = OpenAI(temperature=0,max_tokens=562)




    memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input",return_messages=True)
    chain = load_qa_chain(
       llm, chain_type="stuff", verbose=True, memory=memory, prompt=prompt
    )
    chain({"input_documents": docs, "human_input": query,"memory": memory}, return_only_outputs=True)

     # Access the chat history from memory
    chat_history = chain.memory.chat_memory.messages
    # Get the response from the last message in the chat history
    aimessage_content = chat_history[-1].content
    
    print("RRR",chain.memory)
    return aimessage_content
    
    
    
    
    
    
    
