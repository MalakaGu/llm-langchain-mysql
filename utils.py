import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize components
llm = ChatOpenAI(api_key=api_key)

def initialize_db_connection(uri: str):
    """Initialize the SQL database connection."""
    return SQLDatabase.from_uri(uri)

def get_table_schema(db: SQLDatabase):
    """Retrieve the table schema from the database."""
    return db.get_table_info()

def create_sql_query_chain(db: SQLDatabase, llm: ChatOpenAI):
    """Create the chain to generate SQL queries."""
    sql_template = """
    Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}

    Question: {question}
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(sql_template)

    return (
        RunnablePassthrough.assign(schema=lambda _: get_table_schema(db))
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

def create_response_chain(db: SQLDatabase, llm: ChatOpenAI, sql_chain):
    """Create the full chain to generate natural language responses."""
    response_template = """
    Based on the table schema below, question, SQL query, and SQL response, write a natural language response:
    {schema}

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}
    """
    prompt_response = ChatPromptTemplate.from_template(response_template)

    return (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: get_table_schema(db),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt_response
        | llm
        | StrOutputParser()
    )

def process_user_question(db_uri: str, question: str):
    """Main function to process the user's question and return the final response."""
    # Initialize DB and chains
    db = initialize_db_connection(db_uri)
    sql_chain = create_sql_query_chain(db, llm)
    full_chain = create_response_chain(db, llm, sql_chain)

    # Invoke the chain with the question
    return full_chain.invoke({"question": question})

# Example usage
# if __name__ == "__main__":
#     mysql_uri = os.getenv("MYSQL_URI")
#     user_question = 'how many artists are there?'

#     result = process_user_question(mysql_uri, user_question)
#     print(result)
