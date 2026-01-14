import csv
from datetime import datetime

skill_file = "/home/nekura/Documents/Python/ortools/skill.csv"


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



def process_member_shifts(year, month, start_date_str, end_date_str):
    """
    指定された年月のシフトファイルから、各班の出勤者、有休者、不可情報を日ごとに抽出し、
    加えて、班ごとの当番と専門スキル人員の不足数を計算します。
    """
    file_path = f"shifts_{year}_{month:02d}.csv"
    
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date   = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("エラー: 開始日または終了日の形式が正しくありません (YYYY-MM-DD)。")
        return None

    # スキルとメンバー情報をロード
    all_skills = load_skills(skill_file)
    members_by_team = load_days("", skill_file)

    # 日ごとのデータを保持する辞書
    daily_data = {}

    shift_data_rows = load_csv(file_path)
    if shift_data_rows is None:
        print(f"ファイル '{file_path}' が見つからないか、読み込めませんでした。")
        return None
        
    # 定数
    REQUIRED_SKILLS = {"control": 2, "shovel": 2, "wharf": 3}

    for row in shift_data_rows:
        try:
            current_date = datetime.strptime(row["日付"], "%Y-%m-%d").date()
            current_date_str = row["日付"]
        except (ValueError, KeyError):
            print(f"警告: '日付'列が不正な行をスキップします: {row}")
            continue

        if not (start_date <= current_date <= end_date):
            continue
        
        # --- 1. 日ごとのメンバー情報を初期化・計算 ---
        daily_data[current_date_str] = {
            "teams": {
                "A": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set(), "shift_type": "", "shortages": {}},
                "B": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set(), "shift_type": "", "shortages": {}},
                "C": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set(), "shift_type": "", "shortages": {}},
                "D": {"attendance": set(), "vacation": set(), "early_not_allowed": set(), "over_not_allowed": set(), "shift_type": "", "shortages": {}},
            },
        }

        # --- 2. 各班の情報を整理 ---
        for team_prefix in ["A", "B", "C", "D"]:
            team_data = daily_data[current_date_str]["teams"][team_prefix]
            
            # 当番
            shift_type_str = row.get(f"{team_prefix}班", "")
            if shift_type_str.startswith("甲"):
                team_data["shift_type"] = "甲"
            elif shift_type_str.startswith("乙"):
                team_data["shift_type"] = "乙"
            elif shift_type_str.startswith("丙"):
                team_data["shift_type"] = "丙"
            else:
                team_data["shift_type"] = "公休" # or other default

            # 有休者
            vacation_members_str = row.get(f"{team_prefix}-vacation", "")
            team_data["vacation"] = set(m.strip() for m in vacation_members_str.split(",") if m.strip())
            # 早出不可者
            early_not_allow_str = row.get(f"{team_prefix}-early-notAllow", "")
            team_data["early_not_allowed"] = set(m.strip() for m in early_not_allow_str.split(",") if m.strip())
            # 残業不可者
            over_not_allow_str = row.get(f"{team_prefix}-over-notAllow", "")
            team_data["over_not_allowed"] = set(m.strip() for m in over_not_allow_str.split(",") if m.strip())
            # 出勤者
            all_team_members = set(members_by_team[team_prefix])
            if team_data["shift_type"] == '公休':
                team_data["attendance"] = set()
            else:
                team_data["attendance"] = all_team_members - team_data["vacation"]
            
            # --- 3. 専門スキル不足を計算 ---
            # その班が出勤日でない場合は計算しない
            if team_data["shift_type"] in ["甲", "乙", "丙"]:
                skills_count = {"control": 0, "shovel": 0, "wharf": 0}
                for member in team_data["attendance"]:
                    member_skills = all_skills.get(member, {})
                    for skill in REQUIRED_SKILLS.keys():
                        if member_skills.get(skill, 0) > 0:
                            skills_count[skill] += 1
                
                shortages = {}
                for skill, required_count in REQUIRED_SKILLS.items():
                    shortage = required_count - skills_count[skill]
                    shortages[skill] = shortage if shortage > 0 else 0
                team_data["shortages"] = shortages


    # --- 4. 結果の表示 ---
    for date_str, date_data in sorted(daily_data.items()):
        print(f"\n--- 日付: {date_str} ---")
        # メンバー情報の表示
        for team, data in date_data["teams"].items():
            print(f"  --- {team}班 (当番: {data.get('shift_type', 'N/A')}) ---")
            num_attendance = len(data['attendance'])
            print(f"    出勤者({num_attendance}人): {', '.join(sorted(list(data['attendance']))) or 'なし'}")
            print(f"    有休者: {', '.join(sorted(list(data['vacation']))) or 'なし'}")
            print(f"    早出不可者: {', '.join(sorted(list(data['early_not_allowed']))) or 'なし'}")
            print(f"    残業不可者: {', '.join(sorted(list(data['over_not_allowed']))) or 'なし'}")
            
            # スキル不足情報の表示
            shortages = data.get("shortages", {})
            shortage_messages = []
            if shortages:
                for skill, num in shortages.items():
                    if num > 0:
                        shortage_messages.append(f"{skill.capitalize()}: {num}")
            
            if shortage_messages:
                print(f"    専門スキル不足: " + ", ".join(shortage_messages))
            else:
                if data.get('shift_type') in ["甲", "乙", "丙"]:
                    print("    専門スキル不足: なし")


    return daily_data


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

