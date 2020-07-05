import streamlit as st
from sklearn import datasets
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("Data Classsification using Machine learning Algorithms")
st.write("""
# Explore different classifier
 Which one is the best?
""")

dataset_name=st.sidebar.selectbox("Select Dataset",("Iris","Breast Cancer","Wine dataset"))

classifier_name=st.sidebar.selectbox("Select Classifier",("KNN","SVM","Random Forest"))

def get_dataset(dataset_name):
    if(dataset_name=="Iris"):
        data=datasets.load_iris()
    elif (dataset_name=="Breast Cancer"):
        data=datasets.load_breast_cancer()
    elif(dataset_name=="Wine dataset"):
        data=datasets.load_wine()
    x=data.data
    y=data.target
    return x,y
x,y=get_dataset(dataset_name)
st.write("shape of dataset",x.shape)
st.write("number of classes",len(np.unique(y)))

def add_parameter(classifier_name):
    params=dict()
    if classifier_name=="KNN":
        K=st.sidebar.slider("K",1,15)
        params["K"]=K
    elif classifier_name=="SVM":
        C=st.sidebar.slider("C",0.01,10.0)
        params["C"]=C
    elif classifier_name=="Random Forest":
        max_depth=st.sidebar.slider("max_depth",2,15)
        n_estimators=st.sidebar.slider("n_estimators",1,100)
        params["max_depth"]=max_depth
        params["n_estimators"]=n_estimators
    return params

params=add_parameter(classifier_name)

def get_classifier(classifier_name,params):
    if classifier_name=="KNN":
        clf=KNeighborsClassifier(n_neighbors=params["K"])
    elif classifier_name=="SVM":
        clf=SVC(C=params["C"])
    elif classifier_name=="Random Forest":
        clf=RandomForestClassifier(n_estimators=params["n_estimators"],
                                   max_depth=params["max_depth"],random_state=1234)
    return clf
clf=get_classifier(classifier_name,params)

    #Classification
X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1234)

clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)
acc=accuracy_score(y_test,y_pred)
st.write(f"Classifer= {classifier_name}")
st.write(f"Accuracy ={acc}")


#Plot
pca=PCA(2)
x_projected=pca.fit_transform(x)
x1=x_projected[:,0]
x2=x_projected[:,1]

fig=plt.figure()
plt.scatter(x1,x2,c=y,alpha=0.8,cmap="viridis")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar()

st.pyplot()
