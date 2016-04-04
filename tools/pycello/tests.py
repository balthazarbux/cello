#!/usr/bin/env python
"""Tests for UCF Writer methods."""

import unittest

from ucf_writer import gates_from_csv, parts_from_csv, gate_parts_from_csv


class TestUCFWriterMethods(unittest.TestCase):
    """TestCase for UCF writer methods."""

    def test_gates_from_csv_returns_expected_value(self):
        """Test that gates_from_csv returns expected value."""
        expected_gates = [
            {
                'collection': 'gates',
                'regulator': 'foo',
                'group_name': 'foo',
                'gate_name': 'bar',
                'gate_type': 'baz',
                'system': 'TetR',
                'color_hexcode': '000000'
            },
            {
                'collection': 'gates',
                'regulator': 'foo2',
                'group_name': 'foo2',
                'gate_name': 'bar2',
                'gate_type': 'baz2',
                'system': 'TetR',
                'color_hexcode': '000000'
            },
        ]

        table = [
            {
                'asdf': 'foo',
                'qwer': 'bar',
                'zxcv': 'baz'
            },
            {
                'asdf': 'foo2',
                'qwer': 'bar2',
                'zxcv': 'baz2'
            }
        ]

        header_map = {
            'cds': 'asdf',
            'name': 'qwer',
            'type': 'zxcv'
        }

        gates = gates_from_csv(table, header_map)

        self.assertEqual(gates, expected_gates)

    def test_parts_from_csv_returns_expected_value(self):
        """Testparts_from_csv returns the expected value."""
        expected_parts = [
            {
                'collection': 'parts',
                'type': 'ribozyme',
                'name': 'foo',
                'dnasequence': '0101'
            },
            {
                'collection': 'parts',
                'type': 'rbs',
                'name': 'foo2',
                'dnasequence': '01012'
            },
            {
                'collection': 'parts',
                'type': 'cds',
                'name': 'foo3',
                'dnasequence': '01013'
            },
            {
                'collection': 'parts',
                'type': 'terminator',
                'name': 'foo4',
                'dnasequence': '01014'
            },
            {
                'collection': 'parts',
                'type': 'promoter',
                'name': 'foo5',
                'dnasequence': '01015'
            },
        ]

        table = [
            {
                'asdf': 'foo',
                'zxcv': '0101',
                'asdf2': 'foo2',
                'zxcv2': '01012',
                'asdf3': 'foo3',
                'zxcv3': '01013',
                'asdf4': 'foo4',
                'zxcv4': '01014',
                'asdf5': 'foo5',
                'zxcv5': '01015'
            }
        ]

        header_map = {
            'ribozyme': 'asdf',
            'ribozymeDNA': 'zxcv',
            'rbs': 'asdf2',
            'rbsDNA': 'zxcv2',
            'cds': 'asdf3',
            'cdsDNA': 'zxcv3',
            'terminator': 'asdf4',
            'terminatorDNA': 'zxcv4',
            'promoter': 'asdf5',
            'promoterDNA': 'zxcv5'
        }

        parts = parts_from_csv(table, header_map)

        self.assertEqual(parts, expected_parts)

    def test_gate_parts_from_csv_returns_expected_value(self):
        """Test gate_parts_from_csv returns the expected value."""
        expected_gate_parts = [
            {
                'collection': 'gate_parts',
                'gate_name': 'zxcvzxcv',
                'expression_cassettes': [
                    {
                        'maps_to_variable': 'x',
                        'cassette_parts': [
                            '2',
                            '3',
                            '4',
                            '5'
                        ]
                    }
                ],
                'promoter': '6'
            },
            {
                'collection': 'gate_parts',
                'gate_name': 'ppppp',
                'expression_cassettes': [
                    {
                        'maps_to_variable': 'x',
                        'cassette_parts': [
                            '0',
                            '00',
                            '000',
                            '0000'
                        ]
                    }
                ],
                'promoter': '00000'
            }
        ]

        table = [
            {
                'foo': 'zxcvzxcv',
                'asdf': '2',
                'q': '3',
                'w': '4',
                'e': '5',
                'r': '6'
            },
            {
                'foo': 'ppppp',
                'asdf': '0',
                'q': '00',
                'w': '000',
                'e': '0000',
                'r': '00000'
            }
        ]

        header_map = {
            'name': 'foo',
            'ribozyme': 'asdf',
            'rbs': 'q',
            'cds': 'w',
            'terminator': 'e',
            'promoter': 'r'
        }

        parts = gate_parts_from_csv(table, header_map)
        self.assertEqual(parts, expected_gate_parts)

if __name__ == '__main__':
    unittest.main()
