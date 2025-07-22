import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Reliability sketch")

x=st.file_uploader("Choose a file", type=["csv", "xlsx"], accept_multiple_files=True)
if x:
    data=pd.read_excel(x[0])
    print(data.columns)
# data=pd.read_excel(r"C:\Users\yonat\Downloads\77_08.xlsx")
# print(data['unique_line'])

# line_options=['ALL']+data['unique_line'].unique().tolist()
# col1, col2 = st.columns(2)
#
# # First dropdown (line selection)
# with col1:
#     selected_line = st.selectbox('Choose a line', line_options)
#     if selected_line != 'ALL':
#         data = data[data['unique_line'] == selected_line].reset_index(drop=True)
#
# # Second dropdown (hour selection)
# with col2:
#     hour_options = ['ALL'] + data['Hour'].unique().tolist()
#     selected_hour = st.selectbox('Choose an Hour', hour_options)
#     if selected_hour != 'ALL':
#         data = data[data['Hour'] == selected_hour].reset_index(drop=True)


# print(d)
    st.dataframe(data)
    d=st.slider('Chose station',0,41,value=(2, 8))

    data=data[(data['StopSequence']>=d[0])&(data['StopSequence']<=d[1])].reset_index(drop=True)

    data=data.sort_values(by=['StopSequence','exc']).reset_index(drop=True)

    # title = f'grade vs station Toatl grade for line {data['grade_H'].iloc[0].round(3)}'
    fig=px.bar(x=data['StopSequence'],y=data['value'],color=data['variable'],text=data['RT'],title='line 77 Freq 20')
    # fig.update_layout(    title={'x': 0.5,'xanchor': 'center'})
    # fig.update_traces(textposition='top center')  # Position of the labels

    st.plotly_chart(fig, use_container_width=True)
#
# title = f'Percentage of arrivals in less than 2 minutes'
# fig_2=px.line(x=data['StopOrder'],y=data['less_2'],title=title,text=data['less_2'].round(2))
# fig_2.update_layout(    title={'x': 0.5,'xanchor': 'center'})
# fig_2.update_traces(textposition='top center')  # Position of the labels
#
#
# options = st.multiselect(
#     "Select graphs to grades or Percentage of arrivals :",
#     ['Grades Scatter', 'Arivel line'],
#     default=['Grades Scatter']
# )
# data=data.sort_values(by='StopOrder').reset_index(drop=True)
#
# if 'Grades Scatter' in options:
#
#     st.plotly_chart(fig, use_container_width=True)
#
# if 'Arivel line' in options:
#     st.plotly_chart(fig_2, use_container_width=True)

# graph_col1, graph_col2 = st.columns(2)
# with graph_col1:
#     st.plotly_chart(fig, use_container_width=True)
# with graph_col2:
#     st.plotly_chart(fig_2, use_container_width=True)
#


    data_b=data[['StopSequence','StopName','StopCode']].drop_duplicates().reset_index(drop=True).T

    st.dataframe(data_b)

st.markdown(
        """
        <style>
        .stApp {
            /* Dark blue with grey tint and 80% opacity */
            background-color: rgba(20, 30, 50, 0.8);
            color: white;
            min-height: 100vh;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
)

