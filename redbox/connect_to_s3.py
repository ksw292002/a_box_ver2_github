import boto3

# Boto 3 - S3
s3 = boto3.resource('s3')


def createBucket() :
    bname = input("Enter Bucket name :")

    # s3.create_bucket(Bucket=bname)
    s3.create_bucket(Bucket=bname, CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})

def downFiles() :
    # username = input("Enter user name : ")
    username = 'user004'
    # fname = input("Enter file name : ")
    fname = 'wwdc-20181.jpg'
    url = '{}/{}/{}'.format('http://s3-us-west-2.amazonaws.com', username, fname)
    print(url)

