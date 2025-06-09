#!/usr/bin/env python3
"""
Couch to 5K Audio Generator
Converts text scripts with timestamps into audio files using ElevenLabs API
"""

import os
import re
import json
import time
from pathlib import Path
from typing import List, Tuple, Dict
import requests
from elevenlabs import client, save
from pydub import AudioSegment
from pydub.silence import AudioSegment as silence
import argparse

class C25KAudioGenerator:
    def __init__(self, api_key: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        """
        Initialize the audio generator
        
        Args:
            api_key: ElevenLabs API key
            voice_id: ElevenLabs voice ID (default: Rachel)
        """
        self.api_key = api_key
        self.voice_id = voice_id
        self.client = client
        self.client.set_api_key(api_key)
        
        # Create output directory
        self.output_dir = Path("generated_audio")
        self.output_dir.mkdir(exist_ok=True)
    
    def parse_script_file(self, file_path: str) -> List[Tuple[float, str]]:
        """
        Parse a script file and extract timestamps with text
        
        Args:
            file_path: Path to the script file
            
        Returns:
            List of (timestamp_seconds, text) tuples
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Pattern to match timestamps like "5:00 - " or "10:30 - "
        timestamp_pattern = r'(\d{1,2}):(\d{2})\s*-\s*"([^"]+)"'
        
        matches = re.findall(timestamp_pattern, content, re.MULTILINE | re.DOTALL)
        
        timestamps = []
        for match in matches:
            minutes, seconds, text = match
            total_seconds = int(minutes) * 60 + int(seconds)
            # Clean up the text
            clean_text = text.strip().replace('\n', ' ').replace('  ', ' ')
            timestamps.append((total_seconds, clean_text))
        
        return sorted(timestamps, key=lambda x: x[0])
    
    def generate_speech_segment(self, text: str) -> AudioSegment:
        """
        Generate speech audio for a text segment using ElevenLabs
        
        Args:
            text: Text to convert to speech
            
        Returns:
            AudioSegment containing the generated speech
        """
        try:
            # Generate audio using ElevenLabs
            audio_data = self.client.generate(
                text=text,
                voice=self.voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Save to temporary file and load as AudioSegment
            temp_file = "temp_speech.mp3"
            save(audio_data, temp_file)
            
            audio_segment = AudioSegment.from_mp3(temp_file)
            
            # Clean up temp file
            os.remove(temp_file)
            
            return audio_segment
            
        except Exception as e:
            print(f"Error generating speech for text: {text[:50]}...")
            print(f"Error: {e}")
            return AudioSegment.silent(duration=1000)  # 1 second of silence as fallback
    
    def create_timed_audio(self, timestamps: List[Tuple[float, str]], total_duration: int) -> AudioSegment:
        """
        Create a complete audio file with speech at specified timestamps
        
        Args:
            timestamps: List of (timestamp_seconds, text) tuples
            total_duration: Total duration of the workout in seconds
            
        Returns:
            Complete AudioSegment with timed speech
        """
        # Start with silence for the full duration
        final_audio = AudioSegment.silent(duration=total_duration * 1000)  # Convert to milliseconds
        
        print(f"Creating audio with {len(timestamps)} speech segments over {total_duration} seconds...")
        
        for i, (timestamp, text) in enumerate(timestamps):
            print(f"  Processing {i+1}/{len(timestamps)}: {timestamp}s - {text[:50]}...")
            
            # Generate speech for this text
            speech_audio = self.generate_speech_segment(text)
            
            # Calculate position in milliseconds
            position_ms = int(timestamp * 1000)
            
            # Overlay the speech at the specified timestamp
            if position_ms < len(final_audio):
                final_audio = final_audio.overlay(speech_audio, position=position_ms)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        return final_audio
    
    def get_workout_duration(self, script_content: str) -> int:
        """
        Extract total duration from script content
        
        Args:
            script_content: Content of the script file
            
        Returns:
            Duration in seconds
        """
        # Look for duration information in the header
        duration_patterns = [
            r'Total Duration:\s*(\d+)\s*minutes',
            r'Duration:\s*(\d+)\s*minutes',
            r'(\d+)\s*minutes\s*total'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, script_content, re.IGNORECASE)
            if match:
                return int(match.group(1)) * 60
        
        # Default fallback - estimate from last timestamp
        timestamps = self.parse_script_file("temp_script.txt")
        if timestamps:
            return int(timestamps[-1][0]) + 300  # Add 5 minutes buffer
        
        return 2400  # 40 minutes default
    
    def process_script_file(self, script_file: str) -> str:
        """
        Process a single script file and generate audio
        
        Args:
            script_file: Path to the script file
            
        Returns:
            Path to the generated audio file
        """
        print(f"\n=== Processing {script_file} ===")
        
        # Parse the script
        timestamps = self.parse_script_file(script_file)
        
        if not timestamps:
            print(f"No timestamps found in {script_file}")
            return None
        
        print(f"Found {len(timestamps)} speech segments")
        
        # Get duration
        with open(script_file, 'r', encoding='utf-8') as file:
            content = file.read()
        duration = self.get_workout_duration(content)
        
        # Generate the audio
        audio = self.create_timed_audio(timestamps, duration)
        
        # Generate output filename
        script_name = Path(script_file).stem
        output_file = self.output_dir / f"{script_name}.mp3"
        
        # Export the audio
        print(f"Exporting to {output_file}...")
        audio.export(str(output_file), format="mp3", bitrate="128k")
        
        print(f"✅ Generated: {output_file}")
        return str(output_file)
    
    def process_all_scripts(self, scripts_dir: str = "C25K_Audio_Scripts"):
        """
        Process all script files in the directory
        
        Args:
            scripts_dir: Directory containing script files
        """
        scripts_dir = Path(scripts_dir)
        
        # Find all script files (excluding README)
        script_files = []
        for file in scripts_dir.glob("*.txt"):
            if not file.name.startswith("README"):
                script_files.append(file)
        
        # Sort files naturally
        script_files.sort(key=lambda x: x.name)
        
        print(f"Found {len(script_files)} script files to process")
        
        generated_files = []
        
        for script_file in script_files:
            try:
                output_file = self.process_script_file(str(script_file))
                if output_file:
                    generated_files.append(output_file)
            except Exception as e:
                print(f"❌ Error processing {script_file}: {e}")
                continue
        
        print(f"\n🎉 Audio generation complete!")
        print(f"Generated {len(generated_files)} audio files:")
        for file in generated_files:
            print(f"  - {file}")
        
        return generated_files

def main():
    parser = argparse.ArgumentParser(description="Generate Couch to 5K audio files using ElevenLabs")
    parser.add_argument("--api-key", required=True, help="ElevenLabs API key")
    parser.add_argument("--voice-id", default="21m00Tcm4TlvDq8ikWAM", help="ElevenLabs voice ID (default: Rachel)")
    parser.add_argument("--scripts-dir", default="C25K_Audio_Scripts", help="Directory containing script files")
    parser.add_argument("--single-file", help="Process only a single script file")
    
    args = parser.parse_args()
    
    # Initialize the generator
    generator = C25KAudioGenerator(args.api_key, args.voice_id)
    
    if args.single_file:
        # Process single file
        generator.process_script_file(args.single_file)
    else:
        # Process all files
        generator.process_all_scripts(args.scripts_dir)

if __name__ == "__main__":
    main() 