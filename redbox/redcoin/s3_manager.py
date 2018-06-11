import boto3


# username 받아서 해당 이름의 bucket을 만든다.
def createUserBucket(username) :
    # Boto 3 - S3
    s3 = boto3.resource('s3')

    s3.create_bucket(Bucket=username, CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})


# form으로 받아온 file name과 url을 이용하여 S3에 업로드.
def uploadFile(username, fname, furl) :
    
    # Boto 3 - S3
    s3 = boto3.resource('s3')

    # username이라는 이름을 가진 버킷에 fname으로 저장.
    # 세부 정보는 뒤에...
    s3.Object(username, fname).put(Body=open(furl, 'rb'))