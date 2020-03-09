
# coding: utf-8

# ---
#
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-machine-learning/resources/bANLa) course resource._
#
# ---

# ## Assignment 4 - Understanding and Predicting Property Maintenance Fines
#
# This assignment is based on a data challenge from the Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)).
#
# The Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)) and the Michigan Student Symposium for Interdisciplinary Statistical Sciences ([MSSISS](https://sites.lsa.umich.edu/mssiss/)) have partnered with the City of Detroit to help solve one of the most pressing problems facing Detroit - blight. [Blight violations](http://www.detroitmi.gov/How-Do-I/Report/Blight-Complaint-FAQs) are issued by the city to individuals who allow their properties to remain in a deteriorated condition. Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
#
# The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. This is where predictive modeling comes in. For this assignment, your task is to predict whether a given blight ticket will be paid on time.
#
# All data for this assignment has been provided to us through the [Detroit Open Data Portal](https://data.detroitmi.gov/). **Only the data already included in your Coursera directory can be used for training the model for this assignment.** Nonetheless, we encourage you to look into data from other Detroit datasets to help inform feature creation and model selection. We recommend taking a look at the following related datasets:
#
# * [Building Permits](https://data.detroitmi.gov/Property-Parcels/Building-Permits/xw2a-a7tf)
# * [Trades Permits](https://data.detroitmi.gov/Property-Parcels/Trades-Permits/635b-dsgv)
# * [Improve Detroit: Submitted Issues](https://data.detroitmi.gov/Government/Improve-Detroit-Submitted-Issues/fwz3-w3yn)
# * [DPD: Citizen Complaints](https://data.detroitmi.gov/Public-Safety/DPD-Citizen-Complaints-2016/kahe-efs3)
# * [Parcel Map](https://data.detroitmi.gov/Property-Parcels/Parcel-Map/fxkw-udwf)
#
# ___
#
# We provide you with two data files for use in training and validating your models: train.csv and test.csv. Each row in these two files corresponds to a single blight ticket, and includes information about when, why, and to whom each ticket was issued. The target variable is compliance, which is True if the ticket was paid early, on time, or within one month of the hearing data, False if the ticket was paid after the hearing date or not at all, and Null if the violator was found not responsible. Compliance, as well as a handful of other variables that will not be available at test-time, are only included in train.csv.
#
# Note: All tickets where the violators were found not responsible are not considered during evaluation. They are included in the training set as an additional source of data for visualization, and to enable unsupervised and semi-supervised approaches. However, they are not included in the test set.
#
# <br>
#
# **File descriptions** (Use only this data for training your model!)
#
#     readonly/train.csv - the training set (all tickets issued 2004-2011)
#     readonly/test.csv - the test set (all tickets issued 2012-2016)
#     readonly/addresses.csv & readonly/latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates.
#      Note: misspelled addresses may be incorrectly geolocated.
#
# <br>
#
# **Data fields**
#
# train.csv & test.csv
#
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#
# train.csv only
#
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction]
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
#
#
# ___
#
# ## Evaluation
#
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
#
# The evaluation metric for this assignment is the Area Under the ROC Curve (AUC).
#
# Your grade will be based on the AUC score computed for your classifier. A model which with an AUROC of 0.7 passes this assignment, over 0.75 will recieve full points.
# ___
#
# For this assignment, create a function that trains a model to predict blight ticket compliance in Detroit using `readonly/train.csv`. Using this model, return a series of length 61001 with the data being the probability that each corresponding ticket from `readonly/test.csv` will be paid, and the index being the ticket_id.
#
# Example:
#
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32
#
# ### Hints
#
# * Make sure your code is working before submitting it to the autograder.
#
# * Print out your result to see whether there is anything weird (e.g., all probabilities are the same).
#
# * Generally the total runtime should be less than 10 mins. You should NOT use Neural Network related classifiers (e.g., MLPClassifier) in this question.
#
# * Try to avoid global variables. If you have other functions besides blight_model, you should move those functions inside the scope of blight_model.
#
# * Refer to the pinned threads in Week 4's discussion forum when there is something you could not figure it out.

# In[ ]:




# In[22]:

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
#from sklearn.metrics import confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import preprocessing
#from sklearn.svm import SVC
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.tree import DecisionTreeClassifier

def blight_model():

    # Your code here
    train_df = pd.read_csv('train.csv', encoding = "ISO-8859-1")
    train_df = train_df[train_df['compliance'].notnull()]
    addresses_df = pd.read_csv('addresses.csv', encoding = "ISO-8859-1")
    latlons_df = pd.read_csv('latlons.csv', encoding = "ISO-8859-1")

    #merge train data
    train_df = train_df.merge(addresses_df, how='inner', left_on='ticket_id', right_on='ticket_id')
    train_df = train_df.merge(latlons_df, how='inner', left_on="address", right_on="address")
    train_df.index = train_df['ticket_id']

    #make violation code to digits
    #train_df['violation_code'] = train_df['violation_code'].str.replace("\D+", "")
    le = preprocessing.LabelEncoder()
    train_df[['violation_code', 'disposition']] = train_df[['violation_code', 'disposition']].apply(le.fit_transform)


    X = train_df[['lat', 'lon', 'violation_code', 'disposition', 'judgment_amount']]
    X = X.apply(pd.to_numeric)
    X = X.fillna(0)
    y = train_df['compliance']
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


    grd = GradientBoostingClassifier()
    #grd.fit(X_train, y_train)
    #y_pred_grd = grd.predict_proba(X_test)[:,1]
    #fpr_grd, tpr_grd, _ = roc_curve(y_test, y_pred_grd)
    #roc_auc_grd = auc(fpr_grd, tpr_grd)

    #rf = RandomForestClassifier.fit(X_train, y_train)
    #y_score_svm = rf.fit(X_train, y_train).decision_function(X_test)
    #fpr_svm, tpr_svm, _ = roc_curve(y_test, y_score_svm)
    #roc_auc_svm = auc(fpr_svm, tpr_svm)

    #lr = LogisticRegression().fit(X_train, y_train)
    #y_score_lr = lr.fit(X_train, y_train).decision_function(X_test)
    #fpr_lr, tpr_lr, _ = roc_curve(y_test, y_score_lr)
    #roc_auc_lr = auc(fpr_lr, tpr_lr)


    test_df = pd.read_csv('test.csv', encoding = "ISO-8859-1")
    #merge test data
    test_df = test_df.merge(addresses_df, how='inner', left_on='ticket_id', right_on='ticket_id')
    test_df = test_df.merge(latlons_df, how='inner', left_on="address", right_on="address")
    test_df.index = test_df['ticket_id']
    le = preprocessing.LabelEncoder()
    test_df[['violation_code', 'disposition']] = test_df[['violation_code', 'disposition']].apply(le.fit_transform)
    X_test = test_df[['lat', 'lon', 'violation_code', 'disposition', 'judgment_amount']]
    X_test = X_test.apply(pd.to_numeric)
    X_test = X_test.fillna(0)
    y_proba = grd.fit(X, y).predict_proba(X_test)

    result = pd.Series(y_proba[:,1], index = X_test.index)




    return result
blight_model()


# In[24]:




# In[ ]:



