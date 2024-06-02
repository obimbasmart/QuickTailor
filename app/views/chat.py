from app.views import app_views
from flask import render_template, request
from cloud_storage.s3_cloud_storage import S3StorageService
from app.models.user import User
from app.models.tailor import Tailor
from app.models.product import Product
from app.models.messages import Message
from app import socketio, db
from flask_socketio import send, emit, join_room, leave_room
from flask_login import current_user, login_required


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
        new_message = Message(
            sender_tailor_id=current_user.id,
            reciever_user_id=reciever_id,
            message=message_text,
        )
        notification = Nootification(url="http://localhost:5002/messages/9e0a5d17-8896-4214-b4c7-d42e36496d93",
                content = "💬 New Chat: The user  has replied to your message. Check it out!",
                user_id= reciever_id, sender_tailor_id= current_user.id)

    else:
        new_message = Message(
            sender_user_id=current_user.id,
            reciever_tailor_id=reciever_id,
            message=message_text,
            notification = Nootification(url="http://localhost:5002/messages/9e0a5d17-8896-4214-b4c7-d42e36496d93", 
                content = "💬 New Chat: The user  has replied to your message. Check it out!",
                tailor_id= reciever_id, sender_user_id= current_user.id)

        )
    db.session.add(new_msg, notification)
    db.session.commit()
    # Emit the message to the receiver's room
    emit('recieve_message', {
        'sender_id': current_user.id,
        'message': message_text,
        'image_url': image_url
    }, room=reciever_id)
    print('Message: ',  data)

@app_views.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    return render_template('pages/chat.html', user=current_user.to_dict(), msg=[], other_user=[]) 

@app_views.route('/messages/<msg_id>', methods=['GET', 'POST'])
@login_required
def messages_per_user(msg_id):
    print(current_user.id)
    if current_user.is_tailor:
        # get all messges related to the sender_tailor and reciever_user for display
        msg1 = Message.query.filter_by(reciever_user_id=msg_id).filter_by(sender_tailor_id=current_user.id).all()
        msg2 = Message.query.filter_by(sender_user_id = msg_id).filter_by(reciever_tailor_id=current_user.id).all()

        #prevent a tailor from starting a conversation with a customer, customer should initiate a chat with vendors
        # if there is no message history between the tailor and customer, the tailor cannot start conversation
        if len(msg1 + msg2) < 1:
        # tailor cannot start new conversation with new customer || user query wrong id manually
            return render_template("pages/chat.html", user=current_user.to_dict(), msg=[], other_user=[] )
         
        else:
        # display the conversation history between the tailor and the cutomer
            user = User.query.filter_by(id=msg_id).one_or_none()
            message = sorted(msg1 + msg2, key=lambda msg: msg.created_at)
            formatted_messages = [msg.to_dict() for msg in message]
            return render_template("pages/chat.html", user=current_user.to_dict(), msg=formatted_messages, other_user=user.to_dict())
    # this is for purpose of users who wants to go beyond the provided interface, if not this is not necessary
    elif not current_user.is_tailor:
       print("here we are")
       # get all the message relatd to the sender_user and reciever_tailor for display
       msg1 = Message.query.filter_by(reciever_tailor_id=msg_id).filter_by(sender_user_id=current_user.id).all()
       msg2 = Message.query.filter_by(sender_tailor_id = msg_id).filter_by(reciever_user_id=current_user.id).all()
       #check if tailor  exist
       tailor = Tailor.query.filter_by(id=msg_id).one_or_none()
       print(current_user.id)
       if len(msg1 +msg2) < 1:
       # start a new conversation with the tailor check if user
           if not tailor:
                # if a customer message through a posted product
               product= Product.query.filter_by(id=msg_id).one_or_none()
               if product:
                   return render_template('pages/chat.html', user=current_user.to_dict(), msg=[], other_user=product.tailor.to_dict(), product=product.to_dict())
               return "hello"

           return (render_template("/pages/chat.html", user=current_user.to_dict(), msg=[], other_user=tailor.to_dict())
                   if tailor else render_template("pages/about_us.html"))
            
       else:
       # display the previous conversations with the tailor
           print('ssssssssssss')
           message = sorted(msg1 + msg2, key=lambda msg: msg.created_at)
           formatted_messages = [msg.to_dict() for msg in message]
           return render_template("pages/chat.html", user=current_user.to_dict(), msg=formatted_messages, other_user=tailor.to_dict() )
     
