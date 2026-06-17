import json
from openai import OpenAI
from tools.google_search import google_search
from prompts.system_prompt import SYSTEM_PROMPT


class CompetitorResearchAgent:
    def __init__(self):
        self.client = OpenAI()

    def build_history_text(self, chat_history):
        history_text = ""

        if chat_history is None:
            return history_text

        for message in chat_history[-8:]:
            history_text += f"{message['role']}: {message['content']}\n"

        return history_text

    def understand_query(self, user_input: str, chat_history=None):
        history_text = self.build_history_text(chat_history)

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
You are an intent analyzer for a competitor research agent.

Conversation history:
{history_text}

Latest user message:
{user_input}

Your job:
1. Understand what the user wants.
2. Resolve words like "it", "them", "that company" using conversation history.
3. Create the best Google search query.

Return ONLY valid JSON in this format:

{{
  "intent": "competitor_research or comparison",
  "target_company": "",
  "compare_company": "",
  "search_query": ""
}}

Examples:

If user says "Find competitors of Nanyang Polytechnic":
{{
  "intent": "competitor_research",
  "target_company": "Nanyang Polytechnic",
  "compare_company": "",
  "search_query": "Nanyang Polytechnic competitors Singapore polytechnics comparison"
}}

If history mentions Nanyang Polytechnic and user says "Compare Singapore Polytechnic with it":
{{
  "intent": "comparison",
  "target_company": "Singapore Polytechnic",
  "compare_company": "Nanyang Polytechnic",
  "search_query": "Singapore Polytechnic vs Nanyang Polytechnic comparison courses strengths Singapore"
}}
"""
        )

        try:
            return json.loads(response.output_text)
        except json.JSONDecodeError:
            return {
                "intent": "competitor_research",
                "target_company": user_input,
                "compare_company": "",
                "search_query": f"{user_input} competitors comparison alternatives"
            }

    def run(self, user_input: str, chat_history=None):
        query_info = self.understand_query(user_input, chat_history)

        search_query = query_info["search_query"]

        search_results = google_search(search_query)

        simplified_results = []
        for item in search_results.get("organic", []):
            simplified_results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })

        history_text = self.build_history_text(chat_history)

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            instructions=SYSTEM_PROMPT,
            input=f"""
Conversation history:
{history_text}

Latest user message:
{user_input}

Resolved query information:
{json.dumps(query_info, indent=2)}

Google Search Results:
{json.dumps(simplified_results, indent=2)}

Important:
- Use the resolved query information.
- If compare_company is not empty, compare target_company against compare_company directly.
- Do not treat "it" as unknown if it was resolved from history.
- Give the answer in a readable report format with a markdown table.
"""
        )

        return response.output_text