from pydantic import BaseModel, Field
from collections import defaultdict, Counter
from app.service.langchain_agent_service import LangchainJSONEngine
from dotenv import load_dotenv
from typing import List
import json
load_dotenv()


class RegionDemography(BaseModel):
    state: str = Field(title="State", description="The state or region name.")
    country: str = Field(title="Country", description="The country name.")

class SiteLogRefinedResult(BaseModel):
    """
    This model represents the refined results of the site
    """
    top2_months: List[str] = Field(title="Top 2 Months", description="Top 2 months with the highest number of user interactions. Not year specific. Connvert month number to month name.")
    top_age_group: str = Field(title="Top Age Group", description="Top age group with the highest number of user interactions. Example: 18-24, 25-34, etc.")
    top2_regions: List[RegionDemography] = Field(title="Top 2 Regions", description="Top 2 regions with the highest number of user interactions.")

    bottom2_months: List[str] = Field(title="Bottom 2 Months", description="Bottom 2 months with the lowest number of user interactions. Not year specific. Connvert month number to month name.")
    bottom_age_group: str = Field(title="Bottom Age Group", description="Bottom age group with the lowest number of user interactions. Example: 18-24, 25-34, etc.")
    bottom2_regions: List[RegionDemography] = Field(title="Bottom 2 Regions", description="Bottom 2 regions with the lowest number of user interactions.")




class SiteLogRefinerAgent:
    def __init__(self):
        self.engine = LangchainJSONEngine(
            sampleBaseModel=SiteLogRefinedResult,
            systemPromptText="""
            You are a data analyst. Your task is to analyze the site log data to extract meaningful insights.
            """,
            temperature=0.2
        )

    def run(self, site_log_result):
        # try:
        #     site_log_result = json.loads(site_log_result)
        #     print("*** Site Log Result ***", site_log_result.keys())
        # except Exception as e:
        #     print(">>>> Error in SiteLogRefinerAgent.run", e)
            
        parsed_result = "\n".join([f"{res['text_query']}\nResult: {res['result']}" for res in site_log_result])
        result = self.engine.run(f"""These are the results of the SQL queries on the site log data: {parsed_result}
        Analyze the data and provide the following insights:
        - Top/Bottom 2 months with the highest number of user interactions.
        - Top/Bottom 2 regions with the highest number of user interactions.
        - Top/Bottom age group with the highest number of user interactions.
        - Top/Bottom region with the highest number of user interactions.
        """)

        result_dict = dict(result)
        # Convert List(top2_region) to List[Dict]
        top2_regions = [dict(region) for region in result_dict['top2_regions']]
        result_dict['top2_regions'] = top2_regions

        # Convert List(bottom2_region) to List[Dict]
        bottom2_regions = [dict(region) for region in result_dict['bottom2_regions']]
        result_dict['bottom2_regions'] = bottom2_regions

        # Top Vs Bottom Results 
        top_bottom_results = {
            "top": {
                "months": result_dict['top2_months'],
                "age_group": result_dict['top_age_group'],
                "regions": result_dict['top2_regions']
            },
            "bottom": {
                "months": result_dict['bottom2_months'],
                "age_group": result_dict['bottom_age_group'],
                "regions": result_dict['bottom2_regions']
            }
        }

        return top_bottom_results
    


SITE_LOG_REFINER_AGENT = SiteLogRefinerAgent()