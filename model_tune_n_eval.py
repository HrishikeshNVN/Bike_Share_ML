import pandas as pd
import numpy as np
from feature_selection import Feature_select
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import RandomizedSearchCV

class Model_tuning:

    """
                Method Name: Model_tuning
                Description: This class performs hyperparameter tuning of different models created.
                Output: Returns the trained and tuned models with their scores.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
"""


    def __init__(self,file_obj,logger_obj):

        self.logger_obj = logger_obj
        self.file_obj=file_obj
        feature_select_obj = Feature_select(self.file_obj,self.logger_obj)
        self.X_train,self.X_test,self.y_train,self.y_test,self.best_features = feature_select_obj.get_data_selected_features()

    def get_tuned_model_score(self):
        
        cols = ["dteday","season","yr","mnth","holiday","weekday","workingday","weathersit","temp","atemp","hum","windspeed","casual","registered","cnt"]
        self.logger_obj.log(self.file_obj,"Entered get_tuned_model_score of Model_tuning class")
        try:

            self.models_tuning()
            df = pd.DataFrame(columns=cols)
            df.to_csv("csv_files/new_day_data.csv",mode='w',index=False)
            return self.X_test,self.y_test,self.best_features,self.scores
                
                    
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured in get_tuned_model_score of Model_tuning class. Exception message: '+str(e))
            self.logger_obj.log(self.file_obj,'model tuning unsuccessful.Exited get_tuned_model_score of Model_tuning class')
            raise Exception()


    def models_tuning(self):

        model_n_params_dict = {
    "Linear_regression":{"model":LinearRegression(), "params":{'n_jobs': [-1],
'fit_intercept': [True,False],
 'normalize': [False,True],
 'positive': [True,False]}},
                                                              
    "Decision_tree_regressor":{"model":DecisionTreeRegressor(),"params":{"criterion": ["mse", "mae"],
              "min_samples_split": [10, 20, 40],
              "max_depth": [2, 6, 8],
              "min_samples_leaf": [20, 40, 100],
              "max_leaf_nodes": [5, 20, 100],
              }},
    "Extra_tree_regressor":{"model":ExtraTreesRegressor(),"params":{'bootstrap': [True,False],
 'criterion': ["mse", "mae"],
 'max_depth': [10,20,40,60,80,100,None],
 'max_features': ['auto','sqrt'],
 'min_samples_leaf': [1,2,4],
 'min_samples_split': [2,5,10],
 'n_estimators': [10,40,50,100],
 'n_jobs': [-1],
 'verbose': [10]}},
    "Random_forest_regressor":{"model":RandomForestRegressor(),"params":{'bootstrap': [True,False],
 'criterion': ["mse", "mae"],
 'max_depth': [10,20,40,60,80,100,None],
 'max_features': ['auto','sqrt'],
 'min_samples_leaf': [1,2,4],
 'min_samples_split': [2,5,10],
 'n_estimators': [10,40,50,100],
 'n_jobs': [-1],
 'verbose': [10]
}}}
        self.logger_obj.log(self.file_obj,"Started Model tuning...")

        try:

            self.scores = []
            for model_name, mp in model_n_params_dict.items():
                mdl = RandomizedSearchCV(mp["model"],mp["params"], cv=5, return_train_score=False)
                mdl.fit(self.X_train[self.best_features],self.y_train)
                self.scores.append([model_name,mdl.best_estimator_,mdl.best_params_,mdl.best_score_])
            self.logger_obj.log(self.file_obj,"Model tuning completed successfully...")
                       
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured in models_tuning of Model_tuning class. Exception message: '+str(e))
            self.logger_obj.log(self.file_obj,'model tuning unsuccessful.Exited models_tuning of Model_tuning class')
            raise Exception()

        
            

        

