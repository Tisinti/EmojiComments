from scraping import search_comments
import pandas as pd 
import json 

def scrape_comments(search: str='tagesschau') -> None:
    with open('data/emoji_comments.json', 'w', encoding='UTF-8') as f:
        json.dump(search_comments(search), f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_comments("late night | celebs")