import time
import random
def get_conflict_num(cur_status):
    """
    获取当前状态下互相攻击的皇后对数
    :param cur_status: 棋盘当前的状态
    :return:  当前状态下发生冲突的皇后对数
    """
    n = len(cur_status)
    conflict_num = 0
    for col1 in range(0, n):
        for col2 in range(col1+1, n):
            if cur_status[col1] == cur_status[col2] or ((col2-col1) == abs(cur_status[col1]-cur_status[col2])):
                conflict_num += 1
    return conflict_num

def get_optimal_status(cur_status, cur_conflict):
    """
    返回当前状态最优的邻居状态，如果不存在，返回本身
    :param cur_status: 棋盘当前状态
    :param cur_conflict: 当前状态互相攻击的皇后对数
    :return: 棋盘新的状态和新状态下互相攻击的皇后对数
    """
    n = len(cur_status)
    for i in range(0, n-1):
        for j in range(i+1, n):
            cur_status[i], cur_status[j] = cur_status[j], cur_status[i]
            # 任意两列的皇后调换位置
            new_conflict = get_conflict_num(cur_status)
            if new_conflict < cur_conflict:
            # 若调换后互相攻击的皇后对数比之前少，返回调换后的状态
                cur_conflict = new_conflict
                return cur_status, cur_conflict
            cur_status[i], cur_status[j] = cur_status[j], cur_status[i]
    return cur_status, cur_conflict

def queen_ls_greed(n):
    # n = int(input("请输入皇后数目："))
    status = [i for i in range(n)]
    t1 = time.time()
    random.shuffle(status)
    print("当前棋盘上皇后的位置：\n{}".format(status))
    cur_conflict = get_conflict_num(status)
    if cur_conflict==0:
        print("找到最优解，最优解为：\n{}".format(status))
        t2 = time.time()
        print("程序运行总时间：{}s".format())
    while cur_conflict>0:
        new_status, new_conflict = get_optimal_status(status, cur_conflict)
        if new_conflict==0:
            # 互相攻击的皇后对数为0，表示已经找到最优解
            print("找到最优解，最优解为：\n{}".format(status))
            t2 = time.time()
            print("程序运行总时间：{}s".format(t2-t1))
            break
        elif new_conflict==cur_conflict:
            # 互相攻击的皇后对数没有减少，表示已经陷入局部最优
            random.shuffle(status)
            cur_conflict = get_conflict_num(status)
            if cur_conflict==0:
            # 互相攻击的皇后对数为0，表示已经找到最优解
                print("找到最优解，最优解为：\n{}".format(status))
                t2 = time.time()
                print("程序运行总时间：{}s".format(t2-t1))
                break
            continue
        status = new_status
        cur_conflict = new_conflict

if __name__ == '__main__':
    for i in range(100,1000,50):
        print('i={}'.format(i))
        queen_ls_greed(i)
