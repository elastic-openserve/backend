from pytrends.request import TrendReq
from datetime import datetime, timedelta
import pandas as pd
from pydantic import BaseModel, Field
from collections import defaultdict, Counter
from app.service.langchain_agent_service import LangchainJSONEngine
from dotenv import load_dotenv
load_dotenv()


class SearchTokenModel(BaseModel):
    """
    This model extracts search tokens based on the brand's market scope, TAM, etc.
    """
    search_tokens: list[str] = Field(
        title="Search Tokens",
        description="List of search tokens in the form of common nouns or search queries relevant to the brand. These tokens should be meanningful phrase not a single word."
    )
    product_id: str = Field(title="Product ID", description="The product ID for which trends are simulated.")


class DummyTrendModel(BaseModel):
    country: str = Field(title="Country", description="Country code (e.g., US, IN, etc.)")
    keyword: str = Field(title="Keyword", description="The keyword for which trends are simulated.")
    trendscore: int = Field(title="Trend Score", description="Peak interest score (0-100).")
    top_months: list[str] = Field(title="Top Months", description="Top 3 months where the trend peaked (YYYY-MM format).")
    top_states: list[str] = Field(title="Top States", description="Top 3 states/regions within the country.")



class TrendAnalyzer:
    def __init__(self):
        # Engine to generate search tokens
        self.token_engine = LangchainJSONEngine(
            sampleBaseModel=SearchTokenModel,
            systemPromptText="""
            You are a marketing strategist helping a brand identify the most effective search terms for trend analysis. 
            Based on the brand description, TAM, and market scope, generate a list of highly relevant search tokens (common noun queries). 
            The tokens should be simple, commonly searched phrases like "electric scooter in India", "eco-friendly scooter", "best commuter scooter", etc. 
            Focus on intent-based keywords that would likely appear in Google Trends.
            """
        )

        # Dummy trend data generator
        self.dummy_engine = LangchainJSONEngine(
            sampleBaseModel=DummyTrendModel,
            systemPromptText="""
            You are simulating trend data for a market research report. 
            Given a country and a search token, provide:
            - a realistic peak trendscore (between 60 to 100),
            - top 3 months in the format "YYYY-MM" in 2024.
            - top 3 states/regions where this search term is popular within the country.
            The data should appear realistic and well-distributed.
            """
        )

        self.countries = ['US', 'IN']


    def _get_countrywise_top_states_per_month(self,trend_data):
        country_month_state_counter = defaultdict(lambda: defaultdict(Counter))

        # Step 1: Aggregate data
        for entry in trend_data:
            for country, info in entry.items():
                months = info['top-months']
                states = info['top-states']
                for month in months:
                    country_month_state_counter[country][month].update(states)

        # Step 2: Pick top state(s) for each country-month
        result = defaultdict(dict)
        for country, month_data in country_month_state_counter.items():
            for month, state_counter in month_data.items():
                max_count = max(state_counter.values())
                top_states = [state for state, count in state_counter.items() if count == max_count]
                month_name = datetime.strptime(month, "%Y-%m").strftime("%B")
                result[country][month_name] = top_states

        return dict(result)


    def run(self, description: str):
        # Step 1: Extract search tokens from brand description
        tokens_result = self.token_engine.run(description)
        search_tokens = tokens_result.search_tokens

        # Step 2: Dummy trend simulation instead of actual API calls
        output = []
        
        for country in self.countries:
            for keyword in search_tokens:
                # print(f"Country: {country}, Keyword: {keyword}")
                dummy_data = self.dummy_engine.run(f"Country: {country}, Keyword: {keyword}")
                output.append({
                    dummy_data.country: {
                        "keyword": dummy_data.keyword,
                        "trendscore": dummy_data.trendscore,
                        "top-months": dummy_data.top_months,
                        "top-states": dummy_data.top_states
                    }
                })
        
        # Step 3: Post-process the data
        result = self._get_countrywise_top_states_per_month(output)

        result['product_id'] = tokens_result.product_id
        return result


TREND_ANALYZER = TrendAnalyzer()