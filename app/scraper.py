import requests # HTTP-calls
from bs4 import BeautifulSoup # HTML-parsing
import json # Serialize to JSON
import boto3 # Talk with S3/LocalStack
from datetime import datetime # Timestamping JSON files.

# Fetches page information, User-Agent
def fetch_page(url: str) -> str:
    headers = {
            "User-Agent": "Mozilla/5.0 (compatible; pyscraper/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.Timeout:
        print(f"Timeout: {url} didn't answer within 10 seconds")
        raise
    except requests.exceptions.HTTPError as e:
        print(f"HTTP-error: {e.response.status_code} for {url}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Networking error: {e}")
        raise

#Saves information to S3 LocalStack.
def save_to_s3(data):
    client = boto3.client(
            "s3",
            endpoint_url="http://localhost:4566" 
            #boto3 communicates with LocalStack instead of AWS
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-&M-%S")
    filename = f"{timestamp}_articles.json"

    json_data = json.dumps(data, indent=2, ensure_ascii=False)

    client.put_object(
            Bucket="pyscraper",
            Key=filename,
            Body=json_data
    )


# Extracts articletitles and links from HTML. Missing fields are assigned None instead of breaking parse.
def parse_data(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.find_all("article", class_="product_pod"):
        title_element = article.find("h3")
        title = title_element.find("a").get("title") if title_element else None

        price_element = article.find("p", class_="price_color")
        price = price_element.text.strip() if price_element else None

        if title:
            books.append({"title": title, "price": price})
    return books
def main():
    url = "https://books.toscrape.com"

    html = fetch_page(url)
    data = parse_data(html)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    # save_to_s3(data)


if __name__ == "__main__":
    main()
