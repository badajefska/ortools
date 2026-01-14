import csv
from datetime import date, timedelta
from shift_calc import calculate_shift

# 従業員データとグループ分け
employees = ['Alpha_0','Alpha_1','Alpha_2','Alpha_3','Alpha_4','Alpha_5','Alpha_6','Alpha_7','Alpha_8','Alpha_9',
            'Beta_0','Beta_1','Beta_2','Beta_3','Beta_4','Beta_5','Beta_6','Beta_7','Beta_8','Beta_9',
             'Charlie_0','Charlie_1','Charlie_2','Charlie_3','Charlie_4','Charlie_5','Charlie_6','Charlie_7','Charlie_8','Charlie_9',
             'Delta_0','Delta_1','Delta_2','Delta_3','Delta_4','Delta_5','Delta_6','Delta_7','Delta_8','Delta_9'
]
employee_groups = {"A": [], "B": [], "C": [], "D": []}
mapping = {
    "Alpha": "A",
    "Beta": "B",
    "Charlie": "C",
    "Delta": "D"
}
for e in employees:
    head = e.split("_")[0]
    group_key = mapping[head]
    employee_groups[group_key].append(e)


def make_month_csv():
    year = int(input("Year (例: 2026): "))
    month = int(input("Month (例: 1): "))

    # 月初
    start = date(year, month, 1)

    # 月末を探す（翌月前日方式）
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    end = next_month - timedelta(days=1)

    filename = f"shifts_{year}_{month:02d}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        """
        # 見出し
        writer.writerow([
            "日付",
            "A班", "B班", "C班", "D班",
            "A人数", "B人数", "C人数", "D人数"
        ])
        """
        #　見出し
        writer.writerow([
            "日付",
            "A班","A人数","A-vacation","A-early-notAllow","A-over-notAllow","A-control","A-shovel","A-wharf",
            "B班","B人数","B-vacation","B-early-notAllow","B-over-notAllow","B-control","B-shovel","B-wharf",
            "C班","C人数","C-vacation","C-early-notAllow","C-over-notAllow","C-control","C-shovel","C-wharf",
            "D班","D人数","D-vacation","D-early-notAllow","D-over-notAllow","D-control","D-shovel","D-wharf"
        ])

        d = start
        while d <= end:
            day_str = d.isoformat()

            a = calculate_shift(day_str, "A")
            b = calculate_shift(day_str, "B")
            c = calculate_shift(day_str, "C")
            dshift = calculate_shift(day_str, "D")
            
            """
            writer.writerow([
                day_str,
                a,"","","",
                b,"","","",
                c,"","","",
                dshift,"", "", "", ""
            ])
            """

            writer.writerow([
                day_str,
                # A
                a, len(employee_groups["A"]),"", "", "", "","","",
                # B
                b, len(employee_groups["B"]),"", "", "", "","","",
                # C
                c, len(employee_groups["C"]),"", "", "", "","","",
                # D
                dshift, len(employee_groups["D"]),"", "", "","","",""
            ])

            d += timedelta(days=1)

    print(f"CSV を作成しました: {filename}")


if __name__ == "__main__":
    make_month_csv()
