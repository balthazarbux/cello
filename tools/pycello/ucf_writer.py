#!/usr/bin/env python
import csv
import json
import sys


def gates_from_csv(table, header_map):
    return map(lambda row: {
        'collection': 'gates',
        'regulator': row[header_map['cds']],
        'group_name': row[header_map['cds']],
        'gate_name': row[header_map['name']],
        'gate_type': row[header_map['type']],
        'system': 'TetR',
        'color_hexcode': '000000'
    }, table)


def parts_from_csv(table, header_map):
    parts = []
    for row in table:
        for part in ['ribozyme', 'rbs', 'cds', 'terminator', 'promoter']:
            parts.append({
                'collection': 'parts',
                'type': part,
                'name': row[header_map[part]],
                'dnasequence': row[header_map[part + 'DNA']]
            })
    return parts


def gate_parts_from_csv(table, header_map):
    return map(lambda row: {
        'collection': 'gate_parts',
        'gate_name': row[header_map["name"]],
        'expression_cassettes': [
            {
                'maps_to_variable': 'x',
                'cassette_parts': [
                    row[header_map["ribozyme"]],
                    row[header_map["rbs"]],
                    row[header_map["cds"]],
                    row[header_map["terminator"]]
                ]
            }
        ],
        'promoter': row[header_map["promoter"]]
    }, table)


def response_functions_from_csv(table, header_map):
    return map(lambda row: {
        'collection': 'response_functions',
        'gate_name': row[header_map["name"]],
        'equation': row[header_map["equation"]],
        'variables': [
            {
                'name': 'x',
                'off_threshold': row[header_map["IL"]],
                'on_threshold': row[header_map["IH"]]
            }
        ],
        'parameters': map(
            lambda n: {
                'name': n,
                'value': row[header_map[n]]
            },
            ['ymax', 'ymin', 'K', 'n']
        )
    }, table)


def eugene_rules(roadblock_promoters):
    return {
        'collection': 'eugene_rules',
        'eugene_part_rules': map(
            lambda name: "STARTSWITH %s" % name, roadblock_promoters
        ),
        'eugene_gate_rules': ['ALL_FORWARD']
    }


def write_ucf(table, header_map):
    # description only, values not parsed
    header = {
        'collection': 'header',
        'description': 'placeholder',
        'version': 'placeholder',
        'date': 'placeholder',
        'author': ['author1'],
        'organism': 'Escherichia coli NEB 10-beta',
        'genome': 'placeholder',
        'media': 'placeholder',
        'temperature': '37',
        'growth': 'placeholder',
    }

    # description only, values not parsed
    measurement_std = {
        'collection': 'measurement_std',
        'signal_carrier_units': 'REU',
        'normalization_instructions': 'placeholder',
        'plasmid_description': 'placeholder',
        'plasmid_sequence': 'placeholder',
    }

    # Not used
    nor = {
        'type': 'NOR',
        'max_instances': 10,
    }
    outor = {
        'type': 'OUTPUT_OR',
        'max_instances': 3,
    }
    gate_type_constraints = [nor, outor]
    logic_constraints = {
        'collection': 'logic_constraints',
        'available_gates': gate_type_constraints,
    }

    # For Netsynth motif swapping
    output_or = {
        'collection': 'motif_library',
        'inputs': ['a', 'b'],
        'outputs': ['y'],
        'netlist': ["OUTPUT_OR(y,a,b)"],
    }
    motif_library = [output_or]

    gates = gates_from_csv(table, header_map)
    response_functions = response_functions_from_csv(table, header_map)
    gate_parts = gate_parts_from_csv(table, header_map)
    parts = parts_from_csv(table, header_map)

    roadblock_promoters = (
        'pTac',
        'pBAD',
        'pPhlF',
        'pSrpR',
        'pBM3R1',
        'pQacR',
    )

    eugene = eugene_rules(roadblock_promoters)

    ucf = (
        header,
        measurement_std,
        logic_constraints,
        motif_library,
        gates,
        response_functions,
        gate_parts,
        parts,
        eugene,
    )

    print json.dumps(ucf, indent=2)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Example usage:"

        print ''
        print 'Step 1: write UCF'
        print 'python ucf_writer.py  ../../resources/csv_gate_libraries/gates_Eco1C1G1T1.csv > myName.UCF.json'

        print '\n\n'
        print 'Step 2: post UCF'
        print 'cello post_ucf --name myName.UCF.json --filepath myName.UCF.json'
        print 'or'
        print 'curl -u "username:password" -X POST http://127.0.0.1:8080/ucf/myName.UCF.json --data-urlencode "filetext@myName.UCF.json"'

        print '\n\n'
        print 'Step 3: validate UCF'
        print 'cello validate_ucf --name myName.UCF.json'
        print 'or'
        print 'curl -u "username:password" -X GET http://127.0.0.1:8080/ucf/myName.UCF.json/validate'

        print '\n\n'
        print 'Optional: delete UCF (invalid UCFs should be deleted)'
        print 'cello delete_ucf --name myName.UCF.json'
        print 'or'
        print 'curl -u "username:password" -X GET http://127.0.0.1:8080/ucf/myName.UCF.json/validate'

        print '\n\n'
        print 'cello submit --jobid j3 --verilog resources/0xFE.v --inputs resources/Inputs.txt --outputs resources/Outputs.txt --options "-UCF myName.UCF.json -plasmid false -eugene false"'

        print '\n\n'
        sys.exit()

    csvpath = sys.argv[1]

    with open(csvpath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        # Header
        headers = next(csvreader, None)
        header_map = {}
        i = 0
        for col in headers:
            header_map[col] = i
            i = i + 1

        # Table
        table = []
        for row in csvreader:
            values = []
            for col in row:
                values.append(col)
            table.append(row)

        write_ucf(table, header_map)
