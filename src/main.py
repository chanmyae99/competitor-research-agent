from dotenv import load_dotenv
from agent import CompetitorResearchAgent

load_dotenv()

company_name = input("Enter company name: ")

agent = CompetitorResearchAgent()
result = agent.run(company_name)

print("\n=== Competitor Research Report ===\n")
print(result)