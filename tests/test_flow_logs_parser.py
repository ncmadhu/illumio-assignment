"""Tests for the flow logs parser."""

import unittest
import src.main as flow_log_parser


class TestFlowLogsParser(unittest.TestCase):

    def test_a_get_protocol_name(self):
        """Protocol number to name uniqueness validation"""
        self.assertEqual('tcp', flow_log_parser.get_protocol_name(6))

    def test_b_get_protocol_name_(self):
        """Protocol number to name uniqueness validation"""
        self.assertNotEqual('tcp', flow_log_parser.get_protocol_name(7))

    def test_c_init_lookup_table(self):
        """Same tag for multiple port/protocol combination"""
        tag_info = flow_log_parser.init_lookup_data("sample_lookup_table.csv")
        self.assertEqual('sv_P1', tag_info['25,tcp'])

    def test_d_init_lookup_table(self):
        """Same tag for multiple port/protocol combination"""
        tag_info = flow_log_parser.init_lookup_data("sample_lookup_table.csv")
        self.assertEqual('sv_P1', tag_info['23,tcp'])

    def test_e_init_lookup_table(self):
        """Negative test for port/protocol combination"""
        tag_info = flow_log_parser.init_lookup_data("sample_lookup_table.csv")
        self.assertNotEqual('sv_P1', tag_info['68,udp'])

    def test_f_tag_count_validation(self):
        """validates the tag and port/protocol count combination."""
        tag_counts, port_protocol_count = flow_log_parser.parse_flow_logs("sample_flow_logs.txt",
                                                                          "sample_lookup_table.csv")
        self.assertEqual(3, tag_counts['email'])
        self.assertEqual(1, port_protocol_count['80,tcp'])
        self.assertEqual(2, tag_counts['sv_P1'])
        self.assertEqual(1, port_protocol_count['25,tcp'])
        self.assertEqual(1, port_protocol_count['23,tcp'])
        self.assertEqual(8, tag_counts['untagged'])


