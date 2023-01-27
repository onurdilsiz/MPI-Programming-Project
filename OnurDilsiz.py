# Student Name: Onur Dilsiz
# Student Number: 2019400036
# Compile Status: Compiling
# Program Status: Working
from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if "--input_file" in sys.argv:
  # Get the index of the argument
  index = sys.argv.index("--input_file")
  # Get the value of the argument
  inputfile = sys.argv[index + 1]



if "--merge_method" in sys.argv:
  # Get the index of the argument
  index = sys.argv.index("--merge_method")
  # Get the value of the argument
  merge_method = sys.argv[index + 1]
  

if "--test_file" in sys.argv:
  # Get the index of the argument
  index = sys.argv.index("--test_file")
  # Get the value of the argument
  testfile = sys.argv[index + 1]


#counts unigrams for a worker
def countUni(linesOfWorker):
    unidictWorker={}
    
    for i in range(len(linesOfWorker)):
        liste =linesOfWorker[i].split()
        
        for i in liste:
            if(i in unidictWorker.keys()):
                unidictWorker[i]+= 1
            else:
                unidictWorker[i]=1
    return unidictWorker

#count bigrams
def splitBi(linesOfWorker):
    bigrams=[]
    bigramDict={}

    for i in range(len(linesOfWorker)):
        splitted = linesOfWorker[i].split()
        #print(splitted)
        for i in range(len(splitted)-1):
            bigram=splitted[i]+" "+splitted[i+1]
            #print(bigram)
            bigrams.append(bigram)
            if(bigram in bigramDict.keys()):
                bigramDict[bigram]+=1

            
            else:
                bigramDict[bigram]=1
    return bigramDict


#divides lines to processes
def divider(lines,noOfProcesses):

    length=len(lines)
    sendList=[[] for i in range(noOfProcesses)]

    for i in range(length):
        lines[i]=lines[i].rstrip()

        sendList[i%noOfProcesses].append(lines[i])
    return(sendList)



if rank == 0:
    with open(inputfile, "r", encoding="utf8") as f:
  # Read the contents of the file
        lines = f.readlines()

    # REQUIREMENT 1
    sendList = divider(lines,size-1)
    
    # sends data to workers
    for i in range(1,size):
        comm.send(sendList[i-1], dest=i, tag=11)
    

    # REQUIREMENT 2
    #receive and merge dicts
    if merge_method=="MASTER":
        bigramDict={}
        unigramDict={}
        for i in range(1,size):
            data = comm.recv(source=i, tag=11)
            unidictWorker =data[0]
            bigramDictWorker =data[1]
            for i in unidictWorker.keys():
                if(i in unigramDict):
                    unigramDict[i] += unidictWorker[i]
                else:
                    unigramDict[i] = unidictWorker[i]
            
            for i in bigramDictWorker.keys():
                if(i in bigramDict):
                    bigramDict[i] += bigramDictWorker[i]
                else:
                    bigramDict[i] = bigramDictWorker[i]

    elif merge_method=="WORKERS":
        data = comm.recv(source=size-1,tag=11)
        unigramDict=data[0]
        bigramDict=data[1]


    #calculation of conditional probabilities
    with open(testfile, "r", encoding="utf8") as f:
        tests=f.readlines()
    for i in tests:
        i=i.rstrip()
        unigrams=i.split()
        print(i,":",bigramDict[i]/unigramDict[unigrams[0]])
    

    #print(unigramDict)
        

#Worker processes    
else:
    #receives and counts
    data = comm.recv(source=0, tag=11)
    print("rank:",rank, "number of sentences:",len(data))
    
    unidictWork=countUni(data)
    bigramDictWork=splitBi(data)

    if merge_method=="MASTER":
        #sends dictionaries together
        comm.send([unidictWork,bigramDictWork],dest=0, tag=11)
        # comm.send(bigramDictWork,dest=0, tag=11)



    elif merge_method=="WORKERS":
        if rank==1:
            comm.send([unidictWork,bigramDictWork],dest=rank+1,tag=11)
            
        for i in range(2,size):
            if rank==i:  
                data=comm.recv(source=rank-1,tag=11)
                unidict=data[0]
                bigramDict=data[1]
                for i in unidict.keys():
                    if(i in unidictWork):
                        unidictWork[i] += unidict[i]
                    else:
                        unidictWork[i] = unidict[i]
                
                for i in bigramDict.keys():
                    if(i in bigramDictWork):
                        bigramDictWork[i] += bigramDict[i]
                    else:
                        bigramDictWork[i] = bigramDict[i]
          
                if rank!=(size-1):
                 
                    comm.send([unidictWork,bigramDictWork],dest=rank+1,tag=11)
                 
                else:
                    comm.send([unidictWork,bigramDictWork],dest=0,tag=11)
        