import ast
import os
import socket
import string
import sys
import time
import threading

#  - We set the and store the triggers in a Database from Transaction server
#  - Get quotes of each trigger about to expire
#  - Compare quotes with trigger amount
#  - Go through with the transaction if the price matches
#
# Check every couple seconds:
# 1. Connect to database
# 2. select user records
# 3. Connect to the quoteServer
# 4. Get the current quotes
# 5. Compare trigger amount with quote amount
# 6. If the trigger is BUY_TRIGGER
#     quote amount less than or equal to trigger_amount
#     update user account in DB with the new stock
#     Delete the trigger record
#     update time stamp
#    If the trigger is SELL_TRIGGER
#     if quote amount is greater than or equal to trigger amount
#         update user funds in DB with funds + quote amount
#         Delete the trigger record
#         update timestamp