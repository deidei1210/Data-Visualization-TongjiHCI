import dash
import wordcloud
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import base64
from io import BytesIO


#创建Dash应用程序对象
app = dash.Dash()
# 读取数据并清洗
df = pd.read_csv('googleplaystore.csv')
df = df.dropna(axis=0, how="any")

# 得到每一个分类的名称
name = df['Category'].unique()
# 得到每一个分类下APP的个数
Category_app_counts = df['Category'].value_counts()
print(Category_app_counts)

# 计算每一个APP被下载的总次数
installs = []
for n in name:
    total = 0
    # print(n)
    dff = df[df['Category'] == n]['Installs']
    for d in dff:
        d = d[0:-1]
        d = d.replace(',', '')
        d = int(d)
        total += d
    # print(total)
    installs.append(total)
# 修改配色方案
colors = ['#FFC107', '#FF6384', '#36A2EB', '#FF5722', '#00BCD4', '#8BC34A', '#E91E63',
          '#9C27B0', '#3F51B5', '#2196F3', '#4CAF50', '#FF9800', '#673AB7', '#FF5252']
# draw the category-install Pie graph
categoryInstallPie = go.Figure(data=go.Pie(
    labels=Category_app_counts.index,
    values=Category_app_counts.values,
    hoverinfo='label+value+percent',
    textinfo='none',
    rotation=220,
    customdata=Category_app_counts.index,
    textposition='outside', # 设置标签在饼图外部
    # legend={'orientation': 'v', 'x': 0, 'y': 1}, # 设置图例在左边
    marker=dict(colors=colors) # 设置颜色方案
    ),
    layout=go.Layout(
        title={
            'text':'The Number of Each Category\'s APPs',
            'font': {'color': 'white'}
        }, # 设置标题文本颜色为白色        
        plot_bgcolor='rgb(30, 31, 41)', # 更新整个图表的背景颜色
        paper_bgcolor='rgb(30, 31, 41)', # 更新绘图区域的背景颜色
        font=dict(color='white') # 设置文本颜色为白色
    )

)

# 计算每个rating的App有多少
rateCount = df.Rating.value_counts()
maxCount = max(rateCount)
rateCount = {'Rating': rateCount.index, 'Count': rateCount.values}
dfRateCount = pd.DataFrame(rateCount)
dfRateCount = dfRateCount.sort_values(by="Rating", ascending=True)


def get_color(temp):
    return 'rgb({r}, {g}, {b})'.format(
        r=int(temp/maxCount*200),
        g=int((1-temp/maxCount)*200),
        b=int((1-temp/maxCount)*200)
    )

# draw the category-count Bar graph
barFig = go.Figure(
    data=go.Bar(
        x=dfRateCount.Rating,
        y=dfRateCount['Count'].astype(int),
        customdata=dfRateCount.Count,
        marker={
            'color': [get_color(count) for count in dfRateCount['Count'].astype(int)]
        }
    ),
    layout=go.Layout(
        yaxis={
            'title': 'Count of App',
            'titlefont': {'color': 'white'}, # 设置y轴标题的文本颜色为白色
            'tickfont': {'color': 'white'} # 设置y轴刻度标签的文本颜色为白色
        },
        xaxis={
            'title': 'Rating',
            'titlefont': {'color': 'white'}, # 设置y轴标题的文本颜色为白色
            'tickfont': {'color': 'white'} # 设置y轴刻度标签的文本颜色为白色
        },
        title={
            'text': 'Each Rating\'s App Count',
            'font': {'color': 'white'}
        }, # 设置标题文本颜色为白色        
        plot_bgcolor='rgb(30, 31, 41)', # 更新整个图表的背景颜色
        paper_bgcolor='rgb(30, 31, 41)' # 更新绘图区域的背景颜色

    )
)

# 实现页面的布局
app.layout = html.Div([
    #顶部的单选按钮
    html.Div([
        # 页面主题
        html.H1('Google Play Store Dashboard', style={'textAlign': 'center','color':'white','z-index':2}),
        html.P('2051498 储岱泽 大二', style={'textAlign': 'center','color':'white','z-index':2}),

        html.Div([
            dcc.RadioItems(
                id='type',
                options=[{'label': type, 'value': type} for type in ['Linear', 'Log']],
                value='Log',
                labelStyle={'display': 'inline-block', 'margin-left': '80%'}
            )
        ],
        style={'width': '45%',
                'display': 'inline-block', 
                'margin-left': '45%'})
    ],
        style={
            'borderBottom': 'thin rgb(134,217,236) solid',
            'backgroundColor': 'rgb(30, 31, 41)',
            'padding': '10px 5px'
        }
    ),
    #条形图
    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in name],
            value=name[0]
        ),
         dcc.Graph(id='category-rating-bar')
        ],
        style={'display': 'inline-block', 
               'width': '49%',
               'backgroundColor': 'rgb(30, 31, 41)'}
    ),

    # 添加一个图像组件
    html.Img(id='wordcloud-image', src='',style={'display': 'inline-block', 
                                                'width': '49%',
                                                'backgroundColor': 'rgb(30, 31, 41)'}),

    #随着饼图变化的气泡图和散点图
    html.Div(
        [dcc.Graph(id='graph1'),
         dcc.Graph(id='graph2')],
        style={'display': 'inline-block', 
               'width': '49%',
               'backgroundColor': 'rgb(30, 31, 41)'}
    ),
    #饼图
    html.Div(
        dcc.Graph(
            id='circleGraph',
            figure=categoryInstallPie,
            hoverData={'points': [{'customdata': 'ART_AND_DESIGN'}]}
        ),
        style={'display': 'inline-block', 
               'width': '49%',
               'backgroundColor': 'rgb(30, 31, 41)'}
    ),

    
],
    style={'backgroundColor': 'rgb(30, 31, 41)'}
)

#气泡图的回调函数
@app.callback(
    Output('graph1', 'figure'),
    [
        Input('type','value'),
        Input('circleGraph', 'hoverData')
    ]
)
def updateGraph1(type,hoverData):
    dff = df[df['Category'] == hoverData['points'][0]['customdata']]
    print(dff)
    ydata = dff['Installs']
    yData = []
    for yd in ydata:
        yd = yd[0:-1]
        yd = yd.replace(',', '')
        yd = int(yd)
        yData.append(yd)
    s = dff['Size']
    size = []
    for _s in s:
        if _s == 'Varies with device':
            size.append(0)
            continue
        if 'M' in _s:
            _s = _s.split('M')[0]
            _s = float(_s)
        elif 'k' in _s:
            _s = _s.split('k')[0]
            _s = float(_s) / 1024
        size.append(_s / 2)
    return {
        'data': [go.Scatter(
            x=dff['Rating'].astype(float),
            y=yData,
            mode='markers',
            text=dff['App'] + '<br> Last updated: ' + dff['Last Updated'] + '<br>Size: ' + dff['Size'],
            customdata=dff['App'],
            marker={
                'size': size,
                'opacity': 0.5,
                'color': 'rgb(176,134,234)',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': {
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 10},
            'height': 225,
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': hoverData['points'][0]['customdata']
            }],
            'yaxis': {
                'title': 'Installs',
                'type': 'linear' if type == 'Linear' else 'log'
                # 'type': 'log'
            },
            'xaxis': {
                'title': 'Rating',
                'showgrid': True
            },
            'hovermode': 'closest',
            'plot_bgcolor': 'rgb(30, 31, 41)',
            'paper_bgcolor': 'rgb(30, 31, 41)',
            'font': {'color': 'white'},
        }
    }

#散点图的回调函数
@app.callback(Output('graph2', 'figure'),
              [Input('circleGraph', 'hoverData'),
                Input('type','value')])
def updateGraph2(hoverData, type):
    dff = df[hoverData['points'][0]['customdata'] == df['Category']]
    return {
        'data': [go.Scatter(
            x=dff['Rating'].astype(float),
            y=dff['Reviews'].astype(int),
            mode='markers',
            text=dff['App'] + '<br> Last updated: ' + dff['Last Updated'] + '<br>Size: ' + dff['Size'],
            customdata=dff['App'],
            marker={
                'size': 10,
                'opacity': 0.5,
                'color': 'rgb(236,108,183)',
                'line': {'width': 1, 'color': 'white'}
            }
        )],
        'layout': {
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 10},
            'height': 225,
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': hoverData['points'][0]['customdata']
            }],
            'yaxis': {
                'title': 'Reviews',
                'type': 'linear' if type == 'Linear' else 'log'
                # 'type':'log'
            },
            'xaxis': {
                'title': 'Rating',
                'showgrid': True
            },
            'hovermode': 'closest',
            'plot_bgcolor': 'rgb(30, 31, 41)',
            'paper_bgcolor': 'rgb(30, 31, 41)',
            'font': {'color': 'white'},
            
        }
    }

#定义柱状图的回调函数
@app.callback(Output('category-rating-bar', 'figure'),
              [Input('category-dropdown', 'value')])
def update_bar_chart(category):
    filtered_df = df[df['Category']==category]
    grouped_df = filtered_df.groupby(['Rating']).size().reset_index(name='count')
    data = [go.Bar(x=grouped_df['Rating'], y=grouped_df['count'])]
    layout = go.Layout(title=f'App ratings in {category} category',
                       xaxis={'title': 'Rating'},
                       yaxis={'title': 'Count'},
                       plot_bgcolor= 'rgb(30, 31, 41)',
                       paper_bgcolor= 'rgb(30, 31, 41)',
                       font= {'color': 'white'})
    return {'data': data, 'layout': layout}
# 定义生成词云的回调函数
@app.callback(
    Output('wordcloud-image', 'src'),
    [Input('category-dropdown', 'value')]
)
def generate_wordcloud(category):
    # 根据用户选择的 Category 筛选出对应的 App 名称和对应的 Reviews 数量
    data = df[df['Category'] == category][['App', 'Reviews']]
    # 将单词出现频率转换为浮点型
    data = data.astype({'Reviews': 'float'})
    # 将 App 名称和 Reviews 数量转换为字典形式
    words = dict(zip(data['App'], data['Reviews']))
    # 生成词云图
    wc = wordcloud.WordCloud(width=800, height=400, background_color='black', colormap='Accent').generate_from_frequencies(words)
    # 将词云图转换为 Base64 编码的图片
    img = wc.to_image()
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

if __name__ == '__main__':
    app.run_server(port=8080)#如果不指明运行的端口，则Dash应用程序默认会运行在本地主机（localhost）的8050端口上
