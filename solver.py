import sys
import random
import math
coordlist = []
returnlist = []
totaldist = 0
listholder = []
# Plans: 1. n point random search. 2. keep more than 1 child. 

# Returns the distance between two points with coordinates given as t1 and t2. 
# Structure of t1 is: t1[0] = id, t1[1] = x coordinate, t1[2] = y coordinate. t2 has the same structure.
def calcdist(t1, t2):
    return math.sqrt((t1[1]-t2[1])**2 + (t1[2]-t2[2])**2)

# Points with coordinates listed in list 'lh' are visited in the order given in the list 'l1'. 'calcdist_total' returns the total distance.
def calcdist_total(l1, lh):
    dist = 0
    for i in range(len(l1)-1):
        dist += calcdist(lh[l1[i]-1],lh[l1[i+1]-1])
    dist+= calcdist(lh[l1[0]-1],lh[l1[len(l1)-1]-1])
    return dist

# Function to prevent 'index out of range' error for cases that goes out of the range by 1. Treats the input list 'li' as a circular permutation for the indices len(li) and -1.
def circ(li, num):
    if num == len(li):
        return 0
    if num == -1:
        return len(li)-1
    else: return num

def parse_initial(tspfile):
    f=open(tspfile,"r")
    while 1:
        line=f.readline()
        if "NODE_COORD_SECTION" in line: break
    while 1:
        line = f.readline()
        if "EOF" in line: break
        linetuple=line.split()
        # print(linetuple)
        linetupleInt=(int(linetuple[0]), float(linetuple[1]),float(linetuple[2]))
        coordlist.append(linetupleInt)
    return coordlist

def parse_solution(solfile):
    sol = open(solfile,"r")
    anslist = []

    while True:
        line = sol.readline()
        if not line:
            break
        anslist.append(int(line))
    sol.close()
    return anslist

while True:
    print("\n-----------------Welcome to TSP Solver!-------------------")
    mode = input("Select Your Mode. \nView Detailed Description of each mode: 'help'\n \nGenerate a New Initial Case\n  With Greedy Algorithm from Random Point: 'greed' \n  With Stochastic Rearrangement: 'random'\n\nImprove Last Solution with Stochastic Algorithms\n  Random Search with Two Points: 'RS2'\n  Random Search with Three Points: 'RS3' \n\nView Current Distance: 'view'\nExit Program: 'exit' \n")
    if mode.lower() == 'exit': break
    # Reads through the tsp file given in the second argument in the system call.
    # (For example, 'burma14.tsp' in 'python solver.py burma14.tsp')
    # Stores its information as list of tuples: {id, x_coordinate, y_coordinate} with the name 'listholder'
    listholder = parse_initial(sys.argv[1])
        
    ###############################################################
    

    if mode.lower() == 'random':
        sol = open("solution.csv", "w")
        listholderbuffer = listholder.copy()
        randomisedlistholder = []
        for i in range(len(listholderbuffer)):
            index = random.randint(0,len(listholderbuffer)-1)
            value = listholderbuffer.pop(index)[0]
            randomisedlistholder.append(value)
            sol.write("%d\n"% value)
        sol.close()
        print("Random Initialisation Complete.\n Current Total Distance: ", calcdist_total(randomisedlistholder,listholder))
    
    if mode.lower() == 'help':
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("-------------------------HELP----------------------------")
        print("TSP Algorithm Will 'Try' to Find the Shortest Path Possible to Visit All Points Given")
        hello = input("press any key to return")

    # 'gen' mode is selected. Generates new greedy solution from a randomly chosen point.
    if mode.lower() =='greed':
        count = 0
        sol= open("solution.csv","w")

        first_index =random.randint(0,len(coordlist)-count-1)
        sol.write("%d\n" % (first_index+1))
        print("//First Index was", first_index, "//lenCoordlist was ", len(coordlist))
        first_point = coordlist.pop(first_index)
        second_point = coordlist[random.randint(0,len(coordlist)-1)]
        mindist = calcdist(first_point,second_point)
        minindex = 0

        while (len(coordlist)>1):
            for point in coordlist:
                thisdist = calcdist(first_point, point)
                if thisdist <= mindist:
                    minindex = count
                    mindist = thisdist
                count +=1
            first_point = coordlist.pop(minindex)
            totaldist +=mindist
            count = 0
            second_point = coordlist[random.randint(0,len(coordlist)-1)]
            mindist = calcdist(first_point,second_point)
            sol.write("%d\n" % (first_point[0]))
            minindex=0
            print("len(coordlist)was", len(coordlist))
        sol.write("%d\n" % (second_point[0]))
        print("COMPLETE!!")
        sol.close()
        f.close()
    ################################################################

    if mode.lower() == ('rs2' or 'rs3'):
        generations = int(input("How many thousands of generations more?"))*1000
        ran = int(input("Input the Range of Randomisation: "))

    # Brings the solution.csv file that was saved in the last run, or was generated from the 'gen' command.
    # Calculates the total distance (which is to be minimised) when the points where visited as listed in solution.csv
    # Stores the list of points from solution.csv at 'buflist' and 'anslist'. 
        
    anslist = parse_solution("solution.csv")
    buflist = anslist.copy()
    totaldist0 = calcdist_total(anslist,listholder)
    distbefore = totaldist0
    ################################################################

    #Chooses two random points. Shuffle them. Calculate the new total distance. Save the newly ordered list if the new distance is shorter than before. 
    if mode.lower() =='rs2':
        print('RS2 Started')
        children = input("How many Children in each generation?")
        selection = input("How many ")
        for gen in range(generations):
            index = random.randint(0,len(anslist)-1)
            index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
            buflist[index] = anslist[index2]
            buflist[index2] = anslist[index]
            # totaldist = calcdist_total(buflist,listholder)
            totaldist2 = totaldist0
            if abs(index-index2)==1:
                totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                # if abs(totaldist2-totaldist)<0.001: print("COMPLIES!! at abs==1")
                # else: print("DOESNT COMPLY. Indices are", index, "  ", index2, "diff is", totaldist- totaldist2)
            else:
                totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                # if abs(totaldist2-totaldist)<0.001: print("COMPLIES!! at abs==1")
                # else: print("DOESNT COMPLY. Indices are", index, "  ", index2, "diff is", totaldist- totaldist2)
            if totaldist2 < totaldist0:
                print("Success! New Total dist is ", totaldist2)
                print("The Distance between Two Indices Were", index-index2)
                print("-------------------------------------------")
                anslist = buflist.copy()
                totaldist0 = totaldist2
                sol = open("solution.csv", 'w')
                for number in anslist:
                    sol.write("%d\n" % (number))
            else:
                buflist = anslist.copy()
                totaldist2 = totaldist0


    # Chooses three random points. Shuffle them. Calculate the new total distance. Save the newly ordered list if the new distance is shorter than before. 
    if mode.lower() =='rs3':
        for gen in range(generations):
            index = random.randint(0,len(anslist)-1)
            index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
            
            buflist[index] = anslist[index2]
            buflist[index2] = anslist[index]
            
            # totaldist = calcdist_total(buflist,listholder)
            totaldist2 = totaldist0
            if abs(index-index2)==1:
                totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                # if abs(totaldist2-totaldist)<0.001: print("COMPLIES!! at abs==1")
                # else: print("DOESNT COMPLY. Indices are", index, "  ", index2, "diff is", totaldist- totaldist2)
            else:
                totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                # if abs(totaldist2-totaldist)<0.001: print("COMPLIES!! at abs==1")
                # else: print("DOESNT COMPLY. Indices are", index, "  ", index2, "diff is", totaldist- totaldist2)
            buflist2=buflist.copy()
            index3 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
            while index3 == index:
                index3 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
            buflist2[index3] = buflist[index2]
            buflist2[index2] = buflist[index3]
            # totaldist = calcdist_total(buflist2,listholder)
            if abs(index3-index2)==1:
                totaldist2 -= calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)-1)]-1])
                totaldist2 -= calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)+1)]-1])
                totaldist2 += calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)-1)]-1])
                totaldist2 += calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)+1)]-1])
                # if abs(totaldist2-totaldist)<0.001: print("COMPLIES!! at abs==1")
                # else: print("DOESNT COMPLY. Indices are", index2, "  ", index3, "diff is", totaldist- totaldist2)
            else:
                totaldist2 -= calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)-1)]-1])
                totaldist2 -= calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)+1)]-1])
                totaldist2 -= calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)+1)]-1])
                totaldist2 -= calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)-1)]-1])
                totaldist2 += calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)-1)]-1])
                totaldist2 += calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)+1)]-1])
                totaldist2 += calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)+1)]-1])
                totaldist2 += calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)-1)]-1])
                # if abs(totaldist2-totaldist)<0.001: print("COMPLIES!! 22222222222")
                # else: print("DOESNT COMPLY. Indices are", index2, "  ", index3, "diff is", totaldist- totaldist2)
            
            if totaldist2 < totaldist0:
                print("Success! New Total dist is ", totaldist2)
                print("The Distances between Three Indices Were", index-index2, "  ", index-index3)
                print("-------------------------------------------")
                anslist = buflist2.copy()
                totaldist0 = totaldist2
                sol = open("solution.csv", 'w')
                for number in anslist:
                    sol.write("%d\n" % (number))
            else:
                # print("fail")
                buflist = anslist.copy()
                totaldist2 = totaldist0

    print("Total Amount Improved was", distbefore-totaldist0)
