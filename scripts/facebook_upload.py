#!/usr/bin/env python3
"""
Facebook video upload script using Graph API
Uploads videos as Reels to a Facebook Page
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path

# Configuration
CONFIG_PATH = Path(__file__).parent.parent / "config" / "facebook_credentials.json"
GRAPH_API_VERSION = "v24.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def load_credentials():
    """Load Facebook credentials from config file"""
    if not CONFIG_PATH.exists():
        print(f"❌ Credentials file not found: {CONFIG_PATH}")
        sys.exit(1)
    
    with open(CONFIG_PATH) as f:
        return json.load(f)

def upload_video_reel(video_path: str, description: str = "", creds: dict = None):
    """
    Upload video as a Reel to Facebook Page
    
    Facebook Reels upload is a 3-step process:
    1. Initialize upload session
    2. Upload video file
    3. Publish the Reel
    """
    if creds is None:
        creds = load_credentials()
    
    page_id = creds["page_id"]
    access_token = creds["page_access_token"]
    
    video_path = Path(video_path)
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        return None
    
    file_size = video_path.stat().st_size
    print(f"📹 Uploading: {video_path.name} ({file_size / 1024 / 1024:.1f} MB)")
    
    # Step 1: Initialize upload session
    print("⏳ Step 1/3: Initializing upload session...")
    init_url = f"{BASE_URL}/{page_id}/video_reels"
    init_params = {
        "upload_phase": "start",
        "access_token": access_token
    }
    
    init_response = requests.post(init_url, data=init_params)
    if init_response.status_code != 200:
        print(f"❌ Failed to initialize upload: {init_response.text}")
        return None
    
    init_data = init_response.json()
    video_id = init_data.get("video_id")
    upload_url = init_data.get("upload_url")
    
    if not video_id or not upload_url:
        print(f"❌ Invalid init response: {init_data}")
        return None
    
    print(f"✅ Video ID: {video_id}")
    
    # Step 2: Upload video file
    print("⏳ Step 2/3: Uploading video file...")
    with open(video_path, "rb") as video_file:
        upload_headers = {
            "Authorization": f"OAuth {access_token}",
            "offset": "0",
            "file_size": str(file_size)
        }
        upload_response = requests.post(
            upload_url,
            headers=upload_headers,
            data=video_file.read()
        )
    
    if upload_response.status_code != 200:
        print(f"❌ Upload failed: {upload_response.text}")
        return None
    
    print("✅ Video uploaded successfully")
    
    # Step 3: Publish the Reel
    print("⏳ Step 3/3: Publishing Reel...")
    publish_params = {
        "upload_phase": "finish",
        "video_id": video_id,
        "access_token": access_token,
        "video_state": "PUBLISHED"
    }
    
    if description:
        publish_params["description"] = description
    
    publish_response = requests.post(init_url, data=publish_params)
    
    if publish_response.status_code != 200:
        print(f"❌ Publish failed: {publish_response.text}")
        return None
    
    publish_data = publish_response.json()
    success = publish_data.get("success", False)
    
    if success:
        print(f"✅ Reel published successfully!")
        print(f"🔗 Video ID: {video_id}")
        return video_id
    else:
        print(f"❌ Publish response: {publish_data}")
        return None


def upload_video_feed(video_path: str, description: str = "", creds: dict = None):
    """
    Upload video to Facebook Page feed (not as Reel)
    Simpler single-request upload for smaller videos
    """
    if creds is None:
        creds = load_credentials()
    
    page_id = creds["page_id"]
    access_token = creds["page_access_token"]
    
    video_path = Path(video_path)
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        return None
    
    file_size = video_path.stat().st_size
    print(f"📹 Uploading to feed: {video_path.name} ({file_size / 1024 / 1024:.1f} MB)")
    
    url = f"{BASE_URL}/{page_id}/videos"
    
    with open(video_path, "rb") as video_file:
        files = {
            "source": (video_path.name, video_file, "video/mp4")
        }
        data = {
            "access_token": access_token,
            "description": description
        }
        
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        video_id = result.get("id")
        print(f"✅ Video uploaded successfully!")
        print(f"🔗 Video ID: {video_id}")
        return video_id
    else:
        print(f"❌ Upload failed: {response.text}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Upload video to Facebook")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("-d", "--description", default="", help="Video description/caption")
    parser.add_argument("--reel", action="store_true", help="Upload as Reel (default)")
    parser.add_argument("--feed", action="store_true", help="Upload to feed instead of Reel")
    args = parser.parse_args()
    
    if args.feed:
        video_id = upload_video_feed(args.video_path, args.description)
    else:
        video_id = upload_video_reel(args.video_path, args.description)
    
    if video_id:
        print(f"\n🎉 Success! Video ID: {video_id}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
