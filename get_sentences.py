import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

word = 'bye'
match_word = word.lower()
link_file = "./links/links_{}.csv".format(word)
my_headers = {'cookie': 'over18=1;'}
links = []
match_sentences = []

df = pd.read_csv(link_file)
df.columns = ['links']
links = df['links'].tolist()
# links = ['https://www.ptt.cc/bbs/Road/M.1455808765.A.25A.html']

def get_sentences(contents):
	for i in contents:
		if re.search(rf"[^. a-zA-Z/]{match_word}[^. a-zA-Z/]", i, re.IGNORECASE) or re.search(rf"^{match_word}[^. a-zA-Z]", i, re.IGNORECASE):

			# i = re.sub(r'','',i)
			sentences = re.split('\s+|\,|\~|\～|\◎|\【|\】|\；|\;|\/|\／|\…|\.\.\.|\>', i)
			i = re.sub(r'\(.*\)|\（.*\）|\【.*\】','',i)
			# i = re.sub(r'[\–\-\「\」\、\[\]\《\》\▼\▲\#]+','',i)
			sentences = re.split("\\W", i)

			for s in sentences: 
				if match_word in s.lower() and len(s) <= 30 and s.lower() != match_word.lower():
					match_sentences.append(s + "\n") 
					print(s)


for link in links:
	url = link

	post = requests.get(url, headers = my_headers)
	soup = BeautifulSoup(post.content, 'html.parser')

	main_container = soup.find(id='main-container')
	if main_container == None: continue
	all_text = main_container.text
	pre_text = all_text.split('--')[0]
	texts = pre_text.split('\n')
	contents = texts[2:]
	contents = [re.sub(r'.*http.*$','',c) for c in contents]
	content = ''.join(contents)

	contents = re.split('[。，：？！\!\?\:]', content)
	contents = [x for x in contents if match_word in x.lower()]
	print(contents)
	get_sentences(contents)	

print(len(match_sentences))
match_sentences = list(dict.fromkeys(match_sentences))
print(len(match_sentences))
outF = open("./sentences/sentences_{}.txt".format(word), "w")
outF.writelines(match_sentences)
outF.close()
