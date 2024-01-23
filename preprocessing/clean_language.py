from langdetect import detect, LangDetectException
import pandas as pd
import advertools as adv
import re

COUNTRY = ["Germany", "USA", "Pakistan", "India", "Korea", "Bangladesh",
           "Russia", "Brazil", "Israel", "Palestina", "Japan", "Kenia", 
           "Morroco", "Turkey", "Greece"]

def clean_lang(emoji: pd.DataFrame) -> pd.DataFrame:
    """Remove non englo comments. Also removes pure emoji comments.
    Interestingly enough same english comments were labeled as cypress"""
    
    if 'Language' not in str(emoji.columns):
        emoji['Language'] = emoji['Comment'].apply(get_lang)
        emoji = emoji[emoji['Language'] == 'en']

    # Remove comments that contain flags
    emoji['Flag'] = emoji['Comment'].apply(check_country)
    emoji = emoji[emoji['Flag'] == False]

    emoji.reset_index(drop=True, inplace=True)

    return emoji


def get_lang(comment: str) -> str:
    """Takes in a comment and determines its language"""
    
    try:
        return detect(comment)
    except LangDetectException:
        return None
    
def check_country(comment: str) -> bool:
    """Checks if there is a flag in the comment"""
    
    flag_check = "flag" in str(adv.extract_emoji([comment])['emoji_flat_text'])
    country_check = bool(re.search("|".join(COUNTRY), comment, re.IGNORECASE))

    if flag_check or country_check:
        return True
    else:
        return False
    

 