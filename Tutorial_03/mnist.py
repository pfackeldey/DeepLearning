import numpy as np
import matplotlib.pyplot as plt
import os

# to make DLIPR available put 'software community/dlipr' in your ~/.profile
import dlipr

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical


# ----------------------------------------------
# Data
# ----------------------------------------------
data = dlipr.mnist.load_data()

# plot some examples
data.plot_examples(fname='examples.png')

# reshape the image matrices to vectors
X_train = data.train_images.reshape(-1, 28**2)
X_test = data.test_images.reshape(-1, 28**2)
print('%i training samples' % X_train.shape[0])
print('%i test samples' % X_test.shape[0])

# convert integer RGB values (0-255) to float values (0-1)
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

# convert class labels to one-hot encodings
Y_train = to_categorical(data.train_labels, 10)
Y_test = to_categorical(data.test_labels, 10)


# ----------------------------------------------
# Model and training
# ----------------------------------------------

# make output directory
folder = 'results/'
if not os.path.exists(folder):
    os.makedirs(folder)
"""
#------------------------TASK 1:
#Hyperparameter choosen: batch_size and epochs!
#Grid search:
batch_size_list=[50, 100, 200]
learningrate_list=[1e-4,1e-3, 1e-2]

best=[]

for batchsize in batch_size_list:
    for LearningRate in learningrate_list:
        print "current batch size: ", batchsize
        print "current learning rate: ",LearningRate
        model = Sequential([
            Dense(64, input_shape=(784,)),
            Activation('relu'),
            Dropout(0.5),
            Dense(10),
            Activation('softmax')])
        
        #print(model.summary())
        
        model.compile(
            loss='categorical_crossentropy',
            optimizer=Adam(lr=LearningRate),
            metrics=['accuracy'])
            
        
        fit = model.fit(
            X_train, Y_train,
            batch_size=batchsize,
            epochs=10,
            verbose=1,
            validation_split=0.1,  # split off 10% training data for validation
            callbacks=[])
        
        #LOSS PLOTTING    
        f=plt.figure()
        plt.plot(fit.history["loss"])
        plt.plot(fit.history["val_loss"])
        plt.xlabel("epochs")
        plt.ylabel("loss")
        plt.legend(["training loss","validation loss"],loc="best")
        f.savefig("LOSS_batchsize_"+str(batchsize)+"learningrate_"+str(LearningRate)+".png")
        print fit.history["loss"][-1]
        best.append(fit.history["loss"][-1])
  
print best
print "Minimum loss: ",min(best)
best_index=best.index(min(best))
print "index: ", best_index

BS=0
LR=0.

if (best_index==0):
    BS=50
    LR=1e-4
elif(best_index==1):
    BS=50
    LR=1e-3
elif(best_index==2):
    BS=50
    LR=1e-2
elif(best_index==3):
    BS=100
    LR=1e-4
elif(best_index==4):
    BS=100
    LR=1e-3
elif(best_index==5):
    BS=100
    LR=1e-2
elif(best_index==6):
    BS=200
    LR=1e-4
elif(best_index==7):
    BS=200
    LR=1e-3
elif(best_index==8):
    BS=200
    LR=1e-2

print "DO TRAINING WITH BEST HYPERPARAMETERS:"        
model = Sequential([
            Dense(64, input_shape=(784,)),
            Activation('relu'),
            Dropout(0.5),
            Dense(10),
            Activation('softmax')])
        
#print(model.summary())

model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(lr=1e-3),
    metrics=['accuracy'])
    
fit = model.fit(
    X_train, Y_train,
    batch_size=50,
    epochs=20,
    verbose=2,
    validation_split=0.1,  # split off 10% training data for validation
    callbacks=[])

#BEST VALUES FOUND BY READING OUTPUT INFO
print "*****************************************************************************"
print "Looking at the output results in the following best set of Hyperparameter!!! "        
print "The smallest loss has: batch_size="+str(BS)+" and LearningRate="+str(LR)+" with the following values"
print "loss: ",fit.history["loss"][-1]
print "acc: ", fit.history["acc"][-1]
print "val_loss: ", fit.history["val_loss"][-1]
print "val_acc: ",fit.history["val_acc"][-1]
print "*****************************************************************************"
"""


#-----------------------------TASK 2:
learning_rate_list=[1e-5,1e-4,1e-3,1e-2,1e-1]
batch_size_list=[8,16,32,64,128,256,512]
dropout_fraction_list[0.1,0.2,0.3,0.4,0.5]
activation_function["relu","softmax","sigmoid","tanh"]



# ----------------------------------------------
# Some plots
# ----------------------------------------------

# predicted probabilities for the test set
Yp = model.predict(X_test)
yp = np.argmax(Yp, axis=1)

# plot some test images along with the prediction
for i in range(20):
    dlipr.utils.plot_prediction(
        Yp[i],
        data.test_images[i],
        data.test_labels[i],
        data.classes,
        fname=folder + 'test-%i.png' % i)

# plot the confusion matrix
dlipr.utils.plot_confusion(yp, data.test_labels, data.classes,
                           fname=folder + 'confusion.png')
                           
#TESTING
print "Perform testing on test samples"
[loss, accuracy] = model.evaluate(X_test, Y_test, verbose=1)
print "TEST RESULTS:"
print "test loss: ",loss
print "test accuracy: ",accuracy
print "validation loss: ", fit.history["val_loss"][-1]
print "validation accuracy: ",fit.history["val_acc"][-1]
