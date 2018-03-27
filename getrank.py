# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:dandan.zheng 
@file: getrank.py 
@time: 2018/03/27 
"""

import sys
import pandas as pd
from pymongo import MongoClient


def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    # 计算用户 user_id 的排名、总分数及花费的总时间
    # 所有数据
    data = pd.DataFrame(list(contests.find()))
    if user_id in list(data['user_id']):
        # 计算数据
        statistic_data = data.groupby(['user_id'])['score', 'submit_time'].sum()
        # 排序数据
        sorted_data = statistic_data.sort_values(['submit_time']).sort_values(['score'], ascending=False)
        # 重新设置数据集索引
        index_data = sorted_data.reset_index()
        # 优化索引
        index_data['rank'] = index_data.index + 1
        # 取确定数据
        user_data = index_data[index_data['user_id'] == user_id]
        rank = user_data['rank'].values
        score = user_data['score'].values
        submit_time = user_data['submit_time'].values

        # 依次返回排名，分数和时间，不能修改顺序
        return (rank,score,submit_time)
    else:
        print('Parameter Error!')


if __name__ == '__main__':
    # 1. 判断参数格式是否符合要求
    if len(sys.argv) != 2:
        print('Parameter Error')
        sys.exit(1)
    # 2. 获取 user_id 参数
    user_id = int(sys.argv[1])

    # 根据用户 ID 获取用户排名，分数和时间
    user_data = get_rank(user_id)
    print(user_data)
