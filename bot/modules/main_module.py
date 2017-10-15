from .modules import Module
from .modules.scenarios import *
from .modules.utility import *

callback_query_scenario = CallbackQueryScenario()
message_scenario = MessageScenario()
main_module = Module("main_module", "start",
                     scenarios=[message_scenario, callback_query_scenario])

from bot.modules import start_module
# from bot.modules import repay_module
# from bot.modules import bonus_list_module
# from bot.modules import company_module
# from bot.modules import user_bonus_module
# from bot.modules import feedback_module