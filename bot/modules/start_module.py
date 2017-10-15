from .main_module import *


@message_scenario.command_handler("start", start="вернуться в главное меню")
@message_scenario.message_handler("start")
def start_message(bot, user, update):
    from bot.models import Question, OrderType
    message = Question.objects.get(translate='start')
    types = OrderType.objects.values_list('name', flat=True)
    model_message = generate_message(message=message,
                                     buttons_reply_makrup=types)
    user.push_context(state='check_order_type_view')
    bot.respond(user, model_message)


@message_scenario.message_handler("check_order_type_view")
def check_start_view(bot, user, update):
    from bot.models import OrderType, Order
    try:
        type = OrderType.objects.get(name=update.text)
    except:
        model_message = generate_message(message='dont_know')
        bot.respond(user, model_message)
        return

    order, _ = Order.objects.get_or_create(user=user, type=type, sent=False)
    message = order.check_order_status()
    message_model = generate_message(message)
    user.push_context(state='order_filling', order=order.id,
                      question=message.id)
    bot.respond(user, message_model)


@message_scenario.message_handler("order_filling")
def order_filling(bot, user, update):
    from bot.models import Order, Question

    order_id = user.get_context('order')
    question = Question.objects.get(id=user.get_context('question'))

    order = Order.objects.get(id=order_id)
    if question.check_response(update.text):
        order.set_property(question, update.text)
    else:
        send_dont_know_message()
        return
    message = order.check_order_status()
    if None:
        send_final_message()
        return

    message_model = generate_message(message)
    user.push_context(state='order_filling', order=order.id)
    bot.respond(user, message_model)


def send_final_message():
    pass


def send_dont_know_message():
    pass


# try:
#     user_company = UserCompany.objects.filter(user=user, authorized=True)
#     if user_company:
#         message_type = "start_message_company"
#
# except:
#     pass
#
# find_resp = check_response(message_type, update.text)
# if find_resp:
#     if find_resp == 'my_bonus':
#         from bot.modules.bonus_list_module import favorite_bonus
#
#         favorite_bonus(bot, user, update)
#     elif find_resp == 'repay_bonus':
#         messages = generate_repay_bonus_messages(user)
#         for message in messages:
#             bot.respond(user, message)
#         user.push_context(state="repay_bonus")
#         return
#
# else:
#     from bot.modules.user_bonus_module import add_user_bonus
#     add_user_bonus(bot, user, update)


def generate_repay_bonus_messages(user):
    mesages = [generate_message('repay_bonus')]
    return mesages


@message_scenario.message_handler("default_message")
def default_message(bot, user, update):
    find_resp = check_response("default_message", update.text)
    if find_resp:
        if find_resp == 'start':
            start_state(bot, user, update)
