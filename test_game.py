import pytest

from game import determine_winner, get_computer_move, update_score


@pytest.mark.parametrize(
    "player_move, computer_move",
    [
        ("piedra", "tijera"),
        ("papel", "piedra"),
        ("tijera", "papel"),
    ],
)
def test_player_wins(player_move, computer_move):
    assert determine_winner(player_move, computer_move) == "player"


@pytest.mark.parametrize(
    "player_move, computer_move",
    [
        ("piedra", "papel"),
        ("papel", "tijera"),
        ("tijera", "piedra"),
    ],
)
def test_computer_wins(player_move, computer_move):
    assert determine_winner(player_move, computer_move) == "computer"


@pytest.mark.parametrize(
    "player_move, computer_move",
    [
        ("piedra", "piedra"),
        ("papel", "papel"),
        ("tijera", "tijera"),
    ],
)
def test_ties(player_move, computer_move):
    assert determine_winner(player_move, computer_move) == "tie"


def test_invalid_player_move_raises_value_error():
    with pytest.raises(ValueError):
        determine_winner("lagarto", "piedra")


def test_invalid_computer_move_raises_value_error():
    with pytest.raises(ValueError):
        determine_winner("piedra", "lagarto")


def test_both_invalid_moves_raise_value_error():
    with pytest.raises(ValueError):
        determine_winner("lagarto", "spock")


@pytest.mark.parametrize(
    "player_move, computer_move",
    [
        ("", "piedra"),
        ("piedra", ""),
    ],
)
def test_empty_move_raises_value_error(player_move, computer_move):
    with pytest.raises(ValueError):
        determine_winner(player_move, computer_move)


@pytest.mark.parametrize(
    "player_move, computer_move",
    [
        ("Piedra", "papel"),
        ("papel", "Tijera"),
        ("TIJERA", "piedra"),
    ],
)
def test_uppercase_move_raises_value_error(player_move, computer_move):
    with pytest.raises(ValueError):
        determine_winner(player_move, computer_move)


class FixedRandom:
    def __init__(self, move):
        self.move = move
        self.options = None

    def choice(self, options):
        self.options = options
        return self.move


@pytest.mark.parametrize("move", ["piedra", "papel", "tijera"])
def test_get_computer_move_uses_injected_random(move):
    rng = FixedRandom(move)

    assert get_computer_move(rng=rng) == move
    assert tuple(rng.options) == ("piedra", "papel", "tijera")


def test_get_computer_move_returns_valid_move():
    for _ in range(100):
        assert get_computer_move() in ("piedra", "papel", "tijera")


@pytest.mark.parametrize(
    "result, expected",
    [
        ("player", {"player_wins": 1, "computer_wins": 0, "ties": 0}),
        ("computer", {"player_wins": 0, "computer_wins": 1, "ties": 0}),
        ("tie", {"player_wins": 0, "computer_wins": 0, "ties": 1}),
    ],
)
def test_update_score_increments_correct_counter(result, expected):
    score = {"player_wins": 0, "computer_wins": 0, "ties": 0}

    updated = update_score(score, result)

    assert updated == expected
    assert score == {"player_wins": 0, "computer_wins": 0, "ties": 0}


def test_update_score_invalid_result_raises_value_error():
    with pytest.raises(ValueError):
        update_score({"player_wins": 0, "computer_wins": 0, "ties": 0}, "draw")
