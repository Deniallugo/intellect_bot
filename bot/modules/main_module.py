from .modules import Module
from .modules.scenarios import *
from .modules.utility import *

callback_query_scenario = CallbackQueryScenario()
message_scenario = MessageScenario()
main_module = Module("main_module", "start",
                     scenarios=[message_scenario, callback_query_scenario])

__all__ = ["start_module"]

