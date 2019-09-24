#Local Packages
from AdventureGuruApp import db, basedir
from AdventureGuruApp.models import Destination, Demo, Age, Time, Type
from flask import session
import tensorflow as tf
import numpy as np
import os
#import matplotlib
#matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt


#Input layer
# 1. Cost (0 to 4)
# 2. accessibility (1 to 3)
# 3. times
# 4. ages
# 5. types
# 6. category

def Load_Data(dataSet):
    #OneHot Encoder Mapping
    featureEncoding = {}
    ageList = Age.query.all()
    timeList = Time.query.all()
    typeList = Type.query.all()
    ageList = [age.title for age in ageList]
    timeList = [time.title for time in timeList]
    typeList = [type.title for type in typeList]
    categoryList = db.session.query(Destination.category.distinct()).order_by(Destination.category).all()
    categoryList = [category[0] for category in categoryList]

    index = 3 #1 is cost and 2 is accessibility
    for featureCategory in [ageList,timeList,typeList,categoryList]:
        for feature in featureCategory:
            featureEncoding[feature] = index
            index+=1
    d = index #dimension
    print(featureEncoding)

    #Input Data
    X = []
    Y = []
    for data in dataSet:
        #Intialize Data Point
        x = [0 for x in range(d)]
        dataTitle = data[0]
        destination = Destination.query.filter_by(title=dataTitle).first()

        # 1. Cost (0 to 4)
        x[0] = destination.cost
        # 2. accessibility (1 to 3)
        x[1] = destination.accessibility
        # 3 to d. times, ages, types, category
        for featureCategory in [destination.times,destination.ages,destination.types]:
            for feature in featureCategory:
                if feature.title in featureEncoding.keys():
                    featureIndex = featureEncoding[feature.title]
                    x[featureIndex] = 1
                else:
                    print("ERROR: "+feature.title+" is not a feature")
        if destination.category in featureEncoding.keys():
            featureIndex = featureEncoding[destination.category]
            x[featureIndex] = 1
        else:
            print("ERROR: "+destination.category+" is not a feature")

        #Append Data
        X.append(x)
        Y.append(data[1])

    return X,Y

def Train_demoModel(trainData,trainLabel):
    #Logistic Regression Model
    tf.reset_default_graph()

    #Input Layer
    N = len(trainData) #Number of Data Points
    d = len(trainData[0]) #Dimension
    X = tf.placeholder(tf.float32,shape=[None,d],name="X")
    Y = tf.placeholder(tf.float32,shape=[None,1],name="Y")
    trainData = np.array(trainData)
    trainLabel = np.array(trainLabel)
    trainData =np.reshape(trainData,(N,d))
    trainLabel = np.reshape(trainLabel,(N,1))

    #HyperParameters
    iterations = min(N**2+100,1000)
    learning_rate = 0.01
    Lambda = 0
    reg = tf.constant(Lambda, name = "Lambda")

    #Logistic Regression
    tf.set_random_seed(421)
    W = tf.get_variable(initializer = tf.truncated_normal((d,1),stddev=0.5,seed=421),name = "W")
    b = tf.get_variable(initializer = tf.truncated_normal((1,1),stddev=0.5,seed=421),name = "b")

    logit = tf.add(tf.matmul(X, W), b)
    pred = tf.sigmoid(logit,name="pred")
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=Y,logits=logit))
    correct_pred = tf.equal(tf.round(pred), Y)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    optimizer = tf.train.AdamOptimizer(learning_rate,name="ADAM").minimize(loss)

    #Intialize loss and accuracy
    trainLoss = []
    trainAcc = []

    #Training
    with tf.Session() as sess:
        #Run the initializer
        init = tf.global_variables_initializer()
        sess.run(init)

        for epoch in range(iterations):
            _,current_trainLoss,current_trainAcc = sess.run([optimizer,loss,accuracy], feed_dict={X: trainData, Y: trainLabel})
            trainLoss.append(current_trainLoss)
            trainAcc.append(current_trainAcc)
            print("Epoch: {0}, train loss: {1:.2f}, train accuracy: {2:.01%}".format(epoch + 1, current_trainLoss, current_trainAcc))
        print("Optimization finished!")

        '''
        #Plot Results
        x_axis = np.arange(iterations)+1

        plt.figure(figsize=(10,10))

        plt.subplot(211)
        plt.plot(x_axis,trainLoss,color='c',linewidth=2.0,label="Training")
        plt.ylabel('Loss')
        plt.xlabel('Epochs')
        plt.title("Loss and Accuracy")
        plt.legend()

        plt.subplot(212)
        plt.plot(x_axis,trainAcc,color='c',linewidth=2.0,label="Training")
        plt.ylabel('Accuracy')
        plt.xlabel('Epochs')
        plt.legend()

        plt.show()
        '''
        #Save Session
        lastDemo = db.session.query(Demo).order_by(Demo.id.desc()).first()
        if lastDemo:
            demoID = lastDemo.id+1
        else:
            demoID = 1

        filePath = os.path.join(basedir,"static/demo_models/demo"+str(demoID))
        model = tf.train.Saver()
        save_path = model.save(sess,filePath)

        #Save Session Data to Database
        demoModel = Demo(save_path,iterations,trainLoss[-1],trainAcc[-1])
        db.session.add(demoModel)
        db.session.commit()
        print(demoModel)

    return demoID

def Run_Model(model_id,destination):
    #Generate Graph Filepath
    tf.reset_default_graph()
    meta_file = os.path.join(basedir,"static/demo_models/demo"+str(model_id)+".meta")
    demo = Demo.query.filter_by(id=model_id).first()
    demo_file = demo.model_file
    print(meta_file)
    print(demo_file)

    #Load data
    destination_data,_ = Load_Data([(destination,0)])
    d = len(destination_data[0])
    destination_data = np.array(destination_data)
    destination_data =np.reshape(destination_data,(1,d))

    with tf.Session() as sess:
        #Create Graph
        recommendation_model = tf.train.import_meta_graph(meta_file)
        recommendation_model.restore(sess,demo_file)
        #Access Tensors
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("X:0")
        pred = graph.get_tensor_by_name("pred:0")

        #Run Model
        recommendation = sess.run([pred],feed_dict={x:destination_data})
        return recommendation[0]
