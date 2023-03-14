from imageai.Classification import ImageClassification
import os
import argparse
from gtts import gTTS

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fileName", type=str)

args = parser.parse_args()
execution_path = os.getcwd()

prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth")) # Download the model via this link https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/resnet50-19c8e357.pth
prediction.loadModel()

img_dir = args.fileName 
print(img_dir)
#filePath = "{execution_path}\{dir}\{filename}".format(execution_path=execution_path, dir = "images",filename = args.fileName)
# predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, filePath), result_count=10)
predictions, probabilities = prediction.classifyImage(img_dir, result_count=10)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)
print ("\n"+ predictions[0])

mytext = predictions[0]
  
language = 'en'

myobj = gTTS(text=mytext, lang=language, slow=False)
   
myobj.save("prediction.mp3")

os.system("prediction.mp3")
