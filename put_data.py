import os
import pandas as pd
from db_operations import Db_Opeartions

class Put_Data:

    """
        Method Name: Put_Data
        Description: This method push the data to database.
        Output: Returns a dataframe of user given data.
        On Failure: Raise Exception
         Written By: Hrishikesh Namboothiri.V.N
        """
    
    
    def __init__(self,file_obj,logger_obj):
        
       self.logger_object = logger_obj
       self.file_object = file_obj
       self.db_ops = Db_Opeartions(self.file_object,self.logger_object)
        
    def put_file(self,user_inputs):
        
        cols = ["dteday","season","yr","mnth","holiday","weekday","workingday","weathersit","temp","atemp","hum","windspeed","casual","registered","cnt"]

        self.logger_object.log(self.file_object,"Entered put_file of Put_Data")
        
        try:
            if os.path.isfile("new_day_data.csv"):
                self.logger_object.log(self.file_object,"Found local file to save user given data")
                self.df = pd.DataFrame(user_inputs)
                self.df[cols].to_csv('new_day_data.csv', mode='a', index=False, header=False)
                self.db_ops.data_to_db(user_inputs)
          #      self.logger_object.log(self.file_object,"Pushed data to database and Exits put_file ")
                print("data frame loaded",self.df.head())
                return self.df
                          
        except Exception as e:
            print("Error"+str(e))
            self.logger_object.log(self.file_object,'Exception occured in get_file_to_train method of the Get_Data class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Data Load Unsuccessful.Exited the get_file_to_train method of the Get_Data class')
            raise Exception()