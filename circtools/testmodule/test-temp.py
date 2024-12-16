import os
import re

if os.path.isfile( "/home/bjamshidikia/circtoolsdata/star/star-res/SiC_1/Log.final.out"):  # checking if the sample name star Log.final.out exists
    f = open("/home/bjamshidikia/circtoolsdata/star/star-res/SiC_1/Log.final.out", "r")  # opening the sample name star Log.final.out
else:
    print("Star Log.final.out file for sample : not found ")  # if the file not exists raise an error message
    exit()


#for line in f:
#    match = re.match(" *Number of input reads *",line)
#    if match:
#        reads = re.findall("\d+",line)
#        print(reads[0])

for line in f:
    match = re.search(('Number of input reads'),line)
    #print(match)
    if match:
        reads = re.findall("\d+",line)
        print(reads[0])







 #   for i in range(len(spline)):
  #      spline[i] = spline[i].strip()
 #       if "Number of input reads" in spline[i]:
 #           print("-----------------------------"+str(i))
 #           print("-------------"+spline[i+1])
 #           break
 #       print(spline[i])
 #   if not f.readline():
 #       break
#print(spline)