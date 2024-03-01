import html
import re
import pandas as pd
import ast
import random

TAG_MATCH = re.compile('<.*?>')
EMOJI_PAT = re.compile(
        '[\\U0001f600-\\U0001f64f\\U0001F308-\\U0001F534\\U0000203C-\\U00002B50]+')

def format_emoji_sentence(emoji: pd.DataFrame):
    """Format the dataset"""

    emoji['Comment'] = emoji['Comment'].apply(replace_unicode)
    emoji['Comment'] = emoji['Comment'].apply(replace_tags)
    emoji['Length_Con'] = emoji['Comment'].apply(remove_to_long)
    emoji['Num_Con'] = emoji['Comment'].apply(remove_num_comments)
    emoji['Span'] = emoji['Comment'].apply(add_span)

    emoji = emoji[(emoji['Length_Con'] == True) & (emoji['Num_Con'] == False)]
    emoji = emoji[~emoji['Span'].isna()]
    emoji.reset_index(drop=True, inplace=True)

    return emoji


def remove_to_long(comment: str) -> bool:
    """Removes Sentences that are too long"""

    word_count = len(comment.split(" "))
    if word_count <= 15 and word_count > 1:
        return True
    else:
        return False


def remove_num_comments(comment: str) -> bool:
    """Remove comments with numbers in it """

    return bool(re.search("\d+", comment))


def replace_tags(comment: str) -> str:
    """Replaces/Removes HTML Tags like <b> or <a>"""

    return re.sub(TAG_MATCH, '', comment)


def replace_unicode(comment: str) -> str:
    """Replace weird formatting youtube API gave back"""

    return html.unescape(comment)


def add_span(comment: str) -> list[str]:
    """Get span of Emoji and mark emojis with multiple spans"""

    # Pattern matches all emojis that exist as a label
    res = re.finditer(EMOJI_PAT, comment)
    span = [item.span() for item in res]

    if len(span) > 1 or len(span) == 0:
        return None
    else:
        return ast.literal_eval("[" + str(span)[2:-2] + "]")


def add_random_span(comment: str) -> list[int]:
    """Lets the span point to a random length inside the string"""
    
    start = random.randrange(0, len(comment))
    end = random.randrange(start+1, len(comment)+1)

    return [start, end]
    