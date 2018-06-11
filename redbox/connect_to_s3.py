import boto3

# Boto 3 - S3
s3 = boto3.resource('s3')

bname = input("Enter Bucket name :")

# s3.create_bucket(Bucket=bname)
s3.create_bucket(Bucket=bname, CreateBucketConfiguration={
    'LocationConstraint': 'us-west-2'})

