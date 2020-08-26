# OK, line, ATM, iPhone, ETC, bye, FM, KTV, seven-eleven, Google, facebook

import requests
import pandas as pd

API_KEY = "AIzaSyBP9ysqvHZIcO20oP4WXr53EL4k6_JGc0I"
CSE_ID = "2abcf2a2f14a8ff56"

links = []
query = "facebook"

pages = [1,2,3,4,5,6,7,8,9,10]

for page in pages:
	start = (page - 1) * 10 + 1
	url = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={API_KEY}&cx={CSE_ID}&q={query}&start={start}"

	data = requests.get(url).json()
	search_items = data.get("items")
	for i, search_item in enumerate(search_items, start=1):

		title = search_item.get("title")
		snippet = search_item.get("snippet")
		html_snippet = search_item.get("htmlSnippet")
		link = search_item.get("link")

		print("="*10, f"Result #{i+start-1}", "="*10)
		print("Title:", title)
		print("Description:", snippet)
		print("URL:", link, "\n")
		links.append(link)

writerCSV=pd.DataFrame(data=links)
writerCSV.to_csv('./links/links_{}.csv'.format(query), mode='a', encoding='utf-8', header=False, index=False)

