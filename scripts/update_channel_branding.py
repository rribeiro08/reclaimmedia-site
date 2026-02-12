#!/usr/bin/env python3
"""Update YouTube channel branding (profile picture and banner) via API"""

import pickle
import os
import sys
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
TOKEN_FILE = os.path.expanduser('~/clawd/projects/reclaim-media/config/token.pickle')
CLIENT_SECRET = os.path.expanduser('~/clawd/projects/reclaim-media/config/client_secret.json')

def get_authenticated_service():
    """Get authenticated YouTube service"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def get_channel_id(youtube):
    """Get the channel ID for the authenticated user"""
    response = youtube.channels().list(
        part='id,snippet,brandingSettings',
        mine=True
    ).execute()
    
    if response['items']:
        return response['items'][0]
    return None

def update_channel_image(youtube, channel_id, image_path, image_type='banner'):
    """
    Update channel banner or profile picture
    image_type: 'banner' or 'profile'
    """
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    if image_type == 'banner':
        # Update banner image
        body = {
            'brandingSettings': {
                'image': {
                    'bannerExternalUrl': f'data:image/png;base64,{image_data}'
                }
            }
        }
        
        # Use channelBanners.insert for banner
        media = MediaFileUpload(image_path, mimetype='image/png', resumable=True)
        response = youtube.channelBanners().insert(
            media_body=media
        ).execute()
        
        banner_url = response.get('url')
        print(f"Banner uploaded, URL: {banner_url}")
        
        # Now set the banner URL on the channel
        if banner_url:
            youtube.channels().update(
                part='brandingSettings',
                body={
                    'id': channel_id,
                    'brandingSettings': {
                        'image': {
                            'bannerExternalUrl': banner_url
                        }
                    }
                }
            ).execute()
            print("Banner set on channel!")
        
        return response
    else:
        # Profile picture - this requires Google account API, not YouTube
        print("Note: Profile pictures must be updated via Google Account, not YouTube API")
        print("The YouTube API doesn't support updating profile pictures directly.")
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python update_channel_branding.py <banner|profile> <image_path>")
        sys.exit(1)
    
    image_type = sys.argv[1]
    image_path = os.path.expanduser(sys.argv[2])
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    print(f"Updating channel {image_type}...")
    print(f"Image: {image_path}")
    
    youtube = get_authenticated_service()
    channel = get_channel_id(youtube)
    
    if not channel:
        print("Error: Could not find channel")
        sys.exit(1)
    
    channel_id = channel['id']
    print(f"Channel ID: {channel_id}")
    print(f"Channel Name: {channel['snippet']['title']}")
    
    result = update_channel_image(youtube, channel_id, image_path, image_type)
    
    if result:
        print("Success!")
    else:
        print("Could not update via API")

if __name__ == '__main__':
    main()
