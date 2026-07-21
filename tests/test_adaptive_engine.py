from src.adaptive_engine import calculate_reminder_delay


def test_severe_focus_loss():
    assert calculate_reminder_delay(0, 49) == 5
    assert calculate_reminder_delay(10, 40) == 5


def test_low_distractions():
    assert calculate_reminder_delay(0, 90) == 60
    assert calculate_reminder_delay(1, 85) == 60


def test_two_distractions():
    assert calculate_reminder_delay(2, 80) == 45


def test_three_distractions():
    assert calculate_reminder_delay(3, 75) == 30


def test_four_to_five_distractions():
    assert calculate_reminder_delay(4, 70) == 20
    assert calculate_reminder_delay(5, 70) == 20


def test_high_distractions():
    assert calculate_reminder_delay(6, 65) == 10
    assert calculate_reminder_delay(10, 65) == 10


def test_focus_score_boundary_at_50():
    assert calculate_reminder_delay(0, 50) == 60
