import os
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')  
nltk.download('stopwords')  

stop_words = set(stopwords.words('english'))

# keep paragraph & sentence
def preprocess_text(text, stopwords):
    """
    1. keep sentence structure
    2. use `<PARA>` to keep parapraph info
    3. stopwords
    """
    # `<PARA>`
    text = text.replace("\n\n", " <PARA> ")  

    text = re.sub(r'[^a-zA-Z0-9.,!?;:\s]', ' ', text)

    sentences = sent_tokenize(text)

    # process every sentence
    filtered_sentences = []
    for sentence in sentences:
        words = sentence.split()  # split with space
        words = [word for word in words if word.lower() not in stopwords] 
        filtered_sentences.append(" ".join(words))  # rejoin

    return " ".join(filtered_sentences)

# process all txt files
def process_directory(txt_folder):
    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(txt_folder, filename)
            with open(file_path, "r", encoding='utf-8') as f:
                raw_text = f.read()
                filtered_text = preprocess_text(raw_text, stop_words)

                # output as filtered_txt 
                parent_folder = os.path.dirname(txt_folder)
                filtered_txt_folder = os.path.join(parent_folder, "filtered_txt") 
                os.makedirs(filtered_txt_folder, exist_ok=True)
                output_file_path = os.path.join(filtered_txt_folder, f"filtered_{filename}")

                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(filtered_text)

                print(f"Finished!!!: {filename}")

# main function
if __name__ == '__main__':
    base_dir = "txt"  # Annual Report Folder Path
    process_directory(base_dir)