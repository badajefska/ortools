import csv
from datetime import datetime

def load_csv(filepath):
    rows = []
    try:
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"エラー: {filepath} が見つかりません。")
        return None
    return rows

def calc_total(row):
    """その日の甲・おつ・丙の人数合計を返す"""
    kou=otsu=hei=0 

    for t in ("A","B","C","D"):
        s = row[f"{t}班"]
        n = int(row.get(f"{t}人数")or 0)

        if s.startswith("甲"):
            kou +=n 
        elif s.startswith("乙"):
            otsu +=n 
        elif s.startswith("丙"):
            hei +=n 
    return kou,otsu,hei 

def show_team_shifts():
    try:
        year = int(input("対象年 (例: 2026): "))
        month = int(input("対象月 (例: 2): "))
        filepath = f"shifts_{year}_{month:02d}.csv"

        team  = input("対象班(A or B,C,D): ").upper()

        if team not in("A","B","C","D"):
            print("A/B/C/Dのいずれかを入力してください。")
            return

        start = input("開始日(YYYY-MM-DD): ")
        end   = input("終了日(YYYY-MM-DD): ")

        start_date = datetime.strptime(start,"%Y-%m-%d").date()
        end_date   = datetime.strptime(end,"%Y-%m-%d").date()
    except ValueError:
        print("エラー: 日付や数値の形式が正しくありません。")
        return

    data = load_csv(filepath)
    if data is None:
        return

    print(f"\n [{team}班]")

    for i,row in enumerate(data):
        day =datetime.strptime(row["日付"],"%Y-%m-%d").date()

        if not (start_date <= day <= end_date):
            continue

        # ---班の勤務＆人数---
        shift = row[f"{team}班"]
        n = int(row.get(f"{team}人数")or 0)

        # 今日の合計
        total_kou,total_otsu,total_hei=calc_total(row)

        # 初期値
        result1 =""
        result2 =""

        # --------------甲--------------------
        #
        if shift.startswith("甲"):
            lack_otsu=23-total_otsu
            lack_hei= 21-total_hei

            result1 = f"乙不足:{lack_otsu:2d}"
            result2 = f"丙不足:{lack_hei:2d}"

        # ---------------乙----------------------
        #
        elif shift.startswith("乙"):
            lack_kou=23-total_kou
            lack_hei=21-total_hei

            result1 = f"甲不足:{lack_kou:2d}"
            result2 = f"丙不足:{lack_hei:2d}"

        # ----------------丙---------------------
        #
        elif shift.startswith("丙"):
            lack_otsu = 23-total_otsu
            result1 = f"乙不足:{lack_otsu:2d}"

            # 翌日の甲不足
            if i+1 < len(data):
                next_kou, _, _ = calc_total(data[i + 1])
                lack_next_kou = 23 - next_kou
                result2 = f"翌日甲 不足:{lack_next_kou:2d}"
            else:
                result2 = "翌日データなし"

        print(
            f"{row['日付']} | 勤務:{shift:4}  出勤:{n:2d}  "
            f"{result1}  {result2}"
        )

"""
        # ---その日全体の乙・丙人数を集計---
        total_kou=0 
        total_otsu=0 
        total_hei=0 

        for t in ("A","B","C","D"):
            s = row[f"{t}班"]
            num = int(row.get(f"{t}人数")or 0)

            if s.startswith("甲"):
                total_kou +=num
            elif s.startswith("乙"):
                total_otsu +=num
            elif s.startswith("丙"):
                total_hei

        # 不足人数（全体）
        lack_kou=23-total_kou
        lack_otsu=23-total_otsu
        lack_hei=21-total_hei

        print(f"{row['日付']} | 勤務:{shift:4} "
            f"出勤人数:{n:2d} "
            f"乙不足:{lack_otsu:2d} "
            f"丙不足:{lack_hei:2d}"
        )
"""

if __name__=="__main__":
    show_team_shifts()

