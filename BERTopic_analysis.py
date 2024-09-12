from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd
from pathlib import Path
import numpy as np
import random
from umap import UMAP
from langdetect import detect, DetectorFactory

def bert_visual(path):
    """
    Analyze and visualize topics in textual data from a CSV or Excel file.
    """
    # Set random seeds for reproducibility
    np.random.seed(42)
    random.seed(42)

    # Determine the file extension and read the file accordingly
    file_extension = Path(path).suffix
    try:
        if file_extension == '.csv':
            df = pd.read_csv(path)
        elif file_extension == '.xlsx':
            df = pd.read_excel(path)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Ensure the 'Comment' column exists in the DataFrame
    if 'Comment' not in df.columns:
        print("Error: 'Comment' column not found in the data.")
        return

    # Preprocess the text data: convert to lowercase and remove HTML tags
    df['Comment'] = df['Comment'].str.lower()
    df['Comment'] = df['Comment'].replace(r'<a href=".*?">.*?<\/a>', '', regex=True)
    df['Comment'] = df['Comment'].replace(r'<br>', '', regex=True)

    # Function to check if the text is in English
    def is_english(text):
        try:
            return detect(text) == 'en'
        except:
            return False

    # Apply the function to filter out non-English comments
    df = df[df['Comment'].apply(is_english)]

    # Extract the list of comments for topic modeling
    docs = df['Comment'].tolist()

    # Load the SentenceTransformer model for text embeddings
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Initialize UMAP for dimensionality reduction
    umap_model = UMAP(random_state=42,n_neighbors=15)

    # Initialize BERTopic with the embedding model and UMAP model
    topic_model = BERTopic(embedding_model=embedding_model, umap_model=umap_model, min_topic_size=10)

    # Fit the BERTopic model to the documents and extract topics and probabilities
    try:
        topics, probs = topic_model.fit_transform(docs)
    except Exception as e:
        print(f"Error during BERTopic fitting: {e}")
        return

    # Visualize the topics and their distribution
    try:
        fig = topic_model.visualize_topics()  # Create a topic visualization plot
        barchart = topic_model.visualize_barchart()  # Create a bar chart for topic distribution
        barchart.show()  # Display the bar chart
        fig.show()  # Display the topic visualization plot
    except Exception as e:
        print(f"Error during visualization: {e}")
