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

    try:
        plot_data = json.loads(rd.get('ast_data'))  
        lists = []
        sorted_data = sorted(plot_data, key=lambda x: float(x['moid_ld']))
        for x in range(len(sorted_data)):
    	    lists.append(float(sorted_data[x]['moid_ld']))
        try:
            jobdata = rdjobs.hgetall(jid)
            limit = jobdata['end'] 
            start = jobdata['start']
            result = []
            for x in range(len(lists)):
                if lists[x] >= limit: 
                    break
                elif lists[x] >= start:
                    result.append(lists[x]) 
        except ValueError: 
            return "Make sure the number closest and farthest values are numbers\n"  
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
        plt.savefig('asteroid_graph.png')
        file_bytes = open('./asteroid_graph.png', 'rb').read()
        
        rdimg.set('image', file_bytes)
        return 'Image is Posted\n'
    except TypeError: 
        return "Make sure the data has been posted\n" 
    except NameError:
        return "Make sure the data has been posted\n"
    
    update_job_status(jid, "Completed")

execute_job()
