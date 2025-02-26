# lament
JSON to HTML conversion of Facebook Messenger files

Since 2016, Facebook Messenger has allowed the option for end-to-end encrypted messages, and in 2023, they were established as the default.

This has caused some issues with people exporting Messenger data for archival or viewing purposes. It is a lot quicker to search for information when the data is local, and it is better practice to do so.

Encrypted Facebook Messenger data can be downloaded by selecting "Privacy & safety" on the Facebook menu, then "End-to-end encrypted chats", then "Message storage", and finally "Download secure storage data".

When the file is ready, it will provided as a zip file that contains various binaries in a "media" directory and well-formatted JSON files for each message chat for current Friends.

Despite the formatting, JSON files are less than optimal for humans to read. The following Python script makes use of pandas, json, sys, and datetime modules. Simply copy it into your messages directory, where all the JSON files are located and run:

$ python3 lament.py <username>.json

It will then output a formatted HTML table that can be opened by a browser of your preference. The table includes a human-readable date (rather than the UNIX timestamp), the sender, the message, reactions, and a reference to any media.

The format and logic of the Python script are simple enough that it can be easily extended to other JSON data from Messenger and can be adapted to other JSON data files.
