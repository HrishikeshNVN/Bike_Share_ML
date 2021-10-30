import pandas as pd
import numpy as np
import datetime
import pickle as pkl
from sklearn.metrics import mean_squared_error, r2_score
from model_tune_n_eval import Model_tuning


class Model_eval:

    """
                Method Name: connect_db
                Description: This method establishe connection with cassandra database.
                Output: Connector object to connect with database for all database operations..
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
"""





    def __init__(self,file_obj,logger_obj):

        self.logger_obj = logger_obj
        self.file_obj=file_obj
        model_tune = Model_tuning(self.file_obj,self.logger_obj)
        self.X_test,self.y_test,self.best_features,self.scores = model_tune.get_tuned_model_score()
        self.logger_obj.log(self.file_obj,"Entered Model_eval class of tune_save_model module")
        
    def get_saved_model_n_score(self):

        self.logger_obj.log(self.file_obj,"Entered gett_saved_model_n_score of Model_eval class")
        
        try:

            self.model_evaluation()
            self.logger_obj.log(self.file_obj,"Found best model and created it in model.sav")
            return print("Best model is",self.best_model[0],self.best_model[2])
                  
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured in Entered gett_saved_model_n_score of Model_eval class. Exception message: '+str(e))
            self.logger_obj.log(self.file_obj,'model evaluation unsuccessful.Exited gett_saved_model_n_score of Model_eval class')
            raise Exception()
        

    def model_evaluation(self):
        

        self.logger_obj.log(self.file_obj,"Entered model_evaluation of Model_eval class")

        try:
            self.logger_obj.log(self.file_obj,"Started Model_evaluation")
            final_scores = []
            for i in self.scores:
                i[1].set_params(**i[2])
                y_pred = i[1].predict(self.X_test[self.best_features])
                mse = mean_squared_error(self.y_test,y_pred)
                r2s = r2_score(self.y_test,y_pred)
                final_scores.append([i[0],i[1],mse,r2s])
            
            max_r2s = 0
            for i in final_scores:
                temp = i[3]
                if temp > max_r2s:
                    max_r2s = temp
                    self.best_model = [i[0],i[1],max_r2s]
            self.logger_obj.log(self.file_obj,"Model evaluation completed...")

            filename = 'model_dir/model.sav'
            pkl.dump(self.best_model[1], open(filename, 'wb'))
            
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured in model_evaluation of Model_eval class. Exception message: '+str(e))
            self.logger_obj.log(self.file_obj,'model evaluation unsuccessful.Exited gett_saved_model_n_score of Model_eval class')
            raise Exception()