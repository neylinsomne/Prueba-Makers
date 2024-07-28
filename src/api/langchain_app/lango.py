from ..data.load_data import get_df, get_db, get_schemaa
from langchain_core.prompts import ChatPromptTemplate
# from cassandra.cluster import Cluster
#from langchain_core.chains import create_sql_query_chain
# from cassandra.auth import PlainTextAuthProvider
from langchain_community.chat_message_histories import CassandraChatMessageHistory#, ConversationBufferMemory
#from langchain.memory import CassandraChatMessageHistory
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
#from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent


import json
from .query_handler import get_sql_chain,run_query
from .usuario import get_question
# from langchain_app.memory_handler import setup_memory
import os
import time
import openai 
from dotenv import load_dotenv

def api_request_with_backoff(api_function, *args, **kwargs):
    max_retries = 5
    retry_delay = 4

    for attempt in range(max_retries):
        try:
            return api_function(*args, **kwargs)
        except openai.error.RateLimitError as e:
            if attempt < max_retries - 1:
                print(f"Rate limit reached. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Raising exception.")
                raise e

def ai_response(question: str):
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No OPENAI_API_KEY found in environment variables")

    chat_model = ChatOpenAI(openai_api_key=api_key)
    db = get_db()
    schema = get_schemaa(db)
    MODEL = os.getenv("MODEL")
    llm = ChatOpenAI(model=MODEL, temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)    
    query = agent_executor.invoke(question)
    print(query)

    
    
    template = """
    You are an assistant for sales advisors, your name is Juan. Please respond to the questions based on the schema below, write an SQL query that would answer the User's Questions:
    {schema}

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}
    """
    prompt = ChatPromptTemplate.from_template(template)

    full_chain = (
        RunnablePassthrough.assign(query=lambda _: query).assign(
            response=lambda vars: run_query(db, vars["query"]),
        )
        | prompt
        | (lambda query: api_request_with_backoff(llm, query))
    )

    result = full_chain.invoke({"question": question, "schema": schema})
    #return result
    return query["output"]

if __name__ == "__main__":
    question="How many motorcycles are in the stock"
    ai_response(question)