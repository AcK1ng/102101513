import random

dice1 = [0,0,0,0,0]#玩家一的骰子
dice2 = [0,0,0,0,0]#玩家二的骰子
locked_dice1 = [0,0,0,0,0]#玩家一被锁定的骰子，若该位置为1，则代表第几个骰子被锁定
locked_dice2 = [0,0,0,0,0]
chip1 = 1000
chip2 = 1000
Magnification = 1
lock1 = []
lock2 = []
def judge_shun(dice):
    # 判断是否为顺子
    dice.sort()
    if dice == [1, 2, 3, 4, 6]:
        return 30
    if dice == [1, 2, 3, 4, 5] or dice == [2, 3, 4, 5, 6]:
        return 60
    return 0

def judge_four(dice):
    # 判断是否为四个相同的骰子
    for i in range(1, 7):
        if dice.count(i) >= 4:
            return 40
    return 0

def judge_hulu(dice):
    # 判断是否为葫芦
    dice.sort()
    if (dice[0] == dice[1] and dice[2] == dice[3] and dice[3] == dice[4]) or (dice[0] == dice[1] and dice[1] == dice[2] and dice[3] == dice[4]):
        return 20
    return 0

def judge_three(dice):
    # 判断是否为三个相同的骰子
    for i in range(1, 7):
        if dice.count(i) >= 3:
            return 10
    return 0

def judge_two(dice):
    # 判断是否为两对相同的骰子
    pairs = set()
    for i in range(1, 7):
        if dice.count(i) >= 2:
            pairs.add(i)
    if len(pairs) == 2:
        return 10
    return 0

def judge_five_same(dice):
    # 判断是否为五个骰子全部相同（五连）
    if all(x == dice[0] for x in dice):
        return 100
    return 0

def calculate_score(dice):
    total_score = sum(dice)  # 计算骰子的总点数
        # 五连的情况，奖励分数
    if(judge_five_same(dice) != 0):
        total_score += judge_five_same(dice)
        return total_score
    if(judge_two(dice) != 0):
        total_score += judge_two(dice)
        return total_score
    if(judge_shun(dice) != 0):
        total_score += judge_shun(dice)
        return total_score
    if(judge_hulu(dice) != 0):
        total_score += judge_hulu(dice)
        return total_score
    if(judge_four(dice) != 0):
        total_score += judge_four(dice)
        return total_score
    if(judge_three(dice) != 0):
        total_score += judge_three(dice)
        return total_score
    return total_score
#设置筹码
def setChip():
    global chip1
    global chip2
    chip1 = input("请输入玩家一的筹码数")
    chip2 = input("请输入玩家二的筹码数")
def set_locked(flag):
    numbers = []  # 用于存储输入的数字的列表
    global locked_dice1  # 玩家一被锁定的骰子，若该位置为1，则代表第几个骰子被锁定
    global locked_dice2
    input_string = input("请输入数字，以空格分隔，回车键结束输入： ")

    if input_string.strip() != "-1":  # 检查输入是否为-1，如果是，不进行任何操作
        # 使用 split() 函数将输入的字符串分割成数字的列表
        input_list = input_string.split()
        for num_str in input_list:
            try:
                num = int(num_str)
                numbers.append(num)  # 将数字添加到列表中
            except ValueError:
                print(f"忽略无效的输入: {num_str}")
    if(flag == 1):
        for num in numbers:
            locked_dice1[num - 1] = 1
            lock1.append(dice1[num - 1])
    if(flag == 2):
        for num in numbers:
            locked_dice2[num - 1] = 1
            lock2.append(dice2[num - 1])
    print(lock1)
    print(lock2)

def StartGame():

    global Magnification
    global chip1
    global chip2
    gameNumber = int(input("请输入游戏局数"))
    for gamenuber in range(gameNumber):
        for rounds in range(3):
            for i in range(5):
                num = random.randint(1, 6)
                if(locked_dice1[i] == 0):
                    dice1[i] = num
            print("玩家一的骰子为", end="")
            print(dice1)
            if(rounds <= 1):
                set_locked(1)
                AddMagnification = int(input("请选择增加倍率"))
                Magnification += AddMagnification
            for j in range(5):
                num = random.randint(1, 6)
                if(locked_dice2[j] == 0):
                    dice2[j] = num
            print("玩家二的骰子为",end="")
            print(dice2)
            if (rounds <= 1):
                set_locked(2)
                AddMagnification = int(input("请选择增加倍率"))
                Magnification += AddMagnification
            print("现在的倍率是",end="")
            print(Magnification)
        score1 = calculate_score(dice1)
        print(score1)
        score2 = calculate_score(dice2)
        print(score2)
        if(score1 > score2):
            print("玩家一从玩家二手中夺得了",end="")
            print((score1 - score2) * Magnification,end="")
            print("筹码")
            chip1 += score1
            chip2 -= score2
            print("玩家一目前筹码", end="")
            print(chip1)
            print("玩家二目前筹码", end="")
            print(chip2)
        if (score1 < score2):
            print("玩家二从玩家一手中夺得了", end="")
            print((score2 - score1) * Magnification, end="")
            print("筹码")
            chip1 -= score1
            chip2 += score2
            print("玩家一目前筹码",end="")
            print(chip1)
            print("玩家二目前筹码", end="")
            print(chip2)
        if(score1 == score2):
            print("平局！")
            print("玩家一目前筹码", end="")
            print(chip1)
            print("玩家二目前筹码", end="")
            print(chip2)


StartGame()



