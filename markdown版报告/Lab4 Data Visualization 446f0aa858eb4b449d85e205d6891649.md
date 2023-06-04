# Lab4:Data Visualization

2051498 储岱泽


# 1. Dataset Selection & Task Description

## 1.1 Dataset Selection

The dataset I have chosen is "googleplaystore.csv". This dataset provides specific data on App, Category, Rating, Reviews, and other attributes. It offers valuable insights into the mobile app market on the Google Play Store.

## 1.2 Objectives

The main objective of this data analysis task is to explore and visualize the relationships between different attributes of mobile apps in various categories. By utilizing data visualization techniques, we aim to uncover patterns, trends, and insights that can aid in understanding user preferences, app performance, and market dynamics.

 Next，I will create a dashboard based on the following relationships:

- The relationship between the number of APPs and Ratings for each Category.(bar chart)
- The comparison of App installs within a Category . (word cloud)
- The relationship between the number of Installs and Rating for each Category.(scatter chart)
- The relationship between the number of Reviews and Rating for each Category.(scatter chat)
- The Percentage of Apps in Each Category out of the Total Number of Apps.(Pie chart)

## 1.3 Characteristics

Some key characteristics of the dataset include:

1. **Diverse Categories:** The dataset covers a wide range of app categories, including games, social networking, productivity, entertainment, education, and more. This diversity allows for an extensive analysis of different types of mobile apps and their characteristics.
2. **Rating and Reviews:** The dataset includes user ratings and reviews for each app, which provides an indication of user satisfaction and feedback. Analyzing the relationship between ratings, reviews, and other attributes can provide insights into user preferences and app performance.
3. **Installations:** The dataset also provides information on the number of installations for each app. This allows for the exploration of the popularity and reach of different apps within specific categories.
4. **Size and Price:** Additional attributes such as the size of the app and its price (if applicable) can be utilized to understand user preferences and market dynamics.

# 2. Design



## 2.1 ****Dashboard Overview****

![Untitled](Lab4%20Data%20Visualization%20446f0aa858eb4b449d85e205d6891649/Untitled.png)

## 2.2 “**Number of Apps and Ratings by Category**”-Bar Chart

This bar chart displays the distribution of app ratings within each category. Users can select a specific category from the dropdown menu to observe the corresponding app count for each rating.

![Untitled](Lab4%20Data%20Visualization%20446f0aa858eb4b449d85e205d6891649/Untitled%201.png)

```python
#定义柱状图的回调函数
@app.callback(Output('category-rating-bar', 'figure'),
              [Input('category-dropdown', 'value')])
def update_bar_chart(category):
    filtered_df = df[df['Category']==category]
    grouped_df = filtered_df.groupby(['Rating']).size().reset_index(name='count')
    data = [go.Bar(x=grouped_df['Rating'],
                   y=grouped_df['count'],
                   marker={'color': grouped_df['count'], 'colorscale': 'Sunset', 'cmin': 0, 'cmax': max(grouped_df['count'])})]
    layout = go.Layout(title=f'App ratings in {category} category',
                       xaxis={'title': 'Rating'},
                       yaxis={'title': 'Count'},
                       plot_bgcolor= 'rgb(30, 31, 41)',
                       paper_bgcolor= 'rgb(30, 31, 41)',
                       font= {'color': 'white'})
    return {'data': data, 'layout': layout}
```

## 2.3 “**App Installs Comparison within a Category”-Word Cloud**

The word cloud visualizes the ranking of app downloads within a chosen category. The size of each app name in the word cloud corresponds to the number of downloads, with larger names indicating higher download counts.

![Untitled](Lab4%20Data%20Visualization%20446f0aa858eb4b449d85e205d6891649/Untitled%202.png)

```python
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
    wc = wordcloud.WordCloud(width=800, height=400, background_color='black', colormap='plasma').generate_from_frequencies(words)
    # 将词云图转换为 Base64 编码的图片
    img = wc.to_image()
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"
```

## 2.4”**Percentage of Apps in Each Category**”-Pie Chart

The pie chart illustrates the proportion of apps in each category out of the total number of apps. Users can gain a clear understanding of the distribution of app categories and their relative importance in the dataset.

![Untitled](Lab4%20Data%20Visualization%20446f0aa858eb4b449d85e205d6891649/Untitled%203.png)

```python
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
```

## 2.5 Two Scatter Charts-’Reviews vs Rating’ & ’Installs vs Rating’

 

- The above scatter chart demonstrates the relationship between app installs and ratings within each category. Users can hover their mouse over data points to view the specific values of installs and ratings for a given app.
- Another scatter chart showcases the relationship between app reviews and ratings within each category. Similar to the previous scatter chart, users can explore the detailed information of reviews and ratings by interacting with the chart.

![Untitled](Lab4%20Data%20Visualization%20446f0aa858eb4b449d85e205d6891649/Untitled%204.png)

```python
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
```