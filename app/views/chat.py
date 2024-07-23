from app.views import app_views
import uuid
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



def format_time(time_obj):
    # Format the time in 12-hour format with AM/PM
    formatted_time_12 = time_obj.strftime('%I:%M %p').lstrip('0')

    # Format the time in 24-hour format with AM/PM
    hour = time_obj.strftime('%H')
    minute = time_obj.strftime('%M')
    period = 'PM' if int(hour) >= 12 else 'AM'
    formatted_time_24 = f"{hour}:{minute}"

    return  formatted_time_24


@app_views.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    print("this is file", file)
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    if file:
        unique_id = str(uuid.uuid4())
        file_url = s3_client.upload_single_photo(file, unique_id)  # Upload file to S3
        img = s3_client.generate_presigned_url('get_object', file_url)
        return jsonify({'success': True, 'file_url': file_url, 'the_image': img})
    else:
        return jsonify({'success': False, 'error': 'File upload failed'})
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
    image_generated = data.get('the_image')
    product = data.get('product')
    print(reciever_id, "it is data")
    
    
   
    if not message_text and not image_url:
        emit('error', {'error': 'Message and image cannot  be empty'}, room=current_user.id)
        print(image_url)
        return
     # Check if the message contains only space characters
    if message_text and message_text.strip() == "":
        if image_url:
            message_text = None
        else:
            emit('error', {'error': 'Message cannot contain only spaces'}, room=current_user.id)
            return
    
   
            
    
    # Save message to the database
    if current_user.is_tailor:
        #check if reciever has  had conversation with the tailor and prevent tailor to tailor conversation
        check_msg = Message.query.filter_by(sender_user_id = reciever_id, reciever_tailor_id = current_user.id).all()
        if check_msg:
            
            new_message = Message(
            sender_tailor_id=current_user.id,
            reciever_user_id=reciever_id,
            media_url = image_url if image_url else None,
            message=message_text if message_text else None)
            notification = Notification(url=f"/messages/{current_user.id}",
                content = "💬 New Chat: The user  has replied to your message. Check it out!",
                user_id= reciever_id, sender_tailor_id= current_user.id, is_user=True)
            msg_list = MessageList.query.filter_by(user_id = reciever_id, tailor_id = current_user.id).one_or_none()
            msg_list.message= "Attachment" if not message_text else message_text
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
            if not product:
                msg_list = MessageList(tailor_id=reciever_id, user_id=current_user.id, user_url = f"/messages/{reciever_id}", 
                        tailor_url= f"/messages/{current_user.id}", message="Attachment" if not message_text else message_text, last_sender=current_user.id)
                db.session.add(msg_list)

        else:
       
                msg_list = MessageList.query.filter_by(user_id = current_user.id, tailor_id = reciever_id).one_or_none()
                msg_list.message= message_text if message_text else "Attachment"
                msg_list.last_sender = current_user.id
                msg_list.is_viewed = False
                db.session.commit()

        new_message = Message(
            sender_user_id=current_user.id,
            reciever_tailor_id=reciever_id,
            media_url = image_url if image_url else None,
            message=message_text if message_text else None)
        notification = Notification(url=f"/messages/{current_user.id}", 
                content = "💬 New Chat: The user  has replied to your message. Check it out!",
                tailor_id= reciever_id, sender_user_id= current_user.id)

    if not product:
        db.session.add(new_message)
    db.session.add(notification)
    db.session.commit()


    # Emit the message to the receiver's room     
    
    emit('recieve_message', {
        'sender_id': current_user.id,
        'message': message_text,
        'image_url': image_generated,
        'product': product
      
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

   # print('Message: ',  data)

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

        # Logging for debugging
    # no = Notification.query.all()
    # for m in no:
    #     db.session.delete(m)
    #     db.session.commit()
    # print(no)
    if request.method == 'POST':
        print(f"Handling POST request for product_id: {product_id}")
        print(f"Request method: {request.method}")

        # Handling Message sent from product page
        product = Product.query.filter_by(id=product_id).one_or_none()
        
        
        # Ensure product exists and the current user is not a tailor
        if product and not current_user.is_tailor:
            dat  = {"id": product.id, "image":product.img, "price":product.price, "name": product.name}
            if request.is_json:
                data = request.get_json()
                value = data.get('text', '')
                if not value or  (value and value.strip() == ""):
                    return jsonify("empty message cannot be sent"), 405
                               
                msg1 = Message.query.filter_by(reciever_tailor_id=product.tailor_id, sender_user_id=current_user.id).all()
                msg2 = Message.query.filter_by(sender_tailor_id=product.tailor_id, reciever_user_id=current_user.id).all()
                
                new_message = Message(
                    sender_user_id=current_user.id,
                    reciever_tailor_id=product.tailor_id,
                    message=value,
                    product_id=product_id  # Use product_id here
                )
                db.session.add(new_message)
                db.session.commit()
               
                print(dat, "dlkajfsdlfkj dslkfjsdlk ldskfjsdlkfjsld ")
                return jsonify({"data": dat, "success":True})
            else:
                return jsonify("Invalid content type, expected JSON"), 400

        elif product and current_user.is_tailor:
            return jsonify('Tailor cannot send messages from product page'), 403

    return jsonify("Invalid request method"), 405


@app_views.route('/messages/<msg_id>', defaults={'modal': None}, methods=['GET'])
@app_views.route('/messages/<msg_id>/<modal>', methods=['GET'])
@login_required
def messages_per_user(msg_id, modal):
    # Once this page is visited this particular chat with this id is viewed automatically or manually
    print(modal, "modal here here")
    msg_list = current_user.message_list
    if msg_list:
        for m in msg_list:
            if m.last_sender == msg_id:
                m.is_viewed = True
                db.session.commit()

  
    if current_user.is_tailor and not modal:
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
            json_message = [msg.to_dict() for msg in message]
            if modal:
                return redirect(url_for('app_views.messages'))
            return render_template("pages/chat.html", user=current_user.to_dict(), msg=formatted_messages, other_user=user)
    
    elif not current_user.is_tailor:
        # Get all the messages related to the sender_user and receiver_tailor for display
        if not modal:
            msg1 = Message.query.filter_by(reciever_tailor_id=msg_id, sender_user_id=current_user.id).all()
            msg2 = Message.query.filter_by(sender_tailor_id=msg_id, reciever_user_id=current_user.id).all()
            tailor = Tailor.query.filter_by(id=msg_id).one_or_none() 
        else:
            product = Product.query.filter_by(id=msg_id).one_or_none()
            if product:
                msg1 = Message.query.filter_by(reciever_tailor_id=product.tailor_id, sender_user_id=current_user.id).all()
                msg2 = Message.query.filter_by(sender_tailor_id=product.tailor_id, reciever_user_id=current_user.id).all()
                tailor = Tailor.query.filter_by(id=product.tailor_id).one_or_none() 
            else:
                return jsonify("invalid link")
        
        # Check if tailor exists
       
        m_user = current_user.to_dict()
        
        
        
        if not msg1 and not msg2:
            if not tailor:
                return redirect(url_for('app_views.messages'))
            if modal:
                m_tailor = tailor.to_dict() 
                del m_tailor['cac_number'],m_tailor['account_number'], m_user['message_list']  
                print(m_user)  
                return jsonify({"current_user": m_user, "messages":None, "other_user":m_tailor})
            
            return render_template("/pages/chat.html", user=current_user.to_dict(), msg=[], other_user=tailor)
        
        else:
            # Display the previous conversations with the tailor
            message = sorted(msg1 + msg2, key=lambda msg: msg.created_at)
            
           
          
            # retrun json data for model message pop up
            if modal:
                for m in message:
                    if m.product_id:
                       product = Product.query.filter_by(id=m.product_id).one_or_none()
                       m.m_product = product.to_dict()
                       m.m_product['image'] = product.img
                    if m.media_url:
                       m.m_image= m.image
                
                
                    

                json_message = [msg.to_dict() for msg in message]

                m_user = current_user.to_dict()
                del m_user['message_list']
                return jsonify({"current_user": m_user, "messages":json_message, "other_user":tailor.to_dict()})
            # return the normal template if no modal
            formatted_messages = [msg for msg in message]
            return render_template("pages/chat.html", user=current_user.to_dict(), msg=formatted_messages, other_user=tailor)
    else:
        return   redirect(url_for('app_views.messages'))
