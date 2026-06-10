import unittest
from bt3 import determine_winner

class TestDetermineWinner(unittest.TestCase):
    """
    Unit Test cho hàm determine_winner().
    """
    def test_team_a_wins(self):
        """
        Test case 1:
        Đội A thắng.
        """
        match = {
            "match_id": "M01",
            "team_a": "T1",
            "team_b": "GenG",
            "score_a": 2,
            "score_b": 0,
            "status": "Completed"
        }

        result = determine_winner(match)
        self.assertEqual(result, "T1")

    def test_draw(self):
        """
        Test case 2:
        Trận đấu hòa.
        """
        match = {
            "match_id": "M02",
            "team_a": "JDG",
            "team_b": "BLG",
            "score_a": 1,
            "score_b": 1,
            "status": "Completed"
        }

        result = determine_winner(match)
        self.assertEqual(result, "Draw")

    def test_pending_match(self):
        """
        Test case 3:
        Trận đấu chưa diễn ra.
        """
        match = {
            "match_id": "M03",
            "team_a": "G2",
            "team_b": "FNC",
            "score_a": 0,
            "score_b": 0,
            "status": "Pending"
        }

        result = determine_winner(match)
        self.assertEqual(result, "Not Started")

    def test_team_b_wins(self):
        """
        Test mở rộng:
        Đội B thắng.
        """
        match = {
            "match_id": "M04",
            "team_a": "TES",
            "team_b": "BLG",
            "score_a": 0,
            "score_b": 3,
            "status": "Completed"
        }

        result = determine_winner(match)
        self.assertEqual(result, "BLG")

    def test_missing_key(self):
        """
        Test mở rộng:
        Thiếu dữ liệu trong dictionary.
        """
        match = {
            "match_id": "M05",
            "team_a": "T1",
            "status": "Completed"
        }

        result = determine_winner(match)
        self.assertEqual(result, "Invalid Data")

if __name__ == "__main__":
    unittest.main()