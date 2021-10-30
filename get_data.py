import os
import pandas as pd
from db_operations import Db_Opeartions

class Get_Data:
    
    """
    This class shall  be used for obtaining the data from the source for training.

    Written By: Hrishikesh Namboothiri.V.N

    """
    
    
    def __init__(self,file_object,logger_object):
        
        self.logger_object = logger_object
        self.file_object = file_object
        db_ops = Db_Opeartions(self.file_object, self.logger_object)
        self.file_name = db_ops.data_from_db()
        print(self.file_name)
        self.features = ['dteday','season','yr','mnth','holiday','weekday','workingday','weathersit','temp','atemp','hum','windspeed','casual','registered','cnt']
    def get_file(self):
        
        """
        Method Name: get_file
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

         Written By: Hrishikesh Namboothiri.V.N
        """
        self.logger_object.log(self.file_object,"Entered get_file_to_train of Get_Data")
        
        try:
            if os.path.isfile(self.file_name):
                self.logger_object.log(self.file_object,"Found new file.")
                self.df = pd.read_csv(self.file_name)
                self.logger_object.log(self.file_object,"Collected data from source and Exit Get_Data")
                print("data frame loaded",self.df.head())
                return self.df
                          
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in get_file_to_train method of the Get_Data class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Data Load Unsuccessful.Exited the get_file method of the Get_Data class')
            raise Exception()