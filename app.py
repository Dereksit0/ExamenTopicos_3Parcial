import streamlit as st

from game import determine_winner, get_computer_move, update_score

MOVES = ("piedra", "papel", "tijera")
MOVE_LABELS = {
    "piedra": "Piedra",
    "papel": "Papel",
    "tijera": "Tijera",
}
RESULT_LABELS = {
    "player": "Ganaste",
    "computer": "Perdiste",
    "tie": "Empate",
}


def init_state():
    if "score" not in st.session_state:
        st.session_state.score = {
            "player_wins": 0,
            "computer_wins": 0,
            "ties": 0,
        }
    if "last_player_move" not in st.session_state:
        st.session_state.last_player_move = None
    if "last_computer_move" not in st.session_state:
        st.session_state.last_computer_move = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None


def play_round(player_move: str):
    computer_move = get_computer_move()
    result = determine_winner(player_move, computer_move)

    st.session_state.score = update_score(st.session_state.score, result)
    st.session_state.last_player_move = player_move
    st.session_state.last_computer_move = computer_move
    st.session_state.last_result = result


def reset_score():
    st.session_state.score = {
        "player_wins": 0,
        "computer_wins": 0,
        "ties": 0,
    }
    st.session_state.last_player_move = None
    st.session_state.last_computer_move = None
    st.session_state.last_result = None


def render_last_round():
    if st.session_state.last_result is None:
        st.info("Elige una jugada para comenzar.")
        return

    st.subheader("Última ronda")

    player_col, computer_col = st.columns(2)
    player_col.metric(
        "Tu jugada",
        MOVE_LABELS[st.session_state.last_player_move],
    )
    computer_col.metric(
        "Jugada de la computadora",
        MOVE_LABELS[st.session_state.last_computer_move],
    )

    message = RESULT_LABELS[st.session_state.last_result]

    if st.session_state.last_result == "player":
        st.success(message)
    elif st.session_state.last_result == "computer":
        st.error(message)
    else:
        st.info(message)


def render_scoreboard():
    st.subheader("Marcador")

    score = st.session_state.score
    player_col, computer_col, ties_col = st.columns(3)
    player_col.metric("Tú", score["player_wins"])
    computer_col.metric("Computadora", score["computer_wins"])
    ties_col.metric("Empates", score["ties"])


def main():
    st.set_page_config(page_title="Piedra, Papel o Tijera")
    st.title("Piedra, Papel o Tijera")
    st.caption("Elige tu jugada y compite contra la computadora.")

    init_state()

    columns = st.columns(3)
    for column, move in zip(columns, MOVES):
        if column.button(MOVE_LABELS[move], width="stretch"):
            play_round(move)

    st.divider()
    render_last_round()
    st.divider()
    render_scoreboard()

    if st.button("Reiniciar marcador"):
        reset_score()
        st.rerun()


if __name__ == "__main__":
    main()
