# #Simple SVM
```python
Wiki:
Given a set of training examples, each marked as belonging to one or the other of two categories, an SVM training algorithm builds a model
that assigns new examples to one category or the other.
examples of the separate categories are divided by a clear gap that is as wide as possible.
New examples are then mapped into that same space and predicted to belong to a category based on which side of the gap they fall.
'''

#Simple SVM
'''
If we have linearly separable data in two dimensions, a simple SVM will try to find a boundary that divides the data in 
a way that the misclassification error can be minimized.
Basically, SVM finds the most optimal decision boundary (the one which has maximum margin from the nearest points of all the classes).
The nearest points from the decision boundary that maximize the distance between the decision boundary and the points are called support vectors
'''
#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read the data
path='C:\\Users\\sagi\\bill_authentication.csv'
bankdata=pd.read_csv(path)

#explore the data
bankdata.shape
bankdata.head()

#Preprocessing the data
#(1) Dividing the data into attributes and labels
#(2) dividing the data into training and testing sets.

#attributes and labels
#x is the attributes (what we're using to predict)
x=bankdata.drop('Class', axis=1) #store all the columns of the bankdata except for class col.
#y is the label (what we're trying to predict)
y=bankdata['Class'] #store all the class col.

#training and testing sets
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2)

#Training the Algorithm
'''The svm library contains built-in classes for different SVM algorithms.
Since we are going to perform a classification task, we will use the support vector classifier class, which is written as SVC.
It takes one parameter, which is the kernel type. This is very important. In the case of a simple SVM we simply set this 
parameter as "linear" since simple SVMs can ONLY classify linearly separable data.
'''
#use the fit method to train the algorithm on the training data which is passed as a parameter to the fit method

from sklearn.svm import SVC
svclassifier = SVC(kernel='linear')
svclassifier.fit(x_train,y_train)

#Making Predictions
y_predict=svclassifier.predict(x_test)

#Evaluating the Algorithm
#Confusion matrix, precision, recall, and F1 measures are the most commonly used metrics for classification tasks

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_predict))
print(classification_report(y_test, y_predict))

'''     [N                P]
          
   [N    T Neg             F Neg
   [p    F pos             T pos
'''
#Confusion matrix: summarizing the performance of a classification algorithm- The number of correct and incorrect predictions are shown and broken summarized by each class,
#precision: True positive/ (T positive+ F positive)
#Recall: T pos/ (T pos + F neg)
#F1:a function of Precision and Recall : --> 2* (precision*Recall)/(prec.+ rec)
#Need when you need a balance between rec and prec.

# Results
[[148   1]
 [  0 126]]
              precision    recall  f1-score   support
           0       1.00      0.99      1.00       149
           1       0.99      1.00      1.00       126
   micro avg       1.00      1.00      1.00       275
   macro avg       1.00      1.00      1.00       275
weighted avg       1.00      1.00      1.00       275

```
# Resources
https://stackabuse.com/implementing-svm-and-kernel-svm-with-pythons-scikit-learn/
https://en.wikipedia.org/wiki/Support-vector_machine

