import threading
import config
from telebot import types
import sqlalchemy as db
from sqlalchemy import create_engine, Column, String, Integer, func, Date,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import telebot
from sqlalchemy import or_
import schedule
import time
import pytz
from datetime import datetime
import json
from time import strptime, struct_time, localtime

bot = telebot.TeleBot(config.token)
base = declarative_base()

class User(base):
    __tablename__ = "User"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    user_number = Column('user_number', Integer)
    first_name = Column('first_name',String)
    last_name = Column('last_name',String)

class Rejim(base):
    __tablename__ = "Rejim"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    group_id = Column('group_id', Integer)
    group_name = Column('group_name', String)
    day = Column('day', String)
    text = Column('text', String)
    time = Column('time',String)
    finish = Column('finish',Integer)


class Second_db(base):
    __tablename__ = "Second_db"
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    group_id = Column('group_id', Integer)
    day = Column('day', String)
    days_id = Column('days_id', Integer)
    text = Column('text', String)
    time = Column('time',String)
    finish = Column('finish', Integer)

engine = create_engine('sqlite:///mbaza.db', echo=True, connect_args={'check_same_thread': False})
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
metadata = db.MetaData()

user = db.Table('User', metadata, autoload=True, autoload_with=engine)
rejim = db.Table('Rejim', metadata, autoload=True, autoload_with=engine)
second_db = db.Table('Second_db', metadata, autoload=True, autoload_with=engine)
conn = engine.connect()
  


@bot.message_handler(commands=['groot'])
def posts_from(message):
    try:
        users_list = bot.get_chat_administrators(message.chat.id)
        for i in users_list:
            chatid=i.user.id
            #chatid = kanal(guruh) dagi adminlarni id si

            if (message.from_user.id == chatid):

                try:
                    sess = Session()
                    tartib = Rejim()
                    tartib.user_id = message.from_user.id
                    tartib.group_id = message.chat.id
                    tartib.group_name = message.chat.title
                    tartib.finish = 0
                    sess.add(tartib)

                    sess.commit()
                    sess.close()

                    keyboard_l = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton("🗓 Har hafta", callback_data="hafta_kun")
                    btn2 = types.InlineKeyboardButton("📅 Har oyda", callback_data="only_one_date")
                    btn3 = types.InlineKeyboardButton("🔂 Bir martalik", callback_data="only_one")
                    back = types.InlineKeyboardButton("🔙Ortga", callback_data="one_back")
                    keyboard_l.add(btn1)
                    keyboard_l.add(btn2)
                    keyboard_l.add(btn3)
                    keyboard_l.add(back)
                    msg = bot.send_message(message.from_user.id, "🎯 Xabarnoma turini tanlang",
                                           reply_markup=keyboard_l)
                    bot.delete_message(message.chat.id, message.message_id)

                except Exception as e:
                    bot.send_message(config.admin_id, e)

    except Exception as e:
        bot.send_message(config.admin_id, e)

@bot.message_handler(func=lambda message: message.forward_from_chat)
def posts_from_channels(message):
    users_list = bot.get_chat_administrators(message.forward_from_chat.id)
    for i in users_list:
        chatid=i.user.id
        # chatid = kanal(guruh) dagi adminlarni id s
        if (message.chat.id == chatid):
            tekshir = 1

            try:
                sess = Session()
                tartib = Rejim()
                tartib.user_id = message.chat.id
                tartib.group_id = message.forward_from_chat.id
                tartib.group_name = message.forward_from_chat.title
                tartib.finish = 0
                sess.add(tartib)

                sess.commit()
                sess.close()

                keyboard_l = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("🗓 Har hafta", callback_data="hafta_kun")
                btn2 = types.InlineKeyboardButton("📅 Har oyda", callback_data="only_one_date")
                btn3 = types.InlineKeyboardButton("🔂 Bir martalik", callback_data="only_one")
                back = types.InlineKeyboardButton("🔙Ortga", callback_data="one_back")
                keyboard_l.add(btn1)
                keyboard_l.add(btn2)
                keyboard_l.add(btn3)
                keyboard_l.add(back)
                msg = bot.send_message(message.chat.id, "🎯 Xabarnoma turini tanlang",
                                       reply_markup=keyboard_l)

            except Exception as e:
                bot.send_message(config.admin_id, e)

    if (tekshir == 0):
        bot.send_message(message.chat.id,
                         "☹️ Siz kanal(guruh) da admin emassiz. To'liq malumot olish uchun \n /help")


def data_time_step(message):
    chat_id = message.chat.id
    m_text = message.text
    try:
        if m_text == "🔙Ortga":
            keyboard_l = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Dushanba", callback_data="Monday")
            btn2 = types.InlineKeyboardButton("Seshanba", callback_data="Tuesday")
            btn3 = types.InlineKeyboardButton("Chorshanba", callback_data="Wednesday")
            btn4 = types.InlineKeyboardButton("Payshanba", callback_data="Thursday")
            btn5 = types.InlineKeyboardButton("Juma", callback_data="Friday")
            btn6 = types.InlineKeyboardButton("Shanba", callback_data="Saturday")
            btn7 = types.InlineKeyboardButton("Yakshanba", callback_data="Sunday")
            btn8 = types.InlineKeyboardButton("🔜Keyingi bosqich", callback_data="next")
            back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
            keyboard_l.add(btn1, btn2)
            keyboard_l.add(btn3, btn4)
            keyboard_l.add(btn5, btn6, btn7)
            keyboard_l.add(back, btn8)
            msg = bot.send_message(chat_id,
                                   "🗓 Xabarnoma jo\'natilishi kerak bo\'lgan hafta kuni(lari)ni belgilang.",
                                   parse_mode='html', reply_markup=keyboard_l)
            bot.delete_message(message.chat.id,message.message_id)
            

        elif m_text[2] == ":" and int(m_text[0]) <= 2 and int(m_text[1]) <= 9 and int(m_text[3]) <= 5 and int(
                m_text[4]) <= 9 and not (int(m_text[0]) == 2 and int(m_text[1]) >= 4):
            session = Session()

            up_id = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first().id
            session.query(Rejim).filter(Rejim.id == up_id).update({Rejim.time: m_text}, synchronize_session=False)

            session.commit()
            session.close()
            keyboard_l = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("✅ Ha, matnni yuborish", callback_data="yes_text")
            btn2 = types.InlineKeyboardButton("🙅‍♂️ Yo\'q, qaytadan vaqtni yuborish", callback_data="yes_time")
            keyboard_l.add(btn1)
            keyboard_l.add(btn2)
            bot.send_message(chat_id, "Siz xabarnomani <b>" + m_text + "</b> ga o'rnatmoqchimisiz ?",
                             parse_mode="html", reply_markup=keyboard_l)


        else:
            msg = bot.send_message(chat_id, "Iltimos vaqtni namundagi ko\'rinishda kiriting")
            bot.register_next_step_handler(msg, data_time_step)

    except Exception as e:
        msg =bot.send_message(config.admin_id, e)

        bot.register_next_step_handler(msg, data_time_step)


def data_date_step(message):
    chat_id = message.chat.id
    m_text = message.text
    try:
        if m_text == "🔙Ortga":
            keyboard_l = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("🗓 Har hafta", callback_data="hafta_kun")
            btn2 = types.InlineKeyboardButton("📅 Har oyda", callback_data="only_one_date")
            btn3 = types.InlineKeyboardButton("🔂 Bir martalik", callback_data="only_one")
            back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
            keyboard_l.add(btn1)
            keyboard_l.add(btn2)
            keyboard_l.add(btn3)
            keyboard_l.add(back)
            msg = bot.send_message(chat_id, "🎯 Xabarnoma turini tanlang",
                                               reply_markup=keyboard_l)
            bot.delete_message(message.chat.id,message.message_id)
            

        elif int(m_text[0]) <= 3 and int(m_text[1]) <= 9 and not (int(m_text[0]) == 3 and int(m_text[1]) >= 1) and len(m_text) <=2 :
            if(int(m_text) > 28):
                keyboard_l = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("🗓 Har hafta", callback_data="hafta_kun")
                btn3 = types.InlineKeyboardButton("🔂 Bir martalik", callback_data="only_one")
                back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
                keyboard_l.add(btn1)
                
                keyboard_l.add(btn3)
                keyboard_l.add(back)
                msg = bot.send_message(chat_id, "🎯 Siz kiritgan sana ba\'zi oylarda yo\'qligi sababli xabarnoma  o\'rnatishni imkoni yo\'q. <b>🗓 Har hafta</b> yoki <b>🔂 Bir martalik</b> tartibidan foydalaning",
                                                   reply_markup=keyboard_l,parse_mode="html")

            else:                
                session = Session()
                session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).update(
                    {Rejim.day: m_text}, synchronize_session=False)
                session.commit()
                session.close()
                keyboard_l = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("✅ Ha, vaqtni belgilash", callback_data="yes_time")
                btn2 = types.InlineKeyboardButton("🙅‍♂️ Yo\'q, qayta tanlash", callback_data="only_one_date")
                keyboard_l.add(btn1)
                keyboard_l.add(btn2)
                bot.send_message(chat_id, "📌 Xabarnomani har oyning <b>" + m_text + "</b>-sanasiga o'rnatmoqchimisiz? 🧐",
                                 parse_mode="html", reply_markup=keyboard_l)



        else:
            msg = bot.send_message(chat_id, "📝 1Sanani namunadagi ko\'rinishda kiriting")
            bot.register_next_step_handler(msg, data_date_step)

    except Exception as e: 

        msg = bot.send_message(chat_id, "📝 Sanani namunadagi ko\'rinishda kiriting")
        bot.send_message(config.admin_id,e)
        bot.register_next_step_handler(msg, data_date_step)



def data_sana_step(message):
    chat_id = message.chat.id
    m_text = message.text

    tz = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tz)
    today_date = str(now.strftime('%d.%m.%Y'))
    sana = struct_time(localtime())
    try:
        if m_text == "🔙Ortga":
            keyboard_l = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("🗓 Har hafta", callback_data="hafta_kun")
            btn2 = types.InlineKeyboardButton("📅 Har oyda", callback_data="only_one_date")
            btn3 = types.InlineKeyboardButton("🔂 Bir martalik", callback_data="only_one")
            back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
            keyboard_l.add(btn1)
            keyboard_l.add(btn2)
            keyboard_l.add(btn3)
            keyboard_l.add(back)
            msg = bot.send_message(chat_id, "🎯 Xabarnoma turini tanlang",
                                               reply_markup=keyboard_l)
            bot.delete_message(message.chat.id,message.message_id)
            
            #26.05.2020
        elif m_text[2] == "." and m_text[5] == "." and int(m_text[0]) <= 3 and int(m_text[1]) <= 9 and not (int(m_text[0]) == 3 and int(m_text[1]) >= 1) and int(m_text[3]) <= 1 and int(m_text[4]) <= 9 and not (int(m_text[3]) == 1 and int(m_text[4]) >= 2) and int(m_text[6:10]) >= 2020:

            if strptime(m_text, '%d.%m.%Y') > sana or m_text == today_date:
                print(str(strptime(m_text, '%d.%m.%Y')))
                session = Session()
                session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).update(
                    {Rejim.day: m_text}, synchronize_session=False)
                session.commit()
                session.close()
                keyboard_l = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("✅ Ha, vaqtni belgilash", callback_data="yes_time")
                btn2 = types.InlineKeyboardButton("🙅‍♂️ Yo\'q, qayta tanlash", callback_data="only_one")
                keyboard_l.add(btn1)
                keyboard_l.add(btn2)
                bot.send_message(chat_id, "📌 Xabarnomani  <b>" + m_text + "</b> sanasiga o'rnatmoqchimisiz? 🧐",
                                 parse_mode="html", reply_markup=keyboard_l)

            else:

                msg = bot.send_message(chat_id, "📝 Siz kiritgan sanaga  ushbu vaqt o\'tib ketganligi sababli xabarnoma o\'rnatishni iloji yo\'q.")
                bot.register_next_step_handler(msg, data_sana_step)                    



        else:
            msg = bot.send_message(chat_id, "📝 Sanani namunadagi ko\'rinishda kiriting2")
            bot.register_next_step_handler(msg, data_sana_step)

    except Exception as e: 
        bot.send_message(config.admin_id,e)    
        msg = bot.send_message(chat_id, "📝 Sanani namunadagi ko\'rinishda kiriting1")
        bot.register_next_step_handler(msg, data_sana_step)        


def data_text_step(message):
    m_text = message.text
    chat_id = message.chat.id
    session = Session()

    up_id = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first().id
    session.query(Rejim).filter(Rejim.id == up_id).update({Rejim.text: m_text}, synchronize_session=False)

    data = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first()
    keyboard_l = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("✅ Ha, tartibni saqlash", callback_data="save")
    btn2 = types.InlineKeyboardButton("🙅‍♂️ Yo\'q, matnni o'zgartirmoqchiman", callback_data="yes_text")
    keyboard_l.add(btn1)
    keyboard_l.add(btn2)

    day = data.day
    need_day = day.split()
    kunlar=""
    
    for i in need_day:
        if i == "Monday":
            kunlar = kunlar+"Dushanba "
        if i == "Tuesday":
            kunlar = kunlar+"Seshanba "
        if i == "Wednesday":
            kunlar = kunlar+"Chorshanba "
        if i == "Thursday":
            kunlar = kunlar+"Payshanba "
        if i == "Friday":
            kunlar = kunlar+"Juma "
        if i == "Saturday":
            kunlar = kunlar+"Shanba "
        if i == "Sunday":
            kunlar = kunlar+"Yakshanba "
        if int(i[1]) > 0:
            kunlar = i            
        else:
            kunlar = kunlar+""                       

    bot.send_message(chat_id,
                         "Siz  xabarnomani <b>" + data.group_name + "</b> kanal(guruh)iga\n<b>" + kunlar + "</b> kun(sana) uchun\n<b>" + data.time + "</b> vaqtida <u>" + data.text + "</u> xabarini yuborish tartibini o'rnatmoqchimisiz ?",
                         parse_mode="html", reply_markup=keyboard_l)
    print("kunlar"+kunlar)
    session.commit()
    session.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """ Responses for callback query """
    chat_id = call.from_user.id
    weekdays = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]

    if call.data == "hafta_kun":
        keyboard_l = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Dushanba", callback_data="Monday")
        btn2 = types.InlineKeyboardButton("Seshanba", callback_data="Tuesday")
        btn3 = types.InlineKeyboardButton("Chorshanba", callback_data="Wednesday")
        btn4 = types.InlineKeyboardButton("Payshanba", callback_data="Thursday")
        btn5 = types.InlineKeyboardButton("Juma", callback_data="Friday")
        btn6 = types.InlineKeyboardButton("Shanba", callback_data="Saturday")
        btn7 = types.InlineKeyboardButton("Yakshanba", callback_data="Sunday")
        btn8 = types.InlineKeyboardButton("🔜Keyingi bosqich", callback_data="next")
        back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
        keyboard_l.add(btn1, btn2)
        keyboard_l.add(btn3, btn4)
        keyboard_l.add(btn5, btn6, btn7)
        keyboard_l.add(back, btn8)
        msg = bot.send_message(chat_id,
                               "🗓 Xabarnoma jo\'natilishi kerak bo\'lgan hafta kuni(lari)ni belgilang.",
                               parse_mode='html', reply_markup=keyboard_l)
        bot.answer_callback_query(call.id, "Endi xabarnomani jo\'natish vaqtini belgilang")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "only_one_date":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('🔙Ortga')
        msg = bot.send_message(chat_id,
                         "🎯 Xabarnomani jo\'natish uchun sanani yuboring. \nSanani namunadagi ko\'rinishda yuboring:\n✅ Namuna: <b>16</b>",
                         parse_mode='html',reply_markup=markup)
        bot.answer_callback_query(call.id, "Endi xabarnomani jo\'natish sanasini yuboring")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, data_date_step)


    elif call.data == "only_one":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('🔙Ortga')
        msg = bot.send_message(chat_id,
                         "🎯 Xabarnomani jo\'natish uchun sanani yuboring. \nSanani namunadagi ko\'rinishda yuboring:\n✅ Namuna: <b>27.09.2020</b>",
                         parse_mode='html',reply_markup=markup)
        bot.answer_callback_query(call.id, "Endi xabarnomani jo\'natish sanasini yuboring")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, data_sana_step)        

    elif call.data == "one_back":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('📣 Yangi xabarnomani qo\'shish')
        markup.row('🔕 O\'rnatilgan xabarnomani o\'chirish')
        bot.answer_callback_query(call.id, "Ortga")
        bot.send_message(chat_id, "<i>Men </i>Groot<i>man 🌱</i>",
                                                reply_markup=markup, parse_mode="html")
        bot.delete_message(call.message.chat.id, call.message.message_id)



    elif call.data == "back":
        
        bot.answer_callback_query(call.id, "Ortga")
        keyboard_l = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🗓 Har hafta", callback_data="hafta_kun")
        btn2 = types.InlineKeyboardButton("📅 Har oyda", callback_data="only_one_date")
        btn3 = types.InlineKeyboardButton("🔂 Bir martalik", callback_data="only_one")
        back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
        keyboard_l.add(btn1)
        keyboard_l.add(btn2)
        keyboard_l.add(btn3)
        keyboard_l.add(back)
        msg = bot.send_message(call.from_user.id, "🎯 Xabarnoma turini tanlang",
                                           reply_markup=keyboard_l)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data in weekdays:
        if call.data == "Monday":
            bot.answer_callback_query(call.id, "Dushanba kuni belgilandi")
        if call.data == "Tuesday":
            bot.answer_callback_query(call.id, "Seshanba kuni belgilandi")
        if call.data == "Wednesday":
            bot.answer_callback_query(call.id, "Chorshanba kuni belgilandi")
        if call.data == "Thursday":
            bot.answer_callback_query(call.id, "Payshanba kuni belgilandi")
        if call.data == "Friday":
            bot.answer_callback_query(call.id, "Juma kuni belgilandi")
        if call.data == "Saturday":
            bot.answer_callback_query(call.id, "Shanba kuni belgilandi")
        if call.data == "Sunday":
            bot.answer_callback_query(call.id, "Yakshanba kuni belgilandi")            
                                                                

        try:
            session = Session()
            days = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first()
            new_day = days.day
            if new_day is None:
                up_id = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first().id
                session.query(Rejim).filter(Rejim.id == up_id).update({Rejim.day: call.data}, synchronize_session=False)
            
            else:
                new_day = new_day + ' ' + call.data
                up_id = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first().id
                session.query(Rejim).filter(Rejim.id == up_id).update({Rejim.day: new_day}, synchronize_session=False)
                
                
            session.commit()
            session.close()

        except Exception as e:
            bot.send_message(config.admin_id, e)

    elif call.data == "next":
        session = Session()
        days = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first()
        day = days.day
        need_day = day.split()
        kunlar=""

        for i in need_day:
            if i == "Monday":
                kunlar = kunlar+"Dushanba "
            if i == "Tuesday":
                kunlar = kunlar+"Seshanba "
            if i == "Wednesday":
                kunlar = kunlar+"Chorshanba "
            if i == "Thursday":
                kunlar = kunlar+"Payshanba "
            if i == "Friday":
                kunlar = kunlar+"Juma "
            if i == "Saturday":
                kunlar = kunlar+"Shanba "
            if i == "Sunday":
                kunlar = kunlar+"Yakshanba "
            else:
                kunlar = kunlar+""


        keyboard_l = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("✅ Ha, vaqtni belgilash", callback_data="yes_time")
        btn2 = types.InlineKeyboardButton("🙅‍♂️ Yo\'q, qayta tanlash", callback_data="back_day")
        keyboard_l.add(btn1)
        keyboard_l.add(btn2)
        bot.send_message(chat_id, "<b>" + kunlar + "</b>" + "\n\nYuqoridagi kunlarga xabarnoma o'rnatmoqchimisiz?",
                             parse_mode="html", reply_markup=keyboard_l)
        
        bot.delete_message(call.message.chat.id, call.message.message_id)

        session.close()
        

    elif call.data == "back_day":
        try:
            session = Session()
            up_id = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first().id
            session.query(Rejim).filter(Rejim.id == up_id).update({Rejim.day: ""}, synchronize_session=False)
            # session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).update(
            #         {Rejim.day: ""}, synchronize_session=False)
            session.commit()
            session.close()

            keyboard_l = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Dushanba", callback_data="Monday")
            btn2 = types.InlineKeyboardButton("Seshanba", callback_data="Tuesday")
            btn3 = types.InlineKeyboardButton("Chorshanba", callback_data="Wednesday")
            btn4 = types.InlineKeyboardButton("Payshanba", callback_data="Thursday")
            btn5 = types.InlineKeyboardButton("Juma", callback_data="Friday")
            btn6 = types.InlineKeyboardButton("Shanba", callback_data="Saturday")
            btn7 = types.InlineKeyboardButton("Yakshanba", callback_data="Sunday")
            btn8 = types.InlineKeyboardButton("🔜Keyingi bosqich", callback_data="next")
            back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
            keyboard_l.add(btn1, btn2)
            keyboard_l.add(btn3, btn4)
            keyboard_l.add(btn5, btn6, btn7)
            keyboard_l.add(back, btn8)
            msg = bot.send_message(chat_id,
                                   "Xabarnomani jo\'natish kerak bo\'lgan hafta kunini belgilang.",
                                   parse_mode='html', reply_markup=keyboard_l)
            bot.answer_callback_query(call.id, "Endi xabarnomani jo\'natish kunini belgilang")

        except Exception as e:
            bot.send_message(config.admin_id, e)

    elif call.data == "yes_time":
        bot.answer_callback_query(call.id, "Endi xabarnomani jo\'natish vaqtini belgilang")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('🔙Ortga')
        msg = bot.send_message(chat_id,
                               "🕙 Xabarnomani jo\'natish kerak bo\'lgan vaqtni namunadagi ko\'rinishda yuboring\n\n<b>✅ Namuna: </b>16:00",
                               parse_mode='html',reply_markup=markup)
        bot.register_next_step_handler(msg, data_time_step)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "yes_text":
        bot.answer_callback_query(call.id, "Endi xabarnoma uchun matnni yuboring")
        msg = bot.send_message(chat_id,
                               "🎯 Xabarnomada ko'rsatilishi zarur bo\'lgan xabar matnini yuboring.",
                               parse_mode='html')
        bot.register_next_step_handler(msg, data_text_step)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "save":
        session = Session()
        days = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first()
        need_str = days.day
        need = need_str.split(" ")
        for j in need:
            second = Second_db()
            second.user_id = days.user_id
            second.group_id = days.group_id
            second.day = j
            second.days_id = days.id
            second.time = days.time
            second.text = days.text
            second.finish = 0
            session.add(second)


        up_id = session.query(Rejim).filter(Rejim.user_id == chat_id).filter(Rejim.finish == 0).order_by(Rejim.id.desc()).first().id
        session.query(Rejim).filter(Rejim.id == up_id).update({Rejim.finish: 1}, synchronize_session=False)            
        

        session.commit()
        session.close()
        bot.answer_callback_query(call.id, "🟢 Xabarnoma tartibi o\'rnatildi")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    

    if (call.data)[0:3] == "del":
        try:
            
            bot.answer_callback_query(call.id,"O\'chirildi")
            del_id = int((call.data)[3:])
            session = Session()
            x = session.query(Rejim).filter(Rejim.id == del_id).one()
            session.delete(x)
            session.commit()
            session.close()
            bot.send_message(chat_id,"Tanlangan xabarnoma o\'chirildi")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            bot.send_message(config.admin_id, e)


@bot.message_handler(commands=['start','help','soat'])
def phone(message):
    if(message.text == "/start"):
        _count = session.query(User).filter(User.user_id == message.chat.id).count()

        if (_count == 0):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id, "Iltimos botdan to\'liq foydalanish uchun telefon raqamingizni yuboring",
                             reply_markup=keyboard)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('📣 Yangi xabarnomani qo\'shish')
            markup.row('🔕 O\'rnatilgan xabarnomani o\'chirish')

            bot.send_message(message.chat.id, "<i>Men </i>Groot<i>man 🌱</i>",
                                                reply_markup=markup, parse_mode="html")
    if(message.text == "/help"):
                         
        text = "🌱<i> Men <b>Groot</b>man,</i>\n" \
               "<b>Men sizga guruh yoki kanalga xabarnomalar o\'rnatishda yordam beraman 🕙⏰</b>\n" \
               "\n🔸<i>Mendan foydalanish uchun quyidagi ketma-ketlikni amalga oshiring.</i>\n" \
               "1️⃣ Meni kanal(guruhingizga) qo'shib admin huquqini bering.\n" \
               "2️⃣ So\'ng mendan kanalingizda foydalanmoqchi bo\'lsangiz kanalingizdan biror xabarni menga yo\'naltiring,\n" \
               "2️⃣ Guruhingizda foydalanmoqchi bo\'lsangiz guruhingizda /groot buyrug\'ini yozing.\n\n" \
               "📌 <i>Eslatma: Xabarnomani o\'rnatish uchun siz ham kanal(guruhda) admin bo\'lishingiz kerak!</i>"
        bot.send_message(message.chat.id,text,parse_mode='html')

    if(message.text == "/soat"):
        tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(tz)
        current_time = str(now.strftime("%H:%M"))
        bot.send_message(message.chat.id,current_time)

@bot.message_handler(content_types=['contact', 'text'])
def any_message(message):
    text = message.text
    chat_id = message.chat.id
    if text == "📣 Yangi xabarnomani qo\'shish":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('🔙Ortga')
        bot.send_message(chat_id,
                         "🌱<i> Men <b>Groot</b>man,</i> <b>Birinchi qadam.</b>\n"
                         "1️⃣ Meni guruhingiz yoki kanalingizga admin sifatida qo'shing.\n"
                         "<i>\n📌 To'liq ma'lumot olish uchun /help buyrug'idan foydalaning.</i>",
                         reply_markup=markup, parse_mode="html")

    if text == "🔕 O\'rnatilgan xabarnomani o\'chirish":
        sess = Session()
        delete = sess.query(Rejim).filter(Rejim.user_id == message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        check = 0
        if delete is not None:
            for i in delete:
                
                if i.group_name is not None and i.time is not None and i.id is not None:
                    check=check+1
                    button = types.InlineKeyboardButton(i.group_name + "kanal(guruh)da "+i.time+" da",callback_data="del"+str(i.id))
                    keyboard.add(button)
            if check>0:
                back = types.InlineKeyboardButton("🔙Ortga", callback_data="back")
                keyboard.add(back)
                bot.send_message(chat_id,"O\'chirilishi kerak bo\'lgan xabarnomani tanlang 🎯",reply_markup=keyboard)

            else:
                bot.send_message(chat_id,
                        "Sizda xabarnomalar mavjud emas! /help")                
                            
        else:
            bot.send_message(chat_id,
                        "Sizda xabarnomalar mavjud emas! /help")


    # Sizda xabarnomalar mavjud emas! /help
    if text == "🔙Ortga":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('📣 Yangi xabarnomani qo\'shish')
        markup.row('🔕 O\'rnatilgan xabarnomani o\'chirish')

        bot.send_message(message.chat.id, "<i>Men </i>Groot<i>man 🌱</i>",
                                            reply_markup=markup, parse_mode="html")
    if (message.contact != None):
        try:
            phone_number = str(message.contact.phone_number)
            users = User()
            users.user_id = message.chat.id
            users.first_name = message.chat.first_name
            users.last_name = message.chat.last_name
            users.user_number = phone_number
            session.add(users)
            session.commit()
            session.close()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('📣 Yangi xabarnomani qo\'shish')
            markup.row('🔕 O\'rnatilgan xabarnomani o\'chirish')

            bot.send_message(message.chat.id, "<i>Men </i>Groot<i>man 🌱</i>",
                                                reply_markup=markup, parse_mode="html")

        except Exception as e:
            bot.send_message(config.admin_id, e)


def first_func():
    try:
        tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(tz)
        weekday = now.strftime('%A')
        today_date = str(now.strftime('%d'))
        current_time = str(now.strftime("%H:%M"))
        sana = str(now.strftime("%d.%m.%Y"))
        sessiya = Session()

        result = sessiya.query(Second_db).filter(or_(Second_db.day == today_date, Second_db.day == weekday, Second_db.day == sana)).filter(
            Second_db.time == current_time)

        for natija in result:
            bot.send_message(natija.group_id, natija.text)

        sessiya.commit()
        sessiya.close()

    except Exception as e:
        bot.send_message(config.admin_id, e)


schedule.every().minute.at(':00').do(first_func)
def schedule_checker():
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    bot_polling = threading.Thread(
        target=lambda x=None: bot.polling(none_stop=True))
    schedule1 = threading.Thread(target=schedule_checker)
    schedule1.start()
    bot_polling.start()


""" TODO
1. Bir martalik xabarnoma qo'shish, imkoniyatini qo'shish kerak.
2))))). "Monday kuni belgilandi" english + o'zbekchami bu? Hafta kunlarini ham o'zbekcha
chiqarish kerak.
3.))) Har hafta tugmasini bosgandan so'ng, ortga tugmasini bossa,
bir qadam ortga qaytish kerak, 2 qadam emas!
4.))))) Eski datalar yangilari uchun ham aralashib ketvotti(hafta kunlarini ko'rishda),
bitta guruhga 3-4ta rejalashtirilgan xabar qo'yilgan bo'lsa(hafta kunida) 
eskilarini hafta kunini ham chiqarib bervotti, oyda bir martalik xabar uchun ham 
oldingilarini hisoblab ortig'i bilan xabarlar yozilyabdi.
5.)))))) Boshlab qo'yib tugatmasdan qaytib ketsa boshlangan qadamlarni ham saqlab qo'yvotti,
6.)))) Bo'sh datalar ham bazaga saqlanibdi, 
7.))))) Delete itemlarni ko'rishda error bor, 
------
  File "bot.py", line 463, in any_message
    button = types.InlineKeyboardButton(i.group_name + "kanal(guruh)da "+i.time+" da",callback_data="del"+str(i.id))
  TypeError: Can't convert 'NoneType' object to str implicitly
------ delete ichidagi item bo'sh kelgan qaysi biridir.
8. Har oyning 31 sanasida avto xabar belgilasa bo'ladimi? 
Yo'q, nega? sababi har oyda ham 31 kun mavjud emas. bu holatlar o'ylanmagan.
9.)))) Vaqtni kiritishda orqaga qaytish tugmasi ishlamayabdi. Event handler qo'yish kerak tugmaga.
10.))))) "Har oyda" tugmasini bosgandan keyn int kutvotti boshqa narsa jo`natvorsa bot uxladi :). 
))try except va orqaga tugmasini qo'yish kerak.
11.))))) Aniq vaqtda xabar jo'natilmayabdi, sekundlarda kechikish bor,
sababi every(1).minute qo`yilgan bu misol uchun 11:11:34 da hisoblashni boshlasa,
keyingi minutda ham 34s o`tib run bo`ladi shuni hisobiga 34 sekun kechikish bo`votti.
12.)) Kanal uchun deyarli tekshirmadim, to'liq tekshirib chiqing. 2ta kanal uchun 2ta odam uchun va hk.
"""