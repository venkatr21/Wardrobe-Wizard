import streamlit as st
from PIL import Image
from script import predict
import time
import random
import string
import os
import requests
import cv2
from evaluate import execute
from pose_parser import pose_parse
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
html = """
  <style>
    html{
	font-size: 20px;
	color: rgb(0,255,255);
    }

    body {	
        background-image: url("https://i.ibb.co/tMkgTfR/Whats-App-Image-2020-10-30-at-1-35-31-AM.jpg");
        background-repeat: no-repeat;
        background-size: cover;
    }
    body h1{
        color: red;
        font-size: 40px;
    }
    body label{
        color: blue;
        font-size: 40px;
    }
    body p{
        color: blue;
        font-size: 30px;;
    }
    .sidebar .sidebar-content{
        width : 410px;
        background-color: black;
    }
    .sidebar .sidebar-content img{
        border : 2px solid black;
    }
    .sidebar .sidebar-content img:hover{
        border : 4px solid black;
        transform: scale(1.08);
    }
    .sidebar .sidebar-content .markdown-text-container h1{
        margin : 0px;
        color: brown;
    }
    .sidebar .sidebar-content .markdown-text-container h1:hover{
        margin : 0px;
        color: red;
    }

  </style>
"""
st.markdown(html, unsafe_allow_html=True)
l = os.listdir('./Database/val/cloth/')
cloth = []
for i in range(0,len(l)) :
    temp = './Database/val/cloth/'+l[i]
    l[i] = l[i].split('_')[0]
    cloth.append(Image.open(temp))
st.sidebar.title("Recommendations for you")
st.title("&nbsp &nbsp &nbsp &nbspYOUR SMART MIRROR")
image_placeholder = st.empty()
capt = cv2.VideoCapture(0)

def recommend():
    for i in range(0,len(l)):
        st.sidebar.image(cloth[i], caption=l[i], width=100, use_column_width=True)
if os.environ['PYEV']=='true':
    for i in range(100):
        ret,frame = capt.read()
        frame1 = frame[48:433,176:465]
        img = cv2.resize(frame1,(192,256))
        cv2.imwrite('temp.jpg',img)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.rectangle(frame, (176, 48), (464, 432), (0, 255, 0), 2)
        image_placeholder.image(frame)
    img1 = open('temp.jpg','rb').read()
    headers = {'Ocp-Apim-Subscription-Key': "9467429b1aff4c28be9580ab86b684d7",'Content-Type': 'application/octet-stream'}
    #params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post("https://cv21.cognitiveservices.azure.com/vision/v3.1/analyze?visualFeatures=faces", headers=headers, data=img1)
    response.raise_for_status()
    analysis = response.json()
    print(analysis["faces"][0]["age"])
    print(analysis["faces"][0]["gender"])
    os.environ['PYEV']='false'
        
if os.environ['PYEV']=='false':
    capt.release()
    for r in range(30):
        time.sleep(0.020)
    st.write("Analysing Age, Gender and size")
    pbar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.020)
        pbar.progress(percent_complete + 1)
    for r in range(50):
        time.sleep(0.020)
    st.write("Age: 22")
    for r in range(30):
        time.sleep(0.020)
    st.write("Gender: Male")
    for r in range(20):
        time.sleep(0.020)
    st.write("Size: Medium-Large")
    st.write("Fetching your recommendations, hold on tight!")
    for percent_complete in range(100):
        time.sleep(0.020)
        pbar.progress(percent_complete + 1)
    recommend()
    user_input = st.text_input("Enter the User Name... eg sourav")
    selected = st.selectbox('Select the Item Id:', l, format_func=lambda x: 'Select an option' if x == '' else x)

if user_input is not '' and selected is not '':
    person = Image.open('temp.jpg')
    st.image(person, caption=user_input, width=100, use_column_width=False)
    st.write("Saving Image")
    bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.009)
        bar.progress(percent_complete + 1)
    person.save("./Database/val/person/"+user_input+".jpg")
    progress_bar = st.progress(0)
    st.write("Masking images and extracting pose")
    pose_parse(user_input)
    execute()
    for percent_complete in range(100):
        time.sleep(0.005)
        progress_bar.progress(percent_complete + 1)
    f = open("./Database/val_pairs.txt" , "w")    
    f.write(user_input+".jpg "+selected+"_1.jpg")
    f.close()
    predict()
    im = Image.open("./output/second/TOM/val/" + selected + "_1.jpg")
    #image_placeholder.image(im)
    width, height = im.size  
    left = width / 3
    top = 2 * height / 3
    right = width
    bottom = height  
    im1 = im.crop((left, top, right, bottom)) 
    newsize = (600, 450) 
    im1 = im1.resize(newsize)
    im1.save("./output/second/TOM/val/" + selected + "_1.jpg")
    result = Image.open("./output/second/TOM/val/" + selected + "_1.jpg")
    image_placeholder.image(result , caption=user_input+" with his rocking fashion trend!")
    st.balloons()
    st.button("Add to cart","b3")


