# What is this?
This is a python script to get a subset of data that the bloomsky API provides and push them to keen.io. You can use it to store outside temperature, humidity, etc in keen.io to analyze it in the future.

# Requirements

The required libraries are in the requirements.txt file.

You also need to create a file called config.json and put it in the same directory as getBloomSky.py file.

And last but not least, you need a keen.io account and a project.

# config.json format

You can also find an example config.json.example file in the repo

```
{
  "bloomsky": {
    "api_key": "YOUR BLOOMSKY API KEY HERE"
  },
  "keen.io": {
    "write_key": "YOUR KEEN.IO WRITE KEY HERE",
    "project_id": "YOUR KEEN.IO PROJECT ID HERE"
  },
  "agent_name": "WHATEVER YOU WANT TO NAME YOUR BLOOMSKY"
}
```

That's it! ;)

# FAQ

- Wait what? Why are you converting units? Don't you know that bloomsky has an SI API?

I do know, but the SI unit returns Pressure as an integer, which ends up plotting the Pressure graphs as increments of 1. That doesn't look pretty :(

- Why is this written like a batch file?

I use this to pull data every 5 mins with a cronjob. It just works! :) 
