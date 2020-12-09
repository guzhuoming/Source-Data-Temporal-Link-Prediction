import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import math

def if_exist_phish():
    filePath = 'F:\\ht\\data-0-hop-with-label-816\\'
    li = os.listdir(filePath)
    print(li)
    set1 = set()
    for s in li:
        pos = s.find('.')
        x = s[0:pos]
        set1.add(x)

    set2 = set()
    f = 'F:\\ht\\accounts_label_phish-hack.csv'
    data = pd.read_csv(f)
    address = data['Address']
    for i in range(len(address)):
        set2.add(address[i])

    set3 = set1 & set2
    print('交集长度：{}'.format(len(set3)))

    max = 0
    temp = ''
    for s in set3:
        for i in range(len(data)):
            if data['Address'][i] == s:
                if ','in data['Txn Count'][i]:
                    pos = data['Txn Count'][i].find(',')
                    data['Txn Count'][i] = data['Txn Count'][i][0:pos] + data['Txn Count'][i][pos+1:]
                    print(data['Txn Count'][i])
                if max<int(data['Txn Count'][i]):
                    max = int(data['Txn Count'][i])
                    temp = data['Address'][i]
                break

    print('max={}'.format(max))
    print('temp={}'.format(temp))

def weeks_nodepair():
    # filePath = 'F:\\研一\\Temporal-Link-Prediction\\data\\temporal link features_5_7days_739' # 5周
    filePath = 'F:\\研一\\Temporal-Link-Predicition-fixed\\data\\features_4' # 12个3天
    n = 12
    li = os.listdir(filePath)

    weeks_transaction = {}

    for i in range(n+1):
        weeks_transaction[i]=0

    for l in li:
        f = open(filePath+"\\"+l)
        data = pd.read_csv(f)

        temp = 0
        for i in range(n):
            if data['tran_num'][i] > 0:
                temp += 1
        weeks_transaction[temp] = weeks_transaction[temp]+1
    print(weeks_transaction)
    x = range(n+1)
    y = []
    for i in range(n+1):
        y.append(weeks_transaction[i])
    plt.bar(x,y)
    plt.xlabel('number of weeks with transaction')
    plt.ylabel('number of node pairs')
    # 添加数据标签，也就是给柱子顶部添加标签
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.show()

def plot_transaction():
    # 1515254400
    minTime = 1483200000
    maxTime = 1577808000
    n = 1
    gap = (maxTime-minTime)//(n*86400) + 1
    print('gap = {}'.format(gap))

    # filePath = 'F:\\binance-exchange'
    # li = os.listdir(filePath)
    # print(li)
    # tran = [[0 for i in range(gap)] for i in range(len(li))]

    f = open('F:\\ht\\huobi.csv')
    exchange = pd.read_csv(f)

    tran = [[0 for i in range(gap)] for i in range(len(exchange))]

    for i in range(len(exchange)):
        node = exchange['address'][i]
        try:
            file = open('F:\\ht\\data-0-hop-with-label-816\\{}.csv'.format(node))
            df = pd.read_csv(file)
        except:
            continue

        print('node: {}, len(df) = {}'.format(node, len(df)))

        for j in range(len(df)):
            if df['TimeStamp'][j]<minTime or df['TimeStamp'][j]>maxTime:
                continue
            t = (df['TimeStamp'][j] - minTime)//(86400*n)
            tran[i][t] = tran[i][t] + 1

        x = range(gap)
        y = tran[i]
        plt.bar(x, y)
        plt.xlabel('time')
        plt.ylabel('number of transactions')
        plt.title(node)
        # 添加数据标签，也就是给柱子顶部添加标签
        for a, b in zip(x, y):
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        plt.show()

# def plot_address_transaction():
#     file = open('F:\\ht\\address_continual_transaction.csv')
#     df = pd.read_csv(file)
#     for i in range(len(df)):
#         address = df['address'][i]

def swap(x, y):
    return y, x

def nonzero_timesteps(li):
    ret = 0
    for i in range(len(li)):
        if li[i] > 0:
            ret += 1
    return ret

def plot_address_pair_transaction():
    """
    对每个节点，每个时间段
    :return:
    """
    n = 1
    minTime = 1483200000
    file = open('F:\\ht\\huobi.csv')
    df = pd.read_csv(file)

    dict_list = [{} for i in range(len(df))]

    ans = 0 #
    address2_set = set()

    for i in range(len(df)):
        address = df['address'][i]

        file2 = open('F:\\ht\\data-0-hop-with-label-816\\{}.csv'.format(address))
        data = pd.read_csv(file2)

        for j in range(len(data)):

            x = data['From'][j]
            y = data['To'][j]
            if x>y:
                x, y = swap(x, y)
            address_pair = x+'_'+y
            print('i = {}, j = {}'.format(i, j))
            if address_pair not in dict_list[i]:
                dict_list[i][address_pair] = [0 for k in range(50)]
            t = (data['TimeStamp'][j] - minTime) // (86400 * n)
            t -= 320 # 320-370
            if t>=0 and t<50:
                dict_list[i][address_pair][t] = dict_list[i][address_pair][t] + 1


        for k in dict_list[i].keys():
            if nonzero_timesteps(dict_list[i][k]) > 40:
                ans += 1

                # 记录24个节点对涉及到的除了huobi节点外的节点
                pos = k.find('_')
                x = k[0:pos]
                y = k[pos+1:]
                if x not in df['address']:
                    address2_set.add(x)
                if y not in df['address']:
                    address2_set.add(y)

                x_ = range(len(dict_list[i][k]))
                plt.bar(x_, dict_list[i][k])
                plt.xlabel('time')
                plt.ylabel('transaction')
                plt.title(k)
                print('key = {}'.format(k))
                plt.show()


        address2 = pd.DataFrame(columns=('address',))
        for s in address2_set:
            address2 = address2.append([{'address': s}], ignore_index=True)

        address2.to_csv('F:\\ht\\address2.csv', index=False)
        print('ans = {}'.format(ans))
        print('dict-list.length = {}'.format(len(dict_list[i])))

def plot_address2_transaction():
    file = open('F:\\ht\\address2.csv')
    df = pd.read_csv(file)
    address3 = pd.DataFrame(columns=('address',))
    for i in range(len(df)):
        address = df['address'][i]
        if os.path.exists('F:\\ht\\data-0-hop-with-label-816\\{}.csv'.format(address)):
            print(0)
            address3 = address3.append([{'address': address}], ignore_index=True)
        elif os.path.exists('F:\\ht\\data-only-1-hop-without0-639668\\{}.csv'.format(address)):
            print(1)
            address3 = address3.append([{'address': address}], ignore_index=True)
        elif os.path.exists('F:\\ht\\data-2-hop\\{}.csv'.format(address)):
            print(2)
            address3 = address3.append([{'address': address}], ignore_index=True)
        else:
            print(3)
    address3.to_csv('F:\\ht\\address3.csv', index=False)
if __name__=='__main__':
    # if_exist_phish()
    # plot_transaction()
    # plot_address_pair_transaction()
    plot_address2_transaction()