from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from .models import db, Message
from flask_socketio import emit

from ..main import socketio

message = Blueprint('message', __name__)

@message.route('/send_message', methods=['POST'])
@login_required
def send_message():
    """Handles sending messages.

    If the request method is POST, it retrieves the message text and chat_id from the form.
    It then creates a new message in the database with the current user and chat information.

    Returns:
        JSON response: Indicates success or failure of the message sending operation.
    """
    if request.method == 'POST':
        message_text = request.form.get("message_text")
        chat_id = request.form.get("chat_id")

        if message_text and chat_id:
            new_message = Message(text=message_text, user_id=current_user.id, chat_id=chat_id)
            db.session.add(new_message)
            db.session.commit()
            socketio.emit('message', {'text': message_text, 'user': current_user.name, 'date': new_message.date}, roon=chat_id)
            return jsonify({'success': True, 'message': 'Message envoyé'})
        else:
            return jsonify({'success': False, 'message': 'Message ou ID invalide'})
    else:
        return jsonify({'success': False, 'message': 'Methode de requete invalide'})
    

@message.route('/chat/<int:chat_id>')
@login_required
def display_chat(chat_id):
    """Displays messages for a specific chat.

    Retrieves messages for the specified chat and renders the chat template.

    Args:
        chat_id (int): The ID of the chat to display.

    Returns:
        Rendered template: Renders the chat template with messages for the specified chat.
    """
    chat_messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.date.desc()).all()

    return render_template('chat.html', user=current_user, chat_messages=chat_messages)