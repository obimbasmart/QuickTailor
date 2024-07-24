{% from 'macros/notification.html' import messageList %}
{% from 'macros/messageProfile.html' import modalMessageTop   %}
{% from 'macros/messageProfile.html' import messageBottom   %}
{% from 'macros/messageProfile.html' import messages   %}


{% extends 'base.html' %} 


{% block content %}
<div id="main-div" class="flex flex-col-reverse gap-[7px] py-4  mx-4 mb-8">
 {% if message_list %}

   {% for msg_list in message_list %}

    {% set image_profile %}
    {% if not current_user.is_tailor %}
        <img src="{{ msg_list.tailor.photo }}" class="rounded-full" style="width: 40px; height: 40px;">
    {% else %}
    <div  class="w-12 h-12 flex items-center  p-2 justify-center  text-sm bg-pc-teal-light rounded-full   dark:focus:ring-gray-600">
                  <svg xmlns="http://www.w3.org/2000/svg"
                       width="40"
                       height="40"
                       viewBox="0 0 18 18"
                       fill="none">
                    <path d="M9.15037 9C11.2214 9 12.9004 7.32106 12.9004 5.25C12.9004 3.17893 11.2214 1.5 9.15037 1.5C7.07932 1.5 5.40039 3.17893 5.40039 5.25C5.40039 7.32106 7.07932 9 9.15037 9Z" stroke="#006060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M2.25 16.5C2.67778 15.0249 3.56097 13.7228 4.7733 12.7799C5.98562 11.837 7.46501 11.3015 9 11.25C12.09 11.25 14.7225 13.4325 15.75 16.5" stroke="#006060" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
   </div>

    {% endif %}
    {% endset %}

    {% set message_and_name %}
    <div class="flex flex-col gap-1 justify-between ml-2">
        <div class="leading-[21px] font-normal font-roboto tracking-[0.5px] text-gray-800 text-[16px]" style="color: (--Grey-Darker, #2D2D2D);">
            {% if current_user.is_tailor %}
                {{ msg_list.user.first_name ~ ' ' ~ msg_list.user.lastname  }}
            {% else %}
                {{ msg_list.tailor.first_name ~ ' ' ~ msg_list.tailor.lastname  }}
            {% endif %}
        </div>
        <div class="leading-[21px] font-normal font-roboto tracking-[0.4px] text-gray-800 text-[12px] overflow-hidden" style="height:40px; {% if not msg_list.is_viewed and msg_list.last_sender != current_user.id %} font-weight:bold;  font-size: 14px; {% else %} color:var(--Grey-Dark, #606060); {% endif %}">
		{% if msg_list.last_sender == current_user.id %}

		    {{'You:  ' ~ msg_list.message }}
		{% else  %}
		     {{ msg_list.message }}
                {% endif %}
        </div>
    </div>
    {% endset %}

    <div class="pb-[5px] mt-1" data-msg-id="{{ msg_list.id }}" onclick="handleDivClick(this)" style="{% if loop.first %} border:none; {% else %} border-bottom:1px solid #D8D8D8; {% endif %}">
        {{ messageList(image_profile, message_and_name, msg_list.updated_at|timeago) }}
    </div>

    {% endfor %}
 {% else %}
   <div  id="empty" class="text-center"> Your chat history is empty
   </div>
{% endif %}

</div>

<div id="modal"></div>

// <button id="load-content-button" style="position: fixed; z-index: 201;">Load Content</button>
<script>
     const msgg = `{{message_list}}`;
    for (a of msgg){

        console.log(msgg);
    }
   
    function customTimeFormat(datetimeString, timezoneOffset = 1) {
    // If the input is 'N/A', return 'N/A'
    if (datetimeString === 'N/A') {
        return 'N/A';
    }
    
    // Create a new Date object from the datetime string
    const date = new Date(datetimeString);
   
    // Adjust for the specified timezone offset (in hours)
    const localDate = new Date(date.getTime() + timezoneOffset * 3600000);
    const now = new Date();
    const diff = now - localDate;
    
    // Calculate the difference in various units
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000) ;
    const days = Math.floor(diff / 86400000);
   
    // If the datetime is under 30 seconds
    if (seconds < 30) {
        return 'just now';
    }

    // If the datetime is under 60 seconds
    if (seconds < 60) {
        return `${seconds} seconds ago`;
    }

    // If the datetime is under 60 minutes
    if (minutes < 60) {
        return `${minutes} ${minutes === 1 ? 'miute': 'minutes'} ago`;
    }

   
    // If the datetime is exactly one day old
    if (days === 1) {
        const localHours = localDate.getUTCHours().toString().padStart(2, '0');
        const localMinutes = localDate.getUTCMinutes().toString().padStart(2, '0');
        return `Yesterday at ${localHours}:${localMinutes}`;
    }

    // For dates older than 24 hours
    if (days > 1) {
        // Get the day of the month and determine the correct suffix
        const day = localDate.getUTCDate();
        let suffix = 'th';
        if (day % 10 === 1 && day !== 11) {
            suffix = 'st';
        } else if (day % 10 === 2 && day !== 12) {
            suffix = 'nd';
        } else if (day % 10 === 3 && day !== 13) {
            suffix = 'rd';
        }

        // Get month, day, and year
        const month = localDate.toLocaleString('default', { month: 'short' });
        const year = localDate.getUTCFullYear();

        // Format the datetime to the desired output
        return `${month}, ${day}${suffix} ${year}`;
    }
}
function formatCurrency(value) {
    return new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency: 'NGN'
    }).format(value);
}

document.getElementById('load-content-button').onclick = async function() {
    try {
        const response = await fetch('/messages/c20faad3-7680-4c81-bad6-0a67455539a7/a', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        function sleep(ms) {
         return new Promise(resolve => setTimeout(resolve, ms));
        }
      


        const div = document.getElementById('modal');
        const messagesInterface = document.createElement('div');
        messagesInterface.className = "flex flex-col pt-16 ml-1 mb-[80px]";
        const content = await response.json();
        const heading = `<div class="leading-[21px] font-normal font-roboto tracking-[0.5px] text-gray-800 text-[16px]" style="color: var(--Grey-Dark, #000);"> ${content.other_user.business_name}</div>`;
        const imageInput= `<svg id="attach-button" xmlns="http://www.w3.org/2000/svg" width="14" height="15" viewBox="0 0 14 15" fill="none" style=" cursor: pointer;">
                 <path d="M1 7.5H7M7 7.5H13M7 7.5V13.5M7 7.5V1.5" stroke="#2D2D2D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <input type="file" id="file-input" style="display: none;" accept="image/*" multiple="false">`;
        const textInput =  ` <div > <input id="message-input" type="text" id="msg" class="rounded-lg placeholder-black   focus:outline-none focus:ring-0 focus:border-[white]  peer w-full" placeholder="Type here...." autocomplete="off"> </div>`;
        
        const sendBtn =  `<div id="send" class="">   <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 25" fill="none">
                          <path d="M11.5003 12.5H5.41872M5.24634 13.2972L4.24158 16.2986C3.69128 17.9424 3.41613 18.7643 3.61359 19.2704C3.78506 19.71 4.15335 20.0432 4.6078 20.1701C5.13111 20.3161 5.92151 19.9604 7.50231 19.2491L17.6367 14.6886C19.1797 13.9942 19.9512 13.6471 20.1896 13.1648C20.3968 12.7458 20.3968 12.2541 20.1896 11.8351C19.9512 11.3529 19.1797 11.0057 17.6367 10.3114L7.48483 5.74303C5.90879 5.03382 5.12078 4.67921 4.59799 4.82468C4.14397 4.95101 3.77572 5.28336 3.60365 5.72209C3.40551 6.22728 3.67772 7.04741 4.22215 8.68767L5.24829 11.7793C5.34179 12.061 5.38855 12.2019 5.407 12.3459C5.42338 12.4738 5.42321 12.6032 5.40651 12.731C5.38768 12.875 5.34057 13.0157 5.24634 13.2972Z" stroke="#2D2D2D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
	     </div>`;
        const messageInputs = ` {{ messageBottom("${textInput}", "${sendBtn}","buttom") }}`;
     
        console.log(messageInputs);


       if (content.messages) {
     
            for (const msg of content.messages) {
             
                if (msg.media_url) {
                    const image = `<a href="${msg.m_image}" target="_blank">     
                         <div class="mb-1 p-[2px] rounded-[6px]">
                             <img src="${msg.m_image}" class="h-[255px] w-full" alt="...">
                         </div>
                    </a>`
                    
                    if (msg.sender_user_id ){
                        //   if(msg.message) {
                        //       const messageHTML = `{{ messages('right', '${msg.message}', '${customTimeFormat(msg.created_at)}', '${image}') }}`;
                        
                        //        // Create a temporary container to hold the new message HTML
                        //       const tempDiv = document.createElement('div');
                        //       tempDiv.innerHTML = messageHTML;

                        //       // Prepend the new message to the messagesInterface
                        //      while (tempDiv.firstChild) {
                        //      messagesInterface.appendChild(tempDiv.firstChild);
                        //      }
                        //     }
                        
                        //     else {
                        //         const messageHTML = `{{ messages('right', ' ', '${customTimeFormat(msg.created_at)}', '${image}') }}`;
                        //         const tempDiv = document.createElement('div');
                        //         tempDiv.innerHTML = messageHTML;
                        //         // Prepend the new message to the messagesInterface
                        //         while (tempDiv.firstChild) {
                        //             messagesInterface.appendChild(tempDiv.firstChild);
                        //         }
                        //     }

                    renderMessage('right', msg, image, messagesInterface);
                          
                    }
                    else{
                        //   if(msg.message) {
                        //       const messageHTML = `{{ messages('left', '${msg.message}', '${customTimeFormat(msg.created_at)}', '${image}') }}`;
                        
                        //        // Create a temporary container to hold the new message HTML
                        //       const tempDiv = document.createElement('div');
                        //       tempDiv.innerHTML = messageHTML;

                        //       // Prepend the new message to the messagesInterface
                        //      while (tempDiv.firstChild) {
                        //      messagesInterface.appendChild(tempDiv.firstChild);
                        //      }
                        //     }
                        
                        //     else {
                        //         const messageHTML = `{{ messages('left', ' ', '${customTimeFormat(msg.created_at)}', '${image}') }}`;
                        //         const tempDiv = document.createElement('div');
                        //         tempDiv.innerHTML = messageHTML;
                        //         // Prepend the new message to the messagesInterface
                        //         while (tempDiv.firstChild) {
                        //             messagesInterface.appendChild(tempDiv.firstChild);
                        //         }
                        //     }

                        
                        renderMessage('left', msg, image, messagesInterface);
                    }  
                  
                    
                }
                console.log(msg)
                  
            
            }  
                    




        }
           

        
        
       
        // Get the outerHTML of messagesInterface to pass to the macro
        const msgI = messagesInterface.outerHTML;
        // console.log(messagesInterface);
        
        div.innerHTML = `{{ modalMessageTop('${heading}', '${msgI}', "${messageInputs}") }}`;
        const mainModal = document.getElementById("overlay-for-modal");
        mainModal.tabIndex = -1;
        mainModal.focus();
        async function demo() {
         await sleep(200);
          mainModal.scrollBy(0, mainModal.scrollHeight);
		    // Sleep for 2000 milliseconds (2 seconds)
          
        }
        demo();
        // Function to handle sending a message when the send button is clicked
        document.getElementById('send').onclick = async function() {
    console.log("Send button clicked event fired");
    
    const messageText = document.getElementById('message-input');
    if (!messageText.value) {
        alert('Message cannot be empty');
        return;
    }

    try {
        const csrfToken = await getCSRFToken();
        await sendPostRequest(messageText.value, csrfToken);
        messageText.value = '';  // Clear input after successful request
    } catch (error) {
        console.error('Error:', error);
    }
};

// Function to get CSRF token
async function getCSRFToken() {
    const response = await fetch('/get_csrf_token', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.csrf_token;
}

// Function to send a POST request
async function sendPostRequest(message, csrfToken) {
    const url = '/message/c20faad3-7680-4c81-bad6-0a67455539a7';
    const messageData = { text: message };

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(messageData)
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    console.log('Success:', data);
}

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};
function renderMessage(side, msg, img, mInterface){

let messageHTML;

if (side =="left")
{
    if (img && msg.message){
         messageHTML = `{{ messages('left', '${msg}', '${customTimeFormat(msg.created_at)}', '${img}') }}`;
    }
    else if (img && !msg.message){

         messageHTML = `{{ messages('left', ' ', '${customTimeFormat(msg.created_at)}', '${img}') }}`;
    }
    else {
        messageHTML = `{{ messages('left', '${msg} ', '${customTimeFormat(msg.created_at)}') }}`;
    }



}
else{
      if (img && msg){
         messageHTML = `{{ messages('right', '${msg}', '${customTimeFormat(msg.created_at)}', '${img}') }}`;
    }
    else if (img && !msg){

         essageHTML = `{{ messages('right', ' ', '${customTimeFormat(msg.created_at)}', '${img}') }}`;
    }
    else {
        essageHTML = `{{ messages('right', '${msg} ', '${customTimeFormat(msg.created_at)}') }}`;
    }


}

// Create a temporary container to hold the new message HTML
const tempDiv = document.createElement('div');
tempDiv.innerHTML = messageHTML;

// Prepend the new message to the messagesInterface
 while (tempDiv.firstChild) {
         mInterface.appendChild(tempDiv.firstChild);
 }


}




 const socket = io.connect();

    // Event listener for successful connection
    socket.on('connect', () => {
    console.log('Connected to the server');
    });



    socket.on('new_msg_list', (new_msg_list) => {

	const container = document.getElementById('main-div');
        const existingDiv= document.querySelector(`[data-msg-id= '${new_msg_list.id}']`)
        const currentUserId = '{{ current_user.id  }}';
        if (existingDiv) {
            // Update the message content and time
            existingDiv.style.borderBottom = '1px solid #D8D8D8';
      

            const messageContent = existingDiv.querySelector('.overflow-hidden');
            messageContent.innerText = new_msg_list.last_sender === currentUserId ? `You: ${new_msg_list.message}` : new_msg_list.message;

            // Bold the message if needed
            if (new_msg_list.last_sender !== currentUserId) {
                messageContent.style.fontWeight = 'bold';
                messageContent.style.fontSize = '14px';
                messageContent.style.color = 'var(--Grey-Dark, #606060)';

            } else {
                messageContent.style.color = 'var(--Grey-Dark, #606060)';
            }

            // Update the timestamp (assuming the time is in "2:00am" format, this should be dynamically set)
            const timestampDiv = existingDiv.children[0].children[2]; // Access the third child of the first child
			timestampDiv.innerText = `${new_msg_list.updated_at}`; // Replace with actual timestamp if available
	    
            
            // Move the div to the top
            container.appendChild(existingDiv);
        } else {

	   
            // Create a new div if it doesn't exist (for new messages)
            const isTailor = {{ current_user.is_tailor | tojson }};
            const imageProfile = `<img src="{{ url_for('static', filename='images/product_image_3.png') }}" class="rounded-full" style="width: 60px; height: 60px;">`;

            const name = isTailor ? `${new_msg_list.user_name}`  : `${new_msg_list.tailor_name}`;
            const message = new_msg_list.last_sender === currentUserId ? `You: ${new_msg_list.message}` : new_msg_list.message;

            const messageAndName = `
                <div class="flex flex-col gap-2 justify-between ml-2">
                    <div class="leading-[21px] font-normal font-roboto tracking-[0.5px] text-gray-800 text-[16px]" style="color: (--Grey-Darker, #2D2D2D);">
                        ${name}
                    </div>
                    <div class="leading-[21px] font-normal font-roboto tracking-[0.4px] text-gray-800 text-[12px] overflow-hidden" style="height:40px;">
                        ${message}
                    </div>
                </div>
            `;

            const newDiv = document.createElement('div');
            newDiv.className = 'pb-[10px]';
            newDiv.setAttribute('data-msg-id', new_msg_list.id);
            newDiv.setAttribute('id', `msg-${new_msg_list.id}`);
            newDiv.setAttribute('onclick', 'handleDivClick(this)');
            newDiv.style.borderBottom = container.children.length > 0 ? '1px solid #D8D8D8' : 'none';
            newDiv.innerHTML = ` {{ messageList('${imageProfile}','${ messageAndName}', '${new_msg_list.updated_at}') }}`;

            // Bold the message if needed
            const messageContentNew = newDiv.querySelector('.overflow-hidden');
            if (!new_msg_list.is_viewed && new_msg_list.last_sender !== currentUserId) {
                messageContentNew.style.fontWeight = 'bold';
                messageContentNew.style.fontSize = '14px';
                messageContentNew.style.color = 'var(--Grey-Dark, #606060)';

            } else {
                messageContentNew.style.color = 'var(--Grey-Dark, #606060)';
            }
            if (container.querySelector('#empty') !== null){
		container.querySelector('#empty').remove();
		container.append(newDiv);
            }
	   else{
            container.append(newDiv);
	    }
	    container.scrollTop = container.scrollHeight;
        }
       
    });

    
    function handleDivClick(element) {
        const msgId = element.getAttribute('data-msg-id');
        const existingDiv= document.querySelector(`[data-msg-id= '${msgId}']`)
        const messageContent = existingDiv.querySelector('.overflow-hidden');
        messageContent.style.fontWeight = 'normal';
        messageContent.style.fontSize = '12px';

        fetch(`/get_message?id=${msgId}`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Message ${msgId} marked as viewed.`);
                    window.location.href = data.redirect_url;
                } else {
                    console.error(`Failed to mark message ${msgId} as viewed.`);
                }
            })
            .catch(error => console.error('Error:', error));
    }

/*    document.addEventListener('DOMContentLoaded', function() {
        fetch('/get_messages')
            .then(response => response.json())
            .then(data => {
                const mainDiv = document.getElementById('main-div');
                const container = document.createElement('div');
                 data.forEach(item => {
                    const image_html = `<img src="{{ url_for('static', filename='images/product_image_3.png' ) }}" class="rounded-full" style="width: 50px; height: 50px;">`;
                    const time = "2:30";

                    const middleDiv = document.createElement('div');
		    middleDiv.classList.add('flex', 'flex-row')
				middleDiv.innerHTML = `<div class="flex flex-col gap-1 justify-between ml-2">  <div class="leading-[21px] font-normal font-roboto tracking-[0.5px] text-gray-800  text-[16px]" style="  color: (--Grey-Darker, #2D2D2D);">Morgan Coulture</div> 
                                                       <div class="class="leading-[21px] font-normal font-roboto tracking-[0.4px] text-gray-800  text-[10px]" style="  color:var(--Grey-Dark, #606060);">Ohh!! That was faster than expected.</div>
                                                       </div>`
				container.innerHTML = `{{ messageList('${image_html}', '${middleDiv.innerHTML}', '${time}') }}`;
                    mainDiv.appendChild(container);
                });
            })
            .catch(error => console.error('Error fetching messages:', error));
    });  */
</script>
{% endblock %}
