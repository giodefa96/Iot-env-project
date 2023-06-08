# import influxdb_client
# from influxdb_client import Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS


# class ClientInfluxDB():
#     def __init__(self, url, token, org, bucket):
#         self.url = url
#         self.token = token
#         self.org = org
#         self.bucket = bucket

#     def connect(self):
#         try:
#             return influxdb_client.InfluxDBClient(
#                 url=self.url, token=self.token, org=self.org, bucket=self.bucket
#             )
#         except Exception as e:
#             print(e)
    
#     def write_single_value(self, value, value_fild_name, *args):
        
#         client = self.connect()
#         write_api = client.write_api(write_options=SYNCHRONOUS)
            
#         point = (
#               Point("measurement1")
#               .tag("tagname1", "tagvalue1")
#               .field(value_fild_name, value)
#             )
#         write_api.write(bucket=self.bucket, org=self.org, record=point)




# class InfluxDBConnection():  #client
#     def __init__(self, url, token, org, bucket):  
#         self.url = url  
#         self.token = token  
#         self.org = org  
#         self.bucket = bucket  
  
#     def connect(self):  
#         try:  
#             return influxdb_client.InfluxDBClient(  
#                 url=self.url, token=self.token, org=self.org, bucket=self.bucket  
#             )  
#         except Exception as e:  
#             print(e)  
  
# class Writer():  
#     def __init__(self, connection):  
#         self.connection = connection  
  
#     def write_single_value(self, value, value_fild_name, *args):  
#         client = self.connection.connect()  
#         write_api = client.write_api(write_options=SYNCHRONOUS)  
              
#         point = (  
#               Point("measurement1")  
#               .tag("tagname1", "tagvalue1")  
#               .field(value_fild_name, value)  
#             )  
#         write_api.write(bucket=self.connection.bucket, org=self.connection.org, record=point)  






# class InfluxDBConnection():  
#     def __init__(self, url, token, org, bucket):  
#         self.url = url  
#         self.token = token  
#         self.org = org  
#         self.bucket = bucket  
  
#     def connect(self):  
#         try:  
#             return influxdb_client.InfluxDBClient(  
#                 url=self.url, token=self.token, org=self.org, bucket=self.bucket  
#             )  
#         except Exception as e:  
#             print(e)  
  
# class InfluxDBWriter():  
#     def __init__(self, connection):  
#         self.connection = connection  
#         self.write_api = connection.connect().write_api(write_options=SYNCHRONOUS)  
              
#     def write_single_value(self, value, value_fild_name, *args):  
#         point = (  
#               Point("measurement1")  
#               .tag("tagname1", "tagvalue1")  
#               .field(value_fild_name, value)  
#             )  
#         self.write_api.write(bucket=self.connection.bucket, org=self.connection.org, record=point)  




# # Initialize the InfluxDB connection  
# connection = InfluxDBConnection(url='', token='', org='', bucket='')  
  
# # Initialize the InfluxDB writer  
# writer = InfluxDBWriter(connection=connection)  
  
# # Write a single value  
# writer.write_single_value(value=42, value_field_name='my-value')  
