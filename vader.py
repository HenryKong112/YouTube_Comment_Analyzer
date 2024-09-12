import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from langdetect import detect, DetectorFactory

def vader(path, get_name):
    try:
        """
        Perform sentiment analysis on textual data and export the results.

        Steps:
        1. Download the VADER lexicon if not already present.
        2. Read the input file (CSV or Excel).
        3. Preprocess the 'Comment' column (convert to lowercase, remove HTML tags).
        4. Filter out non-English comments.
        5. Remove pronouns and conjunctions from the text.
        6. Apply VADER sentiment analysis to classify comments as Positive, Negative, or Neutral.
        7. Export the results to a CSV or Excel file.
        8. Show a summary of sentiment analysis including counts and likes.
        9. Generate and display visualizations: 
           - Sentiment distribution (Counts vs Likes)
           - Engagement by Sentiment
           - Sentiment trend over time (if 'PublishedAt' column is available)

        Args:
            path (str): Path to the input CSV or Excel file.
            get_name (str): Base name for the output file.
        """
        
        # Ensure the VADER lexicon is downloaded
        nltk.download('vader_lexicon')

        # Read the input file based on its extension
        file_extension = Path(path).suffix
        if file_extension == '.csv':
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        # Preprocess the 'Comment' column
        df['Comment'] = df['Comment'].str.lower()
        df['Comment'] = df['Comment'].replace(r'<a href=".*?">.*?<\/a>', '', regex=True)
        df['Comment'] = df['Comment'].replace(r'<br>', '', regex=True)

        # Function to check if text is in English
        def is_english(text):
            try:
                return detect(text) == 'en'
            except:
                return False

        # Filter out non-English comments
        df = df[df['Comment'].apply(is_english)]

        # Define and remove pronouns and conjunctions
        pronouns_conjunctions = {
            'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves',
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
            'theirs', 'themselves', 'this', 'that', 'these', 'those', 'is', 'am', 'are', 'was', 
            'were', 'be', 'been', 'being', 'and', 'or', 'but', 'so', 'because', 'although', 
            'if', 'when', 'while'
        }
        
        def remove_pronouns_conjunctions(text):
            words = re.findall(r'\b\w+\b', text)
            filtered_words = [word for word in words if word not in pronouns_conjunctions]
            return ' '.join(filtered_words)

        # Apply the function to each comment
        df['Comment'] = df['Comment'].apply(remove_pronouns_conjunctions)

        # Initialize the VADER sentiment analyzer
        sentiments = SentimentIntensityAnalyzer()
        
        # Apply sentiment analysis
        df["Positive"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["pos"])
        df["Negative"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["neg"])
        df["Neutral"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["neu"])
        df["Compound"] = df["Comment"].apply(lambda x: sentiments.polarity_scores(x)["compound"])
        
        # Classify the overall sentiment
        df["Sentiment"] = df["Compound"].apply(
            lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral')
        )

        # Export the results to a CSV or Excel file
        if file_extension == '.csv':
            df.to_csv(f'VADER_{get_name}.csv', header=True, index=False, encoding='utf-8')
            messagebox.showinfo("Success", "Download successfully!")
        else:
            df.to_excel(f'VADER_{get_name}.xlsx', header=True, index=False)
            messagebox.showinfo("Success", "Download successfully!")

        # Show the sentiment analysis summary in a new window
        count_series = df['Sentiment'].value_counts()
        likes_by_sentiment = df.groupby('Sentiment')['Like'].sum()

        data = {
            'Sentiment': count_series.index.tolist(),
            'Count': count_series.values.tolist(),
            'Likes': likes_by_sentiment.reindex(count_series.index).values.tolist()
        }

        df_summary = pd.DataFrame(data)
        total_counts = df_summary['Count'].sum()
        total_likes = df_summary['Likes'].sum()
        df_summary['Count_Percent'] = round((df_summary['Count'] / total_counts * 100), 3)
        df_summary['Likes_Percent'] = round((df_summary['Likes'] / total_likes * 100), 3)
        df_summary['Engagement'] = round((df_summary['Likes'] / df_summary['Count']), 3)

        # Create a new Tkinter window to display the summary
        show_df_win = tk.Tk()
        show_df_win.title("VADER Summary")
        tree = ttk.Treeview(show_df_win, columns=list(df_summary.columns), show='headings')
        for col in df_summary.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for index, row in df_summary.iterrows():
            tree.insert('', tk.END, values=list(row))
        tree.pack(expand=True, fill='both')

        # Plot graphs
        # Plot 1: Sentiment Distribution (Counts and Likes)
        fig, ax1 = plt.subplots(figsize=(10, 10))
        ax1.bar(df_summary['Sentiment'], df_summary['Count_Percent'], color='skyblue', width=0.4, align='center', label='Count %')
        ax2 = ax1.twinx()
        ax2.bar(df_summary['Sentiment'], df_summary['Likes_Percent'], color='lightcoral', width=0.4, align='edge', label='Likes %')
        ax1.set_xlabel('Sentiment')
        ax1.set_ylabel('Percentage of Counts', color='blue')
        ax2.set_ylabel('Percentage of Likes', color='red')
        plt.title('Sentiment Distribution: Counts vs Likes')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Plot 2: Engagement per Sentiment
        plt.figure(figsize=(9, 9))
        plt.bar(df_summary['Sentiment'], df_summary['Engagement'], color='purple', alpha=0.7)
        plt.title('Engagement (Likes per Count) by Sentiment')
        plt.xlabel('Sentiment')
        plt.ylabel('Likes per Count')

        # Plot 3: Trend of Sentiment Over Time
        if 'PublishedAt' in df.columns:
            df['PublishedAt'] = pd.to_datetime(df['PublishedAt'], errors='coerce', utc=True)
            df.dropna(subset=['PublishedAt'], inplace=True)
            df.sort_values("PublishedAt", ascending=True, inplace=True)
            plt.figure(figsize=(20, 5))
            plt.plot(df['PublishedAt'], df['Compound'], marker='o', linestyle='-', color='b')
            plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gcf().autofmt_xdate()
            plt.title('Trend of Sentiment Over Time', fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Average Sentiment Score', fontsize=12)
        else:
            messagebox.showwarning("Warning", "The 'PublishedAt' column is missing or contains invalid data.")
        
        # Display plots
        plt.tight_layout()
        plt.show()

        show_df_win.mainloop()

    except Exception as e:
        # Show an error message if something goes wrong
        messagebox.showerror("ERROR", f"An error occurred: {e}")
