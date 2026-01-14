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
    """その日の甲・おつ・丙の人数合計と各役割の人数合計を返す"""
    kou=otsu=hei=0
    kou_control=kou_shovel=kou_wharf=0
    otsu_control=otsu_shovel=otsu_wharf=0
    hei_control=hei_shovel=hei_wharf=0

    for t in ("A","B","C","D"):
        s = row[f"{t}班"]
        n = int(row.get(f"{t}人数")or 0)
        l = int(row.get(f"{t}-control")or 0)
        m = int(row.get(f"{t}-shovel")or 0)
        o = int(row.get(f"{t}-wharf")or 0)

        if s.startswith("甲"):
            kou += n
            kou_control += l
            kou_shovel += m
            kou_wharf += o
        elif s.startswith("乙"):
            otsu += n
            otsu_control += l
            otsu_shovel += m
            otsu_wharf += o
        elif s.startswith("丙"):
            hei += n
            hei_control += l
            hei_shovel += m
            hei_wharf += o
    return (kou, otsu, hei,
            kou_control, kou_shovel, kou_wharf,
            otsu_control, otsu_shovel, otsu_wharf,
            hei_control, hei_shovel, hei_wharf)

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
        (total_kou, total_otsu, total_hei,
         total_kou_control, total_kou_shovel, total_kou_wharf,
         total_otsu_control, total_otsu_shovel, total_otsu_wharf,
         total_hei_control, total_hei_shovel, total_hei_wharf) = calc_total(row)

        # 初期値
        result1 =""
        result2 =""
        result3 ="" # control, shovel, wharf の不足
        result4 ="" # control, shovel, wharf の不足 (もう一方の班)

        # --------------甲--------------------
        #
        if shift.startswith("甲"):
            lack_otsu=23-total_otsu
            lack_hei= 21-total_hei

            lack_otsu_control = 2-total_otsu_control
            lack_otsu_shovel = 2-total_otsu_shovel
            lack_otsu_wharf = 3-total_otsu_wharf

            lack_hei_control = 2-total_hei_control
            lack_hei_shovel = 2-total_hei_shovel
            lack_hei_wharf = 3-total_hei_wharf

            result1 = f"乙不足:{lack_otsu:2d}"
            result2 = f"丙不足:{lack_hei:2d}"
            result3 = f"乙con不足:{lack_otsu_control:2d} 乙shov不足:{lack_otsu_shovel:2d} 乙wharf不足:{lack_otsu_wharf:2d}"
            result4 = f"丙con不足:{lack_hei_control:2d} 丙shov不足:{lack_hei_shovel:2d} 丙wharf不足:{lack_hei_wharf:2d}"


        # ---------------乙----------------------
        #
        elif shift.startswith("乙"):
            lack_kou=23-total_kou
            lack_hei=21-total_hei

            lack_kou_control = 2-total_kou_control
            lack_kou_shovel = 2-total_kou_shovel
            lack_kou_wharf = 3-total_kou_wharf

            lack_hei_control = 2-total_hei_control
            lack_hei_shovel = 2-total_hei_shovel
            lack_hei_wharf = 3-total_hei_wharf

            result1 = f"甲不足:{lack_kou:2d}"
            result2 = f"丙不足:{lack_hei:2d}"
            result3 = f"甲con不足:{lack_kou_control:2d} 甲shov不足:{lack_kou_shovel:2d} 甲wharf不足:{lack_kou_wharf:2d}"
            result4 = f"丙con不足:{lack_hei_control:2d} 丙shov不足:{lack_hei_shovel:2d} 丙wharf不足:{lack_hei_wharf:2d}"


        # ----------------丙---------------------
        #
        elif shift.startswith("丙"):
            lack_otsu = 23-total_otsu
            lack_otsu_control = 2-total_otsu_control
            lack_otsu_shovel = 2-total_otsu_shovel
            lack_otsu_wharf = 3-total_otsu_wharf

            result1 = f"乙不足:{lack_otsu:2d}"
            result3 = f"乙con不足:{lack_otsu_control:2d} 乙shov不足:{lack_otsu_shovel:2d} 乙wharf不足:{lack_otsu_wharf:2d}"

            # 翌日の甲不足
            if i+1 < len(data):
                next_kou, _, _, _, _, _, _, _, _, _, _, _ = calc_total(data[i + 1]) # 全ての戻り値を受け取るように修正
                
                # 翌日の甲のcontrol, shovel, wharfの合計を取得
                (next_kou, _, _,
                 next_kou_control, next_kou_shovel, next_kou_wharf,
                 _, _, _,
                 _, _, _) = calc_total(data[i + 1])

                lack_next_kou = 23 - next_kou
                lack_next_kou_control = 2 - next_kou_control
                lack_next_kou_shovel = 2 - next_kou_shovel
                lack_next_kou_wharf = 3 - next_kou_wharf

                result2 = f"翌日甲 不足:{lack_next_kou:2d}"
                result4 = f"翌日甲con不足:{lack_next_kou_control:2d} 翌日甲shov不足:{lack_next_kou_shovel:2d} 翌日甲wharf不足:{lack_next_kou_wharf:2d}"
            else:
                result2 = "翌日データなし"
                result4 = ""

        print(
            f"{row['日付']} | 勤務:{shift:4}  出勤:{n:2d}  "
            f"{result1}  {result2}  {result3}  {result4}"
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

