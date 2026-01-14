from deta.member import process_member_shifts

if __name__ == "__main__":
    try:
        year = 2026
        month = 1
        start_date_str = "2026-01-01"
        end_date_str = "2026-01-03"
        
        print(f"メンバーシフト処理を実行します。ファイル: shifts_{year}_{month:02d}.csv")
        process_member_shifts(year, month, start_date_str, end_date_str)
    except ValueError:
        print("エラー: 年、月、日付の入力形式が正しくありません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
