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

#the modified ant colony optimisation
def ant_colony_optimise(anslist, listholder, generations, number_of_ants, pheromone_from_beforelife):
    phegrandlist = dict()
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
                pheromone = 100/dist
            pherolist[j+1]=pheromone
        phegrandlist[i+1]=pherolist
        # print("Grandlist Generatating... ", i+1, "/", len(listholder))
    # print("-----------------Grandlist Generation Completed---------------")
    
    for i in range(len(anslist)):
        if i==len(anslist)-1:
            phegrandlist[anslist[i]][anslist[0]]*=pheromone_from_beforelife
        else:
            phegrandlist[anslist[i]][anslist[i+1]]*=pheromone_from_beforelife

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
                
                phegrandlist[starting_vertex][thechosen] += 100/calcdist(listholder[starting_vertex-1], listholder[thechosen-1])
                starting_vertex = thechosen
                # if len(remaining_numbers)==0:
                #     print("reached very end")
                #     starting_vertex=verystart  
        # print("One Ant Generation Finished ", gen+1, "/", generations)

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
    return list_tobe_saved

#Chooses two random points. Shuffle them. Calculate the new total distance. Repeat few steps to make children. Choose few of the best children and pass them over to the next generation. Save the newly ordered list if the new distance is shorter than before.
def random_point2(anslist, listholder, generations, ran, children, selection, distbefore):
    buflist = anslist.copy()
    while selection > children**2:
        selection = int(input("You must make more children than the number of children you want to keep. How many best solution to keep in each step again? "))

    children_in_generation = dict()
    # the first swap
    for child in range(children*selection):
        index = random.randint(0,len(anslist)-1)
        index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
        buflist[index] = anslist[index2]
        buflist[index2] = anslist[index]
        totaldist2 = distbefore
        #Swap Distance Calculation Method
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
    distances = list(children_in_generation.keys())
    distances.sort()
    if distbefore>distances[0]: 
        distbefore = distances[0]
    selected_children=dict()
    for i in range(selection):
        selected_children[distances[i]]=children_in_generation[distances[i]]
    selected_children[distbefore]=anslist
    # from second generation.
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
        if distbefore>distances[0]: 
            distbefore = distances[0]
        selected_children=dict()
        for i in range(selection):
            selected_children[distances[i]]=children_in_generation[distances[i]]
    distances = list(children_in_generation.keys())
    distances.sort()
    return selected_children[distances[0]]

#Chooses Three random points and shuffle them
def random_point3(anslist, lisholder,generations, ran, children, selection, distbefore):
    while selection > children**2:
        selection = int(input("You must make more children than the number of children you want to keep. How many best solution to keep in each step again? "))
    buflist = anslist.copy()
    children_in_generation = dict()
    # The first generation
    for child in range(children*selection):
        index = random.randint(0,len(anslist)-1)
        index2 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
        buflist[index] = anslist[index2]
        buflist[index2] = anslist[index]
        totaldist2 = distbefore
        # The first Swap
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
        buflist2=buflist.copy()
        index3 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
        while index3 == index:
            index3 = random.randint(max(0,index-ran), min(index+ran,len(anslist)-1))
        buflist2[index3] = buflist[index2]
        buflist2[index2] = buflist[index3]
        # The Second Swap.
        if abs(index3-index2)==1:
            totaldist2 -= calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)-1)]-1])
            totaldist2 -= calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)+1)]-1])
            totaldist2 += calcdist(listholder[buflist[max(index3,index2)]-1],listholder[buflist[circ(anslist, min(index3,index2)-1)]-1])
            totaldist2 += calcdist(listholder[buflist[min(index3,index2)]-1],listholder[buflist[circ(anslist, max(index3,index2)+1)]-1])
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
    if distbefore>distances[0]: 
        distbefore = distances[0]
    selected_children=dict()
    for i in range(selection):
        selected_children[distances[i]]=children_in_generation[distances[i]]
    selected_children[distbefore]=anslist
    # from the Second generation
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
        if distbefore>distances[0]: 
            distbefore = distances[0]
        selected_children=dict()
        for i in range(selection):
            selected_children[distances[i]]=children_in_generation[distances[i]]
    distances = list(children_in_generation.keys())
    distances.sort()
    return selected_children[distances[0]]

#Checks if a solution file with the name 'solfile' exists
def file_exist(solfile):
    with open(solfile, "a+") as sol:
        sol.seek(0)
        if sol.read() == "": 
            return False
        return True 

# Reads through the tsp file given in the second argument in the system call.
    # (For example, 'burma14.tsp' in 'python solver.py burma14.tsp')
    # Stores its information as list of tuples: {id, x_coordinate, y_coordinate} with the name 'listholder'
listholder = parse_initial(sys.argv[1])

ant_gen = 3 #-ag
ants = 3 #-an

children = 5 #-p, -p2
selection = 3 #-s, -s2
generations = 4000 #-g, -g2
ran = 5 #-r, -r2    

children3 = 5 #-p, -p3
selection3 = 3 #-s, -s3
generations3 = 4000 #-g, -g3
ran3 = 5 #-r, -r3

m = 0

total_generation_number = 10 #-f
pheromone_from_beforelife = 5

if "-p" in sys.argv:
    children = int(sys.argv[sys.argv.index("-p")+1])
    children3 = children
if "-p2" in sys.argv:
    children = int(sys.argv[sys.argv.index("-p2")+1])
if "-p3" in sys.argv:
    children3 = int(sys.argv[sys.argv.index("-p3")+1])
if "-f" in sys.argv:
    total_generation_number = int(sys.argv[sys.argv.index("-f")+1])

if "-ag" in sys.argv:
    ant_gen = int(sys.argv[sys.argv.index("-ag")+1])
if "-an" in sys.argv:
    ants = int(sys.argv[sys.argv.index("-an")+1])
if "-s" in sys.argv:
    selection = int(sys.argv[sys.argv.index("-s")+1])
    selection3 = selection
if "-s2" in sys.argv:
    selection = int(sys.argv[sys.argv.index("-s2")+1])
if "-s3" in sys.argv:
    selection3 = int(sys.argv[sys.argv.index("-s3")+1])
if "-g" in sys.argv:
    generations = int(sys.argv[sys.argv.index("-g")+1])
    generations3 = generations
if "-g2" in sys.argv:
    generations = int(sys.argv[sys.argv.index("-g2")+1])
if "-g3" in sys.argv:
    generations3 = int(sys.argv[sys.argv.index("-g3")+1])

if "-r" in sys.argv:
    ran = int(sys.argv[sys.argv.index("-r")+1])
    ran3 = ran
if "-r2" in sys.argv:
    ran = int(sys.argv[sys.argv.index("-r2")+1])
if "-r3" in sys.argv:
    ran3 = int(sys.argv[sys.argv.index("-r3")+1])
if "-m" in sys.argv:
    m = int(sys.argv[sys.argv.index("-m")+1])
if "-phbf" in sys.argv:
    pheromone_from_beforelife = int(sys.argv[sys.argv.index("-phbf")+1])

points_num = len(listholder)



###############################################################

if file_exist("solution.csv"):
    anslist = parse_solution("solution.csv")
    if len(anslist) != len(listholder):
        anslist = []
        if m: print("Solution.csv detected for TSP set of other length. Erasing This file and Initialising... ")
    else:
        if m: print("Solution.csv detected. Optimisation Will begin from this file.")
else:
    anslist = []
    if m: print("Solution.csv Not detected. Initialising...")

for grand_generation in range(total_generation_number):
    anslist = ant_colony_optimise(anslist, listholder, ant_gen, ants, pheromone_from_beforelife)
    antdist = calcdist_total(anslist,listholder)
    if m: print("[",grand_generation,"] AntCompleted")
    if grand_generation ==0:
        mindist= antdist
        save_solution(anslist, "solution.csv")
        if m: print("Saving Solution", mindist)
    elif antdist < mindist:
        if m: print("Distance Shortened. Saving Solution", antdist)
        mindist = antdist
        save_solution(anslist, "solution.csv")
    
    distbefore = antdist
    anslist = random_point2(anslist,listholder,generations,ran,children,selection, distbefore)
    rs2dist = calcdist_total(anslist,listholder)
    if m: print("[",grand_generation,"] RS2 Completed")
    if rs2dist < mindist:
        if m: print("Distance Shortened. Saving Solution", rs2dist)
        mindist = rs2dist
        save_solution(anslist, "solution.csv")
    

    anslist = random_point3(anslist,listholder,generations3,ran3,children3,selection3, distbefore)
    rs3dist = calcdist_total(anslist,listholder)
    if m: print("[",grand_generation,"] RS3 Completed")
    if rs3dist < mindist:
        if m: print("Distance Shortened. Saving Solution", rs3dist)
        mindist=rs3dist
        save_solution(anslist, "solution.csv")
    
print(calcdist_total(anslist, listholder))
