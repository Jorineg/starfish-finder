import requests
from bs4 import BeautifulSoup
import os
import urllib.parse


def download_images(url, output_dir, visited=None):
    if visited is None:
        visited = set()

    if url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Download images
        for img in soup.find_all("img"):
            img_url = img.get("src")
            if img_url:
                img_url = urllib.parse.urljoin(url, img_url)
                img_name = os.path.basename(urllib.parse.urlparse(img_url).path)
                img_path = os.path.join(output_dir, img_name)

                with open(img_path, "wb") as f:
                    img_response = requests.get(img_url)
                    f.write(img_response.content)
                print(f"Downloaded: {img_name}")

        # Find and follow links to subpages
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                full_url = urllib.parse.urljoin(url, href)
                if full_url.startswith(url):  # Only follow links within the same domain
                    download_images(full_url, output_dir, visited)

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")


# Usage
base_url = "https://kucheriki.com/"  # Replace with the website you want to scrape
output_directory = "downloaded_images"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

download_images(base_url, output_directory)
