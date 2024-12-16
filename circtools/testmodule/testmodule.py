#! /usr/bin/env python3

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
#sys.path.append ('/home/bjamshidikia/repositories/circtools/circtools')

import circ_module.circ_template 
import os
import re


#class CircTest(circ_module.circ_template.CircTemplate):
class TestModule(circ_module.circ_template.CircTemplate):
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
        starfilepath = str(options.starpath) #"/home/bjamshidikia/circtoolsdata/star/star-res"
        multiplier = int(options.multiplier)
        #print(filepath[0:filepath.rfind("/")])
        #outfilepath = filepath[0:filepath.rfind("/")]
        #print(outfilepath + "/bedfile.bed")


    # checking if the given file path is correct  and the files exists if not make an error  ?
        if os.path.isfile(options.filepath + "/CircCoordinates" ) == True:
            CircCoordinate = open(filepath + "/CircCoordinates","r")
        else:
            print("File CircCoordinate not found ")
            exit()

        if os.path.isfile(options.filepath + "/CircRNACount" ) == True:
            CircRNACount = open(filepath + "/CircRNACount","r")
        else:
            print("File CircRNACount not found ")
            exit()



        line = CircCoordinate.readline()    # sending the file pointer to the second line for the first read
        line2 = CircRNACount.readline()     # sending the file pointer to the second line for the first read
        columnlist = line2.split()          # making a list of column names
        outfilelist = columnlist[3:]        # picking up  column name including sample name and .Chimeric.out.junction
        maxread = []                        # defining an empty list for the sample names
        i = 0
        print("   sample name \t  maximum read     "  )    # printing table for reads per samples
        for i in range(len(outfilelist)):
            outfilelist[i] = outfilelist[i].replace(".Chimeric.out.junction","") # removing the .Chimeric.out.junction from each column name to prepare the sample name
            if os.path.isfile(starfilepath+"/"+ outfilelist[i] +"/Log.final.out"):           # checking if the sample name star Log.final.out exists
                f = open(starfilepath+"/"+ outfilelist[i] +"/Log.final.out","r")             # opening the sample name star Log.final.out
            else:
                print("Star Log.final.out file for sample : " + outfilelist[i] + "not found ") # if the file not exists raise an error message
                exit()

            #print(starfilepath+"/"+ outfilelist[i] +"/Log.final.out")
            for line in f:                                                  # walking in star log file line by line
                match = re.match(" *Number of input reads *", line)  # check if the loaded line containing  "Number of input reads"
                if match:                                                   # if  the checked line in TRUE?
                    reads = re.findall("\d+", line)                  # invoke the maximum reads
                    maxread.append(reads[0])                                # append the maximum, reads number to the list

            print( "   "+ str(outfilelist[i]) +  " \t " +   str(reads[0])  )
            f.close()

        i = 1
        j = 0
        for j in range(len(outfilelist)):
            #print(" out files :  " + filepath + "/CountRNA-" + outfilelist[j] )  # printing the out file path and name
            w = open(filepath + "/CountRNA-" + outfilelist[j]+".bed", "w") # openning the appropriate out file
            while True:
                line = CircCoordinate.readline() # sending the file pointer to the second line for every other reads
                line2 = CircRNACount.readline()  # sending the file pointer to the second line for every other reads
                if not line :
                    break
                spline = line.split()       # making a list from the line
                spline2 = line2.split()     # making a list from the line
                wlist = spline[0:4]         # adding first four columns chr,start,end,Gene name
                #wlist.append(spline2[3 + j])
                #wlist.append(maxread[j])
                #division = (int(spline2[3 + j]) / int(maxread[j]))
                wlist.append(str((int(spline2[3 + j]) / int(maxread[j])) * multiplier))  # adding relative number of  (junction/maximum read) * multiplier for each outfile as score
                wlist.append(spline[5])     # adding strand
                wline =  "\t".join(wlist)   # making a tab delimited string
                w.write( wline + "\n" )     # write the tab delimited string in the appropriate file
                i += 1
            print("Output file : " + filepath + "/CountRNA-" + outfilelist[j] + ".bed \n  Number of the lines written : " + str(i))
            i = 0
            w.close() # closing the appropriate out file
            CircCoordinate.seek(0)            #sending the pointer to the beginning of the file
            CircRNACount.seek(0)              #sending the pointer to the beginning of the file
            line = CircCoordinate.readline()  # sending the file pointer to the second line
            line2 = CircRNACount.readline()   # sending the file pointer to the second line

        # closing files
        #print ("Output file : " + filepath + "/CircRNA-Sic_1.bed \n  Number of the lines written : " + str(i)  )
        w.close()               #closing the last output file
        CircCoordinate.close()  # closing the input file CircCoordinate
        CircRNACount.close()    # closing the input file CircRNACount

#        print ("end of test")




