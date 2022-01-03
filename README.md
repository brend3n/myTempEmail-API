

# temp_mail_api

A simple API for interfacing with https://mytemp.email/.

## Features

- Fetch new temporary mailbox
- Pop messages from the inbox
-- Read message and remove it from the inbox.

## Installation

temp_mail_api requires Selenium and BS4 to work properly.
Install the dependencies by cloneing the repo.

## Use

Getting an email address
```python
from temp_mail_api import TempMail
mail = TempMail()
email = mail.get_email_address()
```

Retrieve email from inbox
```python
from temp_mail_api import TempMail
mail = TempMail()
email = mail.get_email_address()
message = mail.get_message()
```



Pop message from inbox
```python
from temp_mail_api import TempMail
mail = TempMail()
mail.delete_message()
```
