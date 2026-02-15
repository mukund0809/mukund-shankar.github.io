#!/usr/bin/env python3
"""
Script to fetch ALL videos from a YouTube channel and save to videos.json
Requires YOUTUBE_API_KEY environment variable to be set

This script will:
1. Fetch ALL videos from your YouTube channel
2. Sort them by publish date (newest first)
3. Save them to videos.json automatically
"""

import os
import json
import sys
from datetime import datetime
from googleapiclient.discovery import build

# Channel ID for @HisOzzness69
CHANNEL_ID = "UCY0y2jGW3FhvZiPUYIK-jWw"  # Replace with your actual channel ID
API_KEY = os.environ.get('YOUTUBE_API_KEY')
MAX_VIDEOS = 50  # Number of latest videos to display (increase to show more)

def get_channel_id_from_handle(youtube, handle):
    """Convert @handle to channel ID if needed"""
    try:
        request = youtube.search().list(
            q=handle,
            type='channel',
            part='id',
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]['id']['channelId']
    except Exception as e:
        print(f"Error finding channel: {e}")
    return None

def get_uploads_playlist_id(youtube, channel_id):
    """Get the uploads playlist ID for a channel"""
    try:
        request = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except Exception as e:
        print(f"Error getting uploads playlist: {e}")
    return None

def fetch_videos(youtube, uploads_playlist_id):
    """Fetch all videos from uploads playlist"""
    videos = []
    next_page_token = None
    
    try:
        while True:
            request = youtube.playlistItems().list(
                playlistId=uploads_playlist_id,
                part='contentDetails,snippet',
                maxResults=50,  # Max allowed by API
                pageToken=next_page_token,
                order='date'
            )
            
            response = request.execute()
            
            for item in response.get('items', []):
                video = {
                    'videoId': item['contentDetails']['videoId'],
                    'title': item['snippet']['title'],
                    'publishedAt': item['snippet']['publishedAt']
                }
                videos.append(video)
                
                # Stop if we have enough videos
                if len(videos) >= MAX_VIDEOS:
                    break
            
            # Stop if we've reached max videos or no more pages
            if len(videos) >= MAX_VIDEOS or 'nextPageToken' not in response:
                break
            
            next_page_token = response.get('nextPageToken')
        
        # Sort by publish date - newest first
        videos.sort(key=lambda x: x['publishedAt'], reverse=True)
        return videos[:MAX_VIDEOS]
    
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

def save_videos(videos):
    """Save videos to JSON file"""
    data = {
        'videos': videos,
        'lastUpdated': datetime.utcnow().isoformat() + 'Z'
    }
    
    with open('videos.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved {len(videos)} videos to videos.json")

def main():
    if not API_KEY:
        print("Error: YOUTUBE_API_KEY environment variable not set")
        sys.exit(1)
    
    # Build YouTube API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # Get uploads playlist ID
    uploads_playlist_id = get_uploads_playlist_id(youtube, CHANNEL_ID)
    if not uploads_playlist_id:
        print("Error: Could not find uploads playlist")
        sys.exit(1)
    
    # Fetch videos
    videos = fetch_videos(youtube, uploads_playlist_id)
    if not videos:
        print("Error: No videos found")
        sys.exit(1)
    
    # Save to JSON
    save_videos(videos)
    print("Done!")

if __name__ == '__main__':
    main()
