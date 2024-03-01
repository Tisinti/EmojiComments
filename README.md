# Creating an Emoji-Text Dataset labeled after Emotions 🎊

This is a Repo which i used to create a dataset that contains Youtube Comments with Emojis. 
The Emotion to each emoji is based on EmoTag 1200. https://github.com/abushoeb/EmoTag 

You can find the final dataset under data/output/emoji_final.json containing 7802 comments!
If you just want the raw comments, there are 23483 emoji comments und data/output/emoji_comments.json.
Or just create your own dataset, using this Repo! Hopefully the below documentation and the comments in the code are enough, if not feel free to do what you want with this Project.

### Code Structure 👾
The main code can be found under src/emojidata

**scraping**
: scrapes emoji_comments from Youtube via the Youtube API. Creates an _emoji_comments.json_ file in data/output.
You **need** a *.env* file in the root of the folder, containing a valid *YT_API* Key for this to work. 

**preprocessing**
: preprocesses and labels the emoji_comments. Creates emoji_final.json and emoji_random.json (with a random span).

**src/notebooks**
: There's also a notebook folder with an Analysis Notebook, that contains a visualization of embeddings that BERT generated based on this dataset.

### Dataset Structure 📋📊

emoji_final.json contains the comment, the label and the span. 
The span points to the emojis that are next to each other is contained in EmoTag 1200.
The Comment is labeled after the first emoji contained in the span.

**data/input**
: EmotagLabels.csv contains each emoji with it's highest corresponding emotion. 
If no Emotion is over 0.5, the Emoji was labeled neutral.

**data/output**
: The scraped comments, with the inbetween steps of preprocessing.

**data/probing**
: Train-Test parquet files for probing a Language Model. The embeddings were not derived from this code, but were used for result analysis.


## This Project was done using PDM - a python package manager 🤖

If you want to start working in this Repository (only you might know why you would want to to this lol),
you probably need to download pdm first. Here's a quick rundown:

1. Make sure you have pipx installed. You can install it via https://pdm-project.org/latest/.
If you are on Windows(), using pipx might be the most convinient method.
2. Go into this repository and run:
`pdm install`
This creates a Virtual Enviroment (Venv) with all dependencies and the correct python version!

Activate the Venv and you are good to go!

If you need a little help with pdm you can take a look at their website 😉:
https://pdm-project.org/latest/usage/dependency/





