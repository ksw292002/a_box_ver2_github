import boto3

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