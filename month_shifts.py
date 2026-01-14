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


def show_shifts():
    try:
        year = int(input("対象年 (例: 2026): "))
        month = int(input("対象月 (例: 2): "))
        filepath = f"shifts_{year}_{month:02d}.csv"

        start = input("開始日 (YYYY-MM-DD): ")
        end   = input("終了日 (YYYY-MM-DD): ")

        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date   = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        print("エラー: 日付や数値の形式が正しくありません。")
        return

    data = load_csv(filepath)
    if data is None:
        return

    for row in data:
        day = datetime.strptime(row["日付"], "%Y-%m-%d").date()

        if not (start_date <= day <= end_date):
            continue

        # 勤務タイプ
        a = row["A班"]
        b = row["B班"]
        c = row["C班"]
        d = row["D班"]

        #---------------------------- 

        #----------------------------
        # 初期化
        total_kou=0 # 甲
        total_otsu=0 # 乙
        total_hei=0 # 丙
        total_kou_control=0
        total_kou_shovel=0
        total_kou_wharf=0
        total_otsu_control=0
        total_otsu_shovel=0
        total_otsu_wharf=0
        total_hei_control=0
        total_hei_shovel=0
        total_hei_wharf=0

        for team in ("A","B","C","D"):
            shift = row[f"{team}班"]
            n = int(row[f"{team}人数"]or 0)
            l = int(row[f"{team}-control"]or 0)
            m = int(row[f"{team}-shovel"]or 0)
            o = int(row[f"{team}-wharf"]or 0)

            if shift.startswith("甲"):
                total_kou +=n 
                total_kou_control +=l 
                total_kou_shovel +=m 
                total_kou_wharf +=o 
            elif shift.startswith("乙"):
                total_otsu +=n 
                total_otsu_control +=l 
                total_otsu_shovel +=m 
                total_otsu_wharf +=o 
            elif shift.startswith("丙"):
                total_hei +=n 
                total_hei_control +=l 
                total_hei_shovel +=m 
                total_hei_wharf +=o 

        # 不足人数
        lack_kou = 23-total_kou
        lack_kou_control = 2-total_kou_control
        lack_kou_shovel = 2-total_kou_shovel
        lack_kou_wharf = 3-total_kou_wharf
        lack_otsu= 23-total_otsu
        lack_otsu_control = 2-total_otsu_control
        lack_otsu_shovel = 2-total_otsu_shovel
        lack_otsu_wharf = 3-total_otsu_wharf
        lack_hei = 21-total_hei
        lack_hei_control = 2-total_hei_control
        lack_hei_shovel = 2-total_hei_shovel
        lack_hei_wharf = 3-total_hei_wharf
        

        #------------------------------------ 

        #------------------------------------ 

        # 人数（空なら 0 に）
        a_n = int(row["A人数"] or 0)
        a_l = int(row["A-control"] or 0)
        a_m = int(row["A-shovel"] or 0)
        a_o = int(row["A-wharf"] or 0)
        b_n = int(row["B人数"] or 0)
        b_l = int(row["B-control"] or 0)
        b_m = int(row["B-shovel"] or 0)
        b_o = int(row["B-wharf"] or 0)
        c_n = int(row["C人数"] or 0)
        c_l = int(row["C-control"] or 0)
        c_m = int(row["C-shovel"] or 0)
        c_o = int(row["C-wharf"] or 0)
        d_n = int(row["D人数"] or 0)
        d_l = int(row["D-control"] or 0)
        d_m = int(row["D-shovel"] or 0)
        d_o = int(row["D-wharf"] or 0)

        total = a_n + b_n + c_n + d_n

        print(
            f"{row['日付']} | "
            f"A:{a:3}({a_n})  "
            f"B:{b:3}({b_n})  "
            f"C:{c:3}({c_n})  "
            f"D:{d:3}({d_n})  "
            f"甲 不足:{lack_kou:2d}  con不足:{lack_kou_control:2d}  shov不足{lack_kou_shovel:2d}  whar不足{lack_kou_wharf:2d}  "
            f"乙 不足:{lack_otsu:2d}  con不足:{lack_otsu_control:2d}  shov不足{lack_otsu_shovel:2d}  whar不足{lack_otsu_wharf:2d}  "
            f"丙 不足:{lack_hei:2d}  con不足:{lack_hei_control:2d}  shov不足{lack_hei_shovel:2d}  whar不足{lack_hei_wharf:2d}  "
        )


if __name__ == "__main__":
    show_shifts()
