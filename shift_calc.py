from datetime import datetime


def calculate_shift(day:str, team:str) -> str | None:
    """
    YYYY-MM-DD を受け取り、勤務タイプを返す
    """
    dtday = datetime.strptime(day, "%Y-%m-%d") - datetime(1899, 12, 31)
    serial = dtday.days + 1

    offsets = {
        "A":0,
        "B":4,
        "C":8,
        "D":12,
    }

    team = team.upper()

    if team not in offsets:
        raise ValueError("team must be A,B,C or D")

    base = serial+6
    value = base-offsets[team]

    # EXCELシリアル → HEX → 末尾
    char = hex(value)
    key = char[-1]

    # ★ 4班制にも対応する勤務テーブル
    threeshiftswork = {
        "1": "甲①", "2": "甲②", "3": "甲③", "4": "甲④", "5": "休",
        "6": "乙①", "7": "乙②", "8": "乙③", "9": "乙④", "a": "休",
        "b": "丙①", "c": "丙②", "d": "丙③", "e": "丙④", "f": "休",
        "0": "休",
    }

    return threeshiftswork.get(key)

