from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from Twilio_SMS.auth_token import SECRET_KEY
from Twilio_SMS.message_lists import ISSS_list_dict
from textblob import TextBlob
import logging


logging.basicConfig(format='%(asctime)s %(levelname)-8s '
    '[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt')

logger = logging.getLogger('Message Logger')

SECRET_KEY = SECRET_KEY
app = Flask(__name__)
app.config.from_object(__name__)


def get_phone_number():
    """
    Function that references a dictionary of available names (key)
    and phone numbers (value) which is passed to the sms_responses() function
    for custom greetings for each user.
    ::returns dict key as var name
    """
    from_number = request.values.get('From')

    if from_number in ISSS_list_dict:
        name = ISSS_list_dict[from_number]
    else:
        name = "Friend"

    return name


def set_session_response():
    # Get message response from user
    counter = session.get('counter', 0)
    counter += 1

    return counter


def sms_responses():
    """
    Function that returns a dictionary of available sms responses to be used
    by the send_sms_response() function
    """
    menu = f" Hello, {get_phone_number()}! This is ISSS's chat messenger " \
        f"service. You can text questions or chat with this number to help " \
        f"you find answers to questions common among international students. " \
        f"\n\nTry typing ''make an appointment'' or ''register for a workshop.''" \
        f" You can also ask questions about OPT and CPT." \
        f"\n\n*Your response is not case-sensitive"

    appt = f"Sure thing, {get_phone_number()}! Click here to make an " \
        f"appointment with your advisor: https://isss.checkappointments.com/"
    isss_request = f"Hi, {get_phone_number()}! Please click here to make an " \
        f"online request: " \
        f"https://form.jotform.com/USFISSS/isss-request-form"
    disclaimer = "Document uploads may be required to complete your request."
    opt = f"Many students have question about OPT, {get_phone_number()}! Not " \
        f"to worry, please click here to learn more about OPT: " \
        f"https://myusf.usfca.edu/isss/students/f-1/employment/opt "
    cpt = f"So you'd like to learn more about CPT, {get_phone_number()}, " \
        f"correct? Great! Please click here to learn about CPT: " \
        f"https://myusf.usfca.edu/isss/students/f-1/employment/cpt"
    isss = f'Hello, {get_phone_number()}! Thank you for inquiring more about ' \
        f'ISSS. To get in touch with ISSS please contact: isss@usfca.edu, ' \
        f'call us at: 415-422-2654, or visit our office on Main Campus ' \
        f'- UC 5th floor. Our normal business hours are Monday-Friday from' \
        f' 9am-5pm. \nTo schedule an appointment with ' \
        f'your advisor click: https://isss.checkappointments.com/'
    loa_wd = f"Good day, {get_phone_number()}. You've indicated that you would " \
        f"like information about taking a leave of absence or withdrawing " \
        f"from USF. Click here to learn what you will need to do: " \
        f"https://myusf.usfca.edu/isss/students/f-1/leave-of-absence-withdrawal"
    call = '4154222654'
    email = 'isss@usfca.edu'

    first_bad_resp = f'{get_phone_number()}, we did not understand your ' \
        f'response. Please choose one of the menu options from above or type ' \
        f'"menu" to see the Main Menu again. If you have already found your ' \
        f'answer, please ignore this message.'
    second_bad_resp = f'Hello, {get_phone_number()}, we still did not understand '\
        f'your message. Try typing "appt" to make an appointment or type "menu"' \
        f' to see the main menu again. You can also type "website" to link to ' \
        f"ISSS's main website page."
    third_bad_resp = f"{get_phone_number()}, we're sorry we are not able to " \
        f"help you with your request. We'll send you back to the main menu now..."
    website = 'https://myusf.usfca.edu/isss'
    contact_isss = f'Hi {get_phone_number()}, you can get a quicker answer if ' \
        f'you call or email ISSS. ' \
        f'\n\nCall: 415-422-2654' \
        f'\nEmail: isss@usfca.edu'
    transfer = f'{get_phone_number()}, if you would like to transfer to ' \
        f'another university you will need to ask ISSS to transfer your SEVIS ' \
        f'record. Please request a transfer out here: ' \
        f'\nhttps://form.jotform.com/USFISSS/isss-request-form'
    sentient_resp1 = f"That's great to hear, {get_phone_number()}! " \
        f"Is there anything else ISSS can help you with today?"
    sentient_resp2 = f"Oh no - we're sorry to hear that {get_phone_number()}! " \
        f"Let's bring you back to the main menu so we can better assist you..."
    sentient_resp3 = f"Thanks for letting us know about that, " \
        f"{get_phone_number()}. You can access ISSS services or get information " \
        f"with by communicating with this chat service. " \
        f'\n\nTry asking a question about OPT or scheduling an appointment. ' \
        f'You can also return to the main ISSS menu by typing "menu". '

    return \
        {
            'menu': menu,
            'appt': appt,
            'isss_request': isss_request,
            'disclaimer': disclaimer,
            'opt': opt,
            'cpt': cpt,
            'isss': isss,
            'loa_wd': loa_wd,
            'call': call,
            'email': email,
            'transfer': transfer,
            'first_bad_resp': first_bad_resp,
            'second_bad_resp': second_bad_resp,
            'third_bad_resp': third_bad_resp,
            'website': website,
            'sentient_resp1': sentient_resp1,
            'sentient_resp2': sentient_resp2,
            'sentient_resp3': sentient_resp3,
            'contact_isss': contact_isss
        }


# keywords for inbound messages to check
isss_general_request = 'travel' or 'cpt' or 'letter' or 'signature' or 'rcl' \
                        or 'reduced course load' or 'opt' or \
                       'STEM' or 'i20' or 'I-20'


@app.route('/sms', methods=['GET', 'POST'])
def send_sms_response():
    """
    Responds to an incoming message with a custom SMS depending on the number of
    the inbound message, the inbound message value as a string, and the
    session counter (cookie).
    ::returns sms response as a string
    """
    inbound_message = request.form.get('Body').lower().strip()
    logger.info(inbound_message)

    # Save the new counter value in the session
    cookie = session['counter'] = set_session_response()

    menu_resp = sms_responses()

    # Use the body of the user's text message to create a new TextBlob object.
    text_blob = TextBlob(inbound_message)

    resp = MessagingResponse()

    # Get sentiment of the user's statement.
    # >>> sentiment = text_blob.sentiment
    # >>> sentiment.polarity
    # 0.0
    sentiment = text_blob.sentiment

    if ('hello' in inbound_message) or ('hi' in inbound_message):
        resp.message(menu_resp['menu'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'appointment' in inbound_message:
        resp.message(menu_resp['appt'])
        logger.info(f'{resp}')
        return str(resp)
    elif isss_general_request in inbound_message:
        resp.message(menu_resp['isss_request'])
        resp.message(menu_resp['disclaimer'])
        logger.info(f'{resp}')
        return str(resp)
    elif ('when' in inbound_message) or ('ready' in inbound_message) :
        resp.message(menu_resp['contact_isss'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'transfer' in inbound_message:
        resp.message(menu_resp['transfer'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'call' in inbound_message:
        resp.message(menu_resp['call'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'email' in inbound_message:
        resp.message(menu_resp['email'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'opt' in inbound_message:
        resp.message(menu_resp['opt'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'cpt' in inbound_message:
        resp.message(menu_resp['cpt'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'isss' in inbound_message:
        resp.message(menu_resp['isss'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'website' in inbound_message:
        resp.message(menu_resp['website'])
        logger.info(f'{resp}')
        return str(resp)
    elif 'menu' in inbound_message:
        resp.message(menu_resp['menu'])
        logger.info(f'{resp}')
        return str(resp)
    elif ('leave of absence' in inbound_message) or \
        ('loa' in inbound_message) or \
        ('leave' in inbound_message):
        resp.message(menu_resp['loa_wd'])
        logger.info(f'{resp}')
        return str(resp)

    # If the polarity of the sentiment is greater than zero, the statement is
    # positive.  Highest positivity is 1.0
    elif sentiment.polarity > 0:
        resp.message(menu_resp['sentient_resp1'])
        return str(resp)

    # If the polarity of the sentiment is less than zero, the statement is
    # negative.  Lowest negativity is -1.0.
    elif sentiment.polarity < 0:
        resp.message(menu_resp['sentient_resp2'])
        resp.message(menu_resp['menu'])
        logger.info(f'{resp}')
        return str(resp)

    # If the polarity is 0.0, TextBlob was unable to determine the sentiment
    # of the statement.  In this case, we'll return a neutral response in turn.
    else:
        resp.message(menu_resp['sentient_resp3'])
        return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

