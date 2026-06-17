import json
from openai import OpenAI

from config import OPENAI_API_KEY
from tools.google_search import google_search
from prompts.system_prompt import SYSTEM_PROMPT


class CompetitorResearchAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        self.tools = [
            {
                "type": "function",
                "name": "google_search",
                "description": "Search Google for competitor research, company comparisons, alternatives, and market information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The Google search query to run."
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                }
            }
        ]

    def build_history_text(self, chat_history):
        if not chat_history:
            return ""

        history_text = ""
        for message in chat_history[-8:]:
            history_text += f"{message['role']}: {message['content']}\n"

        return history_text

    def run(self, user_input: str, chat_history=None):
        history_text = self.build_history_text(chat_history)

        first_response = self.client.responses.create(
            model="gpt-4.1-mini",
            instructions=SYSTEM_PROMPT,
            input=f"""
Conversation history:
{history_text}

Latest user message:
{user_input}

Use the conversation history to resolve references like:
- it
- them
- that company
- previous company

When you need current competitor information, call the google_search tool.
""",
            tools=self.tools
        )

        tool_outputs = []

        for item in first_response.output:
            if item.type == "function_call" and item.name == "google_search":
                arguments = json.loads(item.arguments)
                query = arguments["query"]

                search_result = google_search(query)

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(search_result)
                    }
                )

        if tool_outputs:
            final_response = self.client.responses.create(
                model="gpt-4.1-mini",
                instructions=SYSTEM_PROMPT,
                input=first_response.output + tool_outputs
            )

            return final_response.output_text

        return first_response.output_text