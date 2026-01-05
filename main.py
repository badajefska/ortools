from shifts.shift_calc import calculate_shift
from shifts.month_shifts import show_shifts
from ortools.sat.python import cp_model
import datetime 
import math 

# モデルを生成
model = cp_model.CpModel()

show_shifts()
team = input("Please enter a team(A or B or C or D)")
day = input("Please enter a date(YYYY-MM-DD):")
shift = calculate_shift(day,team)
print(f"The shift for {day} ({team} is: {shift}")

days = [datetime.date(2026,1,d).strftime("%m/%d")for d in range(1,17)]
week = ['Mon','Tue','Wed','Thr','Fri','Sat','San']

# データ
employees = ['Alpha_0','Alpha_1','Alpha_2','Alpha_3','Alpha_4','Alpha_5','Alpha_6','Alpha_7','Alpha_8','Alpha_9',
            'Beta_0','Beta_1','Beta_2','Beta_3','Beta_4','Beta_5','Beta_6','Beta_7','Beta_8','Beta_9',
             'Charlie_0','Charlie_1','Charlie_2','Charlie_3','Charlie_4','Charlie_5','Charlie_6','Charlie_7','Charlie_8','Charlie_9',
             'Delta_0','Delta_1','Delta_2','Delta_3','Delta_4','Delta_5','Delta_6','Delta_7','Delta_8','Delta_9'
]

# 時給と勤務時間
hourly_rates = {'Alpha_0':1000,'Alpha_1':1000,'Alpha_2':1000,'Alpha_3':1200,'Alpha_4':1200,'Alpha_5':1200,'Alpha_6':1200,
                'Alpha_7':1500,'Alpha_8':1500,'Alpha_9':1500,'Beta_0':1000,'Beta_1':1000,'Beta_2':1000,'Beta_3':1200,'Beta_4':1200,
                'Beta_5':1200,'Beta_6':1200,'Beta_7':1500,'Beta_8':1500,'Beta_9':1500,'Charlie_0':1000,'Charlie_1':1000,'Charlie_2':1000,
                'Charlie_3':1200,'Charlie_4':1200,'Charlie_5':1200,'Charlie_6':1200,'Charlie_7':1500,'Charlie_8':1500,'Charlie_9':1500,
                'Delta_0':1000,'Delta_1':1000,'Delta_2':1000,'Delta_3':1200,'Delta_4':1200,'Delta_5':1200,'Delta_6':1200,
                'Delta_7':1500,'Delta_8':1500,'Delta_9':1500
}

shift_days = ['甲①','甲②','甲③','甲④','休','乙①','乙②','乙③','乙④','休',
              '丙①','丙②','丙③','丙④','休','休']

shift_groups = {"甲":[],"乙":[],"丙":[],"休":[]}
shift_mapping =['甲','乙','丙'] 
shift_hours = {
    '甲': 8,
    '乙': 8,
    '丙': 8
}

for d in shift_days:
    key = d[0]
    shift_groups[key].append(d)




roles = ['main', 'sub'] #役割を追加

# 役割ごとのコスト係数（補欠は0とする）
role_cost_multiplier = {
    'main': 1,
    'sub': 0 #補欠の勤務時間はコストに含めない
}

# 4つの班にグループ分け
employee_groups = {"A": [], "B": [], "C": [], "D": []}

mapping = {
    "Alpha": "A",
    "Beta": "B",
    "Charlie": "C",
    "Delta": "D"
}
for e in employees:
    head = e.split("_")[0]
    group_key = mapping[head]   #  Alpha/Beta/Charlie/Delta を取り出す
    employee_groups[group_key].append(e)

#print(days)
#print(shift_groups)
#print(employee_groups)
#print("班数-", len(employee_groups), "班")
#print("日数-", len(days),"日",  "シフト-", len(shift_groups),"回")

#test = len(days) *len(shift_groups) *2
#print(test ,"回分")
#print("本チャン",test/2,"Sub",test/2)
#x = test /len(employee_groups)/2
#tes01 = math.ceil(x)
#print(f'Alpha班員数-{len(employee_groups["A"])}')
#print(f'Alpha班3人目-{employee_groups["A"][2]}')
#print("A班持ち分", x, "回。")


"""
# 変数を定義
# x[(e,d,s,r)]は従業員eが曜日dのシフトsに役割rで入る場合にTrue(1)
x={}
for e in employees:
    for d in days:
        for s in shifts:
            for r in roles:
                x[(e,d,s,r)]=model.NewBoolVar(f'x_{e}_{d}_{s}_{r}')

# 制約条件の追加
# 1.各シフトに必ず1名の担当者と1名の補欠を割り当てる
for d in days:
    for s in shifts:
        model.Add(sum(x][(e,d,s,'main')] for e in employees)==1)
        model.Add(sum(x[(e,d,s,'sub')] for e in employees)==1)

# 2.各従業員は1日に1つの役割にしかつけない
for e in employees:
    for d in days:
            model.Add(sum(x[(e,d,s,r)] for s in shifts for r in roles)<=1)

# 3.専門性に基づくシフト制限（例としてコメントアウト）
# 新人（Aさん）はS1シフトのみ
# for d in days:
#     for s in ['S2', 'S3']:
#         for r in roles:
#             model.Add(x[('新人_A', d, s, r)] == 0)
# ベテラン（Cさん）はS2シフトのみ
# for d in days:
#     for s in ['S1', 'S3']:
#         for r in roles:
#             model.Add(x[('ベテラン_C', d, s, r)] == 0)

# 4.各従業員は7日間のうち最低2つのシフトに入る（役割を問わず）
for e in employees:
    model.Add(sum(x[(e,d,s,r)] for d in days for s in shifts for r in roles)>=2)

# 5.各従業員の担当回数を平準化する
min_shifts_per_employee = 1
max_shifts_per_employee = 2 
for e in employees:
    model.Add(sum(x[(e,d,s,'main')] for d in days for s in shifts) >= min_shifts_per_employee)
    model.Add(sum(x[(e,d,s,'main')] for d in days for s in shifts) <= max_shifts_per_employee)

# 5-1. 各従業員の補欠回数を平準化する
min_sub_per_employee = 1 
max_sub_per_employee = 2 
for e in employees:
    model.Add(sum(x[(e,d,s,'sub')] for d in days for s in shifts) >= min_sub_per_employee)
    model.Add(sum(x[(e,d,s,'sub')] for d in days for s in shifts) <= max_sub_per_employee)

# 目的関数:総人件費
total_cost=model.NewIntVar(0,10000000,'total_cost')
# コストの合計を計算 (補欠はコスト0)
cost_sum = sum(x[(e,d,s,r)] * hourly_rates[e] * shift_hours[s] * role_cost_multiplier[r] 
               for e in employees for d in days for s in shifts for r in roles)
model.Add(total_cost==cost_sum)

# コストを最小化
model.Minimize(total_cost)

# ソルバーの生成と実行
solver = cp_model.CpSolver()
status = solver.Solve(model)

# 結果の表示
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'最適なシフトが見つかりました。総コスト: {solver.ObjectiveValue()}円')
    employee_total_hours = {e: 0 for e in employees}
    employee_total_roles = {e: {'main': 0, 'sub': 0} for e in employees}
    for d in days:
        print(f'\n--- {d}曜日 ---')
        for s in shifts:
            print(f'  - {s}シフト:')
            for r in roles:
                for e in employees:
                    if solver.BooleanValue(x[(e, d, s, r)]):
                        role_jp = "担当" if r == 'main' else "補欠"
                        cost_per_shift = hourly_rates[e] * shift_hours[s] * role_cost_multiplier[r]
                        
                        if r == 'main':
                            employee_total_hours[e] += shift_hours[s]
                        employee_total_roles[e][r] += 1
                        
                        print(f'    {role_jp}: {e}さん ({shift_hours[s]}時間) → 費用: {cost_per_shift}円')

    print("\n--- 各従業員の合計勤務時間と役割回数 ---")
    for e in employees:
        main_count = employee_total_roles[e]['main']
        sub_count = employee_total_roles[e]['sub']
        total_hours = employee_total_hours[e]
        print(f'{e}: 担当{main_count}回, 補欠{sub_count}回 (合計勤務 {total_hours} 時間)')

else:
    print('シフトを作成できませんでした。制約条件を確認してください。')

"""
