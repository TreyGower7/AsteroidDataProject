import uuid
from hotqueue import HotQueue
import redis
import os

redis_ip = os.environ.get('REDIS_HOST')


rd = redis.Redis(host = redis_ip, port=6379, db=0)
rdimg = redis.Redis(host = redis_ip, port=6379, db=1)
rdjobs = redis.Redis(host= redis_ip, port=6379, db=2, decode_responses=True)
q = HotQueue("queue", host= redis_ip, port=6379, db=3)

def get_job_by_id(jid):
    #jid, status, start, end = rdjobs.hmget(generate_job_key(jid), 'jid', 'status', 'start', 'end') 
    #job = _instantiate_job(jid, status, start, end) 
    job = rdjobs.hgetall(generate_job_key(jid)) 
    return job

def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)

def _instantiate_job(jid: str, status: str, start: str, end: str):
    """
    Create the job object description as a python dictionary. Requires the job id, status,
    start and end parameters.
    """
    if type(jid) == str:
        return {'id': jid,
              'status': status,
              'start': start,
              'end': end
        }
    #return {'id': jid.decode('utf-8'),
    #      'status': status.decode('utf-8'),
    #      'start': start.decode('utf-8'),
    #      'end': end.decode('utf-8')
    #}

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rdjobs.hset(job_key,mapping = job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid) 

def add_job(start, end, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, start, end)
    _save_job(generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        _save_job(generate_job_key(jid), job)
    else:
        raise Exception()
