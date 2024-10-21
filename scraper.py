import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def fetch_page():
    # Initialize a session to reuse across requests
    session = requests.Session()

    def extract_links_from_page(url, link_filter):
        """Extract links from a given page based on the filter function."""
        try:
            response = session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract relevant links based on the provided filter function
                links = [a.get('href') for a in soup.find_all('a', href=True) if link_filter(a.get('href'))]
                return links
            else:
                return []
        except requests.RequestException as e:
            print(f"Error retrieving {url}: {e}")
            return []

    def filter_video_links(href):
        """Filter for video links."""
        return "https://draftsex.porn/video/" in href

    def filter_model_links(href):
        """Filter for model links."""
        return "https://draftsex.porn/models/" in href and "html" in href

    def process_pages(base_url, page_range, link_filter):
        """Process multiple pages in parallel and extract links."""
        all_links = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit page fetching tasks in parallel
            future_to_url = {executor.submit(extract_links_from_page, f"{base_url}/page{page}.html", link_filter): page for page in page_range}
            
            for future in future_to_url:
                links = future.result()
                all_links.extend(links)
        return all_links

    

    # Step 21: Collect all video links from categories
    cats = ["top-rated", "most-viewed", "most-recent"]
    video_links = []
    for cat in cats:
        cat_links = process_pages(f'https://draftsex.porn/{cat}', range(10), filter_video_links)
        video_links.extend(cat_links)
    

    # Step 2: Collect all model links
    model_links = process_pages('https://draftsex.porn/models', range(100), filter_model_links)
    
    
    # Step 3: Process all collected links to extract further video links
    vids = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(extract_links_from_page, url, filter_video_links): url for url in model_links}
        
        for future in future_to_url:
            extracted_vids = future.result()
            vids.extend(extracted_vids)

    # Return or print the total links collected
    return vids

