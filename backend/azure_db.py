from azure.cosmos import CosmosClient

COSMOS_URI = "https://smartcropcosmos.documents.azure.com:443/"
COSMOS_KEY = "<67wShnIVRhHzH3tXCO4vZS0dR02RgnN2UQbXPsnoxVsIuKsuy1VGHCt2B60tyU8XWBw6L3BkiOXgACDbl46Tcw==>"

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client("smartcrop")
container = database.get_container_client("sensordata")

def save_sensor_data(data):
    container.create_item(body=data)
