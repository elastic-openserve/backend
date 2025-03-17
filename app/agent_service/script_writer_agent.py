from pydantic import BaseModel, Field
from collections import defaultdict, Counter
from app.service.langchain_agent_service import LangchainJSONEngine
from dotenv import load_dotenv
from typing import List
import json
load_dotenv()



class TextScript(BaseModel):
    title: str = Field(title="Text", description="A very flashy title for the advertisement post.")
    body: str = Field(title="Body", description="The body of the advertisement post.")
    month: str = Field(title="Month", description="The month for which the advertisement is being created.")
    age_group: str = Field(title="Age Group", description="The target age group for the advertisement.")
    region: str = Field(title="Region", description="The target region for the advertisement. It should be a full state and Country name. The format should be 'State, Country'.")
    hashtags: List[str] = Field(title="Hashtags", description="List of hashtags to be used in the advertisement post. The hashtags should be separated by commas and should contain the '#' symbol.")

class TextScripts(BaseModel):
    scripts: List[TextScript] = Field(title="Text Scripts", description="List of advertisement text scripts.")



class ScriptWriterAgent:
    def __init__(self):
        self.engine = LangchainJSONEngine(
            sampleBaseModel=TextScripts,
            systemPromptText="""
            You are a content writer. Your task is to create an advertisement script for a new product.
            """,
            temperature=0.2
        )

    def run(self, input_prompt):
        product_description, trend_result, site_log_refiner_result = input_prompt['product_description'], input_prompt['trend_result'], input_prompt['site_log_refiner_result']
        
        prompt0 = f""" This is the product description: {product_description}.
Here are few insights from the trend analysis and site log data. This Trend Data is not Product specific, it is based on the overall market trends of that category.
Trend Data: {trend_result}.
Here are the insights from log data for the product with particualr product_id with top performing regions, months and age groups.
Site Log Data: {site_log_refiner_result['top']}.
Now, generate a list of advertisement text scripts for the product based on the insights for each month, age group, and region. 
Note: The Title and Body of the advertisement should have synergy with other demographics such as age group and region.
Note: Here your intent should be bring more and more focus on this demograohy as they are the top performers.
        """
        prompt1 = f"""This is the product description: {product_description}.
Here are few insights from the trend analysis and site log data. This Trend Data is not Product specific, it is based on the overall market trends of that category.
Trend Data: {trend_result}.
Here are the insights from log data for the product with particualr product_id with least performing regions, months and age groups.
Site Log Data: {site_log_refiner_result['bottom']}.
Now, generate a list of advertisement text scripts for the product based on the insights for each month, age group, and region.
Note: The Title and Body of the advertisement should have synergy with other demographics such as age group and region.
Note: Here your intent should be capture the audience from these demograohy as they are the least performers.
        """
        result0 = self.engine.run(prompt0)
        result1 = self.engine.run(prompt1)
        
        result = {
            "top": [dict(script) for script in result0.scripts],
            "bottom": [dict(script) for script in result1.scripts]
        }

        result["bucket_id"] = "-1" # Default bucket ID, with no image 
        return result
    


SCRIPT_WRITER_AGENT = ScriptWriterAgent()