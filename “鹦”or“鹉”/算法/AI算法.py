import random
import math

# 游戏状态的表示，0表示未锁定，1表示锁定
initial_strategy = [0, 0, 0, 0, 0]  # 初始锁定策略
initial_multiplier = 1  # 初始倍率
dice_result = [random.randint(1, 6) for _ in range(5)]
best_multiplier_strategy = 1  # 初始化最佳倍率策略为1
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

def calculate_score_dice(strategy, dice):
    total_score = 0
    # 计算骰子的总点数
    total_score += sum([dice[i] for i in range(5) if strategy[i] == 0])

    # 判断是否有奖励分数
    if judge_five_same(dice) != 0:
        total_score += judge_five_same(dice)
    if judge_two(dice) != 0:
        total_score += judge_two(dice)
    if judge_shun(dice) != 0:
        total_score += judge_shun(dice)
    if judge_hulu(dice) != 0:
        total_score += judge_hulu(dice)
    if judge_four(dice) != 0:
        total_score += judge_four(dice)
    if judge_three(dice) != 0:
        total_score += judge_three(dice)

    return total_score

def calculate_score(strategy, multiplier, dice):
    # 根据策略、倍率和骰子计算分数
    total_score = calculate_score_dice(strategy, dice)
    return total_score * multiplier

#模拟退火算法
def simulated_annealing(initial_strategy, initial_multiplier, temperature, cooling_rate, num_iterations, dice):
    current_strategy = initial_strategy
    current_multiplier = initial_multiplier
    current_score = calculate_score(current_strategy, current_multiplier, dice)

    best_strategy = current_strategy
    best_multiplier = current_multiplier
    best_score = current_score

    for i in range(num_iterations):
        #选择当前情况下最好的倍率
        neighbor_multiplier = random.choice([1, 2, 3])

        neighbor_score = calculate_score(choose_strategy, neighbor_multiplier, dice_result)

        # 计算成本差异
        score_difference = neighbor_score - best_score

        # 如果邻近解更好或者按一定概率接受更差的解
        if score_difference > 0 or random.random() < math.exp(score_difference / temperature):
            best_multiplier_strategy = neighbor_multiplier
            best_score = neighbor_score


        # 随机选择邻近的解
        neighbor_strategy = current_strategy[:]
        index_to_change = random.randint(0, len(neighbor_strategy) - 1)
        neighbor_strategy[index_to_change] = 1 - neighbor_strategy[index_to_change]  # 切换锁定状态

        neighbor_multiplier = current_multiplier + random.choice([-1, 0, 1])  # 随机增加或减少倍率

        neighbor_score = calculate_score(neighbor_strategy, neighbor_multiplier, dice)

        # 计算成本差异
        score_difference = neighbor_score - current_score

        # 如果邻近解更好或者按一定概率接受更差的解
        if score_difference > 0 or random.random() < math.exp(score_difference / temperature):
            current_strategy = neighbor_strategy
            current_multiplier = neighbor_multiplier
            current_score = neighbor_score

        # 更新最佳解
        if current_score > best_score:
            best_strategy = current_strategy
            best_multiplier = current_multiplier
            best_score = current_score

        # 降低温度
        temperature *= cooling_rate

    return best_strategy, best_multiplier, best_score

def choose_locking_strategy(dice, current_strategy, game_round):
    # 根据当前骰子和策略选择锁定策略
    # 优先选择锁定已有奖励的骰子，然后根据可能的奖励分数来选择锁定其他骰子
    # 如果已经有一个顺子或葫芦，不再锁定其他骰子
    locked_indices = [i for i, lock in enumerate(current_strategy) if lock == 1]
    unlocked_indices = [i for i, lock in enumerate(current_strategy) if lock == 0]

    # 如果已经有一个顺子或葫芦，不再锁定其他骰子
    if judge_shun(dice) != 0 or judge_hulu(dice) != 0:
        return current_strategy

    if game_round == 1:
        # 在第一轮中，优先锁定已有奖励的骰子
        for i, lock in enumerate(current_strategy):
            if lock == 0 and i not in locked_indices:
                temp_strategy = current_strategy[:]
                temp_strategy[i] = 1
                if calculate_score_dice(temp_strategy, dice) > calculate_score_dice(current_strategy, dice):
                    current_strategy[i] = 1
    elif game_round == 2:
        # 在第二轮中，根据可能的奖励分数来选择锁定其他骰子
        for i in unlocked_indices:
            temp_strategy = current_strategy[:]
            temp_strategy[i] = 1
            if calculate_score_dice(temp_strategy, dice) > calculate_score_dice(current_strategy, dice):
                current_strategy[i] = 1

    return current_strategy


# 示例用法
initial_temperature = 1.0  # 初始温度
cooling_rate = 0.95  # 温度下降速度
num_iterations = 1000  # 迭代次数
choose_strategy = initial_strategy
has_locked = [0,0,0,0,0]
choose_strategy = [0,0,0,0,0]
# 初始筹码数量和对手得分
chip_count = 100  # 你的初始筹码数量
opponent_score = 200  # 对手的得分
num = 0
# 主循环
for game_round in range(1, 4):  # 三轮游戏 # 运行模拟退火算法来选择最佳的倍率策略
    # 根据当前轮次选择合适的锁定策略
    dice_result = [random.randint(1, 6) for _ in range(5 - sum(choose_strategy))]
    #choose_strategy = choose_locking_strategy(dice_result, choose_strategy, game_round)

    # 获取当前轮需要投掷的骰子
    #remaining_dice = [random.randint(1, 6) for i in range(5 - sum(choose_strategy))]


    #best_locking_strategy, best_multiplier_strategy, best_score = simulated_annealing(
        #choose_strategy, initial_multiplier, initial_temperature, cooling_rate, num_iterations, remaining_dice)
    locked_num = random.randint(0,4)
    for i in range(locked_num):
        num = random.randint(0,4)
        if(has_locked[num] == 0):
            choose_strategy[num] = 1
            has_locked[num] = 1

    best_multiplier_strategy = random.randint(0,3)
    # 输出最佳策略和分数

    # 更新筹码数量和对手得分（模拟游戏进展）
    chip_count -= 10  # 示例中简单地减少筹码数量
    opponent_score += 5  # 示例中简单地增加对手得分
    print(f"Round {game_round}:")
    print(f"Best Locking Strategy: {choose_strategy}")
    print(f"Best multiplier_strategy: {best_multiplier_strategy}")
