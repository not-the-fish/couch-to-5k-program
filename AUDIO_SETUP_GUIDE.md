# 🎵 Audio Generation Setup Guide

This guide will help you convert your Couch to 5K text scripts into professional audio coaching files using ElevenLabs AI voices.

## 📋 Prerequisites

### 1. ElevenLabs Account
- Sign up at [elevenlabs.io](https://elevenlabs.io)
- Get your API key from your account dashboard
- **Free tier**: 10,000 characters/month (enough for ~2-3 audio files)
- **Starter plan**: $5/month for 30,000 characters (enough for all files)

### 2. System Requirements
- Python 3.8 or higher
- `ffmpeg` installed (for audio processing)

### 3. Install ffmpeg
```bash
# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## 🚀 Quick Start

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
# Copy the template
cp config.json.template config.json

# Edit config.json and add your ElevenLabs API key
```

### Step 3: Generate Audio
```bash
# Run the easy-to-use generator
python generate_c25k_audio.py
```

## 📝 Detailed Setup

### 1. Python Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv c25k_audio
source c25k_audio/bin/activate  # On Windows: c25k_audio\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Edit `config.json`:
```json
{
  "elevenlabs": {
    "api_key": "your_actual_api_key_here",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "voice_name": "Rachel (default)"
  }
}
```

**Available Voices:**
- **Rachel**: `21m00Tcm4TlvDq8ikWAM` - Clear, motivational female voice (default)
- **Antoni**: `ErXwobaYiN019PkySvjV` - Energetic male voice
- **Bella**: `EXAVITQu4vr4xnSDxMaL` - Warm female voice
- **Josh**: `TxGEqnHWrfWFTfGW9XjX` - Professional male voice

## 🎯 Usage Options

### Option 1: Simple Interactive Script
```bash
python generate_c25k_audio.py
```
Follow the prompts to:
- Generate all 14 audio files
- Test with Week 1 only
- Generate specific scripts

### Option 2: Command Line (Advanced)
```bash
# Generate all audio files
python generate_audio.py --api-key YOUR_API_KEY

# Generate single file
python generate_audio.py --api-key YOUR_API_KEY --single-file "C25K_Audio_Scripts/Week1_Audio_Script.txt"

# Use different voice
python generate_audio.py --api-key YOUR_API_KEY --voice-id "ErXwobaYiN019PkySvjV"
```

## 📊 Cost & Time Estimates

### Character Usage (Approximate)
- **Week 1-4**: ~150 characters per script
- **Week 5-6**: ~180 characters per script  
- **Week 7-9**: ~200 characters per script
- **Total**: ~1,500-2,000 characters for all files

### Time Estimates
- **Single file**: 2-3 minutes
- **All files**: 25-35 minutes
- **Processing**: ~0.5 seconds per speech segment

### ElevenLabs Pricing
- **Free**: 10,000 chars/month (6-7 audio files)
- **Starter**: $5/month, 30,000 chars (all files + extras)
- **Creator**: $11/month, 100,000 chars (multiple programs)

## 📁 Output Files

Generated audio files will be saved to `generated_audio/`:
```
generated_audio/
├── Week1_Audio_Script.mp3
├── Week2_Audio_Script.mp3
├── Week5_Day3_Audio_Script.mp3
├── Week9_Day3_FINAL_Audio_Script.mp3
└── ...
```

Each file contains:
- Precisely timed voice instructions
- Silent periods for jogging/walking
- Complete workout duration (28-40 minutes)

## 🎵 Using the Audio Files

### During Workouts
1. **Start the audio file** when you begin your warm-up
2. **Follow voice instructions** for jogging/walking intervals
3. **Audio automatically guides timing** - no need to watch a timer

### File Organization
- Import to your phone's music app
- Create "Couch to 5K" playlist
- Name files clearly: "C25K Week 1 Day 1", etc.

### Recommended Apps
- **iOS**: Apple Music, Spotify, Overcast
- **Android**: Google Play Music, Spotify, Pocket Casts

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'elevenlabs'"
```bash
pip install elevenlabs==1.2.2
```

### "ffmpeg not found"
```bash
# Install ffmpeg (see Prerequisites section)
```

### "API key invalid"
- Check your ElevenLabs account dashboard
- Ensure API key is copied correctly to `config.json`
- Verify you have available character quota

### "Audio file too quiet/loud"
```bash
# Adjust volume using ffmpeg after generation
ffmpeg -i input.mp3 -filter:a "volume=1.5" output_louder.mp3
```

### Rate Limiting Errors
- Script includes 0.5-second delays between API calls
- If errors persist, try generating files one at a time

## 🎨 Customization

### Custom Voice Instructions
Edit the script files in `C25K_Audio_Scripts/` to:
- Add personal motivation
- Include your name
- Modify pacing instructions
- Add music cues

### Background Music
After generation, you can overlay background music:
```bash
# Example with ffmpeg
ffmpeg -i workout_audio.mp3 -i background_music.mp3 -filter_complex amix=inputs=2:duration=first output.mp3
```

### Different Languages
- Modify scripts to your preferred language
- Use appropriate ElevenLabs voice for that language
- Ensure voice model supports your language

## 📞 Support

### Issues with This Script
- Check the repository README
- Verify all prerequisites are installed
- Test with a single file first

### ElevenLabs API Issues
- Check [ElevenLabs Status](https://status.elevenlabs.io/)
- Review your account quota and usage
- Consult [ElevenLabs Documentation](https://docs.elevenlabs.io/)

### Audio Quality Issues
- Try different voice models
- Adjust bitrate in `config.json`
- Consider the Creator plan for higher quality

## 🎉 Success Tips

1. **Start with Week 1** to test the system
2. **Generate a few files at a time** to manage API quota
3. **Listen to samples** before generating all files
4. **Keep scripts backed up** for future regeneration
5. **Experiment with voices** to find your favorite

---

**Ready to create your personalized Couch to 5K audio coaching experience? Start with the Quick Start section above!** 🏃‍♂️🎵 