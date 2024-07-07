from app.views import app_views
from flask import render_template, request, jsonify, url_for, redirect
from app.cloud_storage.s3_cloud_storage import S3StorageService
from app.models.user import User
from app.models.tailor import Tailor
from app.models.product import Product
from app.models.message import Message, MessageList
from app import socketio
from app.models import db
from flask_socketio import send, emit, join_room, leave_room
from flask_login import current_user, login_required
from app.models.notification import Notification
from datetime import datetime
from app import s3_client




@app_views.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'image_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image_file']  # Get the file
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        file_url = s3_service.upload_image(file, current_user.id)  # Upload file to S3
        return jsonify({'image_url': file_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
@login_required
def handle_connect():
    print("user connected")
    join_room(current_user.id)

@socketio.on('disconnect')
@login_required
def handle_disconnect():
    print("user disconnected")
    leave_room(current_user.id)

@socketio.on('send_message')
@login_required
def handle_send_message(data):
    print("connected sending")
    reciever_id = data['reciever_id']
    message_text = data['message']
    image_url = data.get('image_url')
    if not message_text and not image_url:
        emit('error', {'error': 'Message and image cannot both be empty'}, room=current_user.id)
        return
    
    # Save message to the database
    if current_user.is_tailor:
        #check if reciever has  had conversation with the tailor and prevent tailor to tailor conversation
        check_msg = Message.query.filter_by(sender_user_id = reciever_id, reciever_tailor_id = current_user.id).all()
        if check_msg:
            new_message = Message(
            sender_tailor_id=current_user.id,
            reciever_user_id=reciever_id,
            message=message_text)
            notification = Notification(url=f"/messages/{current_user.id}",
                content = "💬 New Chat: The user  has replied to your message. Check it out!",
                user_id= reciever_id, sender_tailor_id= current_user.id, is_user=True)
            msg_list = MessageList.query.filter_by(user_id = reciever_id, tailor_id = current_user.id).one_or_none()
            msg_list.message= message_text
            msg_list.is_viewed = False
            msg_list.last_sender = current_user.id
            db.session.commit()
        else:
            return
    else:
        # confirm conversation is not a user to user
        check_tailor = Tailor.query.filter_by(id = reciever_id).one_or_none()
        if not check_tailor:
            return
        # get all messges related to the sender_user/tailor  and reciever_tailor/user, create a new ms_glist if no previous message btw them
        msg1 = Message.query.filter_by(reciever_user_id=current_user.id).filter_by(sender_tailor_id=reciever_id).all()
        msg2 = Message.query.filter_by(sender_user_id =current_user.id).filter_by(reciever_tailor_id=reciever_id).all()
        if  not msg1 and not msg2:
            msg_list = MessageList(tailor_id=reciever_id, user_id=current_user.id, user_url = f"/messages/{reciever_id}", 
                     tailor_url= f"/messages/{current_user.id}", message=message_text, last_sender=current_user.id)
            db.session.add(msg_list)

        else:
            msg_list = MessageList.query.filter_by(user_id = current_user.id, tailor_id = reciever_id).one_or_none()
            msg_list.message= message_text
            msg_list.last_sender = current_user.id
            msg_list.is_viewed = False
            db.session.commit()

        new_message = Message(
            sender_user_id=current_user.id,
            reciever_tailor_id=reciever_id,
            message=message_text
            )
        notification = Notification(url=f"/messages/{current_user.id}", 
                content = "💬 New Chat: The user  has replied to your message. Check it out!",
                tailor_id= reciever_id, sender_user_id= current_user.id)


    db.session.add(new_message)
    db.session.add(notification)
    db.session.commit()


    # Emit the message to the receiver's room
    emit('recieve_message', {
        'sender_id': current_user.id,
        'message': message_text,
        'image_url': image_url
    }, room=reciever_id)
    emit('new_notification', {
        'url': notification.url,
        'content': notification.content,
        'id': notification.id
    }, room=reciever_id)
    emit('new_msg_list',  {
        'url': {'user_url':msg_list.user_url, 'tailor_url':msg_list.tailor_url},
        'message': msg_list.message,
        'last_sender': msg_list.last_sender,
        'user_name': msg_list.user.first_name + ' ' + msg_list.user.last_name,
        'tailor_name':  msg_list.tailor.first_name + ' ' + msg_list.tailor.last_name,
        'updated_at':format_time( msg_list.updated_at),
        'is_viewed': msg_list.is_viewed,
        'id': msg_list.id
    }, room=reciever_id)

    print('Message: ',  data)

@app_views.route('/messages', methods=['GET'])
@login_required
def messages():
    product = Product.query.all()
    for p in product:
        print("is a a  apr", p.id)
    print(current_user.id)
    msg_list = current_user.message_list
    for m in msg_list:
        print("thi is upadted at: ", m.updated_at, "and this is created at", m.created_at)
    message_list = sorted(msg_list, key=lambda msg: msg.updated_at)
    formatted_msg_list = [msg for msg in message_list]
    for msg_list in formatted_msg_list:
        msg_list.tailor.img_url = s3_client.generate_presigned_url('get_object', msg_list.tailor.photo_url)

    return render_template('pages/messages.html', user=current_user.to_dict(), message_list=formatted_msg_list)

@app_views.route('/get_message', methods=['GET'])
@login_required
def get_message():
    msg_id = request.args.get('id')
    message_list = MessageList.query.get(msg_id)
    
    if message_list:
        message_list.is_viewed = True
        db.session.commit()
        
        # Determine the redirection URL
        if current_user.is_tailor:
            redirect_url = message_list.tailor_url
        else:
            redirect_url = message_list.user_url
        
        return jsonify({'success': True, 'redirect_url': redirect_url})
    else:
        return jsonify({'success': False, 'error': 'Message not found'}), 404
@app_views.route('/async_get_messages', methods=['GET', 'POST'])
@login_required
def get_messages():

    msg_list = current_user.message_list
    message = sorted(msg_list, key=lambda msg: msg.created_at)
    formatted_messages = [msg.to_dict() for msg in message]
    return jsonify(formatted_messages)
 

@app_views.route('/message/<product_id>', methods=['POST'])
def handle_post(product_id):
    #handling of message sent from product page
    # Check if the request method is POST
    if request.method == 'POST':
        # Handling Message sent from product page
        product = Product.query.filter_by(id=product_id).one_or_none()
        
        
        # Ensure product exists and the current user is not a tailor
        if product and not current_user.is_tailor:
            if request.is_json:
                data = request.get_json()
                value = data.get('text', '')
                               
                msg1 = Message.query.filter_by(reciever_tailor_id=product.tailor_id, sender_user_id=current_user.id).all()
                msg2 = Message.query.filter_by(sender_tailor_id=product.tailor_id, reciever_user_id=current_user.id).all()
                
                new_message = Message(
                    sender_user_id=current_user.id,
                    reciever_tailor_id=product.tailor_id,
                    message=value,
                    product_id=product_id  # Use product_id here
                )
                db.session.add(new_message)
                
                if not msg1 and not msg2:
                    msg_list = MessageList(
                        tailor_id=product.tailor_id,
                        user_id=current_user.id,
                        user_url=f"/messages/{product.tailor_id}",
                        tailor_url=f"/messages/{current_user.id}",
                        message=value,
                        last_sender=current_user.id
                    )
                    db.session.add(msg_list)
                    db.session.commit()
                else:
                    msg_list = MessageList.query.filter_by(user_id=current_user.id, tailor_id=product.tailor_id).one_or_none()
                    if msg_list:
                        msg_list.message = value
                        msg_list.last_sender = current_user.id
                        msg_list.is_viewed = False
                        db.session.commit()
                
                return jsonify("Message sent to the Tailor, you can view the message in your inbox page")
            else:
                return jsonify("Invalid content type, expected JSON"), 400

        elif product and current_user.is_tailor:
            return jsonify('Tailor cannot send messages from product page'), 403

    return jsonify("Invalid request method"), 405


@app_views.route('/messages/<msg_id>', methods=['GET'])
@login_required
def messages_per_user(msg_id):
    # Once this page is visited this particular chat with this id is viewed automatically or manually
    msg_list = current_user.message_list
    if msg_list:
        for m in msg_list:
            if m.last_sender == msg_id:
                m.is_viewed = True
                db.session.commit()

  
    if current_user.is_tailor:
        # Get all messages related to the sender_tailor and receiver_user for display
        msg1 = Message.query.filter_by(reciever_user_id=msg_id, sender_tailor_id=current_user.id).all()
        msg2 = Message.query.filter_by(sender_user_id=msg_id, reciever_tailor_id=current_user.id).all()
        
        # Prevent a tailor from starting a conversation with a customer, customer should initiate a chat with vendors
        # If there is no message history between the tailor and customer, the tailor cannot start conversation
        if not msg1 and not msg2:
            return redirect(url_for('app_views.messages'))
        else:
            # Display the conversation history between the tailor and the customer
            user = User.query.filter_by(id=msg_id).one_or_none()
            message = sorted(msg1 + msg2, key=lambda msg: msg.created_at)
            formatted_messages = [msg for msg in message]
            return render_template("pages/chat.html", user=current_user.to_dict(), msg=formatted_messages, other_user=user.to_dict())
    
    else:
        # Get all the messages related to the sender_user and receiver_tailor for display
        msg1 = Message.query.filter_by(reciever_tailor_id=msg_id, sender_user_id=current_user.id).all()
        msg2 = Message.query.filter_by(sender_tailor_id=msg_id, reciever_user_id=current_user.id).all()
        
        # Check if tailor exists
        tailor = Tailor.query.filter_by(id=msg_id).one_or_none()
        
        if not msg1 and not msg2:
            if not tailor:
                return redirect(url_for('app_views.messages'))
            return render_template("/pages/chat.html", user=current_user.to_dict(), msg=[], other_user=tailor.to_dict())
        
        else:
            # Display the previous conversations with the tailor
            message = sorted(msg1 + msg2, key=lambda msg: msg.created_at)
            formatted_messages = [msg for msg in message]
            return render_template("pages/chat.html", user=current_user.to_dict(), msg=formatted_messages, other_user=tailor.to_dict())
