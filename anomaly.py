import os
import base64
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
#from sklearn.ensemble import IsolationForest



st.set_page_config(page_title = 'Anomaly Detection',layout="wide")

# To hide hamburger (top right corner) and “Made with Streamlit” footer :

hide_streamlit_style1 = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
            content:'Made By Ravinder';
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 0px;
            }
            </style>
            """
st.markdown(hide_streamlit_style1, unsafe_allow_html=True)

hide_streamlit_style2 = """
            <style>
            .css-18e3th9 {/*decrease gap from header*/
                flex: 1 1 0%;
                width: 100%;
                padding: 0rem 5rem 10rem;
                min-width: auto;
                max-width: initial;
                }
                
                h1 { /*Time saver top padding*/
                    font-family: "Source Sans Pro", sans-serif;
                    font-weight: 700;
                    
                    padding: 0rem 0px 0rem;
                    margin: 0px;
                    line-height: 1.4;
                }            

            <style>
            """
st.markdown(hide_streamlit_style2, unsafe_allow_html=True)

upload1,uploadsp,upload2 = st.columns((2,.1,2))

with upload1:
    
    ttl = f'<p style="font-family:sans-serif; font-size: 35px;">Anomaly Detection</p>'
    st.markdown(f"**<h1 style='text-align: center; '>{ttl}</h1>**", unsafe_allow_html=True)
    st.markdown("**In data analysis, anomaly detection (also referred to as outlier detection and sometimes as novelty detection) is generally understood to be the identification of rare items, events or observations which deviate significantly from the majority of the data and do not conform to a well defined notion of normal behaviour.[1] Such examples may arouse suspicions of being generated by a different mechanism,[2] or appear inconsistent with the remainder of that set of data.[3] (wikipedia.org)**")

with upload2:
    data = st.file_uploader("Upload Clean Dataset", type=["txt"])
    if data is not None:
        file = pd.read_fwf(data, colspecs='infer', widths=None, infer_nrows=100).columns.tolist()
        data_name = f'<p style="font-family:sans-serif; color:#AC123E;font-size: 22px;">{data.name}</p>'
    else :
        file = 'data88.txt'
        data_name = f'<p style="font-family:sans-serif; color:#AC123E;font-size: 22px;">{file}</p>'
st.markdown(f"**<h1 style='text-align: center; '>{data_name}</h1>**", unsafe_allow_html=True)    
def main():
    data = np.loadtxt(file, delimiter=',', dtype=str)
    df = pd.DataFrame(data,columns=['values'])
    df.drop(df.shape[0]-1,inplace=True)
    df['values'] = df['values'].astype(int)
    df.reset_index(inplace = True, drop=True) # resetting index
    df1 = df.copy()
    df1['values'] = df1['values'].astype('str')
    
    df['values'] = df['values'].astype('str')
    fig, ax = plt.subplots()
    plot1,plotsp1,plotsp2,plot2 = st.columns((1.5,.1,.1,2))
    with plot2 :
        ttl = f'<p style="font-family:sans-serif;color : blue; font-size: 20px;">Visualising Raw Data</p>'
        st.markdown(f"**<h1 style='text-align: center; '>{ttl}</h1>**", unsafe_allow_html=True)
        dfcat = pd.DataFrame(df[['values']].groupby('values').agg('size')).reset_index().rename(columns={0:'count'}).sort_values('count',ascending=False).reset_index(drop=True)
        fig = px.bar(dfcat, y = 'values', x = 'count', text_auto=True,color='count',title=f"count plot of {df['values'].name}").update_yaxes(categoryorder='min ascending')
        fig.update_layout(title_text=f"Count plot of {df['values'].name}",title={
                                        'y':0.9,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'},title_font_color="red")
        fig.update_layout(
                            autosize=False,
                            width=500,
                            height=dfcat['values'].nunique()*80)
    
        st.plotly_chart(fig)
    with plot1 :
        ttl = f'<p style="font-family:sans-serif; color : blue; font-size: 20px;">Anomalies Detection on Data</p>'
        st.markdown(f"**<h1 style='text-align: center; '>{ttl}</h1>**", unsafe_allow_html=True)
        new_model = joblib.load('Isolation_forest_Model.joblib')
        pred = new_model.predict(df['values'].values.reshape(-1, 1))
        df_new = df.copy()
        df_new['pred'] = pred
        anos = df_new['values'][df_new['pred']==-1].value_counts().index.astype(str)
        lis2=' ‎ ‎,‎ ‎ '.join(anos)
        st.write(f'**<FONT color="#FC7726">►‎ ‎ ‎ ‎ Anomalies Detected :‎ ‎</FONT>**',f'**<FONT color="steelblue">{lis2}</FONT>**',unsafe_allow_html=True)
        no_anos = list(df_new['pred'][df_new['pred']==-1].value_counts().values)[0]
        st.write(f'**<FONT color="#FC7726">►‎ ‎ ‎ ‎ Number of Anomalies Detected :‎ ‎</FONT>**',f'**<FONT color="steelblue">{str(no_anos)}</FONT>**',unsafe_allow_html=True)

        
if __name__=="__main__":
    main()
# -




