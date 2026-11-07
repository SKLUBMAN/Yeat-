import os
import json
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")
# Yeat's official Uploads Playlist ID
UPLOADS_PLAYLIST_ID = "UUV4UK9LNNLViFP4qZA_Wmfw"

def fetch_youtube_posts():
    if not API_KEY:
        print("YOUTUBE_API_KEY environment variable not set. Skipping fetch.")
        return []

    url = (
        f"https://www.googleapis.com/youtube/v3/playlistItems?"
        f"key={API_KEY}&playlistId={UPLOADS_PLAYLIST_ID}&part=snippet&maxResults=25"
    )
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"YouTube API Error: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    posts = []
    
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        resource_id = snippet.get("resourceId", {})
        video_id = resource_id.get("videoId")
        
        if video_id:
            posts.append({
                "platform": "YouTube",
                "title": snippet.get("title", "Untitled Upload"),
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "published_at": snippet.get("publishedAt", ""),
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", "")
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
