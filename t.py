# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:dandan.zheng 
@file: getrank.py
@time: 2018/03/27
"""

import sys
from pymongo import MongoClient
import pandas as pd

userid = 1
client = MongoClient()
db = client.shiyanlou
data = pd.DataFrame(list(db.contests.find()))
print (data)
print (list(data['user_id']))
print (type(list(data['user_id'])))
statistic_data = data.groupby(['user_id'])['score', 'submit_time'].sum()
sorted_data = statistic_data.sort_values(['submit_time']).sort_values(['score'], ascending=False)
index_data = sorted_data.reset_index()
index_data['rank'] = index_data.index + 1
user_data = index_data[index_data['user_id'] == userid]
rank = user_data['rank'].values
score = user_data['score'].values
submit_time = user_data['submit_time'].values
