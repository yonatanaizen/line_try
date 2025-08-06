import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go

st.title("Reliability sketch")
x = st.file_uploader("Choose a file", type=["csv", "xlsx"], accept_multiple_files=True)
if x:

    data = pd.read_excel(x[0])
    data['line'] = data['unique_line'].apply(lambda x: x.split('_')[-1])
    data['Direction'] = data['unique_line'].apply(lambda x: x.split('_')[2])

    st.dataframe(data.head())

    # d = st.slider('Chose station', 0, 41, value=(2, 8))
    #
    # data = data[(data['StopSequence'] >= d[0]) & (data['StopSequence'] <= d[1])].reset_index(drop=True)

    A = list(data.columns[:6]) + list(data.columns[-7:])
    B = list(data.columns[6:-7])
    # B
    result = pd.melt(data, id_vars=A, value_vars=B)
    hour_option = sorted(data['Hour'].unique().tolist())
    directions = data['Direction'].unique().tolist()
    print(directions)

    col1, col2, col3 = st.columns(3)

    with col1:
        line = st.selectbox('Choose a line', data['line'].unique().tolist())

    with col2:
        hour = st.selectbox('Choose an hour', hour_option, index=hour_option.index(8))
    with col3:
        print(333)
        print(directions)
        directions_2 = st.selectbox('Choose a direction', directions, index=0)
    result_a = result[
        (result['line'] == line) & (result['Hour'] == hour) & (result['Direction'] == directions_2)].reset_index(
        drop=True)

    d = st.slider('Chose station', 0, 41, value=(2, 8))

    # result_a=result[(result['line']==line)&(result['Hour']==hour)&(result_a['Direction']==directions_2)].reset_index(drop=True)
    result_a = result_a[(result_a['StopSequence'] >= d[0]) & (result_a['StopSequence'] <= d[1])].reset_index(drop=True)

    A = result_a[result_a['variable'] == 'Time_diff_90'].reset_index(drop=True)
    B = result_a[result_a['variable'] == 'Time_diff_10'].reset_index(drop=True)
    C = result_a[result_a['variable'] == 'Time_diff_80'].reset_index(drop=True)
    D = result_a[result_a['variable'] == 'Time_diff_20'].reset_index(drop=True)
    E = result_a[result_a['variable'] == 'Time_diff_50'].reset_index(drop=True)
    F = result_a[result_a['variable'] == 'Time_diff_30'].reset_index(drop=True)
    G = result_a[result_a['variable'] == 'Time_diff_70'].reset_index(drop=True)
    H = result_a[result_a['variable'] == 'Time_diff_60'].reset_index(drop=True)
    I = result_a[result_a['variable'] == 'Time_diff_40'].reset_index(drop=True)

    # Create the bar trace
    bar_trace_10_90_t = go.Bar(
        name='10-90',
        x=A['StopSequence'],
        y=A['value'] - B['value'],
        base=B['value'],
        marker=dict(
            color=A['grade'],
            colorscale='Greens',
            cmin=0,
            cmax=100,
            colorbar=dict(
                title='Grade',
                x=1.05,
                xanchor='left',
                y=-0.5,
                len=0.8,
                thickness=15
            )
        )
    )

    bar_trace_50 = go.Bar(
        name='50',
        x=E['StopSequence'],
        y=E['value'] - B['value'],
        base=B['value'],
        marker=dict(
            color=E['grade'],
            colorscale='Greens',
            cmin=0,
            cmax=100,
            showscale=False  # Hide this second colorbar
        ),
        text=E['value'].round(),
        textposition='inside',
        textfont=dict(
            size=12,  # Set the desired font size
            color="black"  # Optional: set text color for readability
        )
    )

    bar_trace_20_80 = go.Bar(
        name='20-80',
        x=C['StopSequence'],
        y=C['value'] - D['value'],
        base=D['value'],
        marker=dict(
            color=D['grade'],
            colorscale='Greens',
            cmin=0,
            cmax=100,
            showscale=False  # Hide this second colorbar
        ), visible='legendonly'
        # Optional: set text color for readability
    )

    bar_trace_30_70 = go.Bar(
        name='30-70',
        x=F['StopSequence'],
        y=F['value'] - G['value'],
        base=G['value'],
        marker=dict(
            color=G['grade'],
            colorscale='Greens',
            cmin=0,
            cmax=100,
            showscale=False  # Hide this second colorbar
        ), visible='legendonly'
        # Optional: set text color for readability
    )

    bar_trace_40_60 = go.Bar(
        name='40-60',
        x=H['StopSequence'],
        y=H['value'] - I['value'],
        base=I['value'],
        marker=dict(
            color=I['grade'],
            colorscale='Greens',
            cmin=0,
            cmax=100,
            showscale=False  # Hide this second colorbar
        ), visible='legendonly'
        # Optional: set text color for readability
    )

    # Create annotations below the base of each bar
    annotations = [
                      dict(
                          x=A['StopSequence'].iloc[i],
                          y=B['value'].iloc[i] - 2,  # 2 units below base
                          text=str(round(B['value'].iloc[i])),
                          showarrow=False,
                          font=dict(color="black", size=12),
                          yanchor="top"
                      )
                      for i in range(len(A))
                  ] + [
                      dict(
                          x=A['StopSequence'].iloc[i],
                          y=A['value'].iloc[i] + 6,  # 2 units below top
                          text=str(round(A['value'].iloc[i])),
                          showarrow=False,
                          font=dict(color="black", size=12),
                          yanchor="top"
                      )
                      for i in range(len(A))
                  ]

    max_y = A['value'].max()
    # Plot the figure
    fig = go.Figure(data=[bar_trace_10_90_t, bar_trace_50, bar_trace_20_80, bar_trace_30_70, bar_trace_40_60])
    fig.update_layout(
        barmode='stack',
        yaxis=dict(range=[0, max_y + 8])
    )
    fig.update_layout(annotations=annotations)
    'Graph N 2'
    title = 'Less than 2 option'
    result_a_g3 = result_a[['unique_line', 'StopSequence', 'less_2', 'Direction']].drop_duplicates()
    result_a_g3.sort_values(by='StopSequence', inplace=True)

    fig_3 = px.line(x=result_a_g3['StopSequence'], y=result_a_g3['less_2'], title=title,
                    text=result_a_g3['less_2'].round(2))
    fig_3.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    fig_3.update_traces(textposition='top center')  # Position of the labels
    print(result_a_g3)

    options = st.multiselect(
        "Select graphs to grades or Percentage of arrivals :",
        ['Minute line', 'Arrival percentage'],
        default=['Minute line']
    )

    if 'Minute line' in options:
        st.plotly_chart(fig, use_container_width=True)
    if 'Arrival percentage' in options:
        st.plotly_chart(fig_3, use_container_width=True)

# st.markdown(
#         """
#         <style>
#         .stApp {
#             /* Dark blue with grey tint and 80% opacity */
#             background-color: rgba(20, 30, 50, 0.8);
#             color: white;
#             min-height: 100vh;
#             padding: 1rem;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
# )

#
# st.markdown(
#     """
#     <style>
#     .stApp {
#         /* Soft white background with a slight gradient for better aesthetics */
#         background: linear-gradient(135deg, #ffffff, #f9f9f9);
#         color: #333333;  /* Dark gray text for better readability */
#         min-height: 100vh;
#         padding: 1rem;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

st.markdown(
    """
    <style>
    .stApp {
        /* Gentle gradient with soft teal and subtle green tones */
        background: linear-gradient(135deg, #A8DADC, #457B9D);
        color: #F1FAEE; /* Light muted cream text for readability */
        min-height: 100vh;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)





