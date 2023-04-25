import json
import os
import redis
import matplotlib.pyplot as plt
import time
from jobs import q, update_job_status, rd, rdimg, rdjobs, _save_job

@q.worker
def execute_job(jid):
    """
    Takes user input and generates a graph based on the data the user wants plotted
    args:
        a string specifying a key to access data corresponding to that key
    returns:
        a string ensuring the graph was made or deleted
    """
    update_job_status(jid, "In Progress")

    #try: 
     
    plot_data = json.loads(rd.get('ast_data'))  
    lists = []
    sorted_data = sorted(plot_data, key=lambda x: float(x['moid_ld']))
    for x in range(len(sorted_data)):
        lists.append(float(sorted_data[x]['moid_ld']))
        
       # if lists == []:
       #     update_job_status(jid, "Error") 
       #     return 0
    try:
        jobdata = rdjobs.hgetall(f'job.{jid}')
        #stored_data = json.loads(rd.get("ast_data")) 
        #stored_data = stored_data[f'{jobdata["end"]}, {jobdata["start"]}']  
        #a_dict = {}  
        #for key, value in jobdata.items(): 
        #    a_dict[key] = value 
        #final = json.dumps(a_dict, indent=4)
        #values = json.loads(final) 
        limit = int(jobdata["end"])
        start = int(jobdata["start"])
        result = []
        for x in range(len(lists)):
            if lists[x] >= limit: 
                break
            elif lists[x] >= start:
                result.append(lists[x]) 
    except ValueError: 
        return "Make sure the number closest and farthest values are numbers\n"  
       # if result == []: 
       #     update_job_status(jid, "error")
       #     return 0

    split = (limit - start)/5 
    range1 = [start,start+split] 
    range2 = [start+split, start+(split+split)] 
    range3 = [start+(split+split),start+(split+split+split)]
    range4 = [start+(split+split+split), start+(split+split+split+split)]  
    range5 = [start+(split+split+split+split),limit] 
    
    count1 = len([i for i in result if range1[0] <= i < range1[1]])
    count2 = len([i for i in result if range2[0] <= i < range2[1]])
    count3 = len([i for i in result if range3[0] <= i < range3[1]])
    count4 = len([i for i in result if range4[0] <= i <= range4[1]])
    count5 = len([i for i in result if range5[0] <= i <= range5[1]])
    # Creating the bar graph
    
    fig, ax = plt.subplots()
    ax.bar([1,2,3,4,5],[count1, count2, count3, count4, count5])
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels([f'{start}-{start+(split)}', f'{start+(split)}-{start+(split+split)}', f'{start+(split+split)}-{start+(split+split+split)}', f'{start+(split+split+split)}-{start+(split+split+split+split)}', f'{start+(split+split+split+split)}-{limit}'])
    ax.set_xlabel('Distance from Earth (AU)')
    ax.set_ylabel('Number of Asteroids') 
    ax.set_title('Number of Asteroids a certain Distance from earth') 
        
        # Create some sample data
    #x = [1, 2, 3, 4, 5]
    #y = [1, 4, 9, 16, 25]

# Create a figure and axis object
    #fig, ax = plt.subplots()

# Plot the data on the axis
    #ax.plot(x, y)

# Set the x and y axis labels
    #ax.set_xlabel('X-axis')
    #ax.set_ylabel('Y-axis')

# Set the title of the plot
    #ax.set_title('Simple Plot') 

    plt.savefig('./asteroid_graph.png')
    file_bytes = open('./asteroid_graph.png', 'rb').read()
    #with open('/asteroid_graph.png', 'rb') as f: 
    #    img = f.read() 
    rdimg.hset(f'job.{jid}', "image", file_bytes) 
    #rdjobs.hset(f'job.{jid}', 'status', 'finished')
    
    update_job_status(jid, "finished")

    time.sleep(5) 
    update_job_status(jid, 'complete') 
    #except:
    #    return 'Load Data\n'

if __name__ == '__main__':
    execute_job()
