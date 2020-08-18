import telebot
import config
from telebot import types
import sqlalchemy as db
from sqlalchemy import create_engine, Column, String, Integer, func, Date,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


bot = telebot.TeleBot(config.token)
base = declarative_base()

class User(base):
    __tablename__ = "User"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    user_number = Column('user_number', Integer)
    first_name = ('first_name',String)
    last_name = ('last_name',String)



engine = create_engine('sqlite:///baza.db', echo=True, connect_args={'check_same_thread': False})
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
metadata = db.MetaData()

user = db.Table('User', metadata, autoload=True, autoload_with=engine)
conn = engine.connect()


@bot.message_handler(commands='start')
def phone(message):
    print(message.chat.id)
    _count = session.query(User).filter(User.user_id== message.chat.id).count()

    if(_count != 1):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id,"Iltimos botdan to\'liq foydalanish uchun telelfon raqamingizni yuboring",
                         reply_markup=keyboard)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Yangi guruh(kanal) qo\'shish ')

        bot.send_message(config.admin_id, "Iltimos o\'zingizga kerakli bo\'limni tanlang:", reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def any_message(message):

    try:
        numb = str(message.contact)
        number = numb.split("'")
        phone_number = number[3]
        users=User()
        users.user_id = message.chat.id
        users.first_name = message.chat.first_name
        users.last_name = message.chat.last_name
        users.user_number = phone_number
        session.add(users)
        bot.send_message(message.chat.id,"Urra")
    except Exception as e:
        bot.send_message(message.chat.id,e)

@bot.message_handler(content_types=["text", "photo", "location"])
def message_hand(message):
    m_text = message.text
    global chat_id
    chat_id = message.chat.id
    if (m_text == 'Yangi guruh(kanal) qo\'shish'):
        bot.send_message(message.chat.id,"Yangi guruh(kanal) qo\'shish uchun botni qo\'shmoqchi bo\'lgan")

@bot.message_handler(commands="add")
def command_default(message):
    print(message.forward_from_chat.id)
    # this is the standard reply to a normal message
    bot.send_message(message.chat.id, "I don't understand, try with /help")



bot.polling()
