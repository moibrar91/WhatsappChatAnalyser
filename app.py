import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib
import seaborn as sns
import os
matplotlib.use('Agg')



html_temp="""
    <div style="background-color:springgreen;padding:15px;">
    <h1>WHATSAPP DATA VISUALIZATION AND ANALYSIS</h1>
    </div>
    """
html_temp1="""
    <div style="background-color:springgreen;padding:5px;">
    <h1>Choose->Analyse or Visualize</h1>
    </div>
    """

st.markdown(html_temp,unsafe_allow_html=True)
img=Image.open("images/whatsapp.jpg")
st.image(img,width=700)

st.sidebar.subheader("Files for chat are temporarily uploaded to app, and no data is stores, you data file remains private, and nothing is shared to server")


st.sidebar.markdown(html_temp1,unsafe_allow_html=True)
img2=Image.open("images/whats2.jpg")
st.sidebar.image(img2,width=305)

def process_data(data):
    filename=data
    df=pd.read_csv(filename,header=None,error_bad_lines=False,encoding='utf-8')
    df=df.drop(0)
    df.columns=['Date','Chat']
    messages=df["Chat"].str.split("-",n=1,expand=True)
    df['Time']=messages[0]
    df['Text']=messages[1]
    messages1=df['Text'].str.split(":",n=1,expand=True)
    df['Name']=messages1[0]
    df['Text']=messages1[1]
    df.drop(columns=['Chat'],inplace=True)
    df['Text']=df['Text'].str.lower()
    df['Text']=df['Text'].str.replace('<media omitted>','media shared')
    df['Text']=df['Text'].str.replace('this message was deleted','deletedmsg')
    null_name=df[df['Name'].isnull()]
    df.drop(null_name.index,inplace=True)
    df.dropna(inplace=True)
    df['Date']=pd.to_datetime(df['Date'])
    df['day_of_the_week']=df['Date'].dt.day_name()
    return df

def char_counter(msg):
    if msg==' media shared':
        return 0
    return len(msg)

def word_counter(msg):
    if msg==" media shared":
        return 0
    else:
        words=len(msg.split())
    return words 
def steps():
    st.info("STEPS TO USE")
    
    st.subheader("1-> Open the WhatsApp conversation you would like to have visualized and tap on the group subject or contact name in the navigation bar")
    st.subheader("2-> Scroll to the bottom and tap on 'Export chat' ")
    st.subheader("3-> Select without media")
    st.subheader("4-> Select 'Mail'")
    st.subheader("5-> Enter ur email into the 'To' field , Tap on Send")
    st.subheader("6-> Download your chat from the mail and browse here from that location")
    st.subheader("7-> That's It, now ready to analyse and visualize your chat")

def main():
    activities=['Analysis and Statistics of Chat','Visualization of chat']
    choice=st.sidebar.selectbox("Select Activity",activities)
    if choice=='Analysis and Statistics of Chat':
        st.header("ANALYSIS OF CHAT")
        data=st.file_uploader("Upload a file",type=['txt','csv'])
        if data is None:
            steps()
        else:
            df=process_data(data)
            ##Show processed data
            st.header("Processed Data")
            st.write(df)

            #media msg info
            st.header("Who Share more media msg ?")
            st.subheader(' media msgs info')
            mediamsg=df[df['Text']==' media shared']
            st.write(mediamsg)
            no_mediamsg=mediamsg['Name'].value_counts()
            st.write(no_mediamsg)
            st.bar_chart(no_mediamsg)

            ##word and letter count
            st.header("Words and Letters used by Each person")
            df['Letter_Count']=df['Text'].apply(char_counter)
            df['Word_Count']=df['Text'].apply(word_counter)
            st.write(df[['Text','Letter_Count','Word_Count']])

            ##most active user
            st.header("most active user :")
            active_user=df['Name'].mode()
            st.info(active_user.iloc[0])

            #Number of messages send by each user
            st.header("Number of messages send by each user")
            st.write(df[['Name','Text']].groupby('Name').count())

            #Words used by each person
            st.header("Words used by each person: ")
            name_value_count=df['Name'].value_counts().head(4)
            st.write(name_value_count)

            ##chat go time
            #st.header("how long did the chat go?")

            ##delete file
            # st.header("Delete File")
            # if st.button("Delete uploaded file"):
            #     # os.remove("")
            #     st.write("File Removed")




    else:
        st.header("CHAT VISUALIZATION")
        data=st.file_uploader("Upload a file",type=['txt','csv'])
        if data is None:
            steps()
        else:
            df=process_data(data)
            df['Letter_Count']=df['Text'].apply(char_counter)
            df['Word_Count']=df['Text'].apply(word_counter)
            all_columns_name=df.columns.tolist()

            #Seaborn plot
            if st.checkbox("Correlation plot[Seaborn]"):
                st.write(sns.heatmap(df.corr(),annot=True))
                st.pyplot()

            #Count plot
            if st.checkbox("Plot of Value counts"):
                st.text("Value count by targets")
                all_columns_name=df.columns.tolist()
                primary_col=st.selectbox("Primary Column To GroupBy",all_columns_name)
                selected_columns_names=st.multiselect("Select Columns",all_columns_name)
                if st.button("Plot"):
                    st.text("Generate a plot")
                    if selected_columns_names:
                        vc_plot=df.groupby(primary_col)[selected_columns_names].count()
                    else:
                        vc_plot=df.iloc[:,-1].value_counts()
                    st.write(vc_plot.plot(kind="bar"))
                    st.pyplot()

            
            #pie chart
            if st.checkbox("Pie plot"):
                all_columns_name=df.columns.tolist()
                if st.button("Generate pie plot"):
                    st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
                    st.pyplot()

            #customizable plot
            type_of_plot=st.selectbox("Select type of plot",["area","bar","line","hist","box","kde"])
            selected_columns_names=st.multiselect("Select Columns To Plot",all_columns_name)
            if st.button("Generate a Plot"):
                st.success("Generating a plot of {} for {}".format(type_of_plot,selected_columns_names))
                if type_of_plot=='area':
                    cust_data=df[selected_columns_names]
                    st.area_chart(cust_data)

                if type_of_plot=='bar':
                    cust_data=df[selected_columns_names]
                    st.bar_chart(cust_data)

                if type_of_plot=='line':
                    cust_data=df[selected_columns_names]
                    st.line_chart(cust_data)

                # custom plot

                if type_of_plot:
                    scust_plot=df[selected_columns_names].plot(kind=type_of_plot)
                    st.pyplot()

            if st.button("It's Completed"):
                st.balloons()
   
if __name__ == "__main__":
    main()
