# Couch to 5K Complete Training Program

A comprehensive 9-week program to take you from couch to running 5K (30 minutes) continuously, complete with calendar scheduling and audio coaching scripts.

## 🏃‍♂️ Overview

This repository contains everything you need for a complete Couch to 5K training program:
- **Dynamic Calendar Generation**: Python script to create custom workout schedules
- **Audio Coaching Scripts**: 14 detailed scripts for voice-guided workouts
- **Audio Generation Tools**: Python scripts to create professional AI-powered audio files
- **Progressive Training Plan**: Scientifically designed 9-week progression

## 📅 Program Schedule

- **Default Schedule**: Monday, Wednesday, Friday at 12:00 PM UTC
- **Duration**: 9 weeks (27 total workouts)
- **Customizable**: Generate your own schedule with preferred workout days

## 📁 Repository Contents

### `generate_calendar.py`
Python script to generate custom workout schedules:
- Choose your start date
- Select your preferred workout days
- Set your workout time and timezone
- Generates ICS file compatible with all major calendar apps
- Includes complete workout descriptions and milestones

Usage:
```bash
python generate_calendar.py --start-date 2025-06-09 --workout-days "Monday,Wednesday,Friday" --workout-time "7:00 am CDT"
```

Supported timezones:
- EST/EDT (Eastern)
- CST/CDT (Central)
- MST/MDT (Mountain)
- PST/PDT (Pacific)
- UTC/GMT

### `C25K_Audio_Scripts/`
Complete audio coaching system with 14 scripts:
- **Week 1-4**: Interval training scripts
- **Week 5**: Building to 20-minute milestone
- **Week 6**: Building to 25-minute milestone  
- **Week 7-9**: Continuous running to graduation

Key milestone scripts:
- `Week5_Day3_Audio_Script.txt` - First 20-minute continuous jog
- `Week6_Day3_Audio_Script.txt` - First 25-minute continuous jog
- `Week9_Day3_FINAL_Audio_Script.txt` - Graduation day! 🎉

### 🎵 Audio Generation System
**NEW**: Automatically convert text scripts to professional audio files!

- **`generate_audio.py`** - Full-featured audio generation engine
- **`generate_c25k_audio.py`** - Easy-to-use interactive script
- **`requirements.txt`** - Python dependencies
- **`config.json.template`** - Configuration template
- **`AUDIO_SETUP_GUIDE.md`** - Complete setup and usage guide

Features:
- **ElevenLabs AI Integration**: Professional voice generation
- **Precise Timing**: Voice cues at exact workout moments
- **Multiple Voices**: Choose from various motivational voices
- **Smart Error Handling**: Graceful quota management and recovery
- **Cost Effective**: Generate all files for ~$5/month
- **Customizable**: Edit scripts for personal touches

## 🚀 Getting Started

### 1. Generate Calendar
```bash
# Install dependencies
pip install -r requirements.txt

# Generate calendar with your preferred schedule
python generate_calendar.py --start-date 2025-06-09 --workout-days "Monday,Wednesday,Friday" --workout-time "7:00 am CDT"
```

### 2. Import Calendar
1. Open Google Calendar
2. Click "+" next to "Other calendars"
3. Select "Import"
4. Upload the generated ICS file

### 3. Generate Audio Files
```bash
# Configure API key
cp config.json.template config.json
# Edit config.json with your ElevenLabs API key

# Generate audio files
python generate_c25k_audio.py
```

**📖 See `AUDIO_SETUP_GUIDE.md` for detailed instructions**

### 4. Start Training!
- Begin with Week 1 on your chosen start date
- Follow your custom calendar schedule
- Use audio coaching for perfect timing and motivation

## 📊 Program Progression

| Week | Workout Type | Duration | Description |
|------|-------------|----------|-------------|
| 1 | Intervals | 30 min | 60s jog / 90s walk |
| 2 | Intervals | 31 min | 90s jog / 2min walk |
| 3 | Intervals | 28 min | 90s + 3min jog cycles |
| 4 | Intervals | 31 min | 3min + 5min jogs |
| 5 | Mixed | 30-34 min | Building to 20min continuous |
| 6 | Mixed | 33-35 min | Building to 25min continuous |
| 7 | Continuous | 35 min | 25min continuous jogs |
| 8 | Continuous | 38 min | 28min continuous jogs |
| 9 | Continuous | 40 min | 30min continuous - GRADUATION! |

## 🏆 Major Milestones

- **Week 5, Day 3**: First 20-minute continuous jog (July 11, 2025)
- **Week 6, Day 3**: First 25-minute continuous jog (July 18, 2025)
- **Week 9, Day 3**: Graduation - 30-minute continuous jog (August 8, 2025) 🎓

## 🎯 Features

- **Precise Timing**: Every audio cue timed to the exact second
- **Progressive Motivation**: Encouragement builds with difficulty
- **Milestone Celebrations**: Special coaching for breakthrough moments
- **Complete Coverage**: 27 workouts, 14 audio scripts, full calendar integration
- **AI Voice Generation**: Professional-quality audio files with ElevenLabs
- **Multiple Voice Options**: Choose your preferred coaching voice
- **Cost-Effective**: Generate all audio files for less than $10

## 🛠️ Technical Details

- **Calendar Format**: ICS (iCalendar) - compatible with Google Calendar, Outlook, Apple Calendar
- **Time Zone**: All workouts scheduled for 12:00 PM UTC
- **Audio Scripts**: Text format ready for text-to-speech conversion
- **Audio Generation**: Python scripts using ElevenLabs API
- **Total Duration**: Ranges from 28-40 minutes depending on week

## 🎵 Audio Production

### Automated Generation (Recommended)
- Uses ElevenLabs AI for professional voice quality
- Precise timing with millisecond accuracy
- Multiple voice options (Rachel, Antoni, Bella, Josh)
- Batch processing for all 14 audio files
- Cost: ~$5 for all files

### Manual Production Tips
1. **Voice Selection**: Choose an encouraging, motivational voice
2. **Background Music**: Add upbeat music for jogging, calmer for walking
3. **Sound Effects**: Consider transition beeps between intervals
4. **Volume**: Keep music lower than voice instructions
5. **Format**: Export as MP3 for universal compatibility

### 📱 Getting Audio Files on Your Phone

Once you've generated your audio files, you'll need to get them onto your phone for workouts. Here are several effective methods:

### Cloud Storage (Recommended)
**Google Drive / iCloud / Dropbox**
1. Upload generated audio files to your preferred cloud service
2. Download the cloud app on your phone
3. Download files for offline access before workouts
4. Play directly from the cloud app or your phone's built-in music player

**Benefits**: Automatic sync, works across devices, no cable needed

### Music Streaming Services
**Spotify (Premium)**
1. Create a new playlist in Spotify Desktop app
2. Add your local audio files to the playlist ("Local Files" feature)
3. Download playlist to your phone for offline listening
4. Perfect integration with your existing music setup

**Apple Music / YouTube Music**
- Similar local file upload features available
- Check your service's "local files" or "upload" options

### Direct Transfer Methods
**USB Cable Transfer**
1. Connect phone to computer via USB
2. Copy audio files to phone's Music folder
3. Files will appear in your default music app
4. Works with iPhone (via iTunes/Finder) and Android

**AirDrop (iPhone/Mac)**
1. Select audio files on Mac
2. Right-click → Share → AirDrop
3. Send to your iPhone
4. Files save to Files app, can move to Music

### Workout-Optimized Options
**Dedicated Workout Apps**
- Upload to fitness apps that support custom audio
- Some running apps allow importing coaching tracks

**Voice Recorder Apps**
- Import into voice memo/recorder apps
- Often have better background playback during workouts
- Less likely to shuffle or interrupt with notifications

### Pro Tips for Phone Audio
- **Download for Offline**: Always download files locally before workouts
- **Airplane Mode**: Consider using airplane mode during runs to save battery and avoid interruptions
- **Volume**: Test audio levels before your first workout
- **Backup Storage**: Keep files in multiple locations in case of phone issues
- **File Names**: Keep descriptive names (e.g., "C25K_Week1_Day1.mp3") for easy selection

## 📈 Success Tips

- **Consistency**: Follow the Mon/Wed/Fri schedule religiously
- **Pace**: Focus on completing the time, not speed
- **Rest**: Take rest days seriously for recovery
- **Hydration**: Stay well-hydrated throughout the program
- **Form**: Maintain good running posture and breathing
- **Audio**: Use the generated audio files for perfect timing

## 🛠️ Troubleshooting

### Audio Generation Issues

**API Quota Exceeded**
- The script will stop gracefully when ElevenLabs credits run out
- Successfully generated files are preserved
- Add more credits to your account to continue
- Re-run generation to continue from where it left off

**Understanding Workout Audio Files**
- Audio files are **mostly silent by design** (95%+ silence is normal)
- Voice cues occur only at specific workout moments (e.g., "start jogging", "switch to walking")
- A 30-minute file may contain only 2-3 minutes of actual speech
- Long periods of silence are intentional for uninterrupted workouts

**Cost Management**
- Each full generation uses ~1000-2000 characters (~$1-2)
- Test with Week 1 first to verify your setup
- Generate files individually if needed to control costs

## 🎉 Graduation

Upon completing Week 9, Day 3, you will have officially graduated from couch to 5K runner! You'll be able to run continuously for 30 minutes - a incredible transformation in just 9 weeks.

## 📞 Program Source

Based on the proven Couch to 5K plan from [c25k.com](https://c25k.com/c25k_plan/), adapted with modern calendar integration and comprehensive audio coaching.

## 🔧 Repository Structure

```
couch-to-5k-program/
├── README.md                           # This file
├── AUDIO_SETUP_GUIDE.md               # Audio generation guide
├── generate_calendar.py                # Calendar generation script
├── requirements.txt                    # Python dependencies
├── config.json.template               # Configuration template
├── generate_audio.py                  # Full audio generation engine
├── generate_c25k_audio.py             # Easy-to-use audio generator
└── C25K_Audio_Scripts/                # Audio coaching scripts
    ├── README_Audio_Instructions.txt   # Usage instructions
    ├── Week1_Audio_Script.txt         # Week 1 coaching
    ├── Week2_Audio_Script.txt         # Week 2 coaching
    ├── ...                            # Additional weeks
    └── Week9_Day3_FINAL_Audio_Script.txt # Graduation!
```

---

**Ready to transform your life? Your journey from couch to 5K starts Monday, June 9, 2025 at 12:00 PM UTC!** 🏃‍♂️✨ 