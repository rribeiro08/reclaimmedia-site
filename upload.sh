#!/bin/bash
# Reclaim Media - Multi-Platform Video Upload Script
# Usage: ./upload.sh <platform> <video_file> [options]
#
# Platforms:
#   youtube, yt    - YouTube upload
#   facebook, fb   - Facebook Reel upload
#   all            - Upload to all platforms
#
# Examples:
#   ./upload.sh youtube video.mp4 -t "Title" -d "Description"
#   ./upload.sh facebook video.mp4 -d "Caption for Facebook"
#   ./upload.sh all video.mp4 -t "Title" -d "Description"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate" 2>/dev/null || {
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv "$SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
    pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
}

show_help() {
    echo "Reclaim Media - Video Upload Tool"
    echo ""
    echo "Usage: $0 <platform> <video_file> [options]"
    echo ""
    echo "Platforms:"
    echo "  youtube, yt    Upload to YouTube"
    echo "  facebook, fb   Upload to Facebook as Reel"
    echo "  all            Upload to all platforms"
    echo ""
    echo "YouTube Options:"
    echo "  -t, --title       Video title (required for YouTube)"
    echo "  -d, --description Video description"
    echo "  -p, --privacy     Privacy: public, private, unlisted (default: public)"
    echo "  -c, --category    Category ID (default: 22 for People & Blogs)"
    echo ""
    echo "Facebook Options:"
    echo "  -d, --description Caption for the Reel"
    echo "  --feed            Upload to feed instead of Reel"
    echo ""
    echo "Examples:"
    echo "  $0 youtube video.mp4 -t 'My Video' -d 'Description'"
    echo "  $0 facebook video.mp4 -d 'Check this out! #reels'"
    echo "  $0 all video.mp4 -t 'My Video' -d 'Description'"
}

if [ $# -lt 2 ]; then
    show_help
    exit 1
fi

PLATFORM="$1"
shift

case "$PLATFORM" in
    youtube|yt)
        echo "📺 Uploading to YouTube..."
        python3 "$SCRIPT_DIR/scripts/youtube_upload.py" "$@"
        ;;
    facebook|fb)
        echo "📘 Uploading to Facebook..."
        python3 "$SCRIPT_DIR/scripts/facebook_upload.py" "$@"
        ;;
    all)
        VIDEO_FILE="$1"
        shift
        echo "🌐 Uploading to all platforms..."
        echo ""
        echo "📺 YouTube upload:"
        python3 "$SCRIPT_DIR/scripts/youtube_upload.py" "$VIDEO_FILE" "$@"
        YT_RESULT=$?
        echo ""
        echo "📘 Facebook upload:"
        python3 "$SCRIPT_DIR/scripts/facebook_upload.py" "$VIDEO_FILE" "$@"
        FB_RESULT=$?
        echo ""
        if [ $YT_RESULT -eq 0 ] && [ $FB_RESULT -eq 0 ]; then
            echo "✅ All uploads completed successfully!"
        else
            echo "⚠️  Some uploads failed"
            [ $YT_RESULT -ne 0 ] && echo "  - YouTube: Failed"
            [ $FB_RESULT -ne 0 ] && echo "  - Facebook: Failed"
        fi
        ;;
    -h|--help|help)
        show_help
        exit 0
        ;;
    *)
        echo "❌ Unknown platform: $PLATFORM"
        echo "Use: youtube, facebook, or all"
        echo "Run '$0 --help' for more info"
        exit 1
        ;;
esac
