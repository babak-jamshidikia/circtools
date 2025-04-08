#! /usr/bin/env python3
from logging import exception
from nis import match

# Copyright (C)2024 Babak Jamshidikia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either self.version 3 of the License, or
# (at your option) any later self.version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#import sys
#sys.path.append ('~/repositories/circtools/circtools')

import circ_module.circ_template
import os
import re
import requests
import json
import time
import openpyxl
import statistics
import validators
from openpyxl.styles import PatternFill
from datetime import datetime


import os
import re

class Circhemy(circ_module.circ_template.CircTemplate):
    def __init__(self,argparse_arguments,program_name, version):

        # get the user supplied options
        self.cli_params = argparse_arguments
        self.program_name = program_name
        self.version = version
#        self.command = 'Rscript'

    def module_name(self):
        """"Return a string representing the name of the module."""
        return self.program_name

    def run_module(self):
        # we first need to make sure all parameters are sane, the R script does not validate any parameters

        options = self.cli_params
        filepath = str(options.filepath) # input files directoryt bath
        requestdata = options.requestdata
        infile = str(options.infile)
        outfile = str(options.oufile)

#        print("filepath: " + filepath + " request : " + requestdata )
        #filepath = "/home/bjamshidikia/circtoolsdata"
        url = "https://circhemy.jakobilab.org/api/query"
        server = "https://rest.ensembl.org"
        ext = "/lookup/symbol/mus_musculus"

        try:
            page = requests.get(url)
#           print(page.status_code )
        except requests.exceptions.ConnectionError as err :  #HTTPError as err:
            print("Error in URL Connection")
            exit()

        try:
            page = requests.get(server)
        except requests.exceptions.ConnectionError as err :
            print("Error in ensemble URL Connection")
            exit()

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        if os.path.isfile(filepath + "/" + infile) == True:
            CircCoordinate = open(filepath +"/"+ infile, "r")
        else:
            print("File "+ infile +" not found ")
            exit()
        line = CircCoordinate.readline()  # sending the file pointer to the second line for the first read
        # print(line)

        # writing header line

        w = open(filepath + "/" + outfile , "w") #open(filepath + "/CountRNA-" + outfilelist[j]+".bed", "w") # openning the appropriate out file
        spline = line.split()
        wlist = spline[0:8]

#        listtimes = []
        listrecords = []
#        requestarray = []
        abbreviationdict = {
            "csn": "CSNv1",
            "cba": "circBase",
            "cpd": "Circpedia2",
            "gen": "Gene",
            "cal": "CircAtlas2",
            "rct": "riboCIRC",
            "ens": "ENSEMBL",
            "crn": "circRNADb",
            "erb": "exoRBase2",
            "ent": "Entrez",
            "cbn": "circBank",
            "ast": "Arraystar",
            "des": "Description",
            "dbs": "deepBase2",
            "pub": "Pubmed"
        }
        outstring = ""
        requestarray = requestdata # requestdata.split(',')
        outfildslist = []
        lsgenes = []
        print(outstring)
        for item in requestarray :
            if item in abbreviationdict.keys():
                outstring = outstring + ',"' + abbreviationdict[item] + '"'
                wlist.append(abbreviationdict[item])
                outfildslist.append(abbreviationdict[item])
            else :
                print ("error in abbreviations")
                exit()

        outstring= outstring[1:]
        wlist.append("description")
        wlist.append("biotype")
        wlist.append("id")
        wline = "\t".join(wlist)
        w.write(wline + "\n")
    #    print("header is : " + wline)

        line = CircCoordinate.readline()
        spline = line.split()  # making a list from the line
        chromosome = "chr" + spline[0]  # "chr22"
        chrstart = spline[1]  # "36341370"
        chrstop = spline[2]  # "36349255"
        chrStrand = spline[5]
        lsgenes.append('"' + spline[3]+'"')
        while True:
            if not line:
                break

            data = '{"input": [{"query": "' + chromosome + '", "field": "Chr", "operator1": "AND", "operator2": "is"},' \
                                                       '{"query": "' + chrstart + '", "field": "Start", "operator1": "AND", "operator2": "is"},' \
                                                       '{"query": "' + chrstop + '", "field": "Stop", "operator1": "AND", "operator2": "is"}' \
#                                                       '{"query": "' + chrStrand + '", "field": "Strand", "operator1": "AND", "operator2": "is"}'
        

            lsreadlines = []
            lsreadlines.append([spline[0:8]])



            for i in range(0, 500):

                line = CircCoordinate.readline()  # sending the file pointer to the second line for every other reads

                if not line:
                    break
                spline = line.split()  # making a list from the line
                wlist = spline[0:8]         # adding first four columns chr,start,end,Gene name
                chromosome = "chr" + spline[0]  # "chr22"
                chrstart = spline[1]  # "36341370"
                chrstop = spline[2]  # "36349255"
                chrStrand = spline[5]
                lsgenes.append('"' + spline[3] + '"')

                #    print("chr : "+ chromosome + " Start : " + chrstart + " Stop : " + chrstop  )
                data1 = ',{"query": "' + chromosome + '", "field": "Chr", "operator1": "OR", "operator2": "is"},' \
                        '{"query": "' + chrstart + '", "field": "Start", "operator1": "AND", "operator2": "is"},' \
                        '{"query": "' + chrstop + '", "field": "Stop", "operator1": "AND", "operator2": "is"}' \
#                        '{"query": "' + chrStrand + '", "field": "Strand", "operator1": "AND", "operator2": "is"}'
                data = data + data1
                #    print(data)
                lsreadlines.append([spline[0:8]])
                i += 1


            data = data + '],'
            data = data + ' "output": ['+ outstring +',"Chr","Start","Stop","Strand"]}'

            #data ={"input": [{"query": "chr1", "field": "Chr", "operator1": "AND", "operator2": "is"},{"query": "935772", "field": "Start", "operator1": "AND", "operator2": "is"},{"query": "939412", "field": "Stop", "operator1": "AND", "operator2": "is"},{"query": "+", "field": "Strand", "operator1": "AND", "operator2": "is"},{"query": "chr1", "field": "Chr", "operator1": "OR", "operator2": "is"},{"query": "3740233", "field": "Start", "operator1": "AND", "operator2": "is"},{"query": "3746186", "field": "Stop", "operator1": "AND", "operator2": "is"},{"query": "+", "field": "Strand", "operator1": "AND", "operator2": "is"}], "output": ["Circpedia2","Chr","Start","Stop","Strand"]}
            # print(data)
            #exit()
            # print(",".join(lsgenes))

            strgenes =  ",".join(lsgenes)






            try:
                response = requests.post(url, data=data, headers=headers)
                jsondata = response.json()
                # print(response.json())
                # exit()
                listrecords.append(len(jsondata["rowData"]))
            except KeyError as err :
                print ( "There is a rowData key error ")
                exit()

            # print(server)
            # print(ext)
            # print(headers)
            strdata = '{ "symbols" : ['+ strgenes + ']}'
            # print(strdata)
            # exit()

            try:
                r = requests.post(server + ext, headers=headers, data=strdata)

            except KeyError as err:
                print("There is a rowData key error ")
                exit()

            decoded = r.json()
            # print(decoded)
            # exit()




                # print(err)
    #       CircCoordinate.seek(0, 0)
    #        lsreadlines = []
    #       jsondata = {}
            strcircpedia = ""
            if (len(jsondata["rowData"]) == 0) :
                exit()
            for i in range(0,len(lsreadlines)):
            #    print(" i = " + str(i))
                chromosome = "chr" + str(lsreadlines[i][0][0])
                chrstart = lsreadlines[i][0][1]
                chrstop= lsreadlines[i][0][2]
                chrstrand = lsreadlines[i][0][5]
                genename  = lsreadlines[i][0][3]
                # print(str(len(jsondata["rowData"])))
                for j in range(0,len(jsondata["rowData"])):
                    jj = jsondata["rowData"][j]#["Circpedia2"]
                    # print( str(jsondata["rowData"][j]["Chr"]) + " , " + str(jsondata["rowData"][j]["Start"]) + " , " + str(jsondata["rowData"][j]["Stop"]))
                    if str(jsondata["rowData"][j]["Chr"]).strip() == chromosome.strip() and str(jsondata["rowData"][j]["Start"]).strip() == chrstart.strip() and str(jsondata["rowData"][j]["Stop"]).strip() == chrstop.strip() and str(jsondata["rowData"][j]["Strand"]).strip() == chrstrand.strip()  :
                        #print( " circpedia2: "+ str(jsondata["rowData"][j]["Circpedia2"]))
                        strcircpedia = ""
                        for item in outfildslist:

                            if  (str(jsondata["rowData"][j][item]).strip() != ""):
                                strcircpedia =  strcircpedia+"\t" + str(jsondata["rowData"][j][item])
                            else:
                                strcircpedia = strcircpedia + "\t" + "N/A"


                    j +=1
                # print(strcircpedia)
                lsreadlines[i][0].append(strcircpedia)
                if decoded.get(genename) != None :
                    lsreadlines[i][0].append(str(decoded[genename]["description"]))
                    lsreadlines[i][0].append(str(decoded[genename]["biotype"]))
                    lsreadlines[i][0].append(str(decoded[genename]["id"]))
                else :
                    lsreadlines[i][0].append("N/A")
                    lsreadlines[i][0].append("N/A")
                    lsreadlines[i][0].append("N/A")


                wline = "\t".join(lsreadlines[i][0])

                w.write( wline + "\n" )     # write the tab delimited string in the appropriate file
                strcircpedia = ""
                i += i
            # w.write("---------------------------\n")

    #closing files
        w.close()               #closing the last output file
        CircCoordinate.close()  # closing the input file CircCoordinate
#       CircRNACount.close()    # closing the input file CircRNACount





