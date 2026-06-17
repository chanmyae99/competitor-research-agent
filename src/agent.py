import json
from openai import OpenAI
from tools.google_search import google_search
from prompts.system_prompt import SYSTEM_PROMPT


class CompetitorResearchAgent:
    def __init__(self):
        self.client = OpenAI()

    def run(self, company_name: str):
        search_query = f"{company_name} competitors and alternatives"

        search_results = google_search(search_query)

        simplified_results = []
        for item in search_results.get("organic", []):
            simplified_results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })

        prompt = f"""
                    {SYSTEM_PROMPT}

                    # Context

                    Company:
                    {company_name}

                    Google Search Results:
                    {json.dumps(simplified_results, indent=2)}
                """

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text