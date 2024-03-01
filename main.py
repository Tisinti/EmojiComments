from src.emojidata import search_comments
from src.emojidata import clean_lang
from src.emojidata import format_emoji_sentence, add_span, label_comments
from src.emojidata import add_random_span
import json
import pandas as pd
from sklearn.model_selection import train_test_split


def scrape_comments(search: str) -> None:
    """
    Scrape comments under channels that apply to search. 
    Your search should be a topic like cooking or gaming etc.
    Creates a emoji_comments.json with all the raw emoji comments.
    """

    with open('data/output/emoji_comments.json', 'w', encoding='UTF-8') as f:
        json.dump(search_comments(search), f, ensure_ascii=False, indent=4)


def format() -> None:
    """Format the cleaned data"""

    emoji = pd.read_json('data/output/emoji_lang.json', orient='index')
    formoji = format_emoji_sentence(emoji)
    formoji[['Comment', 'Span']].to_json("data/output/emoji_formatted.json", orient='index',
                                         force_ascii=False, indent=4)
    print(str(len(emoji)) + " und " + str(len(formoji)))


def label() -> None:
    """Label the formatted data"""

    emoji = pd.read_json('data/output/emoji_formatted.json', orient='index')
    emoji['Label'] = emoji['Comment'].apply(label_comments)
    emoji = emoji[~emoji['Label'].isna()]

    emoji.reset_index(drop=True, inplace=True)
    emoji[['Label', 'Comment', 'Span']].to_json("data/output/emoji_final.json", orient='index',
                                                force_ascii=False, indent=4)


def train_test() -> None:
    """Split train test"""
    data = pd.read_json("data/output/emoji_final.json", orient="index")
    train, test = train_test_split(
        data, random_state=42, shuffle=True, train_size=0.8)
    train.to_parquet("data/probing/train.parquet")
    test.to_parquet("data/probing/test.parquet")


def random_span() -> None:
    """Generate Dataset with random span"""

    data = pd.read_json("data/output/emoji_final.json", orient="index")
    data['Span'] = data['Comment'].apply(add_random_span)
    data.to_json("data/output/emoji_random.json", orient='index',
                 force_ascii=False, indent=4)


if __name__ == "__main__":
    data = pd.read_json("data/output/emoji_final.json", orient="index")
    print(data.groupby(['Label'])['Comment'].count())
