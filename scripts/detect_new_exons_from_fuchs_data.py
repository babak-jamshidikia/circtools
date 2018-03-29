#!/usr/bin/env python3

# Copyright (C) 2018 Tobias Jakobi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import sys


def check_input_files(input_file_list):
    """Checks supplied list of files for existence.
    Will halt the program if file not accessible
    """
    for file in input_file_list:
        # check if exists
        if not os.path.isfile(file):
            message = ("File " + str(file) + " cannot be found, exiting.")
            sys.exit(message)


def parse_bed_file(input_file, annotation, local_dict, min_coverage):

    with open(input_file) as fp:

        for line in fp:

            if line.startswith("#"):
                continue

            line = line.rstrip()

            columns = line.split('\t')

            start = 0
            stop = 0

            location_string = columns[3].split('|')
            coverage = float(location_string[2])

            if coverage >= min_coverage:
                for wobble in range(-10, 10):

                    if columns[0] + "_" + str(int(columns[1])+wobble) in annotation:
                        start = 1

                    if columns[0] + "_" + str(int(columns[2])+wobble) in annotation:
                        stop = 1

                if start == 0 and stop == 0:
                    location = columns[0] + "\t" + str(columns[1]) + "\t" + str(columns[2])
                    if location not in local_dict:
                        local_dict[location] = 1
                    else:
                        local_dict[location] += 1

    return local_dict


def parse_gtf_file(input_file):
    from collections import OrderedDict
    import sys

    annotation = OrderedDict()

    try:
        file_handle = open(input_file)
    except PermissionError:
        message = ("Input file " + str(input_file) + " cannot be read, exiting.")
        sys.exit(message)
    else:

        with file_handle:
            line_iterator = iter(file_handle)
            for line in line_iterator:
                # we skip any comment lines
                if line.startswith("#"):
                    continue

                # split up the annotation line
                columns = line.split('\t')

                # we only want the coordinates of the gene entries
                if not (columns[2] == "exon"):
                    continue

                # we do not want any 0-length intervals -> bedtools segfault
                if int(columns[4]) - int(columns[3]) == 0:
                    continue

                start_key = str(columns[0])+"_"+str(columns[3])
                stop_key = str(columns[0])+"_"+str(columns[4])

                annotation[start_key] = 1
                annotation[stop_key] = 1

    return annotation

# main script starts here


parser = argparse.ArgumentParser(description='Output newly identified exons compare to reference annotation')

group = parser.add_argument_group("Input")

group.add_argument("-a",
                   "--annotation",
                   dest="base_exon_file",
                   help="Base annotation in GTF format (ENSEMBL)",
                   required=True
                   )

group.add_argument("-g",
                   "--group-assignment",
                   dest="assignment",
                   help="Assignment of BED files to sample groups",
                   required=True,
                   nargs='+',
                   type=int
                   )

group.add_argument("-f",
                   "--bed-files",
                   dest="bed_files",
                   help="Space-separated list of BED files to scan",
                   required=True,
                   nargs='+',
                   )

group.add_argument("-t",
                   "--threshold",
                   dest="threshold",
                   help="Minimal number of samples that have to agree on a novel exon [default: 2]",
                   type=int,
                   default=2
                   )

group.add_argument("-c",
                   "--coverage",
                   dest="min_coverage",
                   help="Minimal coverage of exons [default: 1.0 == 100%]",
                   type=float,
                   default=1.0
                   )

args = parser.parse_args()

check_input_files(args.bed_files)


if len(args.bed_files) != len(args.assignment):
    print("Differing counts for BED files and group assignment, exiting.")
    exit(-1)

if args.threshold > len(args.bed_files):
    print("Threshold > number of provided sources files.")
    exit(-1)


global_dict = {}

assignment_dict = {}

final_dict = {}

gtf_input = parse_gtf_file(args.base_exon_file)

num_files = len(args.bed_files)

sample_num = len(set(args.assignment))

file_dict = {}

for file in range(0, num_files):

    if args.assignment[file] not in global_dict:
        global_dict[args.assignment[file]] = {}

    file_dict[args.bed_files[file]] = args.assignment[file]

    if args.assignment[file] not in assignment_dict:
        assignment_dict[args.assignment[file]] = 1
    else:
        assignment_dict[args.assignment[file]] += 1

    global_dict[args.assignment[file]] = parse_bed_file(args.bed_files[file],
                                                        gtf_input,
                                                        global_dict[args.assignment[file]],
                                                        args.min_coverage
                                                        )

# remove non-stringent exons
for sample in global_dict:
    final_dict[sample] = {}
    for key in global_dict[sample]:
        if global_dict[sample][key] >= args.threshold:
            final_dict[sample][key] = global_dict[sample][key]

for sample in final_dict:

    file = open("sample_"+str(sample)+".gtf", "w")

    for key in final_dict[sample]:
        entry = key.split('\t')

        sep = "\t"

        file.write(sep.join([entry[0], "circtools", "exon", entry[1], entry[2], ".", ".", ".", "."])+"\n")

    file.close()