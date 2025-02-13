# Flow Log Parser
This Python script processes flow logs and matches them with a lookup table to generate tag counts and port/protocol combination counts. The results are saved to an output file with a timestamped filename.
## Features
- Parses flow logs to extract destination ports and protocols.
- Matches extracted data with a lookup table to assign tags.
- Counts occurrences of each tag and port/protocol combination.
- Generates an output file with detailed counts.
## Requirements
Python 3.9 or higher (for functools.cache).
## Required Python modules:
```text
collections
csv
os
socket
argparse
functools
datetime
```
## Installation
Clone this repository or copy the script into your project directory.
Ensure you have Python installed (version 3.9+).
Install any missing dependencies using pip (if necessary).

## Usage
Run the script from the command line with the following arguments:
```bash
python3 flow_log_parser.py --flow_log_file <FLOW_LOG_FILE> --lookup_table_csv <LOOKUP_TABLE_CSV> --output_path <OUTPUT_DIRECTORY>
```

## Input File Formats
### Flow Logs File:
The flow logs file should contain space-separated values where:
The 7th column represents the destination port.
The 8th column represents the protocol number.
### Example:
```text
log1 log2 log3 log4 log5 log6 80 6
log1 log2 log3 log4 log5 log6 443 17
```
### Lookup Table CSV:
The lookup table CSV should have the following columns:
dstport: Destination port.
protocol: Protocol name (e.g., TCP, UDP).
tag: Tag associated with the port/protocol combination.
### Example:
```text
dstport,protocol,tag
80,tcp,web
443,tcp,secure_web
53,udp,dns
```
## Output
The script generates an output file in the specified directory with a name like output_YYYYMMDD_HHMMSS.txt. The file contains:
Tag Counts: A summary of tag occurrences.
```text
Tag Counts:
Tag,Count
web,10
secure_web,5
untagged,2
```
Port/Protocol Combination Counts: A breakdown of port/protocol combinations and their counts.
```text
Port/Protocol Combination Counts:
Port,Protocol,Count
80,tcp,10
443,tcp,5
```
## Functions Overview
### init_lookup_data(lookup_table_csv)
Parses the lookup table CSV file and returns a dictionary mapping <port>,<protocol> combinations to their tags.
### get_protocol_name(protocol_number)
Returns the protocol name (e.g., "tcp", "udp") for a given protocol number using the socket module.
### parse_flow_logs(flow_log_file, lookup_table_csv, output_path=None)
Parses flow logs, matches them with the lookup table data, and generates tag and port/protocol counts.
### generate_output_file(output_path, tag_counts, port_protocol_count)
Creates an output file in the specified directory containing tag counts and port/protocol combination counts.
### main()
Handles command-line arguments and orchestrates the parsing process.
### Notes
Ensure that both input files (flow_log_file and lookup_table_csv) are formatted correctly to avoid errors.
The script uses caching (functools.cache) for efficient protocol name lookups.
## License
This project is licensed under the MIT License. Feel free to use and modify it as needed. This README provides clear instructions on what the script does, how to use it, and what input/output formats are expected. Let me know if you'd like further refinements!
