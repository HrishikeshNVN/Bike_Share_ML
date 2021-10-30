from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import PreparedStatement
from cassandra.query import SimpleStatement, BatchStatement
from numpy import dtype
import pandas as pd
import os


class Db_Opeartions:
    
    def __init__(self,file_obj,logger_obj):
        
        self.file_obj = file_obj
        self.logger_obj = logger_obj
        pass
        
    def connect_db(self):


        """
                Method Name: connect_db
                Description: This method establishe connection with cassandra database.
                Output: Returns file name of the collected data..
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
        """

        self.logger_obj.log(self.file_obj,"\n Entered into connect_db function of Db_Opeartions class \n")
                
        try:
            cloud_config= {
                    'secure_connect_bundle': 'database_folder/secure-connect-bike-sharing-db.zip'
            }
            auth_provider = PlainTextAuthProvider('JKnSZtdNaTzZnheBJnUvWeXF','k.28ghFcfhf0mn+-PXEz5YJWK2dZB-+QaqLTs2OyOKkR,NF5p-XtPlRXY0zrJAdy-8+4JDyFY.h7+A_OtAqIsZNZvulM5WNBAv9.S6NtxXXoWzUlHQB7Pm99d10k0US.')
           
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            row = session.execute("select release_version from system.local").one()
            if row:
                print(row[0])
            else:
                print("An error occurred.")
            return session
        except Exception as e:
                self.logger_obj.log(self.file_obj,"\n Error occured while connecting with database \n"+str(e))
                print("ERROR FROM DB....."+str(e))



    def data_to_db(self,user_inputs):

        #Establishes connection with database
        session = self.connect_db()

        self.logger_obj.log(self.file_obj,"\n Entered into data_to_db function of Db_Opeartions class \n")
          

        try:

            val = []
            for i,j in enumerate(user_inputs[0].items()):
                val.append(j[1])
            print(val)
            t = tuple(val)

            row = session.execute("""SELECT table_name  FROM system_schema.tables WHERE keyspace_name='bike_sharing';""")
            table_name = []
            for i in row:
                table_name.append(i[0])

            if "new_day" in table_name:
                ## If table exists insert the data
                session.execute("""insert into bike_sharing.new_day(dteday,season,yr,mnth,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,casual,registered,cnt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",t)
          
            else:
            ##As table does not exit we creates and insert value
                session.execute("""create table bike_sharing.new_day(dteday text,season int,yr int,mnth int,holiday int,weekday int,workingday int,weathersit int,temp decimal,atemp decimal,hum decimal,windspeed decimal,casual int,registered int,cnt int,PRIMARY KEY(dteday))""")
                session.execute("""insert into bike_sharing.new_day(dteday,season,yr,mnth,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,casual,registered,cnt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",t)
            self.logger_obj.log(self.file_obj,"\n User given data entered successfdully to database. \n")
            return print("Data entered successfully")
        except Exception as e:
            print("eRROR"+str(e))
            self.logger_obj.log(self.file_obj,"error occured at db_input_predicted_data method in db_operations module \n"+str(e))
            raise Exception()



    def data_from_db(self):

        self.logger_obj.log(self.file_obj,"\n Entered into data_from_db function to collect data \n")
                
        try:
            df = pd.DataFrame()
            session = self.connect_db()
            print(session)
            for row in session.execute('SELECT * FROM bike_sharing.day;'):
                df = df.append(pd.DataFrame(row , index=row._fields).transpose())
            df
            df.to_csv("csv_files/day.csv")
            return "csv_files/day.csv"
        except Exception as e:
                self.logger_obj.log(self.file_obj,"\n Error occure while downloading data from database \n"+str(e))
                print("ERROR FROM DB....."+str(e))

