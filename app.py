import streamlit as st
import pandas as pd
import numpy as np



html_temp="""
    <div style="background-color:springgreen;padding:15px;">
    <h1>WHATSAPP DATA VISUALIZATION AND ANALYSIS</h1>
    </div>
    """
html_temp1="""
    <div style="background-color:mediumseagreen;padding:5px;">
    <h1>STEPS TO START WITH</h1>
    </div>
    """

st.markdown(html_temp,unsafe_allow_html=True)
data=st.file_uploader("Upload a file")
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
#df.drop(df[df['Name'].isnull()],inplace=True)


st.sidebar.markdown(html_temp1,unsafe_allow_html=True)

st.sidebar.header("Steps To Use")
st.sidebar.image("images/whats2.jpg")
st.sidebar.subheader("1-> Open the WhatsApp conversation you would like to have visualized and tap on the group subject or contact name in the navigation bar")
st.sidebar.subheader("2-> Scroll to the bottom and tap on 'Export chat' ")
st.sidebar.subheader("3-> Select without media")
st.sidebar.subheader("4-> Select 'Mail'")
st.sidebar.subheader("5-> Enter ur email into the 'To' field , Tap on Send")
st.sidebar.subheader("6-> Download your chat from the mail and browse here from that location")
st.sidebar.subheader("7-> That's It, now ready to analyse and visualize your chat")

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

def main():
    if st.checkbox("Show Processed Data:"):
        st.header("Processed Data")
        st.write(df)

    if st.checkbox("Who Share more media msg ?"):
        st.subheader(' media msgs info')
        mediamsg=df[df['Text']==' media shared']
        st.write(mediamsg)
        no_mediamsg=mediamsg['Name'].value_counts()
        st.write(no_mediamsg)
        st.bar_chart(no_mediamsg)

    if st.checkbox("Words and Letters used by Each person"):
        df['Letter_Count']=df['Text'].apply(char_counter)
        df['Word_Count']=df['Text'].apply(word_counter)
        st.write(df[['Text','Letter_Count','Word_Count']])
        
    if st.checkbox("Words used by each person: "):
        name_value_count=df['Name'].value_counts().head(4)
        st.write(name_value_count)

    if st.checkbox("most active user :"):
        active_user=df['Name'].mode()
        st.info(active_user.iloc[0])

    if st.checkbox("Number of messages send by each user"):
        st.write(df[['Name','Text']].groupby('Name').count())

    if st.checkbox("how long did the chat go"):
        pass

    #customizable plot
    st.header("Visualization of chats data")
    all_columns_name=df.columns.tolist()
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
            cust_plot=df[selected_columns_names].plot(kind=type_of_plot)
            st.pyplot()

    if st.button("It's Completed"):
        st.balloons()
    
    
if __name__ == "__main__":
    main()
