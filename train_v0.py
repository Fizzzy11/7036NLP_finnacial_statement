import os
import glob
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# load FinBERT
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

# raed
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# split for every 300 words
def split_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# analize
def analyze_sentiment(text_chunks):
    total_positive, total_negative, total_neutral = 0, 0, 0
    
    for chunk in text_chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)  # softmax
        
        # adduo Positive, Neutral, Negative 
        total_negative += scores[0][0].item()
        total_neutral += scores[0][1].item()
        total_positive += scores[0][2].item()
    
    return total_positive, total_negative, total_neutral

# rename files
def parse_filename(filename):
    parts = filename.replace("filtered_", "").replace(".txt", "").split("-")
    stock = parts[0]  
    date = f"{parts[1]}_{parts[2]}_{parts[3]}" 
    cik = parts[4]  
    return stock, date, cik

# save as CSV
def process_all_reports(input_folder, output_csv):
    results = []
    files = glob.glob(os.path.join(input_folder, "*.txt"))


    for file_path in files:
        filename = os.path.basename(file_path)
        print(f"Processing: {filename}")

        stock, date, cik = parse_filename(filename)

        # read and split txt
        report_text = load_text(file_path)
        text_chunks = split_text(report_text, chunk_size=300)
        
        # compute the score
        total_positive, total_negative, total_neutral = analyze_sentiment(text_chunks)

        # ratio
        total_score = total_positive + total_negative + total_neutral
        positive_ratio = round(total_positive / total_score * 100, 2) if total_score > 0 else 0
        negative_ratio = round(total_negative / total_score * 100, 2) if total_score > 0 else 0
        neutral_ratio = round(total_neutral / total_score * 100, 2) if total_score > 0 else 0

        # save
        results.append({
            "stock": stock,
            "cik": cik,  
            "date": date,  
            "positive": round(total_positive, 4),
            "negative": round(total_negative, 4),
            "neutral": round(total_neutral, 4),
            "positive_ratio": positive_ratio,
            "negative_ratio": negative_ratio,
            "neutral_ratio": neutral_ratio
        })

    # save
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    print(f"Finised!!! Save as {output_csv}")


input_folder = "filtered_txt"  # report folder Path
output_csv = "financial_sentiment_results.csv"  # output file name 

process_all_reports(input_folder, output_csv)
