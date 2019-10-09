import sys
import random
import math
import collections
#I used numpy only for calculating weighted random. I swear I didnot exploit this
import numpy
import operator

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

#parse from tspfile
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
    f.close()
    return coordlist

#parse from saved solution file 'solfile'
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

#Save the list 'order' in the file named 'solfile'
def save_solution(order, solfile):
    with open(solfile, 'w+') as sol:
        for number in order:
            sol.write("%d\n" %number)

#randomise the given list 'list1'
def randomise_list(list1):
    li = list1.copy()
    randomisedlistholder=list()
    for i in range(len(li)):
        index = random.randint(0,len(li)-1)
        value = li.pop(index)[0]
        randomisedlistholder.append(value)
    return randomisedlistholder

# Reads through the tsp file given in the second argument in the system call.
    # (For example, 'burma14.tsp' in 'python solver.py burma14.tsp')
    # Stores its information as list of tuples: {id, x_coordinate, y_coordinate} with the name 'listholder'
listholder = parse_initial(sys.argv[1])
###############################################################


while True:
    print("\n-----------------Welcome to TSP Solver!-------------------")
    mode = input("Select Your Mode. \nView Detailed Description of each mode: 'help'\n \nGenerate a New Initial Case\n  With Greedy Algorithm from Random Point: 'greed' \n  With Stochastic Rearrangement: 'random'\n  With Ant Colony Optimisation: 'ant'\n\nImprove Last Solution with Stochastic Algorithms\n  Random Search with Two Points: 'RS2'\n  Random Search with Three Points: 'RS3' \n\nView Current Distance: 'view'\nExit Program: 'exit' \n")
    if mode.lower() == 'exit': break

    if mode.lower() == 'random':
        randomisedlistholder = randomise_list(listholder)
        save_solution(randomisedlistholder,"solution.csv")
        print("Random Initialisation Complete.\n Current Total Distance: ", calcdist_total(randomisedlistholder,listholder))
    
    if mode.lower() == 'help':
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("-------------------------HELP----------------------------")
        print("TSP Algorithm Will 'Try' to Find the Shortest Path Possible to Visit All Points Given")
        hello = input("press any key to return")

    # 'gen' mode is selected. Generates new greedy solution from a randomly chosen point.
    if mode.lower() =='greed':
        count = 0
        greedylist = list()
        coordlist = listholder.copy()
        
        first_index =random.randint(0,len(coordlist)-count-1)
        greedylist.append(first_index+1)
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
            greedylist.append(first_point[0])
            minindex=0
            print("len(coordlist)was", len(coordlist))
        greedylist.append(second_point[0])
        save_solution(greedylist,"solution.csv")
        print("COMPLETE!! Distance was ", calcdist_total(greedylist,listholder))
        continue
    
    ################################################################

    if mode.lower() == 'rs2' or mode.lower() == 'rs3':
        generations = int(input("How many generations more?"))
        ran = int(input("Input the Range of Randomisation: "))
        anslist = parse_solution("solution.csv")
        buflist = anslist.copy()
        totaldist0 = calcdist_total(anslist,listholder)
        distbefore = totaldist0

    # Brings the solution.csv file that was saved in the last run, or was generated from the 'gen' command.
    # Calculates the total distance (which is to be minimised) when the points where visited as listed in solution.csv
    # Stores the list of points from solution.csv at 'buflist' and 'anslist'. 
        
    
    ################################################################

    #Chooses two random points. Shuffle them. Calculate the new total distance. Repeat few steps to make children. Choose few of the best children and pass them over to the next generation. Save the newly ordered list if the new distance is shorter than before. 
    if mode.lower() =='rs2':
        children = int(input("How many Children from each parent? "))
        selection = int(input("How many best parents passed to next step? "))
        while selection > children**2:
            selection = int(input("You must make more children than the number of children you want to keep. How many best solution to keep in each step again? "))

        children_in_generation = dict()
        for child in range(children*selection):
            index = random.randint(0,len(anslist)-1)
            index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
            buflist[index] = anslist[index2]
            buflist[index2] = anslist[index]
            totaldist2 = distbefore
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
            children_in_generation[totaldist2] = buflist
            buflist = anslist.copy()
        distances = list(children_in_generation.keys())
        distances.sort()
        print("Best Distance at First Gen: ", distances[0])
        if distbefore>distances[0]: 
            print("SUCCESSFUL! Improved by", distbefore-distances[0])
            distbefore = distances[0]
        else: print("No Progress Made at this Gen")
        selected_children=dict()
        for i in range(selection):
            selected_children[distances[i]]=children_in_generation[distances[i]]
        selected_children[distbefore]=anslist
        print("------------------------------------------------------")

        for gen in range(generations-1):
            parents = list(selected_children.keys())
            children_in_generation = dict()
            
            for key in parents:
                anslist = selected_children[key]
                totaldist2 = calcdist_total(selected_children[key], listholder)

                for child in range(children):
                    buflist = anslist.copy()
                    index = random.randint(0,len(anslist)-1)
                    index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
                    buflist[index] = anslist[index2]
                    buflist[index2] = anslist[index]
                    if abs(index-index2)==1:
                        totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                        totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                    else:
                        totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                        totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                        totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                        totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                    children_in_generation[totaldist2] = buflist
                    buflist = anslist.copy()
            children_in_generation.update(selected_children)
            distances = list(children_in_generation.keys())
            distances.sort()
            print("Best Distance at",gen+2, "th Gen: ", distances[0])
            if distbefore>distances[0]: 
                print("SUCCESSFUL! Improved by", distbefore-distances[0])
                distbefore = distances[0]
            else: print("NO Progress at This Gen")
            print("--------------------------------------------------")
            selected_children=dict()
            for i in range(selection):
                selected_children[distances[i]]=children_in_generation[distances[i]]
        distances = list(children_in_generation.keys())
        distances.sort()
        print("Final Distance was", distances[0])
        order_tobe_saved = selected_children[distances[0]]
        print("ERROR: ", calcdist_total(order_tobe_saved,listholder)-distances[0])
        save_solution(order_tobe_saved, "solution.csv")
        print("The Best Child Safely Stored at Solution.csv. Other Children are Discarded :'(")

    #Chooses two random points. Shuffle them. Calculate the new total distance. Repeat few steps to make children. Choose few of the best children and pass them over to the next generation. Save the newly ordered list if the new distance is shorter than before.
    if mode.lower() =='rs3':
        children = int(input("How many Children from each parent? "))
        selection = int(input("How many best parents passed to next step? "))
        while selection > children**2:
            selection = int(input("You must make more children than the number of children you want to keep. How many best solution to keep in each step again? "))

        children_in_generation = dict()
        for child in range(children*selection):
            index = random.randint(0,len(anslist)-1)
            index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
            buflist[index] = anslist[index2]
            buflist[index2] = anslist[index]
            totaldist2 = distbefore
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

            children_in_generation[totaldist2] = buflist
            buflist = anslist.copy()
        distances = list(children_in_generation.keys())
        distances.sort()
        print("Best Distance at First Gen: ", distances[0])
        if distbefore>distances[0]: 
            print("SUCCESSFUL! Improved by", distbefore-distances[0])
            distbefore = distances[0]
        else: print("No Progress Made at this Gen")
        selected_children=dict()
        for i in range(selection):
            selected_children[distances[i]]=children_in_generation[distances[i]]
        selected_children[distbefore]=anslist
        print("------------------------------------------------------")

        for gen in range(generations-1):
            parents = list(selected_children.keys())
            children_in_generation = dict()
            
            for key in parents:
                anslist = selected_children[key]
                totaldist2 = calcdist_total(selected_children[key], listholder)

                for child in range(children):
                    buflist = anslist.copy()
                    index = random.randint(0,len(anslist)-1)
                    index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
                    buflist[index] = anslist[index2]
                    buflist[index2] = anslist[index]
                    if abs(index-index2)==1:
                        totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                        totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                    else:
                        totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                        totaldist2 -= calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                        totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)-1)]-1])
                        totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)+1)]-1])
                        totaldist2 += calcdist(listholder[anslist[max(index,index2)]-1],listholder[anslist[circ(anslist, min(index,index2)+1)]-1])
                        totaldist2 += calcdist(listholder[anslist[min(index,index2)]-1],listholder[anslist[circ(anslist, max(index,index2)-1)]-1])
                    children_in_generation[totaldist2] = buflist
                    buflist = anslist.copy()
            children_in_generation.update(selected_children)
            distances = list(children_in_generation.keys())
            distances.sort()
            print("Best Distance at",gen+2, "th Gen: ", distances[0])
            if distbefore>distances[0]: 
                print("SUCCESSFUL! Improved by", distbefore-distances[0])
                distbefore = distances[0]
            else: print("NO Progress at This Gen")
            print("--------------------------------------------------")
            selected_children=dict()
            for i in range(selection):
                selected_children[distances[i]]=children_in_generation[distances[i]]
        distances = list(children_in_generation.keys())
        distances.sort()
        print("Final Distance was", distances[0])
        order_tobe_saved = selected_children[distances[0]]
        print("ERROR: ", calcdist_total(order_tobe_saved,listholder)-distances[0])
        save_solution(order_tobe_saved, "solution.csv")
        print("The Best Child Safely Stored at Solution.csv. Other Children are Discarded :'(")

    #Uses Modified Ant Algorithms (The Greedy Ants Colony Algorithm). Starts from the initial tsp file.
    if mode.lower() =='ant':
        generations = int(input("How many Generations? "))
        number_of_ants = int(input("How many ants? "))
        grandlist = dict()
        vertex_number = len(listholder)

        for i in range(vertex_number):
            pherolist=dict()
            for j in range(vertex_number):
                dist = calcdist(listholder[i],listholder[j])
                if i==j: 
                    pheromone = 0
                elif dist==0:
                    pheromone = 0
                else:
                    pheromone = 1000000/dist
                pherolist[j+1]=pheromone
            grandlist[i+1]=pherolist
            print("Grandlist Generatating... ", i+1, "/", len(listholder))
        print("-----------------Grandlist Generation Completed---------------")
        phegrandlist = grandlist.copy()
        for gen in range(generations):
            grandlist = phegrandlist.copy()

            for k in range(number_of_ants):
                remaining_numbers = list(range(1,len(grandlist)+1))
                verystart=0
                while len(remaining_numbers):
                    if verystart==0: 
                        starting_vertex_index = random.randint(0,len(remaining_numbers)-1)
                        starting_vertex=remaining_numbers[starting_vertex_index]
                        thelist = list(grandlist[starting_vertex].values())
                        remaining_numbers.remove(starting_vertex)
                        verystart = starting_vertex
                    else:
                        thelist = list(grandlist[starting_vertex].values())
                        remaining_numbers.remove(starting_vertex)
                    sum_of_pheromones = sum(thelist)
                    probability = list(map(lambda a: a/sum_of_pheromones, thelist))
                    if sum(probability) !=1.0:
                        probability = [x + 1.0-sum(probability) if x == max(probability) else x for x in probability]
                    a = list()
                    for i in range(len(listholder)):
                        a.append(i+1)
                    if len(remaining_numbers)==0:
                        thechosen=verystart
                        
                    else:
                        thechosen = numpy.random.choice(a, p=probability)
                        while not (thechosen) in remaining_numbers:
                            thechosen = numpy.random.choice(a, p=probability)
                    
                    phegrandlist[starting_vertex][thechosen] += 1000000/calcdist(listholder[starting_vertex-1], listholder[thechosen-1])
                    starting_vertex = thechosen
                    # if len(remaining_numbers)==0:
                    #     print("reached very end")
                    #     starting_vertex=verystart
                print("one ant finished tour. killing this ant... INDEX ----", k+1,"/",number_of_ants)
                    
            print("One Ant Generation Finished ", gen+1, "/", generations)
        print("Retrieving the Best Solution Brought by the Ants...")

        list_tobe_saved = list()
        starting_vertex = random.randint(0,vertex_number)
        list_tobe_saved.append(starting_vertex)
        while len(phegrandlist):
            next_vertex = list(max(phegrandlist[starting_vertex].items(), key=operator.itemgetter(1)))[0]
            i=1
            while next_vertex in list_tobe_saved:
                if next_vertex == lastly_added: break
                phegrandlist[starting_vertex].pop(next_vertex)
                next_vertex = list(max(phegrandlist[starting_vertex].items(), key=operator.itemgetter(1)))[0]
                i+=1
            list_tobe_saved.append(next_vertex)
            lastly_added = next_vertex
            phegrandlist.pop(starting_vertex)
            starting_vertex=next_vertex
        list_tobe_saved.pop()
        save_solution(list_tobe_saved, "solution.csv")
        
        print("List Length is", len(list_tobe_saved))
        print("Total Distance is", calcdist_total(list_tobe_saved, listholder))
    # Chooses three random points. Shuffle them. Calculate the new total distance. Save the newly ordered list if the new distance is shorter than before. 
    hello = input("Press Any Key +Enter to Return to Menu.")