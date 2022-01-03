
# temp_mail_api

A simple API for interfacing with https://mytemp.email/.

## Features

- Fetch new temporary mailbox
- Pop messages from the inbox
-- Read message and remove it from the inbox.

## Installation

temp_mail_api requires Selenium and BS4 to work properly.
Install the dependencies by clonging the repo.

## Use

_Getting an email address_

`import temp_mail_api as tmp`
`driver = tmp.start()`
`email_url, inbox,hash = tmp.get_email_address(driver)`

_Retrieve email from inbox._
`import temp_mail_api as tmp`
`driver = tmp.start()`

`email_url, inbox,hash =` `tmp.get_email_address(driver)`

`message = tmp.get_message(inbox,hash)`

_Pop message from inbox_
`import temp_mail_api as tmp`
`driver = tmp.start()`
`tmp.delete_message(driver)`

