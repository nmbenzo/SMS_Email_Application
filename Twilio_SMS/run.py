from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from Twilio_SMS.auth_token import SECRET_KEY
import Twilio_SMS.phone_num_and_response as responses
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


def set_session_response():
    # Get message response from user
    counter = session.get('counter', 0)
    counter += 1

    return counter


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

    menu_resp = responses.sms_responses()

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
    elif ('appointment' in inbound_message) or ('advisor' in inbound_message):
        resp.message(menu_resp['appt'])
        logger.info(f'{resp}')
        return str(resp)
    elif ('when' in inbound_message) or ('ready' in inbound_message):
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
    elif ('workshop' in inbound_message) and ('opt' in inbound_message):
        resp.message(menu_resp['workshop'])
        logger.info(f'{resp}')
        return str(resp)
    elif ('workshop' in inbound_message):
        resp.message(menu_resp['workshop'])
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
    elif ('travel' in inbound_message) or ('cpt' in inbound_message) \
        or ('letter' in inbound_message) or ('rcl' in inbound_message) \
        or ('i20' in inbound_message) or ('i-20' in inbound_message) \
        or ('reduced course load' in inbound_message):
        resp.message(menu_resp['isss_request'])
        resp.message(menu_resp['disclaimer'])
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

