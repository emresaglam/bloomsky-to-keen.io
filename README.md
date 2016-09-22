# What is this?
This is a python script to get a subset of data that the bloomsky API provides and push them to keen.io. You can use it to store outside temperature, humidity, etc in keen.io to analyze it in the future.

# Requirements

Only python requirement is to install the keen.io library

`pip install keen`

You also need to create a file called config.json and put it in the same directory as getBloomSky.py file.

And last but not least, you need a keen.io account and a project.

# config.json format

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
