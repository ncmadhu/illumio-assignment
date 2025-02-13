"""Entry point for flow log parser."""
import collections
import csv
import os
import socket
import argparse
from functools import cache
from datetime import datetime


def init_lookup_data(lookup_table_csv):
    """Parses lookup table data and returns a dictionary containing tag information."""
    tag_info = {}
    with open(lookup_table_csv, "r", encoding='utf-8') as lookup_table:
        lookup_data = csv.DictReader(lookup_table)
        for port_proto_tag in lookup_data:
            key = f"{port_proto_tag['dstport']},{port_proto_tag['protocol'].lower()}"
            tag_info[key] = port_proto_tag['tag']
    return tag_info


@cache
def get_protocol_name(protocol_number):
    """Returns protocol name for a given protocol number"""
    for name in dir(socket):
        if name.startswith("IPPROTO_") and getattr(socket, name) == protocol_number:
            return name[8:].lower()  # Remove the "IPPROTO_" prefix
    return None


def parse_flow_logs(flow_log_file, lookup_table_csv, output_path=None):
    """Parses flow logs and matches with lookup table data to produce tag and port/protocol counts."""
    tag_info = init_lookup_data(lookup_table_csv)
    tag_counts = collections.defaultdict(int)
    port_protocol_count = collections.defaultdict(int)
    with open(flow_log_file, 'r') as flow_logs:
        for log in flow_logs:
            log_data = log.split(' ')
            # Only process version 2 flow logs
            if log_data[0] == '2':
                dst_port = log_data[6]
                protocol = get_protocol_name(int(log_data[7]))
                key = f'{dst_port},{protocol}'
                if key in tag_info:
                    tag_counts[tag_info[key]] += 1
                else:
                    tag_counts['untagged'] += 1
                port_protocol_count[key] += 1
    if output_path:
        generate_output_file(output_path, tag_counts, port_protocol_count)
    return tag_counts, port_protocol_count


def generate_output_file(output_path, tag_counts, port_protocol_count):
    """Generates the output file containing tag and port/protocol counts"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = os.path.join(output_path, f"output_{timestamp}.txt" )
    with open(file_name, 'w') as file:
        file.write('Tag Counts:\n')
        file.write('Tag,Count\n')
        for key, value in tag_counts.items():
            file.write(f'{key},{value}\n')
        file.write('Port/Protocol Combination Counts:\n')
        file.write('Port,Protocol,Count \n')
        for key, value in port_protocol_count.items():
            file.write(f'{key},{value}\n')


def main():
    """Parse command line, run the main program."""
    parser = argparse.ArgumentParser(
        description='Input values to flow log parser',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--flow_log_file',
                        type=str,
                        required=True,
                        help='Enter the absolute file path containing the flow logs')

    parser.add_argument('--lookup_table_csv',
                        type=str,
                        required=True,
                        help='Enter the absolute file path containing the lookup table data')

    parser.add_argument('--output_path',
                        type=str,
                        required=True,
                        help='Enter the directory path to store the output data')

    args = parser.parse_args()
    parse_flow_logs(args.flow_log_file, args.lookup_table_csv, args.output_path)


if __name__ == "__main__":
    main()