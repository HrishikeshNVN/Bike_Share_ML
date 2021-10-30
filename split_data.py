import pandas as pd
import numpy as np
import resreg
from preprocess_data import Pre_Process_data
from sklearn.model_selection import train_test_split
class Split_data:

    def __init__(self,file_obj,logger_obj):

        self.logger_obj = logger_obj
        self.file_obj=file_obj
        data_process = Pre_Process_data(self.file_obj,self.logger_obj)
        self.X, self.y = data_process.get_processesd()
        self.logger_obj.log(self.file_obj,'Entered Split_data class')


    def get_train_test_os(self):

        self.logger_obj.log(self.file_obj,'Started get_train_test method...')


        try:
            self.oversample()
            self.logger_obj.log(self.file_obj,'Exited get_train_test method...')
            return self.X_train,self.X_test,self.y_train,self.y_test
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Error occured while Splits_data....')
            self.logger_obj.log(self.file_obj,'Unsuccessful split due to...'+str(e))
            raise Exception()

    def splits_to_train_test(self):

        try:
            self.logger_obj.log(self.file_obj,'Started split data to train and test...')
            self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X,self.y,test_size=0.3)
            self.logger_obj.log(self.file_obj,'Train data test data splitted successfully....')
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Failed to split_data ')
            self.logger_obj.log(self.file_obj,'Error occured in Split_data class'+str(e))
            raise Exception()
    #        return self.X_train,self.X_test,self.y_train,self.y_test

    def oversample(self):

        try:
            self.logger_obj.log(self.file_obj,'Oversampling started...')
            self.splits_to_train_test()
            relevance = resreg.sigmoid_relevance(self.y_train, cl=np.percentile(self.y,10), ch=np.percentile(self.y, 90))
 #           self.X_train1, self.y_train1 = resreg.random_oversample(self.X_train, self.y_train, relevance, relevance_threshold=0.5,
 #                                               over='balance')

            self.X_train1, self.y_train1 =  resreg.smoter(self.X_train, self.y_train, relevance)
                                                
            self.X_train = pd.DataFrame(self.X_train1,columns= self.X_train.columns)
            self.y_train = pd.DataFrame(self.y_train1,columns=self.y_train.columns)

        except Exception as e:
            self.logger_obj.log(self.file_obj,'Error occured while oversampling..')
            self.logger_obj.log(self.file_obj,'Failed to oversample....'+str(e))
            raise Exception()
            
