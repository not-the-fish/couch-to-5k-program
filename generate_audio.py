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
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import argparse

class QuotaExceededException(Exception):
    """Raised when API quota is exceeded"""
    pass

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
        self.client = ElevenLabs(api_key=api_key)
        self.quota_exceeded = False
        
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
            
        Raises:
            QuotaExceededException: When API quota is exceeded
        """
        if self.quota_exceeded:
            raise QuotaExceededException("API quota previously exceeded")
            
        try:
            # Generate audio using ElevenLabs
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_monolingual_v1"
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)
            
            # Save to temporary file and load as AudioSegment
            temp_file = "temp_speech.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_bytes)
            
            audio_segment = AudioSegment.from_mp3(temp_file)
            
            # Clean up temp file
            os.remove(temp_file)
            
            return audio_segment
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ Error generating speech for text: {text[:50]}...")
            print(f"Error: {e}")
            
            # Check if this is a quota exceeded error
            if "quota_exceeded" in error_str or "exceeds your quota" in error_str:
                self.quota_exceeded = True
                print("🚨 API quota exceeded! Stopping audio generation.")
                raise QuotaExceededException(f"ElevenLabs API quota exceeded: {e}")
            
            # For other errors, return silence as fallback
            print("⚠️  Using silence as fallback for this segment")
            return AudioSegment.silent(duration=1000)  # 1 second of silence as fallback
    
    def create_timed_audio(self, timestamps: List[Tuple[float, str]], total_duration: int) -> AudioSegment:
        """
        Create a complete audio file with speech at specified timestamps
        
        Args:
            timestamps: List of (timestamp_seconds, text) tuples
            total_duration: Total duration of the workout in seconds
            
        Returns:
            Complete AudioSegment with timed speech
            
        Raises:
            QuotaExceededException: When API quota is exceeded
        """
        # Start with silence for the full duration
        final_audio = AudioSegment.silent(duration=total_duration * 1000)  # Convert to milliseconds
        
        print(f"Creating audio with {len(timestamps)} speech segments over {total_duration} seconds...")
        
        for i, (timestamp, text) in enumerate(timestamps):
            print(f"  Processing {i+1}/{len(timestamps)}: {timestamp}s - {text[:50]}...")
            
            try:
                # Generate speech for this text
                speech_audio = self.generate_speech_segment(text)
                
                # Calculate position in milliseconds
                position_ms = int(timestamp * 1000)
                
                # Overlay the speech at the specified timestamp
                if position_ms < len(final_audio):
                    final_audio = final_audio.overlay(speech_audio, position=position_ms)
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except QuotaExceededException:
                # Re-raise quota exceeded to stop processing
                raise
        
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
            Path to the generated audio file, or None if failed
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
        
        try:
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
            
        except QuotaExceededException as e:
            print(f"❌ Cannot generate {script_file}: {e}")
            print("💡 Tip: Add more credits to your ElevenLabs account to continue")
            return None
    
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
        failed_files = []
        
        for script_file in script_files:
            try:
                output_file = self.process_script_file(str(script_file))
                if output_file:
                    generated_files.append(output_file)
                else:
                    failed_files.append(str(script_file))
                    
                # If quota exceeded, stop processing remaining files
                if self.quota_exceeded:
                    remaining_files = script_files[script_files.index(script_file) + 1:]
                    if remaining_files:
                        print(f"\n⚠️  Skipping {len(remaining_files)} remaining files due to quota exceeded:")
                        for remaining_file in remaining_files:
                            print(f"  - {remaining_file.name}")
                            failed_files.append(str(remaining_file))
                    break
                    
            except Exception as e:
                print(f"❌ Error processing {script_file}: {e}")
                failed_files.append(str(script_file))
                continue
        
        # Final summary
        print(f"\n🎉 Audio generation summary:")
        print(f"✅ Successfully generated: {len(generated_files)} files")
        
        if generated_files:
            print("Generated files:")
            for file in generated_files:
                print(f"  - {file}")
        
        if failed_files:
            print(f"\n❌ Failed to generate: {len(failed_files)} files")
            print("Failed files:")
            for file in failed_files:
                print(f"  - {Path(file).name}")
                
        if self.quota_exceeded:
            print(f"\n💰 API quota exceeded during processing.")
            print(f"💡 Add more credits to your ElevenLabs account to generate the remaining {len(failed_files)} files.")
        
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