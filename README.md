# Surf Butler

An Alexa skill that helps me log surf sessions when I get home.

The idea here is to log my experience for a session and combine that with
the buoy, wind and tide data for that spot (or close to it) at that time.

There's also an intent that reports current conditions for the spot I request.

## Approach

"Alexa, open surf butler"
"Log an entry for {spot} at {time}"
"Waves were soft, wind roughed things up etc etc"

Alexa will collect the spot, time and my notes.
Then the handler will go and collect some wind, tide and wave data.

## Details

DynamoDB is the persistence layer.
Partition key is the spot I surfed and the sort key is the timestamp.
The value will be a dictionary:
    time
    spot
    rating
    notes
    conditions: weather, wave and tide
    etc

I'm updating the lambda function configuration manually for now in the
[alexa developer console](https://developer.amazon.com/alexa/console/ask).

## ToDo

- indicate buoy positions when doing spot reports.
Currently the user can't tell which buoy the reading came from.
