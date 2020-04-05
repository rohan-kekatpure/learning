# INSTRUCTIONS
# 1. Install Redis locally
#     $ brew install redis
#
# 2. Install python redis client
#     $ pip install redis
#
# 3 Start Redis server
#     $ brew services start redis
# 
# 4. Run the following code

import redis
import numpy as np
from uuid import uuid4

N_VGG = 4096

def get_features():    
    r = np.random.normal(size=(N_VGG, ))
    return np.around(r, 2)


def get_job_id():
    return uuid4().hex[:8]


def main():
    # Redis connection
    config = {'host': 'localhost', 'port': 6379}
    client = redis.Redis(**config)
    client.flushall()

    # Keys for arrays holding job_id and binarized feature-vector values
    key_job_ids = 'job_id'
    key_features = 'features'

    # Push to job_ids and feature vectors to respective redis arrays
    for _ in range(5):    
        job_id = get_job_id()        
        v = get_features()

        client.lpush(key_job_ids, job_id)
        client.lpush(key_features, v.tobytes())

    # Retrieve list of keys and construct numpy array from values
    job_ids = client.lrange(key_job_ids, 0, -1)
    job_ids = [j.decode('ascii') for j in job_ids]

    features_binary = client.lrange(key_features, 0, -1)
    features = np.zeros(shape=(len(features_binary), N_VGG))

    for i, row in enumerate(features_binary):
        v = np.frombuffer(row)
        features[i] = v

    # Compute Euclidean distance exhaustively
    new_image = get_features()  # proxy for new job
    distances = np.linalg.norm(features - new_image, axis=1)
    closest_match = job_ids[distances.argmin()]

    print(job_ids)
    print(distances)
    print('closest_match = ', closest_match)


if __name__ == '__main__':
    main()


