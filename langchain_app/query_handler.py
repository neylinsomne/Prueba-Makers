from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from data.load_data import get_df, get_db, get_schemaa

def create_query_prompt(question, schema):
    
    prompt_template = """Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}

    Question: {question}
    SQL Query:
    """
    return ChatPromptTemplate.from_template(prompt_template)

def run_query(db, query):
    
    try:
        return db.run(query)
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None

def get_sql_chain(question, schema, llm):
    
    prompt = create_query_prompt(question, schema)
    sql_chain = (
        RunnablePassthrough.assign(schema=schema)
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )
    
    return sql_chain