import os
import boto3
from uuid import uuid4
import logging as log

def get_todo_db():
    _DB = DynamoDBTodo(
        boto3.resource('dynamodb').Table(
            os.environ['TODOS_TABLE_NAME'])
    )
    return _DB

def check_dynamodb_table_exists(table_name):
    client = boto3.client('dynamodb')
    response = client.list_tables()
    if table_name in response['TableNames']:
        return True
    return False

def init_api_table_dynamodb():
    table_name = os.getenv('TODOS_TABLE_NAME')
    reset_table_startup = True if os.getenv('RESET_TODO_TABLE_ON_STARTUP').lower()=="yes" else False
    
    if (check_dynamodb_table_exists(table_name) & reset_table_startup):
        log.info("Reset TODOS table from Dynamodb...")
        table = boto3.resource('dynamodb').Table(table_name)
        table.delete()
        table.wait_until_not_exists()

    if (not check_dynamodb_table_exists(table_name)):
        client = boto3.client('dynamodb')
        key_schema = [
            {
                'AttributeName': 'uid',
                'KeyType': 'HASH',
            }
        ]
        attribute_definitions = [
            {
                'AttributeName': 'uid',
                'AttributeType': 'S',
            }
        ]

        client.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )
        waiter = client.get_waiter('table_exists')
        waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
        log.info('New table created: %s'%(table_name))
    return table_name


class DynamoDBTodo(object):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def add_item(self, title, description=''):
        uid = str(uuid4())
        self._table.put_item(
            Item={
                'uid': uid,
                'title': title,
                'description': description
            }
        )
        return uid

    def get_item(self, uid):
        response = self._table.get_item(
            Key={
                'uid': uid,
            },
        )
        return response['Item']

    def delete_item(self, uid):
        self._table.delete_item(
            Key={
                'uid': uid,
            }
        )

    def update_item(self, uid, title=None, description=None):
        item = self.get_item(uid)
        if title is not None:
            item['title'] = title
        if description is not None:
            item['description'] = description
        self._table.put_item(Item=item)
