import secrets
import string
import chess

from django.shortcuts import render, redirect
from django.http import JsonResponse


rooms = {}

def make_move(request, room_id):

    if room_id not in rooms:
        return JsonResponse({
            "error": "Room not found"
        }, status=404)

    if request.method != "POST":
        return JsonResponse({
            "error": "POST required"
        }, status=405)

    room = rooms[room_id]

    session_id = request.session.session_key

    if not session_id:
        return JsonResponse({
            "error": "No player session"
        }, status=403)

    # Determine who is making the move
    if room["white"] == session_id:
        player = chess.WHITE

    elif room["black"] == session_id:
        player = chess.BLACK

    else:
        return JsonResponse({
            "error": "Spectators cannot make moves"
        }, status=403)

    board = room["board"]

    # Check whose turn it is
    if board.turn != player:
        return JsonResponse({
            "error": "Not your turn"
        }, status=403)

    move_uci = request.POST.get("move")

    if not move_uci:
        return JsonResponse({
            "error": "No move provided"
        }, status=400)

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return JsonResponse({
            "error": "Invalid move format"
        }, status=400)

    # SERVER validates the move
    if move not in board.legal_moves:
        return JsonResponse({
            "error": "Illegal move"
        }, status=400)

    board.push(move)

    return JsonResponse({
        "success": True,
        "fen": board.fen()
    })

def get_board(request, room_id):

    if room_id not in rooms:
        return JsonResponse({
            "error": "Room not found"
        }, status=404)

    board = rooms[room_id]["board"]

    return JsonResponse({
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
    })

def board(request):
    return render(request, 'home.html')

def create_room(request):
    room_id = ''.join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(8)
    )

    rooms[room_id] = {
        "white": None,
        "black": None,
        "board": chess.Board(),
    }

    return redirect("room", room_id=room_id)

def room(request, room_id):

    if room_id not in rooms:
        return render(request, "404.html")

    room = rooms[room_id]

    session_id = request.session.session_key

    # Give the browser a session if it doesn't have one
    if session_id is None:
        request.session.create()
        session_id = request.session.session_key

    player = None

    if room["white"] == session_id:
        player = "white"

    elif room["black"] == session_id:
        player = "black"

    elif room["white"] is None:
        room["white"] = session_id
        player = "white"

    elif room["black"] is None:
        room["black"] = session_id
        player = "black"

    else:
        player = "spectator"

    return render(request, "board.html", {
        "room_id": room_id,
        "player": player,
    })