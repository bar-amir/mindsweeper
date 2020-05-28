Readers
=======================================

.. automodule:: mindsweeper.readers
   :members:
   :undoc-members:
   :show-inheritance:

Adding readers (supporting other file formats)
---------------------------------------
Reader receive a reader-function, which supports the reading of a single file format. To support other formats, new reader-functions should be implemented:

* Write a reader-function under the name of the file format it reads (the file's format is identified by the file's extension). Save the reader function in a file called ``reader_<file-format>`` and put it under the readers module directory.
* The reader-function is actually a generator. It receives a path to a file and yields every message it reads in a format the server supports.
* The first yielded message has to be a message of type 'user'.
* File formats are identified by the file's extension, so for example, a reader-function that supports the reading of a Mind file, would accept files that ends with ``.mind.*`` (it might support different types of compression or encoding). The function would be called ``mind`` and be saved in a file called ``reader_mind.py``.
* Mind files are supported by default, therefor the framework also supports reading files that use Protocol Buffers. Put your ``.proto`` file under `readers/proto` and make sure to run ``scripts/compile-protos.sh``. Decorate your function with ``@proto_reader`` and the compiled module will be imported automatically. For an example, look at ``reader_mind.py``.