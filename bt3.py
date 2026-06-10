import logging

logging.basicConfig(
    level=logging.INFO,
    filename="tournament_app.log",
    format="[%(asctime)s] - [%(levelname)s] - %(message)s"
)

matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]

def menu():
    """
    Hiển thị menu chương trình.
    """
    print("""===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====
1. Hiển thị lịch thi đấu & Kết quả
2. Thêm trận đấu mới
3. Cập nhật tỷ số trận đấu
4. Báo cáo thống kê
5. Thoát chương trình
==================================================""")

def display_matches(match_list):
    """
    Hiển thị danh sách trận đấu.

    Args:
        match_list (list): Danh sách trận đấu.
    """
    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return
    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<10} | {'Đội A':<15} | {'Đội B':<15} | {'Tỷ số':<10} | Trạng thái")
    print("-" * 70)
    for match in match_list:
        try:
            print(f"{match['match_id']:<10} | {match['team_a']:<15} | {match['team_b']:<15} | {match['score_a']}-{match['score_b']:<8} | {match['status']}")
        except KeyError as error:
            print("Dữ liệu trận đấu không hợp lệ.")
            logging.error(f"Missing key: {error}")
    logging.info("User viewed the match list.")

def find_index(match_list, match_id):
    """
    Tìm vị trí trận đấu theo mã.

    Args:
        match_list (list): Danh sách trận đấu.
        match_id (str): Mã trận đấu.

    Returns:
        int: Vị trí hoặc -1 nếu không tìm thấy.
    """
    for index, match in enumerate(match_list):
        if match["match_id"] == match_id:
            return index
    return -1

def add_new_match(match_list):
    """
    Thêm trận đấu mới.

    Args:
        match_list (list): Danh sách trận đấu.
    """
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")
    match_id = input("Nhập mã trận đấu: ").strip()
    if match_id == "":
        print("Mã trận đấu không được để trống.")
        logging.warning("User tried to add a match with empty match ID.")
        return
    if find_index(match_list, match_id) != -1:
        print(f"Lỗi: Mã trận đấu {match_id} đã tồn tại.")
        logging.warning(f"Match ID {match_id} already exists.")
        return
    team_a = input("Nhập tên Đội A: ").strip()
    team_b = input("Nhập tên Đội B: ").strip()
    if team_a == "" or team_b == "":
        print("Tên đội không được để trống.")
        logging.warning("User tried to add a match with empty team name.")
        return
    match_list.append({
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    })
    print(f"\nThành công: Đã thêm trận đấu {match_id}.")
    logging.info(f"Match {match_id} added successfully")

def input_score(team_name):
    """
    Nhập điểm hợp lệ.

    Args:
        team_name (str): Tên đội.

    Returns:
        int: Điểm hợp lệ.
    """
    while True:
        try:
            score = int(input(f"Nhập điểm {team_name}: "))
            if score < 0:
                print("Điểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"Negative score input detected: {score}")
                continue
            return score
        except ValueError as error:
            print("Điểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"Invalid score input. Error: {error}")

def update_score(match_list):
    """
    Cập nhật tỷ số trận đấu.

    Args:
        match_list (list): Danh sách trận đấu.
    """
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
    index = find_index(match_list, match_id)
    if index == -1:
        print(f"Không tìm thấy trận đấu mang mã {match_id}.")
        logging.warning(f"User tried to update non-existing match {match_id}")
        return
    match = match_list[index]
    print(f"\nTrận đấu: {match['team_a']} vs {match['team_b']} ({match['status']})")
    score_a = input_score("Đội A")
    score_b = input_score("Đội B")
    match["score_a"] = score_a
    match["score_b"] = score_b
    if score_a == 0 and score_b == 0:
        confirm = input("Tỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").lower()
        if confirm == "y":
            match["status"] = "Completed"
        else:
            match["status"] = "Pending"
    else:
        match["status"] = "Completed"
    print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
    logging.info(f"Match {match_id} score updated successfully")

def determine_winner(match):
    """
    Xác định đội thắng.

    Args:
        match (dict): Thông tin trận đấu.

    Returns:
        str: Tên đội thắng, Draw hoặc Not Started.
    """
    try:
        if match["status"] == "Pending":
            return "Not Started"
        if match["score_a"] > match["score_b"]:
            return match["team_a"]
        if match["score_b"] > match["score_a"]:
            return match["team_b"]
        return "Draw"
    except KeyError as error:
        logging.error(f"Missing key: {error}")
        return "Invalid Data"

def generate_report(match_list):
    """
    Tạo báo cáo thống kê.

    Args:
        match_list (list): Danh sách trận đấu.
    """
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    total = 0
    for match in match_list:
        if match["status"] == "Completed":
            winner = determine_winner(match)
            print(f"{match['match_id']}: {match['team_a']} {match['score_a']}-{match['score_b']} {match['team_b']} | Kết quả: {winner}")
            total += 1
    if total == 0:
        print("Chưa có trận đấu nào hoàn thành.")

    print(f"\nTổng số trận đã hoàn thành: {total}")
    logging.info("User generated tournament report.")

def main():
    """
    Hàm điều khiển chương trình.
    """
    while True:
        menu()
        choice = input("Chọn chức năng (1-5): ").strip()
        try:
            choice = int(choice)
            match choice:
                case 1:
                    display_matches(matches)
                case 2:
                    add_new_match(matches)
                case 3:
                    update_score(matches)
                case 4:
                    generate_report(matches)
                case 5:
                    print("Thoát chương trình.")
                    logging.info("System closed.")
                    break
                case _:
                    print("Không hợp lệ.")
                    logging.warning(
                        "Invalid menu choice selected"
                    )
        except ValueError:
            print("Không hợp lệ.")
            logging.warning("Invalid menu choice selected")
main()