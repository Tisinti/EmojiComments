import pandas as pd
import re

EMO_TAG = pd.read_csv("data/input/EmoTagLabels.csv")
EMOJI_PAT = re.compile(
        '[\\U0001f600-\\U0001f64f\\U0001F308-\\U0001F534\\U0000203C-\\U00002B50]')


def get_likely_emotion(row: pd.Series):
    """Label the Emoji with the biggest corresponding emotion.
    If all Emotions are under 0.5, label as neutral"""

    if row.max() < 0.5:
        return "neutral"
    return row.idxmax(axis=0)


def emo_tag_labels() -> None:
    """Format the EmoTag Dataset"""

    emotions = ['anger', 'anticipation', 'disgust', 'fear',
                'joy', 'sadness', 'surprise', 'trust']
    label = pd.read_csv("data/input/EmoTag1200-scores.csv")
    
    label['label'] = label[emotions].apply(get_likely_emotion, axis=1)
    label[['unicode', 'emoji', 'name', 'label']].to_csv(
        "data/input/EmoTagLabels.csv", index=False)
    

def label_comments(comment: str) -> str:
    """Returns the label that matches the first emoji"""

    emojis = re.findall(EMOJI_PAT, comment)
    label = EMO_TAG[EMO_TAG['emoji'].isin(emojis)]['label'].values.tolist()

    if label:
        return label[0]
    else:
        return None

    

