import boto3
from boto3.dynamodb.conditions import Key
from typing import Any, Dict, Union
from surf_data import DynamoDBConfig


DDB_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"



class SurfDiaryDB():
    def __init__(self):
        self.TABLE_NAME = DynamoDBConfig.TABLE_NAME
        self.ddb = boto3.resource(
            'dynamodb',
            region_name=DynamoDBConfig.REGION
        )

    def persist_entry(self, args: Dict[str, Union[str, float]]):
        tb = self.ddb.Table(self.TABLE_NAME)
        return tb.put_item(**args)
    
    def get_latest_entry(self, surf_spot: str) -> Dict[str, Any]:
        """
        Returns the latest entry rocorded for the given spot.
        """
        tb = self.ddb.Table(self.TABLE_NAME)
        resp = tb.query(
            Select='ALL_ATTRIBUTES',
            Limit=1,
            ConsistentRead=False,
            ScanIndexForward=False,
            KeyConditionExpression=Key(DynamoDBConfig.PARTITION_KEY).eq(surf_spot)
        )
        return resp["Items"][0]
