import random

VALID_MOVES = ("piedra", "papel", "tijera")

BEATS = {
    "piedra": "tijera",
    "papel": "piedra",
    "tijera": "papel",
}


def determine_winner(player_move: str, computer_move: str) -> str:
    for move, name in ((player_move, "del jugador"), (computer_move, "de la computadora")):
        if not isinstance(move, str) or move not in VALID_MOVES:
            raise ValueError(
                f"Jugada {name} inválida: {move!r}. "
                f"Jugadas válidas: {', '.join(VALID_MOVES)}"
            )

    if player_move == computer_move:
        return "tie"

    if BEATS[player_move] == computer_move:
        return "player"

    return "computer"


SCORE_KEYS = {
    "player": "player_wins",
    "computer": "computer_wins",
    "tie": "ties",
}


def get_computer_move(rng=None) -> str:
    source = rng if rng is not None else random
    return source.choice(VALID_MOVES)


def update_score(score: dict, result: str) -> dict:
    if not isinstance(result, str) or result not in SCORE_KEYS:
        raise ValueError(f"Resultado inválido: {result!r}")

    updated = dict(score)
    updated[SCORE_KEYS[result]] += 1
    return updated
