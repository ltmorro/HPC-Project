from mpi4py import MPI                                                                   
import itertools                                                                         
comm = MPI.COMM_WORLD                                                                    
rank = comm.Get_rank()                                                                   
size = comm.Get_size()                                                                   
                                                                                         
#Part 1                                                                                  
ids = []                                                                                 
for j in range(0, 500):                                                                  
    if(j % size == rank):                                                                
        if(j>=100):                                                                      
            f = open('/users/ltmorro/job_events/part-00'+str(j)+'-of-00500.csv', "r")    
        elif(j>=10):                                                                     
            f = open('/users/ltmorro/job_events/part-000'+str(j)+'-of-00500.csv', "r")   
        else:                                                                            
            f = open('/users/ltmorro/job_events/part-0000'+str(j)+'-of-00500.csv', "r")  
        for line in f:                                                                   
            id = line.split(',')[2]                                                      
            ids.append(id)                                                               
all_ids = comm.gather(ids, root=0)                                                       
if(rank == 0):                                                                           
    all_ids = list(itertools.chain.from_iterable(all_ids))                               
    all_ids = set(all_ids)                                                               
    print(len(all_ids))                                                                  