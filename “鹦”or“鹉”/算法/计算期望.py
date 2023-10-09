import numpy as np
# 初始化期望分数数组
expect = np.zeros(7736, dtype=float)
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

def generate_dice_combinations():
    # 生成所有可能的骰子组合
    combinations = []
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            for d3 in range(1, 7):
                for d4 in range(1, 7):
                    for d5 in range(1, 7):
                        combinations.append([d1, d2, d3, d4, d5])
    return combinations

def calculate_expectations(combinations):
    # 使用动态规划计算期望分数
    n = len(combinations)
    expect = np.zeros(n, dtype=float)  # 初始化期望分数数组

    for idx in range(n):
        combo = combinations[idx]
        score = calculate_score(combo)

        # 计算下一步的期望分数
        next_expectation = 0
        for i in range(1, 7):
            next_idx = find_combo_index(combinations, combo[1:] + [i])
            if next_idx is not None:
                next_expectation += expect[next_idx]

        # 计算当前组合的期望分数
        expectation = score + next_expectation / 6.0
        expect[idx] = expectation

    # 打印期望分数
    for idx, expectation in enumerate(expect):
        print(f"Combo {idx + 1}: {expectation:.2f}")
    print(combinations)
def find_combo_index(combinations, target_combo):
    for idx, combo in enumerate(combinations):
        if combo == target_combo:
            return idx
    return None

if __name__ == "__main__":
    combinations = generate_dice_combinations()
    calculate_expectations(combinations)