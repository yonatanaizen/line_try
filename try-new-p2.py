import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Reliability sketch")

x=st.file_uploader("Choose a file", type=["csv", "xlsx"], accept_multiple_files=True)
y=st.file_uploader("Choose a seconds file", type=["csv", "xlsx"], accept_multiple_files=True)

if x and y:
    data=pd.read_excel(x[0])
    data_2 = pd.read_excel(y[0])

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

    # st.plotly_chart(fig, use_container_width=True)


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

    a = data[data['variable'] == 'per_low'].reset_index(drop=True)
    b = data[data['variable'] == 'per_up'].reset_index(drop=True)
    # b['exc_diffrence'] = (b['exc'] - b['exc'].shift(1)) / b['exc'].shift(1)
    b['exc_diffrence'] = (b['exc'].shift(-1)-b['exc']  ) / b['exc'].shift(-1)

    b['Color'] = 'dodgerblue'
    b.loc[b['exc_diffrence'] > 0.15, 'Color'] = 'red'


    # fig_2 = go.Figure()
    from plotly.subplots import make_subplots

    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig_2.add_trace(go.Bar(x=a['StopSequence'], y=b['exc'] - a['exc'],base=a['exc'],marker=dict(color=b['Color']),text=b['exc'], textposition='outside'  ),    secondary_y=False)

    fig_2.update_layout( barmode='overlay',  title="Time distribution",    yaxis=dict(range=[0, max(b['exc'].max()+5, a['exc'].max())])  )
    fig_2.add_trace(go.Bar(  x=a['StopSequence'],        y=b['exc'] - a['exc'],base=a['exc'],marker=dict(color=b['Color']),text=a['exc'],textposition='inside',     insidetextanchor='start'    ),    secondary_y=False  )

    fig_2.add_trace(go.Scatter(x=a['StopSequence'],y=a['Grade'],text=a['Grade'],    mode="lines+text",textposition="top center",    line=dict(color='green')  ),secondary_y=True)

    title = f'Percentage of arrivals in less than 2 minutes'

    data_2=data_2[(data_2['StopSequence']>=d[0])&(data_2['StopSequence']<=d[1])].reset_index(drop=True)


    fig_3 = px.line(x=data_2['StopSequence'], y=data_2['less_2'], title=title, text=data_2['less_2'].round(2))
    fig_3.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    fig_3.update_traces(textposition='top center')  # Position of the labels

    # st.plotly_chart(fig_2, use_container_width=True)

    options = st.multiselect(
        "Select graphs to grades or Percentage of arrivals :",
        [ 'Minute line','Time arivel precentege','percent Scatter'],
        default=['Minute line']
    )
    # data = data.sort_values(by='StopOrder').reset_index(drop=True)

    if 'percent Scatter' in options:
        st.plotly_chart(fig, use_container_width=True)

    if 'Minute line' in options:
        st.plotly_chart(fig_2, use_container_width=True)
    if 'Time arivel precentege' in options:
        st.plotly_chart(fig_3, use_container_width=True)

    data_b=data[['StopSequence','StopName','StopCode']].drop_duplicates().reset_index(drop=True).T

    st.dataframe(data_b)

st.header('Methodology:')

st.write('We compute two criteria: the first measures the difference between the 90th and 10th percentiles (0.9, 0.1) of consecutive arrivals, and the second calculates the difference between the 95th and 5th percentiles (0.95, 0.05) of the daily median.The final grade is calculated as 100 minus the average of these two criteria')

st.markdown("""
### Example:

Suppose we have 1,000 arrivals in a day.  
We create a vector of differences, sort it, and calculate the following percentiles:
- 90th percentile: 90  
- 10th percentile: 10  
- 95th percentile: 95  
- 5th percentile: 5  

Now, we compute the differences:
- 90th - 10th = 80  
- 95th - 5th = 90  

The final grade is calculated as:  
**100 − average of the two differences = 100 − ((80 + 90) / 2) = 15**
""")

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

