from general import General, ErrorHandler
from bot_modules import Listener, RoleManager
from broken_picture_phone import BPC
from lockdown import Lockdown
from message_copier import Copier
from roler import Roler
from tools import Tools
from pruner import Pruner

lockdown_cogs = [General, RoleManager,
                 Listener, BPC, Copier, Roler, Tools, Pruner]

other_cogs = [ErrorHandler, Lockdown]
