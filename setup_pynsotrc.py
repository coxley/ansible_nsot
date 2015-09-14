#!/bin/env python2.7

from os.path import expanduser

contents = '''
[pynsot]
url = http://localhost:8990/api
secret_key = qONJrNpTX0_9v7H_LN1JlA0u4gdTs4rRMQklmQF9WF4=
auth_method = auth_token
email = test@example.com
default_site = 1
'''

home = expanduser("~")
with open('%s/.pynsotrc' % home, 'w') as f:
    f.write(contents)
