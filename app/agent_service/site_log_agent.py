from app.service.sql_engine_service import get_sitelog_inmemory_db,SITELOG_INMEM_DB
from app.service.gemini_service import GeminiModel, GeminiJsonEngine
from app.service.common_utils import load_json_data


from pydantic import BaseModel, Field
from typing import List
import pandas as pd
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/debasmitroy/Desktop/programming/gemini-agent-assist/key.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "hackathon0-project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"


SITELOG_INMEM_DB = get_sitelog_inmemory_db(load_json_data("app/data/sitelog.json"))

class SiteLogQuery(BaseModel):
    text_query: str = Field(title="Text Query", description="The text query to search in the site log.")
    sql_query: str = Field(title="SQL Query", description="Corresponding SQL query to search in the site log.")

class SiteLogQueries(BaseModel):
    queries: List[SiteLogQuery] = Field(title="Site Log Queries", description="List of text queries and their corresponding SQL queries.")


class SiteLogAgent:
    def __init__(self, target_product_id: str):
        global SITELOG_INMEM_DB
        SITELOG_INMEM_DB_COLS, SITELOG_INMEM_DB_HEAD = SITELOG_INMEM_DB.query_data("SELECT * FROM sitelog LIMIT 5")
        self.PD_SITELOG_INMEM_DB_HEAD = pd.DataFrame(SITELOG_INMEM_DB_HEAD, columns=SITELOG_INMEM_DB_COLS)

        self.engine = GeminiJsonEngine(
                                    model_name="gemini-2.0-flash-001",
                                    basemodel=SiteLogQueries,
                                    temperature=0.5,
                                    max_output_tokens=1024,
                                    systemInstructions=None,
                                    max_retries=5,
                                    wait_time=30
                                    )
        
    def run(self,target_product_id):

        # Validate the product ID
        PRODUCT_ID_COUNT = SITELOG_INMEM_DB.query_data(f"SELECT COUNT(*) FROM sitelog WHERE product_id = '{target_product_id}'")
        if PRODUCT_ID_COUNT[1][0][0] == 0:
            raise ValueError(f"Product ID '{target_product_id}' not found in the site log.")

        queries_result = self.engine(
            [
                "You are a SQL expert. Your task is to write a SQL script to query data from the given table. Note: you are generating a SQL script for SQLLite's python library. You must be careful while writing complex queries as it is very sensitive.",
                f"Here are the first few rows of the table sitelog: {self.PD_SITELOG_INMEM_DB_HEAD}.",
                f"Now generate a list of text queries and their corresponding SQL queries to search in the site log to fetch some useful information and groupings.",
                f"Example: From which regions are most of the users purchasing the product with product_id = {target_product_id}? Give me the percentage of users from each region.",
                f"SQL Query: SELECT region, COUNT(*) * 100.0 / (SELECT COUNT(*) as PERCENT FROM sitelog WHERE product_id = '{target_product_id}') as percentage FROM sitelog WHERE product_id = '{target_product_id}' GROUP BY region ORDER BY percentage DESC;",
                f"You are allowed to write multiple queries. Make sure to provide the text query and the corresponding SQL query in the response.",
                f"Always extract percentage not count. Also, make sure to order the results in both TOP and BOTTOM order with limit 3.",
                f"Use different groupings based on Age, Demography, Gender, Month etc."
            ]
        )

        final_result = []
        succes = 0
        for query in queries_result[0]['queries']:
            try:
                result = SITELOG_INMEM_DB.query_data(query['sql_query'])
                succes += 1
            except Exception as e:
                pass
            final_result.append({
                "text_query": query['text_query'],
                "sql_query": query['sql_query'],
                "result": result
            })
        
        print(f"Successful queries: {succes} out of {len(queries_result[0]['queries'])}")
        return final_result
    

# Initialize the SiteLogAgent
SITE_LOG_AGENT=SiteLogAgent(target_product_id="P001")