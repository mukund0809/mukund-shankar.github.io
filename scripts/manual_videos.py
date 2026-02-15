#!/usr/bin/env python3
"""
Simple script to manually fetch videos from YouTube channel
Usage: python get_channel_id.py

This will help you find your channel ID and optionally fetch videos
"""

import json
from datetime import datetime

def manual_video_entry():
    """Manually add videos if you have the IDs"""
    print("\n" + "="*60)
    print("MANUAL VIDEO ENTRY")
    print("="*60)
    print("\nIf you know your YouTube video IDs, you can manually add them here.")
    print("Video ID is the part after 'v=' in a YouTube URL")
    print("(Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ → dQw4w9WgXcQ)")
    print("\nEnter video IDs (one per line, press Enter twice when done):\n")
    
    videos = []
    count = 1
    
    while True:
        video_id = input(f"Video {count} ID (or press Enter to finish): ").strip()
        if not video_id:
            break
        
        title = input(f"Video {count} Title (optional): ").strip()
        if not title:
            title = f"Guitar Video {count}"
        
        video = {
            "videoId": video_id,
            "title": title,
            "publishedAt": datetime.utcnow().isoformat() + 'Z'
        }
        videos.append(video)
        count += 1
        print()
    
    if videos:
        # Reverse to show newest first
        videos.reverse()
        
        data = {
            'videos': videos,
            'lastUpdated': datetime.utcnow().isoformat() + 'Z'
        }
        
        with open('videos.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully saved {len(videos)} videos to videos.json")
        print("  Your videos will now appear on the website!")
        return True
    
    return False

def find_channel_id_instructions():
    """Print instructions to find channel ID"""
    print("\n" + "="*60)
    print("HOW TO FIND YOUR YOUTUBE CHANNEL ID")
    print("="*60)
    print("""
1. Go to your YouTube channel: https://www.youtube.com/@HisOzzness69

2. Open page source (right-click → "View page source", or press Ctrl+Shift+I)

3. Press Ctrl+F to search for: channelId

4. Look for: "channelId":"UC..." 
   Copy the entire ID starting with "UC"
   Example: UCAbcDef123GhIjk456LmNoPqR

5. Update scripts/fetch_videos.py, line 9:
   CHANNEL_ID = "PASTE_YOUR_ID_HERE"

Need API key setup? Check YOUTUBE_SETUP.md for full instructions.
    """)

if __name__ == '__main__':
    print("="*60)
    print("YouTube Video Manager")
    print("="*60)
    
    choice = input("""
Choose an option:
1) Manually add video IDs
2) Get help finding channel ID
3) Exit

Enter choice (1-3): """).strip()
    
    if choice == '1':
        manual_video_entry()
    elif choice == '2':
        find_channel_id_instructions()
    else:
        print("Goodbye!")
