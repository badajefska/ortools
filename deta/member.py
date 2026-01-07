import csv
from datetime import datetime

skill_file = "/home/nekura/Documents/Python/ortools/skill.csv"
#filepath = f"/home/nekura/Documents/Python/ortools/shifts_{year}_{month:2d}.csv"


def load_skills(skill_file:str):
    """
    skill.csvを読み込み、メンバーごとのスキルレベルを辞書として返す
    """
    skills = {}
    with open(skill_file,newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            member = row.pop("member")
            # スキルレベルを整数に変換
            skills[member] = {k.strip(): int(v) for k ,v in row.items()}
    return skills


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


def split(s:str):
    """カンマ区切りの文字列をsetに変換"""
    s = (s or "").strip()
    if not s:
        return set()
    return set(x.striip() for x in s.split(",") if x.strip())

def load_days(input_file:str,skill_file:str):
    """
    skill.csvの読み込む、後に日毎のデータ構造とメンバー情報を返す
    """
    # スキルファイルから全メンバーをロード
    all_skills = load_skills(skill_file)
    all_members = list(all_skills.keys())

    days = []

    # 班員の整理
    MEMBERS_BY_TEAM = {team: [] for team in ["A", "B", "C", "D"]}
    for member in all_members:
        if member.startswith("Alpha"):
            MEMBERS_BY_TEAM["A"].append(member)
        elif member.startswith("Beta"):
            MEMBERS_BY_TEAM["B"].append(member)
        elif member.startswith("Charlie"):
            MEMBERS_BY_TEAM["C"].append(member)
        elif member.startswith("Delta"):
            MEMBERS_BY_TEAM["D"].append(member)

    return(MEMBERS_BY_TEAM)


"""
def show_member():
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

        for team in ("A","B","C","D"):
            shift = row[f"{team}班"]
            n = int(row[f"{team}人数"]or 0)

            if shift.startswith("甲"):
                total_kou +=n 
            elif shift.startswith("乙"):
                total_otsu +=n 
            elif shift.startswith("丙"):
                total_hei +=n 
        # 不足人数
        lack_kou = 23-total_kou
        lack_otsu= 23-total_otsu
        lack_hei = 21-total_hei


        #------------------------------------ 

        #------------------------------------ 

        # 人数（空なら 0 に）
        a_n = int(row["A人数"] or 0)
        b_n = int(row["B人数"] or 0)
        c_n = int(row["C人数"] or 0)
        d_n = int(row["D人数"] or 0)

        total = a_n + b_n + c_n + d_n

        print(
            f"{row['日付']} | "
            f"A:{a:3}({a_n})  "
            f"B:{b:3}({b_n})  "
            f"C:{c:3}({c_n})  "
            f"D:{d:3}({d_n})  "
            f"甲 不足:{lack_kou:2d}  "
            f"乙 不足:{lack_otsu:2d}  "
            f"丙 不足:{lack_hei:2d}"
        )
"""

def process_member_shifts(year, month, start_date_str, end_date_str):
    """
    指定された年月のシフトファイルから、各班の出勤者、有休者、不可情報を日ごとに抽出します。
    """
    file_path = f"shifts_{year}_{month:02d}.csv"
    
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date   = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("エラー: 開始日または終了日の形式が正しくありません (YYYY-MM-DD)。")
        return

    # skill.csvから全メンバーのリストを取得
    members_by_team = load_days("", skill_file)

    # 日ごとのデータを保持する辞書
    daily_team_data = {}

    shift_data_rows = load_csv(file_path)
    if shift_data_rows is None:
        print(f"ファイル '{file_path}' が見つからないか、読み込めませんでした。")
        return

    for row in shift_data_rows:
        try:
            current_date = datetime.strptime(row["日付"], "%Y-%m-%d").date()
            current_date_str = row["日付"]
        except (ValueError, KeyError):
            print(f"警告: '日付'列が不正な行をスキップします: {row}")
            continue

        if not (start_date <= current_date <= end_date):
            continue
        
        # その日のデータ構造を初期化
        daily_team_data[current_date_str] = {
            "A": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set()},
            "B": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set()},
            "C": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set()},
            "D": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set()},
        }

        for team_prefix in ["A", "B", "C", "D"]:
            # 有休者
            vacation_members_str = row.get(f"{team_prefix}-vacation")
            if vacation_members_str:
                for member in [m.strip() for m in vacation_members_str.split(",") if m.strip()]:
                    daily_team_data[current_date_str][team_prefix]["vacation"].add(member)

            # 早出不可者
            early_not_allow_members_str = row.get(f"{team_prefix}-early-notAllow")
            if early_not_allow_members_str:
                for member in [m.strip() for m in early_not_allow_members_str.split(",") if m.strip()]:
                    daily_team_data[current_date_str][team_prefix]["early_not_allowed"].add(member)

            # 残業不可者
            over_not_allow_members_str = row.get(f"{team_prefix}-over-notAllow")
            if over_not_allow_members_str:
                for member in [m.strip() for m in over_not_allow_members_str.split(",") if m.strip()]:
                    daily_team_data[current_date_str][team_prefix]["over_not_allowed"].add(member)

            # 出勤者を計算 (全メンバー - その日の有休者)
            all_team_members = set(members_by_team[team_prefix])
            vacation_today = daily_team_data[current_date_str][team_prefix]["vacation"]
            daily_team_data[current_date_str][team_prefix]["attendance"] = all_team_members - vacation_today

    # 結果の表示
    for date_str, team_info in sorted(daily_team_data.items()):
        print(f"\n--- 日付: {date_str} ---")
        for team, data in team_info.items():
            print(f"  --- {team}班 ---")
            print(f"    出勤者: {', '.join(sorted(list(data['attendance']))) or 'なし'}")
            print(f"    有休者: {', '.join(sorted(list(data['vacation']))) or 'なし'}")
            print(f"    早出不可者: {', '.join(sorted(list(data['early_not_allowed']))) or 'なし'}")
            print(f"    残業不可者: {', '.join(sorted(list(data['over_not_allowed']))) or 'なし'}")
    
    return daily_team_data


if __name__ == "__main__":
    try:
        year = int(input("対象年 (例: 2026): "))
        month = int(input("対象月 (例: 2): "))
        start_date_str = input("開始日 (YYYY-MM-DD): ")
        end_date_str = input("終了日 (YYYY-MM-DD): ")
        
        print(f"メンバーシフト処理を実行します。ファイル: shifts_{year}_{month:02d}.csv")
        process_member_shifts(year, month, start_date_str, end_date_str)
    except ValueError:
        print("エラー: 年、月、日付の入力形式が正しくありません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

