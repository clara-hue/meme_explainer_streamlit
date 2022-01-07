import numpy as np
import streamlit as st
from PIL import Image
import pandas as pd
from analytics import getReferences, getGroup, getSpeaker, getTextFromImage, \
    getPublicFigure, get_featureDesc, getStatement, getResults

#analyse all pictures with the given models, right now only mock up data
@st.experimental_memo
def getData(images):
    df = pd.DataFrame(columns=["image","References","Public figure","Group affiliation",
                               "Speaker and Addressee","text"]) #the analyzed labels
    listPics=[]
    listRef=[]
    listPub=[]
    listGroup =[]
    listSpeaker=[]
    listText=[]
    listStatement=[]

    for pic in images: # each picture gets analyzed, for more details see file analytics.py
        if pic.name not in listPics:
            listPics.append(pic.name)
            listRef.append(getReferences(pic))
            listPub.append(getPublicFigure(pic))
            listGroup.append(getGroup(pic))
            listStatement.append(getStatement(pic))
            listSpeaker.append(getSpeaker(pic))
            listText.append(getTextFromImage(Image.open(pic)))
    #get results in the dataframe, use the filename as index
    zippedStatement=zip(listGroup,listStatement)
    listStatement=[i[0]+" "+i[1] for i in zippedStatement]
    df["image"] = listPics
    df["References"]=listRef
    df["Public figure"] =listPub
    df["Group affiliation"]=listGroup
    df["Statement"]=listStatement
    df["Speaker and Addressee"]= listSpeaker
    df["text"]=listText
    df.set_index("image",inplace=True)
    #use session state for the buttons, reset them each time, the input data changes
    st.session_state.index = 0

    return df




st.title("Hate Meme Detector")
st.write("Welcome to our *Hate Meme Detector*! Using the side bar, you can upload a number of images. "
         "Our algorithm will then detect different aspects of the potential hate meme. Using the selector on the "
         "bottom half of the page you can select the features which you want to analyse!")

#create fileuploader on the sidebar
with st.sidebar:
    pictures = st.file_uploader("Upload your images here", accept_multiple_files=True, type=["png","jpg","jpeg"])
    data= getData(pictures)



imgCont = st.container()
resCont = st.container()

if pictures:
    #in imgCont the image will be displayed & the buttons next & prev are implemented
    with imgCont:
        col1, col2, col3 = st.columns([1,5,1])
        next=col3.button("Next")
        prev=col1.button("Prev")

        #use session state & buttons to navigate to the next picture
        maxLenPics = len(pictures)
        if next:
            st.session_state.index += 1
        if prev:
            st.session_state.index -= 1
        if st.session_state.index == maxLenPics:
            st.session_state.index -= 1
        if st.session_state.index < 0:
            st.session_state.index += 1

        #Display the picture, the found text & the image title
        pic = pictures[st.session_state.index]
        imgTitle = pic.name
        img = Image.open(pic)
        col2.image(img, use_column_width="always")
        col2.caption(imgTitle)
        col2.write("**Text identified in picture: **" + data.at[imgTitle, "text"])

    #in resCont the results from analyzing the meme is displayed
    with resCont:

        st.subheader("Results")
        features=["References","Public figure","Group affiliation", "Statement", "Speaker and Addressee"]

        for i in features:
            getResults(data,imgTitle,i)




























