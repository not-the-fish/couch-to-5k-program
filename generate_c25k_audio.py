#!/usr/bin/env python3
"""
Simple Couch to 5K Audio Generator
Easy-to-use script for generating workout audio files
"""

import os
import json
import sys
from pathlib import Path

# Try to import the main generator
try:
    from generate_audio import C25KAudioGenerator
except ImportError:
    print("❌ Error: Could not import generate_audio module")
    print("Make sure you're running this from the project directory")
    sys.exit(1)

def load_config():
    """Load configuration from config.json"""
    config_file = Path("config.json")
    
    if not config_file.exists():
        print("❌ config.json not found!")
        print("Please copy config.json.template to config.json and add your API key")
        print("\n📝 Steps:")
        print("1. cp config.json.template config.json")
        print("2. Edit config.json and add your ElevenLabs API key")
        print("3. Run this script again")
        return None
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Error loading config.json: {e}")
        return None

def main():
    print("🎵 Couch to 5K Audio Generator")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    # Check API key
    api_key = config["elevenlabs"]["api_key"]
    if api_key == "YOUR_ELEVENLABS_API_KEY_HERE":
        print("❌ Please set your ElevenLabs API key in config.json")
        return
    
    # Get voice settings
    voice_id = config["elevenlabs"]["voice_id"]
    voice_name = config["elevenlabs"]["voice_name"]
    
    print(f"🎤 Using voice: {voice_name}")
    print(f"📁 Scripts directory: C25K_Audio_Scripts")
    print(f"💾 Output directory: {config['audio_settings']['output_directory']}")
    
    # Ask user what to generate
    print("\n🎯 What would you like to generate?")
    print("1. All audio files (14 files, ~30-45 minutes)")
    print("2. Just Week 1 (test single file)")
    print("3. Specific week/script")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    # Initialize generator
    try:
        generator = C25KAudioGenerator(api_key, voice_id)
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return
    
    if choice == "1":
        # Generate all files
        print("\n🚀 Generating all audio files...")
        print("⚠️  This will take 20-30 minutes and use ~1000-2000 ElevenLabs characters")
        confirm = input("Continue? (y/N): ").strip().lower()
        
        if confirm == 'y':
            generator.process_all_scripts()
        else:
            print("Cancelled.")
    
    elif choice == "2":
        # Test with Week 1
        print("\n🧪 Generating Week 1 audio file (test)...")
        script_file = "C25K_Audio_Scripts/Week1_Audio_Script.txt"
        
        if Path(script_file).exists():
            generator.process_script_file(script_file)
        else:
            print(f"❌ Script file not found: {script_file}")
    
    elif choice == "3":
        # Specific file
        print("\n📋 Available scripts:")
        scripts_dir = Path("C25K_Audio_Scripts")
        script_files = []
        
        for i, file in enumerate(sorted(scripts_dir.glob("*.txt")), 1):
            if not file.name.startswith("README"):
                script_files.append(file)
                print(f"  {i}. {file.name}")
        
        try:
            file_choice = int(input(f"\nEnter file number (1-{len(script_files)}): ")) - 1
            if 0 <= file_choice < len(script_files):
                selected_file = script_files[file_choice]
                print(f"\n🎵 Generating: {selected_file.name}")
                generator.process_script_file(str(selected_file))
            else:
                print("❌ Invalid file number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 