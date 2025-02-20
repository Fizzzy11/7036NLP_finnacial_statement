from sec_edgar_downloader import Downloader

# Initialize SEC downloader (replace with your actual email)
from sec_edgar_downloader import Downloader

# Initialize the SEC EDGAR downloader with a valid user agent and email
dl = Downloader(company_name="zhaidanjie", email_address="zhaidanjie@gmail.com")

# Download the most recent 10-K filing for Apple (AAPL)
tickers = [
    "MSFT", "AAPL", "NVDA", "GOOGL", "META", "AVGO", "AMZN", "ORCL"
]

years = ["2019", "2020", "2021", "2022", "2023"]

for ticker in tickers:
    for year in years:
        print(f"Downloading {ticker} 10-K for {year}...")
        dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")

foreign_tickers = ["TSM", "ASML"]

for ticker in foreign_tickers:
    for year in years:
        print(f"Downloading {ticker} 20-F for {year}...")
        dl.get("20-F", ticker, after=f"{year}-01-01", before=f"{year}-12-31")
