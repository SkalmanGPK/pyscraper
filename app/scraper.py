import requests # HTTP-calls
from bs4 import BeautifulSoup # HTML-parsing
import json # Serialize to JSON
import boto3 # Talk with S3/LocalStack

def fetch_page(url):
    pass

def save_to_s3(data):
    pass

def parse_data(html):
    pass


def main():
    url = "https://example.com"

    html = fetch_page(url)
    data = parse_data(html)
    save_to_s3(data)


if __name__ == "__main__":
    main()
