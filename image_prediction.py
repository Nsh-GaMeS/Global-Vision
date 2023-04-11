from imageai.Classification import ImageClassification
import os
import argparse
from gtts import gTTS

#a pretrained model for object recognition and detection is used here but it was slightly modified  
# Download the model via this link https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/resnet50-19c8e357.pth

# create dynamic arg value (variables for when the function is called)
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fileName", type=str)

args = parser.parse_args()#get and set the arguments from when th function was called
execution_path = os.getcwd()
img_dir = args.fileName 

#inizialize the prediction model
prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth")) 
prediction.loadModel()

#process the image 
predictions, probabilities = prediction.classifyImage(img_dir, result_count=10)

#print the first prediction with the probability 
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)
print ("\n"+ predictions[0])

def text_to_specch(text):
    mytext = text
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("prediction.mp3")
    os.system("prediction.mp3")

text_to_specch(predictions[0])

def get_prediction(index):
    return predictions[index]

def get_probability(index):
    return probabilities[index]