# test_score.py
from Score import add_score, get_scores

def test_add_score():
    result = add_score("Eddie", 3)
    assert result != -1, "Score should be added successfully"
    print("Score added successfully")

def test_get_scores():
    scores = get_scores()
    assert len(scores) > 0, "Scores should not be empty"
    print(f"Scores: {scores}")

if __name__ == "__main__":
    test_add_score()
    test_get_scores()