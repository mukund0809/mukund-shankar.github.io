# YouTube Videos Auto-Update Setup

This guide will help you set up automatic YouTube video fetching for your website.

## How It Works

1. **GitHub Actions Workflow** - Runs daily (or on-demand) to fetch your latest YouTube videos
2. **YouTube Data API** - Retrieves your video metadata (title, thumbnail, publish date)
3. **videos.json** - Stores the video data that your website reads and displays
4. **Website** - Automatically displays your latest videos on the Guitaring tab

## Setup Instructions

### Step 1: Get Your YouTube Channel ID

Your channel ID is needed for the automation script. You can find it:

1. Go to your channel: https://www.youtube.com/@HisOzzness69
2. Look at the URL or go to Settings → Basic Info
3. Copy your Channel ID (starts with "UC...")

In the file `scripts/fetch_videos.py`, replace this line with your actual channel ID:
```python
CHANNEL_ID = "UCY0y2jGW3FhvZiPUYIK-jWw"  # Replace with your actual channel ID
```

### Step 2: Create a YouTube Data API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the **YouTube Data API v3**
4. Create an API key (Credentials → Create Credentials → API Key)
5. Copy your API key

### Step 3: Add API Key to GitHub Secrets

1. Go to your GitHub repository: https://github.com/mukund0809/mukund-shankar.github.io
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `YOUTUBE_API_KEY`
5. Value: Paste your API key from Step 2
6. Click "Add secret"

### Step 4: Test the Automation

1. Go to your GitHub repository
2. Click "Actions" tab
3. Click "Update YouTube Videos" workflow on the left
4. Click "Run workflow" → "Run workflow"
5. Wait for it to complete (should take 1-2 minutes)
6. Check that `videos.json` has been updated with your actual videos

### Step 5: Done!

Your website will now:
- **Automatically fetch** your latest videos every day at 12:00 UTC
- **Display them** on the Guitaring tab
- **Update videos.json** in your repository

You can change the schedule in `.github/workflows/update_videos.yml` by modifying the cron expression.

## Manual Testing

To test locally before publishing, run:
```bash
export YOUTUBE_API_KEY="your_api_key_here"
python scripts/fetch_videos.py
```

This will update `videos.json` with your actual videos.

## Customization

- **Change update frequency**: Edit the cron expression in `.github/workflows/update_videos.yml`
  - `0 12 * * *` = daily at 12:00 UTC
  - `0 */6 * * *` = every 6 hours
  - `0 0 * * 0` = weekly on Sunday at midnight

- **Change number of videos**: Edit `MAX_VIDEOS` in `scripts/fetch_videos.py`

- **Customize display**: Edit the HTML and CSS in `index.html` under the "Latest Videos" section

## Troubleshooting

**Videos not updating?**
- Check GitHub Actions tab for error logs
- Make sure API key is set correctly in secrets
- Verify your Channel ID is correct

**"API key invalid" error?**
- Double-check your API key in GitHub secrets
- Make sure YouTube Data API is enabled in Google Cloud Console

**Want to manually update?**
- Go to Actions → Update YouTube Videos → Run workflow
- Or modify `videos.json` directly with your video IDs
