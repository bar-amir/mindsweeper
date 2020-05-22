Client
======

Clients are responsible to convert files to messages readable by the server, and upload them to it. Messages are either saved directly to the database, or goes through parsers first (more on messages).

Readers
-------
To read from the data file, the client uses a reader. Mindsweeper supports reading .mind files.

Adding readers
--------------
Adding your own readers is easy. Drop your 'reader_<file-extension>.py' in the readers file. Mindsweeper will look for it when it would be asked to upload a '.<file-extension>.*' file. The reader file should contain a function with the signature <file-extension>(path), where path is the path to the file.

Since .mind files uses protocol buffers, dealing with other formats doing so is also made easy. Drop your protobuf file in readers/protos/<file-extension>.proto. Run the script run-pipeline.sh and it will compile the necessary modules for you (or you can do it by yourself, but notice the naming conventions).

A reader should be a generator for messages. The first yield is always a user message. All messages should have the status 'uploaded'.