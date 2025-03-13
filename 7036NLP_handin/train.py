import os
import glob
import pandas as pd
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nltk.tokenize import sent_tokenize

# load FinBert
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

# Read report
def load_text(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()

# word split
def split_text(text, max_tokens=400):
    """
    1. split with `<PARA>`
    2. if length over 400, use `.`、`?`、`!` to split
    3. make sure at least one sentence will in one single chunk
    """
    paragraphs = text.split("<PARA>")  
    chunks = []

    for para in paragraphs:
        words = para.split()
        token_count = len(tokenizer.tokenize(para))  # count token

        if token_count <= max_tokens:
            # as one chunk
            chunks.append(para.strip())
        else:
            # split by sentence
            sentences = sent_tokenize(para)
            current_chunk = []
            current_tokens = 0

            for sentence in sentences:
                sentence_tokens = len(tokenizer.tokenize(sentence))

                if sentence_tokens > max_tokens:
                    if current_chunk:
                        chunks.append(" ".join(current_chunk)) 
                        current_chunk = []  
                        current_tokens = 0
                    chunks.append(sentence)  
                elif current_tokens + sentence_tokens <= max_tokens:
                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens
                else:
                    # if current chunk over max_tokens，save first and start a new chunk
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [sentence]
                    current_tokens = sentence_tokens

            # rest chunk
            if current_chunk:
                chunks.append(" ".join(current_chunk))

    return chunks

# analyze
def analyze_sentiment(text_chunks):
    total_positive, total_negative, total_neutral = 0, 0, 0
    
    for chunk in text_chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)  # softmax
        
        total_negative += scores[0][0].item()
        total_neutral += scores[0][1].item()
        total_positive += scores[0][2].item()
    
    return total_positive, total_negative, total_neutral

# txt name
def parse_filename(filename):
    filename = filename.replace("filtered_", "").replace(".txt", "")
    parts = filename.split("-")
    
    stock = parts[0] 
    date = f"{parts[1]}_{parts[2]}_{parts[3]}"  
    cik = parts[4]  
    
    return stock, date, cik

# process all reports and save as a CSV file
def process_all_reports(input_folder, output_csv):
    results = []
    files = glob.glob(os.path.join(input_folder, "*.txt"))

    print(f"Get {len(files)} reports, start processing... \n")

    for file_path in files:
        filename = os.path.basename(file_path)
        print(f"Processing on: {filename}")

        stock, date, cik = parse_filename(filename)

        report_text = load_text(file_path)
        text_chunks = split_text(report_text, max_tokens=400)

        total_positive, total_negative, total_neutral = analyze_sentiment(text_chunks)

        total_score = total_positive + total_negative + total_neutral
        positive_ratio = round(total_positive / total_score * 100, 2) if total_score > 0 else 0
        negative_ratio = round(total_negative / total_score * 100, 2) if total_score > 0 else 0
        neutral_ratio = round(total_neutral / total_score * 100, 2) if total_score > 0 else 0

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

    # save as a CSV file 
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    print(f"Done!!! Save as: {output_csv}")

# main function
input_folder = "filtered_txt"
output_csv = "financial_sentiment_results_final.csv"

process_all_reports(input_folder, output_csv)