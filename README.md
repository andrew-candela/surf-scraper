# Surf Diaries

An Alexa skill that helps me log surf sessions when I get home.

The idea here is to log my experience for a session and combine that with
the bouy, wind and tide data for that spot (or close to it) at that time.

There's also an intent that reports current conditions for the spot I request.

## Approach

"Alexa, open surf diary"
"Log an entry for {spot} at {time}"
"Waves were soft, wind roughed things up etc etc"

Alexa will collect the spot, the time and my notes.
Then I'll have to go and get the data from surfline.
I wonder if it's possible to get data in the past?

## Details

I'll use DynamoDB as the persistence layer.
The key will be the datetime that I made the log entry.
The value will be a dictionary:
    time
    spot
    rating
    notes
    conditions: weather, wave and tide
