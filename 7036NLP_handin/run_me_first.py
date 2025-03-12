import subprocess
import os

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
