from datetime import datetime, timedelta, time
from icalendar import Calendar, Event
import pytz
import argparse
from typing import List, Tuple
import re

# Define the workout program
WORKOUTS = [
    # Week 1
    {
        "description": "Brisk five-minute warmup walk. Then alternate 60 seconds of jogging and 90 seconds of walking for a total of 20 minutes.",
        "duration": 60  # minutes
    },
    {
        "description": "Brisk five-minute warmup walk. Then alternate 60 seconds of jogging and 90 seconds of walking for a total of 20 minutes.",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk. Then alternate 60 seconds of jogging and 90 seconds of walking for a total of 20 minutes.",
        "duration": 60
    },
    # Week 2
    {
        "description": "Brisk five-minute warmup walk. Then alternate 90 seconds of jogging and two minutes of walking for a total of 20 minutes.",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk. Then alternate 90 seconds of jogging and two minutes of walking for a total of 20 minutes.",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk. Then alternate 90 seconds of jogging and two minutes of walking for a total of 20 minutes.",
        "duration": 60
    },
    # Week 3
    {
        "description": "Brisk five-minute warmup walk, then do two repetitions of the following: Jog 90 Seconds, Walk 90 Seconds, Jog 3 Minutes, Walk 3 Minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then do two repetitions of the following: Jog 90 Seconds, Walk 90 Seconds, Jog 3 Minutes, Walk 3 Minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then do two repetitions of the following: Jog 90 Seconds, Walk 90 Seconds, Jog 3 Minutes, Walk 3 Minutes",
        "duration": 60
    },
    # Week 4
    {
        "description": "Brisk five-minute warmup walk, then: Jog 3 minutes, Walk 90 seconds, Jog 5 minutes, Walk 2.5 minutes, Jog 3 minutes, Walk 90 seconds, Jog 5 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then: Jog 3 minutes, Walk 90 seconds, Jog 5 minutes, Walk 2.5 minutes, Jog 3 minutes, Walk 90 seconds, Jog 5 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then: Jog 3 minutes, Walk 90 seconds, Jog 5 minutes, Walk 2.5 minutes, Jog 3 minutes, Walk 90 seconds, Jog 5 minutes",
        "duration": 60
    },
    # Week 5
    {
        "description": "Brisk five-minute warmup walk, then: Jog 5 minutes, Walk 3 minutes, Jog 5 minutes, Walk 3 minutes, Jog 5 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then: Jog 8 minutes, Walk 5 minutes, Jog 8 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog for 20 minutes with no walking.",
        "duration": 60
    },
    # Week 6
    {
        "description": "Brisk five-minute warmup walk, then: Jog 5 minutes, Walk 3 minutes, Jog 8 minutes, Walk 3 minutes, Jog 5 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then: Jog 10 minutes, Walk 3 minutes, Jog 10 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog 25 minutes with no walking.",
        "duration": 60
    },
    # Week 7
    {
        "description": "Brisk five-minute warmup walk, then jog 25 minutes.",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog 25 minutes.",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog 25 minutes.",
        "duration": 60
    },
    # Week 8
    {
        "description": "Brisk five-minute warmup walk, then jog 28 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog 28 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog 28 minutes",
        "duration": 60
    },
    # Week 9
    {
        "description": "Brisk five-minute warmup walk, then jog 30 minutes",
        "duration": 60
    },
    {
        "description": "Brisk five-minute warmup walk, then jog 30 minutes",
        "duration": 60
    },
    {
        "description": "The final workout! Congratulations! Brisk five-minute warmup walk, then jog 30 minutes",
        "duration": 60
    }
]

def parse_time_and_timezone(time_str: str) -> Tuple[time, pytz.timezone]:
    """Parse time string in format 'HH:MM am/pm TIMEZONE' or 'HH am/pm TIMEZONE'"""
    # Common timezone abbreviations
    timezone_map = {
        'EST': 'America/New_York',
        'EDT': 'America/New_York',
        'CST': 'America/Chicago',
        'CDT': 'America/Chicago',
        'MST': 'America/Denver',
        'MDT': 'America/Denver',
        'PST': 'America/Los_Angeles',
        'PDT': 'America/Los_Angeles',
        'UTC': 'UTC',
        'GMT': 'UTC'
    }
    
    # Normalize the input string
    time_str = time_str.strip().lower()
    
    # Try different time formats
    formats = [
        r'(\d{1,2})(?::(\d{2}))?\s+(am|pm)\s+([a-z]{3,4})',  # 7:00 am cdt
        r'(\d{1,2})(?::(\d{2}))?(am|pm)\s+([a-z]{3,4})',     # 7:00am cdt
        r'(\d{1,2})\s+(am|pm)\s+([a-z]{3,4})'                # 7 am cdt
    ]
    
    match = None
    for pattern in formats:
        match = re.match(pattern, time_str)
        if match:
            break
    
    if not match:
        raise ValueError(
            "Invalid time format. Please use one of these formats:\n"
            "- '7:00 am CDT'\n"
            "- '7:00am CDT'\n"
            "- '7 am CDT'"
        )
    
    # Extract components
    if len(match.groups()) == 4:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        am_pm = match.group(3)
        tz_abbr = match.group(4).upper()  # Convert timezone to uppercase for lookup
    else:  # 3 groups for the simple format
        hour = int(match.group(1))
        minute = 0
        am_pm = match.group(2)
        tz_abbr = match.group(3).upper()  # Convert timezone to uppercase for lookup
    
    # Convert to 24-hour format
    if am_pm == 'pm' and hour != 12:
        hour += 12
    elif am_pm == 'am' and hour == 12:
        hour = 0
    
    # Get timezone
    if tz_abbr not in timezone_map:
        raise ValueError(
            f"Unsupported timezone: {tz_abbr}\n"
            "Supported timezones are: EST, EDT, CST, CDT, MST, MDT, PST, PDT, UTC, GMT"
        )
    
    # Create time object
    time_obj = time(hour, minute)
    return time_obj, pytz.timezone(timezone_map[tz_abbr])

def parse_workout_days(days_str: str) -> List[int]:
    """Convert comma-separated days to list of weekday numbers (0=Monday, 6=Sunday)"""
    day_map = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }
    
    days = [day.strip().lower() for day in days_str.split(',')]
    return [day_map[day] for day in days]

def generate_calendar(start_date: datetime, workout_days: List[int], workout_time: time, timezone: pytz.timezone, output_file: str):
    cal = Calendar()
    cal.add('prodid', '-//Couch to 5K Calendar//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')

    # Convert start_date to the specified timezone
    start_date = timezone.localize(start_date.replace(
        hour=workout_time.hour,
        minute=workout_time.minute,
        second=0,
        microsecond=0
    ))
    
    current_date = start_date
    workout_index = 0
    
    while workout_index < len(WORKOUTS):
        # Skip to next workout day
        while current_date.weekday() not in workout_days:
            current_date += timedelta(days=1)
        
        workout = WORKOUTS[workout_index]
        week_num = workout_index // 3 + 1
        day_num = workout_index % 3 + 1
        
        event = Event()
        event.add('summary', f'C25K Week {week_num} Day {day_num}')
        if workout_index == len(WORKOUTS) - 1:
            event['summary'] += ' - FINAL WORKOUT! 🎉'
            
        event.add('description', workout['description'])
        event.add('dtstart', current_date)
        event.add('dtend', current_date + timedelta(minutes=workout['duration']))
        event.add('status', 'CONFIRMED')
        event['uid'] = f'c25k-w{week_num}d{day_num}@calendar'
        
        cal.add_component(event)
        
        # Move to next day
        current_date += timedelta(days=1)
        workout_index += 1

    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())

def main():
    parser = argparse.ArgumentParser(description='Generate Couch to 5K calendar')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--workout-days', required=True, help='Comma-separated workout days (e.g., "Monday,Wednesday,Friday")')
    parser.add_argument('--workout-time', required=True, 
                       help='Workout time and timezone (e.g., "7:00 am CDT", "7:00am CDT", or "7 am CDT")')
    parser.add_argument('--output', default='couch_to_5k_calendar.ics', help='Output ICS file path')
    
    args = parser.parse_args()
    
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        workout_days = parse_workout_days(args.workout_days)
        workout_time, timezone = parse_time_and_timezone(args.workout_time)
        
        if len(workout_days) != 3:
            print("Error: Exactly 3 workout days must be specified")
            return
            
        generate_calendar(start_date, workout_days, workout_time, timezone, args.output)
        print(f"Calendar generated successfully: {args.output}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 