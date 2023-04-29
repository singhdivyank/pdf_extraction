"""
connect to AWS services- Textract and DynamoDB
"""

# required imports
import boto3

from datetime import datetime

# import constants
from config import (
    DYNAMODB_TABLES, 
    DYNAMODB_THROUGHPUT
)

def textract_extraction(bytes):
    """
    apply detect_document_text API to 
    detect text in invoice file line-by-line
    :param bytearray bytes: the image as binary

    return: string
    """

    extracted_text = ""

    try:
        client = boto3.client('textract')
        # get response from textract API
        response = client.detect_document_text(
            Document = {
                'Bytes': bytes,
            }
        )

        detected_blocks = response.get('Blocks', [])
        detected_blocks = sorted(detected_blocks, key=lambda x: x['confidence'])
        for _, block in enumerate(detected_blocks):
            if block.get('BlockType', '').lower() == 'line' and block.get('Confidence')>=98:
                extracted_text = extracted_text + " " + block.get('Text')
    except Exception as error:
        print(f"textract_extraction :: Exception :: {str(error)}")
    
    return extracted_text
    
def dynamodb_func(table_dict, file_name, file_type):
    """
    save results to DynamoDB table
    :param dict table_dict: results to update
    :param string file_name: name of file
    :param string file_type: the type of file (resume/kyc/invoice)
    """

    def create_table(table_name):
        """
        create DynamoDB table
        :param string table_name: name of table
        """

        table = dynamodb_client.create_table(
            TableName = table_name,
            KeySchema = [
                {
                    'AttributeName': 'file_name',
                    'KeyType': 'HASH' # Partition Key
                },
                {
                    'AttributeName': 'updated_at',
                    'KeyType': 'RANGE' # Sort Key
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'file_name',
                    'AttributeType': 'S'
                }, 
                {
                    'AttributeName': 'updated_at',
                    'KeyType': 'S'
                }
            ],
            ProvisionedThroughput = DYNAMODB_THROUGHPUT
        )
        return table

    try:
        dynamodb_client = boto3.resource('dynamodb')
        table = dynamodb_client.Table(DYNAMODB_TABLES.get(file_type))

        # create table if it does not exist
        if table.item_count:
            table = create_table(table)
        
        # update table attributes
        timestamp = str(datetime.now())
        table.put_item(Item={'file_name': file_name, 'updated_at': timestamp})
        for key in table_dict:
            table.put_item(Item={key: table_dict.get(key)})
    except Exception as error:
        print(f"dynamodb_func :: Exception :: {str(error)}")
