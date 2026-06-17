from tools.google_search import google_search

results = google_search("OpenAI competitors")

for idx, item in enumerate(results.get("organic", []), start=1):
    print(f"\n{idx}. {item['title']}")
    print(item['link'])
    print(item['snippet'])