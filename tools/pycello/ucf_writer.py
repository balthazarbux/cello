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
        'parameters': [
            {
                'name': 'ymax',
                'value': row[header_map["ymax"]]
            },
            {
                'name': 'ymin',
                'value': row[header_map["ymin"]]
            },
            {
                'name': 'K',
                'value': row[header_map["K"]]
            },
            {
                'name': 'n',
                'value': row[header_map["n"]]
            },
        ]
    }, table)


def eugene_rules(roadblock_promoters):
    eugene_rules = {}
    eugene_rules["collection"] = "eugene_rules"
    eugene_rules["eugene_part_rules"] = []
    eugene_rules["eugene_gate_rules"] = []

    eugene_rules["eugene_gate_rules"].append("ALL_FORWARD")

    for promoter_name in roadblock_promoters:
        eugene_rules["eugene_part_rules"].append("STARTSWITH " + promoter_name)

    return eugene_rules


def write_ucf(table, header_map):
    # description only, values not parsed
    header = {}
    header["collection"] = "header"
    header["description"] = "placeholder"
    header["version"] = "placeholder"
    header["date"] = "placeholder"
    header["author"] = ["author1"]
    header["organism"] = "Escherichia coli NEB 10-beta"
    header["genome"] = "placeholder"
    header["media"] = "placeholder"
    header["temperature"] = "37"
    header["growth"] = "placeholder"

    # description only, values not parsed
    measurement_std = {}
    measurement_std["collection"] = "measurement_std"
    measurement_std["signal_carrier_units"] = "REU"
    measurement_std["normalization_instructions"] = "placeholder"
    measurement_std["plasmid_description"] = "placeholder"
    measurement_std["plasmid_sequence"] = "placeholder"

    # Not used
    logic_constraints = {}
    nor = {}
    nor["type"] = "NOR"
    nor["max_instances"] = 10
    outor = {}
    outor["type"] = "OUTPUT_OR"
    outor["max_instances"] = 3
    gate_type_constraints = []
    gate_type_constraints.append(nor)
    gate_type_constraints.append(outor)
    logic_constraints["collection"] = "logic_constraints"
    logic_constraints["available_gates"] = gate_type_constraints

    # For Netsynth motif swapping
    motif_library = []
    output_or = {}
    output_or["collection"] = "motif_library"
    output_or["inputs"] = ["a", "b"]
    output_or["outputs"] = ["y"]
    output_or["netlist"] = []
    output_or["netlist"].append("OUTPUT_OR(y,a,b)")
    motif_library.append(output_or)

    gates = gates_from_csv(table, header_map)

    response_functions = response_functions_from_csv(table, header_map)

    gate_parts = gate_parts_from_csv(table, header_map)

    parts = parts_from_csv(table, header_map)

    roadblock_promoters = []
    roadblock_promoters.append("pTac")
    roadblock_promoters.append("pBAD")
    roadblock_promoters.append("pPhlF")
    roadblock_promoters.append("pSrpR")
    roadblock_promoters.append("pBM3R1")
    roadblock_promoters.append("pQacR")

    eugene = eugene_rules(roadblock_promoters)

    ucf = []
    ucf.append(header)
    ucf.append(measurement_std)
    ucf.append(logic_constraints)
    ucf.extend(motif_library)
    ucf.extend(gates)
    ucf.extend(response_functions)
    ucf.extend(gate_parts)
    ucf.extend(parts)
    ucf.append(eugene)

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
