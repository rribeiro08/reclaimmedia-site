#!/usr/bin/env python3
"""
YouTube Video Uploader for Reclaim Media
Uses OAuth 2.0 for authentication with YouTube Data API v3
"""

import os
import sys
import json
import argparse
import pickle
import httplib2
from pathlib import Path
from datetime import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Scopes needed for YouTube upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / 'config'
CLIENT_SECRET = CONFIG_DIR / 'client_secret.json'
TOKEN_FILE = CONFIG_DIR / 'token.pickle'

# Video categories (YouTube category IDs)
CATEGORIES = {
    'film': '1',
    'autos': '2', 
    'music': '10',
    'pets': '15',
    'sports': '17',
    'travel': '19',
    'gaming': '20',
    'vlog': '22',
    'comedy': '23',
    'entertainment': '24',
    'news': '25',
    'howto': '26',
    'education': '27',
    'science': '28',
    'nonprofits': '29',
}

def get_authenticated_service():
    """Authenticate and return YouTube service."""
    creds = None
    
    # Load existing token if available
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"Error: Client secret not found at {CLIENT_SECRET}")
                print("Please download OAuth credentials from Google Cloud Console")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Save credentials for next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_file, title, description='', 
                 category='entertainment', tags=None, privacy='private'):
    """
    Upload a video to YouTube.
    
    Args:
        youtube: Authenticated YouTube service
        video_file: Path to video file
        title: Video title
        description: Video description
        category: Category name (from CATEGORIES dict)
        tags: List of tags
        privacy: 'private', 'public', or 'unlisted'
    
    Returns:
        Video ID if successful, None otherwise
    """
    if tags is None:
        tags = []
    
    category_id = CATEGORIES.get(category.lower(), '24')  # default to entertainment
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False
        }
    }
    
    # Create media upload object
    video_path = Path(video_file)
    if not video_path.exists():
        print(f"Error: Video file not found: {video_file}")
        return None
    
    media = MediaFileUpload(
        str(video_path),
        chunksize=1024*1024,  # 1MB chunks
        resumable=True
    )
    
    print(f"Uploading: {video_path.name}")
    print(f"Title: {title}")
    print(f"Privacy: {privacy}")
    
    try:
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"Upload progress: {progress}%")
        
        video_id = response['id']
        print(f"\n✓ Upload complete!")
        print(f"Video ID: {video_id}")
        print(f"URL: https://youtube.com/watch?v={video_id}")
        
        return video_id
        
    except HttpError as e:
        print(f"HTTP error during upload: {e}")
        return None
    except Exception as e:
        print(f"Error during upload: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Upload videos to YouTube')
    parser.add_argument('video', help='Path to video file')
    parser.add_argument('-t', '--title', required=True, help='Video title')
    parser.add_argument('-d', '--description', default='', help='Video description')
    parser.add_argument('-c', '--category', default='entertainment', 
                        choices=list(CATEGORIES.keys()), help='Video category')
    parser.add_argument('--tags', nargs='+', default=[], help='Video tags')
    parser.add_argument('-p', '--privacy', default='private',
                        choices=['private', 'public', 'unlisted'],
                        help='Privacy status')
    parser.add_argument('--auth-only', action='store_true',
                        help='Only authenticate, do not upload')
    
    args = parser.parse_args()
    
    print("Authenticating with YouTube...")
    youtube = get_authenticated_service()
    print("✓ Authenticated successfully\n")
    
    if args.auth_only:
        print("Auth-only mode. Exiting.")
        return
    
    video_id = upload_video(
        youtube,
        args.video,
        args.title,
        description=args.description,
        category=args.category,
        tags=args.tags,
        privacy=args.privacy
    )
    
    if video_id:
        print("\nUpload successful!")
    else:
        print("\nUpload failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
