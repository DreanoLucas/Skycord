from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import db
from flask_login import current_user, login_required

from .models import FriendRequest, User, Friend, Chat, ChatMember, Message

friend = Blueprint('friend', __name__)

@friend.route('/ajouter')
@login_required
def ajouter():

    amisDemandeListe = []
    friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, accepted=False).all()
    
    for friend_request in friend_requests:
        sender = User.query.filter_by(id=friend_request.sender_id).first()
        sender.id_demande = friend_request.id  # Ajoutez l'ID de la demande d'ami comme attribut
        amisDemandeListe.append(sender)
    
    return render_template('ajouter.html', donnees=amisDemandeListe)

@friend.route('/groupe')
@login_required
def groupe():
    return render_template('groupe.html')

@friend.route('/parametre')
@login_required
def parametre():
    return render_template('parametre.html')


@friend.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    if request.method == 'POST':
        friend_name = request.form['friend_name']

        ami_exist = User.query.filter_by(login=friend_name).first()

        if ami_exist:
            if ami_exist.id == current_user.id:
                print('soi meme')
                flash("Vous ne pouvez pas vous ajouter vous-même en tant qu'ami.", category='error')
            else:
                existing_friendship = Friend.query.filter(
                    ((Friend.user_id == current_user.id) & (Friend.friend_id == ami_exist.id)) |
                    ((Friend.user_id == ami_exist.id) & (Friend.friend_id == current_user.id))
                ).first()
                if existing_friendship:
                    flash(f"{friend_name} est déjà dans votre liste d'amis.", category='error')
                else:
                    existing_request = FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=ami_exist.id, accepted=False).first()
                    if existing_request:
                        flash(f"Une demande d'ami est déjà en attente pour {friend_name}.", category='error')
                    else:
                        new_request = FriendRequest(sender_id=current_user.id, receiver_id=ami_exist.id)
                        db.session.add(new_request)
                        db.session.commit()
                        flash(f"Demande d'ami envoyée à {friend_name}. Attendez la confirmation.", category='success')

        else:
            flash(f"{friend_name} n'existe pas.", category='error')

    return redirect(url_for('friend.ajouter'))



@friend.route('/accept_demand/<int:demande_id>', methods=['POST'])
def accept_demand(demande_id):
    friend_request = FriendRequest.query.get(demande_id)
    print(friend_request)
    print(demande_id)
    if friend_request:
        friend_request.accepted = True

        friend_entry_1 = Friend(user_id=friend_request.sender_id, friend_id=friend_request.receiver_id)
        friend_entry_2 = Friend(user_id=friend_request.receiver_id, friend_id=friend_request.sender_id, reciprocal=True)
        db.session.add_all([friend_entry_1, friend_entry_2])
        new_chat = Chat(chat_name=f"{friend_request.sender.name} et {friend_request.receiver.name}", is_group=False)
        db.session.add(new_chat)
        db.session.commit()
        chat_member_1 = ChatMember(chat_id=new_chat.chat_id, user_id=friend_request.sender_id)
        chat_member_2 = ChatMember(chat_id=new_chat.chat_id, user_id=friend_request.receiver_id)
        db.session.add_all([chat_member_1, chat_member_2])
        db.session.commit()

        flash(f"Vous êtes maintenant ami avec {friend_request.sender.name}.", category='success')
    else:
        flash("Demande d'ami introuvable ou déjà acceptée.", category='error')

    return redirect(url_for('friend.ajouter'))



@friend.route('/reject_demand/<int:demande_id>', methods=['POST'])
def reject_demand(demande_id):
    friend_request = FriendRequest.query.get(demande_id)
    print(friend_request)
    if friend_request:
        db.session.delete(friend_request)
        db.session.commit()
        flash(f"Vous avez refusé la demande d'ami de {friend_request.sender.name}.", category='success')
    else:
        flash("Demande d'ami introuvable.", category='error')

    return redirect(url_for('friend.ajouter'))



@friend.route('/getChatDetails/<int:chat_id>')
@login_required
def getChatDetails(chat_id):
    members = ChatMember.query.filter_by(chat_id=chat_id).all()
    member_ids = [member.user_id for member in members]

    all_messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.date).all()
    receiverName = User.query.filter_by(id=member_ids[1]).first().name

    if(receiverName == current_user.name):
        receiverName = User.query.filter_by(id=member_ids[0]).first().name
    messages_users = []

    for message in all_messages:
        sender = User.query.filter_by(id=message.user_id).first().id
        receiver = User.query.filter_by(id=message.user_id).first().id

        user = sender if message.user_id == member_ids[0] else receiver
        messages_users.append({
            'Sender': current_user.id,
            'Receiver': receiverName,
            'UserId': user,
            'Username': User.query.filter_by(id=user).first().name,
            'Text': message.text,
            'Date': message.date
        })

    session['sorted_messages'] = messages_users
    return redirect(url_for('views.home'))



from flask import jsonify
@friend.route('/remove_all_friendships')
def remove_all_relationships():
    try:
        # Supprimer toutes les entrées de la table Friend
        db.session.query(Friend).delete()

        # Supprimer toutes les entrées de la table FriendRequest
        db.session.query(FriendRequest).delete()


        db.session.query(Chat).delete()
        db.session.query(ChatMember).delete()
        # Valider la transaction
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Toutes les relations ont été supprimées.'}), 200
    except Exception as e:
        # En cas d'erreur, annuler la transaction et renvoyer une réponse d'erreur
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
      

@friend.route('/check_friendship/<int:user_id1>/<int:user_id2>', methods=['GET'])
def check_friendship(user_id1, user_id2):
    friendship_entry = Friend.query.filter(
        (Friend.user_id == user_id1) & (Friend.friend_id == user_id2) |
        (Friend.user_id == user_id2) & (Friend.friend_id == user_id1)
    ).first()

    if friendship_entry:
        # Les utilisateurs sont déjà amis
        return jsonify({'status': 'success', 'message': 'Les utilisateurs sont amis.'}), 200
    else:
        # Les utilisateurs ne sont pas amis
        return jsonify({'status': 'error', 'message': 'Les utilisateurs ne sont pas amis.'}), 404