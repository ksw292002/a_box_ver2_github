import boto3

def createFileList() :
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    tname = input("Enter User Name :")
    f_name = input("Enter File Name :")
    f_url = input("Enter File URL :")


    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='flist_'+tname,
        KeySchema=[
            {
                'AttributeName': 'f_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'f_url',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'f_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'f_url',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


    # Wait until the table exists.
    print("Wating for creating table")
    table.meta.client.get_waiter('table_exists').wait(TableName='flist_'+tname)

    # Print out some data about the table.
    print("Table created")
    print("count :")
    print(table.item_count)

def uploadFileInfo(fname, furl, username) :
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table(username)

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    print(table.creation_date_time)

    table.put_item(
    Item={
            'f_name': fname,
            'f_url': furl,
        }
    )