import boto3

from aarwild_utils.io import S3Connection

bucket_name = 'arinthewild'
object_name = 'jobs/261f91d9/source.jpg'
expiration = 60 

def create_presigned_url(bucket_name, object_name, expiration=3600):    
    s3_client = boto3.client('s3')

    params = {
        'Bucket': bucket_name,
        'Key': object_name
    }

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params=params,
            ExpiresIn=expiration
        )

    except ClientError as e:
        logging.error(e)        
        return
    
    return response


def test_create_presigned_url():
    presigned_url = create_presigned_url(bucket_name, object_name, expiration=expiration)
    print('url -:> {}'.format(presigned_url))


def test_get_presigned_url():
    s3 = S3Connection()
    url = s3.get_presigned_url(bucket_name, object_name, expiration=60)
    print(url)


if __name__ == '__main__':
    test_get_presigned_url()