import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import random
import streamlit as st
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/Cellar/tesseract/4.1.3/bin/tesseract"



def getTextFromImage(image):
    text = pytesseract.image_to_string(image)
    return text


def getReferences(image):
    posRes=["Reference between text and image: text span | image", "Reference of text outside: text span | meaning",
            "Reference of image outside: image | meaning"]
    rand = random.randint(0,2)
    return posRes[rand]

def getPublicFigure(image):
    res= ["Public figure: Yes, Name: Angela Merkel", "Public figure: No"]
    return random.choice(res)

def getGroup(image):
    groups = ["Foreigners / Migrants", "Disabled / Sick","Elites","People of Color","Women","Jews","Judiciary",
              "LGBTQ+ ","Media / Press","Muslims","Specific Nationality / Origin (Nationalitat","Police",
              "Government / Politics","Religious group","Environmental Movement / Greens","political spectrum left",
              "political spectrum right","Other"]

    return random.choice(groups)

def getSpeaker(image):
    speaker=["inside the meme, image only","inside the meme, text only", "inside the meme, image & text",
             "outside/ unknown"]
    addressee=["in the text", "in the image", "other", "the reader directly"]
    return "The speaker is {s}. The speaker is addressing someone {a}".format(s=random.choice(speaker),
                                                                              a=random.choice(addressee))

def getStatement(image):
    statement = ["are greedy", "are terrorists", "are hated", "are violent", "are criminal", "are household appliances",
                 "are part of a conspiracy", " have sex with pets", "have sex with goats"]
    return random.choice(statement)



def get_featureDesc(feature):
    dictFeat={"References":"There can be both references inside the meme"
                           " itself (between text and image) and references in the meme pointing outside",
              "Public figure":"Public figures recognized in the image and how they are important to understand "
                              "the meme",
              "Group affiliation":"What groups can be identified.",
              "Speaker and Addressee":"Who is speaking and where the speaker can be found (inside the image/ text)",
              "Statement": "The intended meaning of the meme and the statement about the group."}
    return dictFeat[feature]

def getResults(df,img, feature):
    res=df.at[img,feature]
    desc=get_featureDesc(feature)
    featureMark="##### "+feature
    st.markdown(featureMark)
    st.caption(desc)
    st.write(res)
    st.markdown("---")






