from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
import json
import os
import random

# Set default window size and color
Window.size = (400, 700)
Window.clearcolor = (0.1, 0.1, 0.2, 1)
Window.borderless = False  # Ensure window has borders

class UserData:
    @staticmethod
    def save_user(username, email):
        data = {
            'username': username,
            'email': email,
            'total_credits': 50,
            'messages_sent': 0
        }
        with open('user_data.json', 'w') as f:
            json.dump(data, f)
    
    @staticmethod
    def load_user():
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def update_credits(credits):
        data = UserData.load_user()
        if data:
            data['total_credits'] = credits
            with open('user_data.json', 'w') as f:
                json.dump(data, f)

# Bot responses with credit costs
BOT_RESPONSES = {
    "merhaba": {
        "cost": 1,
        "responses": [
            "Merhaba! Size nasıl yardımcı olabilirim?",
            "Hoş geldiniz! Bugün size nasıl yardımcı olabilirim?",
            "Merhaba! Benimle her konuda sohbet edebilirsiniz."
        ]
    },
    "nasılsın": {
        "cost": 2,
        "responses": [
            "İyiyim, teşekkür ederim! Siz nasılsınız?",
            "Çok iyiyim, siz nasılsınız?",
            "Harika! Umarım sizin de gününüz güzel geçiyordur."
        ]
    },
    "ne yapıyorsun": {
        "cost": 2,
        "responses": [
            "Size yardımcı olmak için buradayım. Nasıl yardımcı olabilirim?",
            "Sizinle sohbet etmek için bekliyordum. Nasıl yardımcı olabilirim?",
            "Her türlü konuda size destek olmaya hazırım."
        ]
    },
    "hava": {
        "cost": 3,
        "responses": [
            "Hava durumu hakkında konuşmak ister misiniz?",
            "Bugün gerçekten güzel bir gün, değil mi?",
            "Hava durumu her zaman ilginç bir konu!"
        ]
    },
    "müzik": {
        "cost": 3,
        "responses": [
            "Müzik harika bir konu! En sevdiğiniz tür nedir?",
            "Müzik ruhun gıdasıdır. Hangi sanatçıları dinlemeyi seversiniz?",
            "Müzik hakkında konuşmayı çok severim!"
        ]
    },
    "film": {
        "cost": 3,
        "responses": [
            "Film önerileri almak ister misiniz?",
            "Hangi tür filmleri seviyorsunuz?",
            "Son zamanlarda izlediğiniz güzel bir film var mı?"
        ]
    },
    "kitap": {
        "cost": 3,
        "responses": [
            "Kitap okumayı sever misiniz? Size önerilerde bulunabilirim.",
            "En son okuduğunuz kitap hangisiydi?",
            "Hangi tür kitapları okumayı tercih edersiniz?"
        ]
    },
    "spor": {
        "cost": 3,
        "responses": [
            "Spor yapmayı sever misiniz?",
            "Hangi spor dallarıyla ilgileniyorsunuz?",
            "Favori takımınız hangisi?"
        ]
    },
    "yemek": {
        "cost": 3,
        "responses": [
            "Yemek yapmayı sever misiniz?",
            "En sevdiğiniz yemek nedir?",
            "Size güzel tarifler önerebilirim!"
        ]
    },
    "teşekkür": {
        "cost": 1,
        "responses": [
            "Rica ederim! Başka nasıl yardımcı olabilirim?",
            "Ne demek, her zaman!",
            "Ben teşekkür ederim! Başka bir konuda yardıma ihtiyacınız var mı?"
        ]
    },
    "görüşürüz": {
        "cost": 1,
        "responses": [
            "Görüşmek üzere! İyi günler!",
            "Hoşça kalın! Tekrar görüşmek üzere!",
            "İyi günler! Yine beklerim!"
        ]
    },
    "default": {
        "cost": 2,
        "responses": [
            "Bu konu hakkında daha fazla bilgi verebilir misiniz?",
            "İlginç bir konu. Devam edin, sizi dinliyorum.",
            "Size bu konuda nasıl yardımcı olabilirim?"
        ]
    }
}

class WelcomeScreen(Screen):
    def on_enter(self):
        pass

class Message(BoxLayout):
    message_text = StringProperty('')
    is_user = BooleanProperty(False)
    cost = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self.opacity = 0
        Animation(opacity=1, duration=0.3).start(self)

    def _finish_init(self, dt):
        self.bind(size=self._update_rect, pos=self._update_rect)
        self._update_rect(None, None)

    def _update_rect(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_user:
                Color(rgba=get_color_from_hex('#4C5BE0'))
            else:
                Color(rgba=(0.15, 0.15, 0.3, 1))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

class LoginScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.focus_username())
    
    def focus_username(self):
        self.ids.username.focus = True
        self.ids.username.bind(on_text_validate=lambda x: self.focus_password())
        self.ids.password.bind(on_text_validate=lambda x: self.login())
    
    def focus_password(self):
        self.ids.password.focus = True
        self.ids.username.background_color = (0.15, 0.15, 0.3, 1)

    def validate_password(self, password):
        return len(password) <= 6

    def login(self, *args):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        
        if not username or not password:
            if not username:
                self.ids.username.background_color = (0.8, 0.2, 0.2, 1)
            if not password:
                self.ids.password.background_color = (0.8, 0.2, 0.2, 1)
            return
        
        if not self.validate_password(password):
            self.ids.password.background_color = (0.8, 0.2, 0.2, 1)
            self.ids.password.text = ""
            self.ids.password.hint_text = "Maximum 6 characters!"
            return
        
        try:
            # Save user data
            UserData.save_user(username, username + "@example.com")
            
            # Update chat screen
            chat_screen = self.manager.get_screen('chat')
            chat_screen.username = username
            chat_screen.credits = 50
            chat_screen.save_credits()
            
            # Switch to chat screen
            self.manager.current = 'chat'
            
        except Exception as e:
            print(f"Login error: {e}")
            # Reset fields on error
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.ids.username.background_color = (0.8, 0.2, 0.2, 1)
            self.ids.password.background_color = (0.8, 0.2, 0.2, 1)
    
    def forgot_password(self):
        self.manager.current = 'forgot_password'

class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)
        self.verification_code = None
    
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.focus_phone())
    
    def focus_phone(self):
        self.ids.phone.focus = True
        self.ids.phone.bind(on_text_validate=lambda x: self.send_code())
    
    def send_code(self):
        phone = self.ids.phone.text.strip()
        if phone and len(phone) == 10:
            self.verification_code = str(random.randint(100000, 999999))
            print(f"Verification code: {self.verification_code}")
            verification_screen = self.manager.get_screen('verification')
            verification_screen.verification_code = self.verification_code
            verification_screen.phone = phone
            self.manager.current = 'verification'
        else:
            self.ids.phone.background_color = (0.8, 0.2, 0.2, 1)
    
    def back_to_login(self):
        self.manager.current = 'login'

class VerificationScreen(Screen):
    verification_code = StringProperty(None)
    phone = StringProperty('')
    
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.focus_code())
    
    def focus_code(self):
        self.ids.code.focus = True
        self.ids.code.bind(on_text_validate=lambda x: self.verify_code())
    
    def verify_code(self):
        entered_code = self.ids.code.text.strip()
        if entered_code == self.verification_code:
            self.manager.current = 'new_password'
        else:
            self.ids.code.background_color = (0.8, 0.2, 0.2, 1)
            self.ids.code.text = ""
    
    def back_to_forgot(self):
        self.manager.current = 'forgot_password'

class NewPasswordScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.focus_password())
    
    def focus_password(self):
        self.ids.new_password.focus = True
        self.ids.new_password.bind(on_text_validate=lambda x: self.focus_confirm())
    
    def focus_confirm(self):
        self.ids.confirm_password.focus = True
        self.ids.confirm_password.bind(on_text_validate=lambda x: self.save_password())
    
    def validate_password(self, password):
        return len(password) <= 6
    
    def save_password(self, *args):
        new_pass = self.ids.new_password.text.strip()
        confirm_pass = self.ids.confirm_password.text.strip()
        
        if not self.validate_password(new_pass):
            self.ids.new_password.background_color = (0.8, 0.2, 0.2, 1)
            self.ids.new_password.text = ""
            self.ids.new_password.hint_text = "Maximum 6 characters!"
            return
        
        if new_pass and confirm_pass and new_pass == confirm_pass:
            self.manager.current = 'login'
        else:
            if not new_pass:
                self.ids.new_password.background_color = (0.8, 0.2, 0.2, 1)
            if not confirm_pass:
                self.ids.confirm_password.background_color = (0.8, 0.2, 0.2, 1)
            if new_pass != confirm_pass:
                self.ids.confirm_password.background_color = (0.8, 0.2, 0.2, 1)
                self.ids.confirm_password.text = ""
                self.ids.confirm_password.hint_text = "Passwords don't match!"

class ProfileScreen(Screen):
    user_data = DictProperty({
        'username': '',
        'email': '',
        'total_credits': 0,
        'messages_sent': 0
    })
    
    def on_enter(self):
        self.load_user_data()
    
    def load_user_data(self):
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as f:
                self.user_data.update(json.load(f))
    
    def save_user_data(self):
        with open('user_data.json', 'w') as f:
            json.dump(dict(self.user_data), f)
    
    def logout(self):
        self.manager.current = 'login'

class BuyCreditsScreen(Screen):
    def __init__(self, **kwargs):
        super(BuyCreditsScreen, self).__init__(**kwargs)
        self.credit_packages = [
            {'amount': 100, 'price': '10₺'},
            {'amount': 250, 'price': '20₺'},
            {'amount': 500, 'price': '35₺'},
            {'amount': 1000, 'price': '60₺'}
        ]
        self.selected_amount = 0
        self.selected_price = ''
    
    def select_package(self, amount, price):
        self.selected_amount = amount
        self.selected_price = price
        # Enable the payment form
        self.ids.payment_form.opacity = 1
        self.ids.payment_form.disabled = False
    
    def validate_card(self):
        card_number = self.ids.card_number.text.strip()
        card_holder = self.ids.card_holder.text.strip()
        expiry_date = self.ids.expiry_date.text.strip()
        cvv = self.ids.cvv.text.strip()
        
        # Basic validation
        if not card_number or len(card_number) != 16 or not card_number.isdigit():
            self.ids.card_number.background_color = (0.8, 0.2, 0.2, 1)
            return False
        
        if not card_holder:
            self.ids.card_holder.background_color = (0.8, 0.2, 0.2, 1)
            return False
        
        if not expiry_date or len(expiry_date) != 5 or expiry_date[2] != '/':
            self.ids.expiry_date.background_color = (0.8, 0.2, 0.2, 1)
            return False
        
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            self.ids.cvv.background_color = (0.8, 0.2, 0.2, 1)
            return False
        
        return True
    
    def buy_credits(self):
        if self.selected_amount == 0:
            return
        
        if not self.validate_card():
            return
        
        chat_screen = self.manager.get_screen('chat')
        chat_screen.credits += self.selected_amount
        chat_screen.save_credits()
        
        profile_screen = self.manager.get_screen('profile')
        profile_screen.user_data['total_credits'] += self.selected_amount
        profile_screen.save_user_data()
        
        # Reset form
        self.ids.card_number.text = ''
        self.ids.card_holder.text = ''
        self.ids.expiry_date.text = ''
        self.ids.cvv.text = ''
        self.selected_amount = 0
        self.selected_price = ''
        
        self.manager.current = 'chat'
    
    def on_text_validate(self, instance):
        if instance == self.ids.card_number:
            self.ids.card_holder.focus = True
        elif instance == self.ids.card_holder:
            self.ids.expiry_date.focus = True
        elif instance == self.ids.expiry_date:
            self.ids.cvv.focus = True
        elif instance == self.ids.cvv:
            self.buy_credits()
    
    def format_expiry_date(self, instance, value):
        text = value.replace('/', '')[:4]
        if len(text) > 2:
            text = text[:2] + '/' + text[2:]
        instance.text = text
    
    def format_card_number(self, instance, value):
        text = ''.join(filter(str.isdigit, value))[:16]
        instance.text = text

class UserInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(UserInfoScreen, self).__init__(**kwargs)
        self.load_user_info()
    
    def load_user_info(self):
        if os.path.exists('user_info.json'):
            with open('user_info.json', 'r') as f:
                self.user_info = json.load(f)
                if self.user_info:
                    self.ids.name.text = self.user_info.get('name', '')
                    self.ids.surname.text = self.user_info.get('surname', '')
                    self.ids.age.text = str(self.user_info.get('age', ''))
                    self.ids.phone.text = self.user_info.get('phone', '')
                    self.ids.address.text = self.user_info.get('address', '')
    
    def save_user_info(self):
        user_info = {
            'name': self.ids.name.text.strip(),
            'surname': self.ids.surname.text.strip(),
            'age': self.ids.age.text.strip(),
            'phone': self.ids.phone.text.strip(),
            'address': self.ids.address.text.strip()
        }
        
        # Basic validation
        if not all([user_info['name'], user_info['surname'], user_info['age'], user_info['phone']]):
            return False
        
        with open('user_info.json', 'w') as f:
            json.dump(user_info, f)
        return True
    
    def validate_and_continue(self):
        if self.save_user_info():
            self.manager.current = 'chat'
        else:
            # Show error state on empty fields
            for field_id in ['name', 'surname', 'age', 'phone']:
                if not self.ids[field_id].text.strip():
                    self.ids[field_id].background_color = (0.8, 0.2, 0.2, 1)

class ChatScreen(Screen):
    credits = NumericProperty(50)
    username = StringProperty('')
    
    def welcome_message(self):
        welcome_text = f"Merhaba {self.username}! Size nasıl yardımcı olabilirim?"
        self.add_message(welcome_text, False, 0)
    
    def on_enter(self):
        # Load user data
        user_data = UserData.load_user()
        if user_data:
            self.username = user_data['username']
            self.credits = user_data.get('credits', 50)
        
        Clock.schedule_once(lambda dt: self.focus_message_input())
        self.load_messages()
        self.load_credits()
        
        # If this is first time entering chat, show welcome message
        if not os.path.exists('messages.json'):
            Clock.schedule_once(lambda dt: self.welcome_message(), 0.5)
    
    def focus_message_input(self):
        self.ids.message_input.focus = True
    
    def check_credits(self):
        if self.credits <= 10:
            self.add_message("Kredi miktarınız azalıyor! Daha fazla kredi satın almak ister misiniz?", False, 0)
        elif self.credits <= 0:
            self.add_message("Kredileriniz tükendi! Sohbete devam etmek için lütfen kredi satın alın.", False, 0)
            Clock.schedule_once(lambda dt: self.show_buy_credits(), 1)
    
    def show_buy_credits(self):
        if not os.path.exists('user_info.json'):
            self.manager.current = 'user_info'
        else:
            self.manager.current = 'buy_credits'
    
    def show_profile(self):
        self.manager.current = 'profile'
    
    def load_messages(self):
        if os.path.exists('messages.json'):
            with open('messages.json', 'r', encoding='utf-8') as f:
                messages = json.load(f)
                for msg in messages:
                    self.add_message(msg['text'], msg['is_user'])
    
    def send_message(self, *args):
        message = self.ids.message_input.text.strip()
        if message:
            min_cost = min(topic['cost'] for topic in BOT_RESPONSES.values())
            if self.credits < min_cost:
                self.add_message("Üzgünüm, krediniz yetersiz! Lütfen daha fazla kredi satın alın.", False, 0)
                Clock.schedule_once(lambda dt: self.show_buy_credits(), 1)
                return
            
            self.add_message(message, True, 0)
            self.ids.message_input.text = ''
            
            Clock.schedule_once(lambda dt: self.bot_response(message.lower()), 0.5)
            Clock.schedule_once(lambda dt: self.focus_message_input(), 0.1)
    
    def bot_response(self, user_message):
        response_data = None
        cost = 0
        
        for key, data in BOT_RESPONSES.items():
            if key in user_message:
                response_data = data
                cost = data['cost']
                break
        
        if not response_data:
            response_data = BOT_RESPONSES['default']
            cost = response_data['cost']
        
        if self.credits < cost:
            self.add_message("Üzgünüm, bu yanıt için yeterli krediniz yok. Lütfen daha fazla kredi satın alın.", False, 0)
            return
        
        self.credits -= cost
        response = random.choice(response_data['responses'])
        
        self.add_message(f"[Kullanılan kredi: {cost}]", False, cost)
        Clock.schedule_once(lambda dt: self.add_message(response, False, 0), 0.5)
        
        self.save_credits()
        UserData.update_credits(self.credits)
        self.check_credits()
    
    def add_message(self, text, is_user, cost=0):
        message = {
            'message_text': text,
            'is_user': is_user,
            'cost': cost
        }
        self.ids.chat_history.data.append(message)
        Clock.schedule_once(lambda dt: self.scroll_bottom())
    
    def scroll_bottom(self):
        rv = self.ids.chat_history
        if rv.children:
            box = rv.children[0]
            if box.height > rv.height:
                rv.scroll_y = 0
    
    def save_credits(self):
        with open('credits.json', 'w') as f:
            json.dump({'credits': self.credits}, f)
        UserData.update_credits(self.credits)
    
    def load_credits(self):
        if os.path.exists('credits.json'):
            with open('credits.json', 'r') as f:
                data = json.load(f)
                self.credits = data.get('credits', 50)

class EchoaApp(App):
    def build(self):
        Builder.load_file('echoai.kv')
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(ForgotPasswordScreen(name='forgot_password'))
        sm.add_widget(VerificationScreen(name='verification'))
        sm.add_widget(NewPasswordScreen(name='new_password'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(BuyCreditsScreen(name='buy_credits'))
        sm.add_widget(UserInfoScreen(name='user_info'))
        return sm

if __name__ == '__main__':
    # Create necessary directories
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Create necessary files
    if not os.path.exists('messages.json'):
        with open('messages.json', 'w') as f:
            json.dump([], f)
    
    if not os.path.exists('credits.json'):
        with open('credits.json', 'w') as f:
            json.dump({'credits': 50}, f)
    
    if not os.path.exists('user_data.json'):
        with open('user_data.json', 'w') as f:
            json.dump({
                'username': '',
                'email': '',
                'total_credits': 50,
                'messages_sent': 0
            }, f)
    
    if not os.path.exists('user_info.json'):
        with open('user_info.json', 'w') as f:
            json.dump({}, f)
    
    # Create icons if they don't exist
    if not os.path.exists('assets/logo.png'):
        from create_robot_icon import create_logo, create_avatars
        create_logo()
        create_avatars()
    
    try:
        EchoaApp().run()
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...") 