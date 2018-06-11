import boto3


# username 받아서 해당 이름의 bucket을 만든다.
def createUserBucket(username) :
    # Boto 3 - S3
    s3 = boto3.resource('s3')

    s3.create_bucket(Bucket=username, CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})
