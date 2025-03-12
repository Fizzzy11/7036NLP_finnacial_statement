import subprocess
import os

import requests,time,csv,os,re,,threading
import pandas as pd
import concurrent.futures
import os,psutil
import html2text
import multiprocessing 
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk
import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


def run_script(script_name):
    try:
        script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.py")
        subprocess.run(["python", script_path], check=True)
        print(f"Successfully ran {script_name}.py")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}.py: {e}")

if __name__ == "__main__":
    scripts = [
        "information_acquiring",
        "download_annual_report",
        "html2txt",
        "split&stopwords",
        "train"
    ]
    
    for script in scripts:
        run_script(script)
