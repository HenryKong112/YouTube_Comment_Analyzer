# Introduction
This analytical tool is designed for analyzing comments on YouTube videos using VADER sentiment analysis and BERTopic for topic modeling.

<img src='GUI.png'>

You can download YouTube comments as .xlsx/.csv file using my YouTube-Comment-Extractor(https://github.com/HenryKong112/HenryKong112-YouTube-Comment-Extractor).

You can merge several excel/csv file into one using my EXCEL-CSV-MERGER(https://github.com/HenryKong112/EXCEL-CSV-MERGER).


# Documentation

### 1. UMAP

https://umap-learn.readthedocs.io/en/latest/parameters.html

### 2. Sentence-transformer
https://sbert.net/docs/sentence_transformer/pretrained_models.html#semantic-search-models

# Limitation

- VADER struggles with recognizing negation, idioms, and sarcasm.
- The Topic Modelling (BERTopic) button might not generate graphs if there aren't enough comments.
- Analysis is limited to English comments only.

# Instruction

### 1. Select the .xlsx / .csv file that contain the comments 

- Click `Browse` to choose the file
- OR enter the file path directly in the entry box

- Data must contains the following column:

| Column Name  | Data Type | Description                                           |
|--------------|-----------|-------------------------------------------------------|
| `PublishedAt` | DATETIME  | The date and time when the comment was originally published. |
| `Like`       | INTEGER   | The total number of likes (positive ratings) the comment has received. |
| `Comment` | TEXT      | The text content of the comment.                     |


### 2. Click Sentiment Analysis (VADER)


You will receive three graphs, one VADER summary table, and a new Excel/CSV file containing sentiment classification for each comment.

Graphs:

- Sentiment Distribution: Count vs. Likes
- Engagement (Likes per Count) by Sentiment
- Sentiment Trend Over Time

VADER Summary Table Schema:

| Column Name     | Data Type | Description                                                   |
|-----------------|-----------|---------------------------------------------------------------|
| `Sentiment`     | String    | The sentiment category of the data. Can be one of `Positive`, `Negative`, or `Neutral`. |
| `Count`         | Integer   | The total number of occurrences for each sentiment.            |
| `Likes`         | Integer   | The total number of likes corresponding to each sentiment.     |
| `Count_Percent` | Float     | The percentage share of each sentiment's occurrence, calculated as a proportion of the total. |
| `Likes_Percent` | Float     | The percentage share of total likes that each sentiment received. |
| `Engagement`    | Float     | Number of likes per count.  

### 3. Click Topic Modelling (BERTopic)

The pre-trained model used here is `all-MiniLM-L6-v2`,as it is a lot faster in running and still offers good quality. You will see two graphs in your browser.

Graphs:

- Topic Word Scores

    > This chart provides a ranked list of the most relevant words for each topic identified in a topic modeling analysis.

    > Words with the highest scores are considered more representative of the respective topic.
    
    > It helps to interpret what each topic is about based on the dominant words associated with it.
    



- Intertopic Distance Map

    >This visualization typically uses a 2D plot to show how distinct or related different topics are in terms of their content.

    >Topics that are close together share more similarities, while those further apart are more distinct.

    >The size of the circles representing topics often corresponds to the prevalence of each topic within the dataset.