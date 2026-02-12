# Reclaim Media - Multi-Platform Video Publisher

Automated video upload to YouTube and Facebook for the Reclaim Media brand.

## Quick Start

```bash
# YouTube upload
./upload.sh youtube video.mp4 -t "Video Title" -d "Description"

# Facebook Reel upload  
./upload.sh facebook video.mp4 -d "Caption with #hashtags"

# Upload to all platforms
./upload.sh all video.mp4 -t "Title" -d "Description"
```

## Setup Status

### ✅ YouTube
- **Channel:** Configured via OAuth
- **Credentials:** `config/youtube_client_secret.json` + `config/youtube_token.json`
- **Privacy:** Default public

### ✅ Facebook
- **Page:** Reclaim Media (ID: 903807692825542)
- **Credentials:** `config/facebook_credentials.json`
- **Token expires:** ~Feb 2026
- **Permissions:** pages_manage_posts, instagram_content_publish, pages_read_engagement

### 🔲 Instagram (Not yet connected)
- Requires connecting Instagram Business Account to Facebook Page
- Use Meta Business Suite to link accounts

## Directory Structure

```
reclaim-media/
├── config/
│   ├── youtube_client_secret.json    # YouTube OAuth client
│   ├── youtube_token.json            # YouTube auth token (auto-generated)
│   └── facebook_credentials.json     # Facebook Page token
├── scripts/
│   ├── youtube_upload.py             # YouTube upload script
│   └── facebook_upload.py            # Facebook Reel upload script
├── upload.sh                         # Main upload wrapper
├── venv/                             # Python virtual environment
└── README.md
```

## Platform-Specific Options

### YouTube
```bash
./upload.sh youtube video.mp4 \
  -t "Video Title" \
  -d "Video description" \
  -p public|private|unlisted \
  -c 22  # Category ID (22=People & Blogs)
```

### Facebook
```bash
./upload.sh facebook video.mp4 \
  -d "Caption with #hashtags" \
  --reel     # Upload as Reel (default)
  --feed     # Upload to feed instead
```

## Token Renewal

### YouTube
YouTube tokens auto-refresh. If auth fails, delete `config/youtube_token.json` and re-run upload.

### Facebook  
Page token expires ~60 days. To renew:
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select "Reclaim Media" app
3. Add permissions: pages_manage_posts, pages_show_list, pages_read_engagement, instagram_content_publish
4. Click "Generate Access Token"
5. Run: `GET /me/accounts` to get new Page token
6. Update `config/facebook_credentials.json`

## Troubleshooting

### YouTube: "Token has been expired or revoked"
```bash
rm config/youtube_token.json
./upload.sh youtube video.mp4 -t "Test"  # Will prompt for re-auth
```

### Facebook: "Invalid access token"
Token expired. Follow renewal steps above.

### Facebook: "pages_manage_posts permission required"
Regenerate token with proper permissions in Graph API Explorer.

## Dependencies

- Python 3.9+
- google-api-python-client
- google-auth-oauthlib
- requests

Install: `pip install -r requirements.txt`
