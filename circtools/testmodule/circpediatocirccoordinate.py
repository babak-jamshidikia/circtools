import os
import re
import requests
import json
import time
# initializing parameters


start_time = time.time()
filepath = "/home/bjamshidikia/circtoolsdata"
url = "https://circhemy.jakobilab.org/api/query"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

if os.path.isfile(filepath + "/CircCoordinates" ) == True:
    CircCoordinate = open(filepath + "/CircCoordinates","r")
else:
        print("File CircCoordinate not found ")
        exit()

line = CircCoordinate.readline()    # sending the file pointer to the second line for the first read
#print(line)

# writing header line
w = open(filepath + "/circpediacircCoordinte.bed", "w") #open(filepath + "/CountRNA-" + outfilelist[j]+".bed", "w") # openning the appropriate out file
spline = line.split()
wlist = spline[0:8]
wlist.append("Circpedia2")
wline = "\t".join(wlist)
w.write(wline + "\n")
line = CircCoordinate.readline()

spline = line.split()       # making a list from the line
chromosome = "chr" + spline[0]  # "chr22"
chrstart = spline[1]  # "36341370"
chrstop = spline[2]  # "36349255"
#print("chr : " + chromosome + " Start : " + chrstart + " Stop : " + chrstop)
data = '{"input": [{"query": "' + chromosome + '", "field": "Chr", "operator1": "AND", "operator2": "is"},' \
       '{"query": "' + chrstart + '", "field": "Start", "operator1": "AND", "operator2": "is"},' \
       '{"query": "' + chrstop + '", "field": "Stop", "operator1": "AND", "operator2": "is"}'
#print (data)
#exit()
for i in range(0,10):

    line = CircCoordinate.readline() # sending the file pointer to the second line for every other reads
#    print ( "i = " + str(i))
    if not line :
        break
    spline = line.split()       # making a list from the line
    #wlist = spline[0:8]         # adding first four columns chr,start,end,Gene name
    chromosome = "chr" + spline[0]  #"chr22"
    chrstart = spline[1]#"36341370"
    chrstop = spline[2] #"36349255"
#    print("chr : "+ chromosome + " Start : " + chrstart + " Stop : " + chrstop  )

    data1 =  ',{"query": "' + chromosome + '", "field": "Chr", "operator1": "OR", "operator2": "is"},{"query": "' + chrstart + '", "field": "Start", "operator1": "AND", "operator2": "is"},{"query": "' + chrstop + '", "field": "Stop", "operator1": "AND", "operator2": "is"}'
    data = data + data1
#    print(data)
    i +=  1
data = data + '],'

data = data + ' "output": ["Circpedia2","Chr","Start","Stop"]}'
#print(data)


response = requests.post(url, data=data, headers=headers)
     # print(response.json())
jsondata = response.json()
#print(jsondata)
#if jsondata["rowData"] != []:

#item_dict = json.loads(jsondata)

#print (item_dict)

#jsondata["rowData"]
totaltime = time.time() - start_time
print(totaltime)
for i in range(0,len(jsondata["rowData"])):
    jj = jsondata["rowData"][i]#["Circpedia2"]
    print(jj)
    i += i
#    print("type is " + str(type(jj)))
#    if jj == None :
#        wline =  "\t".join(wlist)   # making a tab delimited string
#    else:
#        wlist.append(jj)     # adding strand
#        wline = "\t".join(wlist)
#    print(wline)
#    w.write( wline + "\n" )     # write the tab delimited string in the appropriate file

w.close()               #closing the last output file
CircCoordinate.close()  # closing the input file CircCoordinate



