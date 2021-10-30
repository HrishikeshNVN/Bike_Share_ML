import pandas as pd
import numpy as np
import datetime
from get_data import Get_Data
from logger import App_Logger


class Pre_Process_data:

    """
                Class Name: Pre_Process_data
                Description: This class performs all data preprocessing methods..
                Output: Pre processed data in the form of dapendent and independent.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
    """


    
    def __init__(self,file_obj,logger_obj):

        self.file_obj = open("logs","a")
        self.logger_obj = App_Logger()
        self.logger_obj = logger_obj
        self.file_obj=file_obj
        self.logger_obj.log(self.file_obj,"Entered to Pre_Process_data Class")
        gd = Get_Data(self.file_obj,self.logger_obj)
        self.df = gd.get_file()
    
    def get_processesd(self):
        self.logger_obj.log(self.file_obj,'Entered get_processesd of  Pre_Process_data class')

        try:
        
            self.encode_categorical_features()
            self.casual_reg_prob()
            self.remove_no_use_cols()
            self.outlier_removal()
            self.dep_indep_seperator()
            self.logger_obj.log(self.file_obj,'Successfully completed data pre processing')
            return self.X,self.y
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured while getting pre_processed data '+str(e))
            self.logger_obj.log(self.file_obj,'Data pre processing unsuccessful.Exited get_processesd of Pre_process_data class')
            raise Exception()

    
    def encode_categorical_features(self):

        self.logger_obj.log(self.file_obj,"Strated encoding /n")

        wether_dict = {1:"Clear/Fewclouds", 2:"Mist/Cloudy" , 3:"LightSnow/LightRain", 4:"HeavyRain"}
        season_dict = {1:"winter", 2:"spring", 3:"summer", 4:"fall"}
        weekday_dict = {6:"Sunday",0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday"}

        try:
            self.df["date"] = pd.DatetimeIndex(self.df["dteday"])
            self.df["day"] = pd.DatetimeIndex(self.df["date"]).day
            self.df["month"] = pd.DatetimeIndex(self.df["date"]).month_name()
            self.df["year"] = pd.DatetimeIndex(self.df["date"]).year

            self.df["weathersit"].replace(wether_dict, inplace=True)
            self.df["season"].replace(season_dict, inplace=True)
            self.df["weekday"].replace(weekday_dict, inplace=True)

            self.df["jul_sep_jun_aug"] = self.df["month"].apply(lambda month : 1 if month in ["July","August","September"] else 0)
            self.df["oct_may"] = self.df["month"].apply(lambda month : 1 if month in ["October","May"] else 0)
            self.df["dec_mar_nov_apr"] = self.df["month"].apply(lambda month : 1 if month in ["December","March","November","April"] else 0)
            self.df["jan_feb"] = self.df["month"].apply(lambda month : 1 if month in ["January","February"] else 0)

            self.df = self.encoding_fn('season')
            self.df = self.encoding_fn('weekday')
            self.df = self.encoding_fn('weathersit')
            self.logger_obj.log(self.file_obj,"encoded categorical values successfully.... /n")

        
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured in encode_categorical_features of Pre_process data class. Exception message: '+str(e))
            self.logger_obj.log(self.file_obj,'encode_categorical_features unsuccessful.Exited encode_categorical_features of Pre_process data class')
            raise Exception()




    def encoding_fn(self,feature):
        tdf = pd.get_dummies(self.df[feature], drop_first=True)
        self.df.drop(feature, axis=1, inplace=True)
        return pd.concat([self.df,tdf], axis=1)

    def remove_no_use_cols(self):
        self.logger_obj.log(self.file_obj,"Started to remove no_use_cols.... /n")

        try:

            self.logger_obj.log(self.file_obj,"Removed  features /n")
            self.df.drop(labels=["dteday","mnth","date","month","year","instant","casual","registered","atemp"], axis=1, inplace=True)
#        return self.df
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Exception occured while removing no use cols...... /n"+str(e))
            self.logger_obj.log(self.file_obj,"Unsuccessful feature removal .... /n")
            raise Exception()


    def dep_indep_seperator(self):
        self.logger_obj.log(self.file_obj,"Started dependent independent seperation.... /n")

        try:

            self.logger_obj.log(self.file_obj,"Seperated independent and dependent /n")
            self.y = self.df[["cnt"]]
            self.X = self.df.drop(["cnt"], axis=1)
    #        return self.X,self.y
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Error occured while seperating feature and target...... /n"+str(e))
            self.logger_obj.log(self.file_obj,"Unsuccessful feature target seperation.... /n")
            raise Exception()


    def casual_reg_prob(self):

        
        self.logger_obj.log(self.file_obj,"Calculating probability of casual and registered columns.... /n")
        try:
            self.new_df = self.df.describe()[["casual","registered","cnt"]].iloc[1:2]
            self.new_df["casual_prob"] = (self.new_df["casual"]/self.new_df["cnt"])*100
            self.new_df["reg_prob"] = (self.new_df["registered"]/self.new_df["cnt"])*100
            self.new_df.to_csv("csv_files/prob.csv",index=False)
            self.logger_obj.log(self.file_obj,"Calculating probability of casual and registered columns.... /n")
            pass
        except Exception as e:
                self.logger_obj.log(self.file_obj,"Error occured while calculating casual and registered probability value...... /n"+str(e))
                self.logger_obj.log(self.file_obj,"Unsuccessful calculation in casual_reg_prob of Pre_process_data .... /n")
                raise Exception()


    def outlier_removal(self):
        self.df = self.df[(self.df["cnt"]<self.df["cnt"].quantile(0.90)) & (self.df["cnt"]>self.df["cnt"].quantile(0.10))]
        return self.df