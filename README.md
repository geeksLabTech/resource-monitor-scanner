# resource-monitor-scanner

# Requiremetns
`pip install -r requirements.txt`

# Running
running the script will log the stats to a csv, if time is not passed it will take 300s (5 min) as default recording duration, if called with negative duration it will be 
recording data until forced to stop (Ctrl+C)

`python main.py <time>`

at any time of the execution it can be stopped and there will still be a valid csv to use

# GPU and OS Support
The system theoretically supports both AMD and NVIDIA GPUs, and also multiple GPUs but it has only been tested in a single NVIDIA GPU, in an ArchLinux system.

# Contributions
All contributions are wellcome, even testing in different hardware configurations.