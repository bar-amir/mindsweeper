Parsers
=======================================

.. automodule:: mindsweeper
   :members:

.. automodule:: mindsweeper.parsers
   :members:

Implementing parsers
---------------------------------------
* Adding your own parsers is relatively easy. Implement the logic of your parser inside a function ``parser_name``, that receives a message, parses it and returns the parsed message. Save the function in a file called ``parser_<parser_name>.py``, and place the file in the parsers module directory. The file should also contain a ``msg_types`` set of the message types your parser accepts. If all of this is done correctly, the server will publish these types of received messages to the parser's queue.
* The parser needs to change the message status to 'ready' in order for the output message to be consumed by the saver. You could decide not to do so, but instead change the message type, allowing a message to be passed through a chain of parsers before being saved to the database.

CLI
---------------------------------------

.. click:: mindsweeper.parsers.__main__:main
   :prog: python -m mindsweeper.parsers
   :show-nested: