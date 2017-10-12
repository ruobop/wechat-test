# Test access_token_handler
#-*-coding:utf-8 -*-

import access_token_handler

print access_token_handler.check_expire()
print access_token_handler.get_access_token()

if access_token_handler.check_expire():
    print access_token_handler.get_access_token()
else:
    print 'Not expire yet!'
