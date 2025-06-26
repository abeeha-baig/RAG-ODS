import base64
import os

def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def get_templates():
    # Paths to images
    bot_image_path = os.path.join("templates", "basha.jpg")
    user_image_path = os.path.join("templates", "human.jpg")
    
    # Load images
    bot_image_base64 = load_image_as_base64(bot_image_path)
    user_image_base64 = load_image_as_base64(user_image_path)

    # Define templates
    bot_template = f'''
    <div class="chat-message bot">
        <div class="avatar">
            <img src="data:image/jpg;base64,{bot_image_base64}" alt="Bot">
        </div>
        <div class="message">{{{{MSG}}}}</div>
    </div>
    '''

    user_template = f'''
    <div class="chat-message user">
        <div class="avatar">
            <img src="data:image/jpg;base64,{user_image_base64}" alt="User">
        </div>    
        <div class="message">{{{{MSG}}}}</div>
    </div>
    '''

    return bot_template, user_template

def get_css():
    css = '''
    <style>
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .avatar img {
      max-width: 32px;
      max-height: 32px;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-message .message {
      width: 80%;
      padding: 0 1.5rem;
      color: #fff;
    }
    </style>
    '''
    return css
