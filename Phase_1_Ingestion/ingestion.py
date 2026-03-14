import csv
import json
from datetime import datetime, timedelta
from google_play_scraper import Sort, reviews

def fetch_recent_reviews(app_id="com.nextbillion.groww", weeks=4, max_count=1000):
    """
    Phase 1: Fetch recent reviews from Google Play Store.
    """
    print(f"Phase 1: Fetching reviews for {app_id}...")
    cutoff_date = datetime.now() - timedelta(weeks=weeks)
    
    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=max_count 
    )

    filtered_reviews = []
    for review in result:
        if review['at'] >= cutoff_date:
            filtered_reviews.append({
                "date": review['at'].strftime("%Y-%m-%d %H:%M:%S"),
                "rating": review['score'],
                "title": "",
                "text": review['content'].replace('\n', ' ').strip()
            })

    print(f"Phase 1 Complete: Fetched {len(filtered_reviews)} reviews.")
    return filtered_reviews

def save_raw_data(reviews_data, csv_path="sample_reviews.csv", json_path="sample_reviews.json"):
    if not reviews_data:
        return
        
    # Save CSV
    keys = reviews_data[0].keys()
    with open(csv_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(reviews_data)
        
    # Save JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(reviews_data, f, indent=4)
    print(f"Data saved to {csv_path} and {json_path}")
