""" InfluxDB Singleton Class """
from influxdb import InfluxDBClient
import os
from dotenv import load_dotenv
load_dotenv()
class InfluxDBLog:  
    singleton = None 
    client_influxDB = None 

    def __new__(cls, *args, **kwargs):  
        if not cls.singleton:  
            cls.singleton = object.__new__(InfluxDBLog)  
        return cls.singleton  

    def __init__(self):
        self.client_influxDB = InfluxDBClient(os.getenv("INFLUXDB_SERVER"),
                                                os.getenv("INFLUXDB_PORT"),
                                                os.getenv("INFLUXDB_USERNAME"),
                                                os.getenv("INFLUXDB_PASSWORD"),
                                                os.getenv("INFLUXDB_DB"))


    def addEntry(self, measurement, tag_name, tag_value, field1_name, field1_value):
        if self.client_influxDB is not None:
            json_body = [
                    {
                        "measurement": measurement,
                        "tags": {
                            tag_name: tag_value
                        },
                        "fields": {
                            field1_name: field1_value,
                            
                        }
                    }]
            self.client_influxDB.write_points(json_body)

   