from flask import Flask, request
from Twilio_SMS.message_lists import ISSS_list_dict


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
    workshop = f"Great to hear you'd like more information about our workshops, " \
        f"{get_phone_number()}. You can learn more or register for a workshop " \
        f"here: \nhttps://isss.checkappointments.com/"
    opt_processing_times_general = 'Generally, it will take USCIS between ' \
        '90-100 days to process OPT applications. Please be sure to plan your ' \
        'employment or travel carefully'
    opt_travel = f'There are very specific guidelines you must be aware of while' \
        f' traveling on OPT, {get_phone_number()}. Please see the ' \
        f'ISSS guidelines for travel while on OPT:' \
        f'\n\nhttps://myusf.usfca.edu/isss/students/f-1/employment/opt/after-mailing-application'
    transfer = f'{get_phone_number()}, if you would like to transfer to ' \
        f'another university you will need to ask ISSS to transfer your SEVIS ' \
        f'record. Please request a transfer out here: ' \
        f'\nhttps://form.jotform.com/USFISSS/isss-request-form'
    sentiment_resp1 = f"That's great to hear, {get_phone_number()}! " \
        f"Is there anything else ISSS can help you with today?"
    sentiment_resp2 = f"Oh no - we're sorry to hear that {get_phone_number()}! " \
        f"Let's bring you back to the main menu so we can better assist you..."
    sentiment_resp3 = f"Thanks for letting us know about that, " \
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
            'opt_processing_time': opt_processing_times_general,
            'opt_travel': opt_travel,
            'website': website,
            'workshop': workshop,
            'sentiment_resp1': sentiment_resp1,
            'sentiment_resp2': sentiment_resp2,
            'sentiment_resp3': sentiment_resp3,
            'contact_isss': contact_isss
        }