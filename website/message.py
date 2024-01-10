from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from .models import db, Message
from .models import FriendRequest, User, Friend, Chat, ChatMember

# from flask_socketio import emit
from datetime import datetime
# from ..main import socketio

message = Blueprint('message', __name__)

idDuChat = -1



@message.route('/getChatDetails/<int:chat_id>')
@login_required
def getChatDetails(chat_id):
    global idDuChat
    idDuChat = chat_id


    members = ChatMember.query.filter_by(chat_id=chat_id).all()
    member_ids = [member.user_id for member in members]
    print(member_ids)

    all_messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.date).all()
    messages_users = []

    receiverName = User.query.filter_by(id=member_ids[1]).first().name

    if(receiverName == current_user.name):
        receiverName = User.query.filter_by(id=member_ids[0]).first().name
    messages_users = []

    for message in all_messages:
        sender = User.query.filter_by(id=message.user_id).first().name
        receiver = User.query.filter_by(id=message.user_id).first().name 

        user = sender if message.user_id == member_ids[0] else receiver
        messages_users.append({
            'Receiver': receiverName,
            'User': user,
            'Text': message.text,
            'Date': message.date,
            'ReceiverName': receiver
        })

    session['sorted_messages'] = messages_users
    return redirect(url_for('views.home'))

@message.route('/send_message', methods=['POST'])
@login_required
def send_message():
    """Handles sending messages.

    If the request method is POST, it retrieves the message text and chat_id from the form.
    It then creates a new message in the database with the current user and chat information.

    Returns:
        JSON response: Indicates success or failure of the message sending operation.
    """

    if(idDuChat != -1):
        if request.method == 'POST':
            message_text = request.form.get("message")
            print(message_text)
            if message_text and idDuChat:
                new_message = Message(text=message_text, user_id=current_user.id, chat_id=idDuChat, date=datetime.now())
                db.session.add(new_message)
                db.session.commit()
                return redirect(url_for('message.display_chat', chat_id=idDuChat))    
    return redirect(url_for('views.home')) 
    

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
    return redirect(url_for('message.getChatDetails', chat_id=chat_id))
    return redirect(url_for('views.home', user=current_user, chat_messages=chat_messages, chat_id=chat_id)) 