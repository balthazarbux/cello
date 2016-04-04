import unittest

from ucf_writer import gates_from_csv


class TestGatesFromCSV(unittest.TestCase):
    def test_method_returns_expected_value(self):
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

if __name__ == '__main__':
    unittest.main()
