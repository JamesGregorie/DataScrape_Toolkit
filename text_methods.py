import pandas as pd
from collections import Counter
import requests
from bs4 import BeautifulSoup
import nltk

class Soupify(): 
    def __init__(self, url):
        self.url = url
        
    def make_soup(self):
        url=self.url
        r = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        t = r.text
        soup = BeautifulSoup(t, 'html.parser')
        return soup

    def links(self):
        soup = self.make_soup()
        links = soup.find_all('a')
        link_set = set([item.get('href') for item in links])
        link_list = []
        for link in link_set:
            try:
                if self.url in link:
                    link_list.append(link)
                else:
                    try:
                        link_list.append(self.url+link)
                    except:
                        pass
            except:
                pass
        link_list.remove("")
        return link_list
    
    def word_counts(self, type):
        words = []
        soup = self.make_soup()
        text_blocks = [t.text for t in soup.find_all(type)]
        word_list = [sentence.split(" ") for sentence in text_blocks]
        for list_ in word_list:
            [words.append(word) for word in list_ if word != ""]
        counts = pd.DataFrame.from_dict(Counter(words), 'index', columns=['counts']).sort_values('counts', ascending=False)
        counts.reset_index(inplace=True)
        counts['part_of_speech'] = [v for k,v in nltk.pos_tag(list(counts['index']))]
        return counts
    
    def filtered_counts(self, type, part_abbrv):
        all_text = self.word_counts(type)
        filtered_words = all_text[all_text['part_of_speech']==part_abbrv]
        return filtered_words