import pandas as pd
import pickle as pkl
from put_data import Put_Data
import numpy as np
from logger import App_Logger


class Prediction_class:

    """
                Method Name:Prediction_class
                Description: This class predicts the output using the model for the user given inputs.
                Output: Predicted output.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
"""


    
    def __init__(self):


        self.file_obj = open("log_files/Prediction_logs","a")
        self.logger_obj = App_Logger()
        #self.file_obj = file_obj
        #self.logger_obj = logger_obj
        

        self.wether_dict = {1:"Clear/Fewclouds", 2:"Mist/Cloudy" , 3:"LightSnow/LightRain", 4:"HeavyRain"}
        self.season_dict = {1:"winter", 2:"spring", 3:"summer", 4:"fall"}
        self.weekday_dict = {0:"Sunday",1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday"}
        self.best_feat = list(pd.read_csv("csv_files/best_features.csv"))
    
    def predict(self,user_ip):
        

        try:
            self.user_inputs = user_ip
            self.user_df = pd.DataFrame(user_ip)
            self.user_df["date"]=pd.DatetimeIndex(self.user_df["dteday"])

            self.user_df["day"] = pd.DatetimeIndex(self.user_df["date"]).day
            self.user_df["month"] = pd.DatetimeIndex(self.user_df["date"]).month_name()
            self.user_df["year"] = pd.DatetimeIndex(self.user_df["date"]).year

            self.user_df.drop(labels=["dteday","mnth","date"], axis=1, inplace=True)


            self.user_df["weathersit"].replace(self.wether_dict, inplace=True)
            self.user_df["season"].replace(self.season_dict, inplace=True)
            self.user_df["weekday"].replace(self.weekday_dict, inplace=True)


            self.user_df["jul_sep_jun_aug"] = self.user_df["month"].apply(lambda month : 1 if month in ["July","August","September"] else 0)
            self.user_df["oct_may"] = self.user_df["month"].apply(lambda month : 1 if month in ["October","May"] else 0)
            self.user_df["dec_mar_nov_apr"] = self.user_df["month"].apply(lambda month : 1 if month in ["December","March","November","April"] else 0)
            self.user_df["jan_feb"] = self.user_df["month"].apply(lambda month : 1 if month in ["January","February"] else 0)


                # dropping 'month', 'year' columns as it is redundant now
            self.user_df.drop(['month'], axis=1, inplace=True)
            self.user_df.drop(['year'], axis=1, inplace=True)



            self.user_df = self.encoding_fn(self.user_df,'season')
            self.user_df = self.encoding_fn(self.user_df,'weekday')
            self.user_df = self.encoding_fn(self.user_df,'weathersit')

                ##Need to include scaling.............

                

            diff_cols = list(set(self.best_feat).difference(set(self.user_df.columns)))
            print("difference columns&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& \n",diff_cols)
            self.user_df[diff_cols]=0
            inter_cols = list(set(self.user_df.columns).intersection(set(self.best_feat)))
            print("INTERSECTION columnswwwwwwwwwwwwwwwwwwww&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& \n",inter_cols)
            
            all_cols = list(set(diff_cols).union(set(inter_cols)))
            print("UNION columnsxxxxxxxxxxxxxxxxxxx&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& \n",all_cols)
            

            loaded_model = pkl.load(open("model_dir/model.sav", 'rb'))
            result = loaded_model.predict(self.user_df[all_cols])
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#################",result)
            prob_df = pd.read_csv("csv_files/prob.csv")
            casual_val = int((float(prob_df.casual_prob)/100)*result)
            reg_val = int((float(prob_df.reg_prob)/100)*result)
            cnt = casual_val+reg_val
            self.user_inputs[0].update({"casual":casual_val,"registered":reg_val,"cnt":cnt})
            puts = Put_Data(self.file_obj,self.logger_obj)
            puts.put_file(self.user_inputs)
            return cnt,casual_val,reg_val
        except Exception as e:
            self.logger_obj.log(self.file_obj,"\n Error occured while predicting \n"+str(e))
            print("Failed prediction....."+str(e))


    def encoding_fn(self,df,feature):
        tdf = pd.get_dummies(df[feature])
        df.drop(feature, axis=1, inplace=True)
        return pd.concat([df,tdf], axis=1)