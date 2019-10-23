# set the matplotlib backend so figures can be saved in the background
import matplotlib
 
# import the necessary packages
from .livenessnet import LivenessNet
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.utils import np_utils
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import cv2
import os


class Liveness_training:
    def __init__(self):
        self.INIT_LR = 1e-4
        self.BS = 8
        self.EPOCHS = 50

    def train(self):
        # grab the list of images in our dataset directory, then initialize
        # the list of data (i.e., images) and class images
        print("[INFO] loading images...")
        imagePaths = list(paths.list_images("dataset/liveness_detector/" ))
        data = []
        labels = []
        
        for imagePath in imagePaths:
            # extract the class label from the filename, load the image and
            # resize it to be a fixed 32x32 pixels, ignoring aspect ratio
            label = imagePath.split(os.path.sep)[-2]
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (32, 32))
        
            # update the data and labels lists, respectively
            data.append(image)
            labels.append(label)
        
        # convert the data into a NumPy array, then preprocess it by scaling
        # all pixel intensities to the range [0, 1]
        data = np.array(data, dtype="float") / 255.0

        # encode the labels (which are currently strings) as integers and then
        # one-hot encode them
        le = LabelEncoder()
        labels = le.fit_transform(labels)
        labels = np_utils.to_categorical(labels, 2)
        
        # partition the data into training and testing splits using 75% of
        # the data for training and the remaining 25% for testing
        (trainX, testX, trainY, testY) = train_test_split(data, labels,
            test_size=0.25, random_state=42)

        # construct the training image generator for data augmentation
        aug = ImageDataGenerator(rotation_range=20, zoom_range=0.15,
            width_shift_range=0.2, height_shift_range=0.2, shear_range=0.15,
            horizontal_flip=True, fill_mode="nearest")
        
        # initialize the optimizer and model
        print("[INFO] compiling model...")
        opt = Adam(lr=self.INIT_LR, decay=self.INIT_LR / self.EPOCHS)
        model = LivenessNet.build(width=32, height=32, depth=3,
            classes=len(le.classes_))
        model.compile(loss="binary_crossentropy", optimizer=opt,
            metrics=["accuracy"])
        
        # train the network
        print("[INFO] training network for EPOCHS")
        H = model.fit_generator(aug.flow(trainX, trainY, batch_size=self.BS),
            validation_data=(testX, testY), steps_per_epoch=len(trainX) // self.BS,
            epochs=self.EPOCHS)

        # evaluate the network
        print("[INFO] evaluating network...")
        predictions = model.predict(testX, batch_size=self.BS)
        print(classification_report(testY.argmax(axis=1),
            predictions.argmax(axis=1), target_names=le.classes_))
        
        # save the network to disk
        print("[INFO] serializing network to model")
        model.save("dataset/liveness_model/liveness.model")
        
        # save the label encoder to disk
        f = open("dataset/liveness_model/livenesspickle.le", "wb")
        f.write(pickle.dumps(le))
        f.close()
        
        # plot the training loss and accuracy
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(np.arange(0, self.EPOCHS), H.history["loss"], label="train_loss")
        plt.plot(np.arange(0, self.EPOCHS), H.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, self.EPOCHS), H.history["acc"], label="train_accuracy")
        plt.plot(np.arange(0, self.EPOCHS), H.history["val_acc"], label="val_accuracy")
        plt.title("Training Loss and Accuracy on Dataset")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="lower left")
        plt.savefig("dataset/liveness_model/plot")
