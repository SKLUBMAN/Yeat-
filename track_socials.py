import os
import json
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")
YEAT_CHANNEL_ID = "UCV4UK9LNNLViFP4qZA_Wmfw"

def fetch_youtube_posts():
    if not API_KEY:
        print("YOUTUBE_API_KEY environment variable not set. Skipping fetch.")
        return []

    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"key={API_KEY}&channelId={YEAT_CHANNEL_ID}&part=snippet,id&order=date&maxResults=10"
    )
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"YouTube API Error: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    posts = []
    
    for item in data.get("items", []):
        if item.get("id", {}).get("kind") == "youtube#video":
            posts.append({
                "platform": "YouTube",
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "published_at": item["snippet"]["publishedAt"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            })
            
    return posts

def save_social_data(data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/social_posts.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} social posts to {file_path}")

if __name__ == "__main__":
    posts = fetch_youtube_posts()
    save_social_data(posts)
  
