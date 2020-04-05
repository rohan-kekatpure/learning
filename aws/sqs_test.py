import boto3
from uuid import uuid4
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue


NUM_MESSAGES = 10000
FEED_IDS = Queue(maxsize=NUM_MESSAGES)


def submit_messages():
    client = boto3.client('sqs')
    queues = client.list_queues(QueueNamePrefix='feed')
    queue_url = queues['QueueUrls'][0]

    for _ in range(NUM_MESSAGES):
        feed_id = uuid4().hex[:8]    
        print(feed_id)
        response = client.send_message(
            QueueUrl=queue_url, 
            MessageBody=feed_id,
            MessageGroupId='feed',
            MessageDeduplicationId=feed_id
        )


def receive_one(n):
    print(n)
    client = boto3.client('sqs')
    queues = client.list_queues(QueueNamePrefix='feed')
    queue_url = queues['QueueUrls'][0]
    # print('here > ' + n)

    response = client.receive_message(QueueUrl=queue_url, WaitTimeSeconds=2)        
    # print(json.dumps(response, indent=2))
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    body = message['Body']            


    FEED_IDS.put_nowait(body)        
    

if __name__ == '__main__':
    # submit_messages()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(1000):            
            executor.submit(receive_one, i)        

    qsize = FEED_IDS.qsize()
    while not FEED_IDS.empty():
        print(FEED_IDS.get())

    print(qsize)
