'''
Logger
======

Configure example
-----------------

Django < 1.3

.. code-block:: python

    import os
    import logging
    from django_logger import LoggerClass

    logging.setLoggerClass(LoggerClass(
        file_suffix = '.log',
        stream_enabled = True,
        default_level = logging.DEBUG,
        files_path = os.path.abspath(os.path.join(PROJECT_PATH, 'var', 'log')),
    ))

Logging example
---------------

.. code-block:: python

    import logging      # this is python logging module (standard library).

    logger = logging.getLogger('feeder.myspace')
    logger.info('Hello, %s.', 'World')

    try:
        do_something()
    except:
        logger.exception('something goes wrong')      # log with exception information

'''


import os
import logging

_PYTHON_LOGGER = logging.getLoggerClass()

class BaseLogger(_PYTHON_LOGGER):
    '''
    Base of configured logger class.
    '''
    class Meta:
        files_path = os.getcwd()
        file_suffix = '.log'
        file_encoding = 'utf-8'
        file_enabled = True
        stream_enabled = False

        default_level = logging.DEBUG
        default_message_format = '[%(asctime)s] [%(levelname)s]: %(message)s'
        default_date_format = '%a %b %d %H:%M:%S %Y'

    def __init__(self, name):
        _PYTHON_LOGGER.__init__(self, name)
        _meta = self._meta = self.Meta()

        self.setLevel(_meta.default_level)
        self.formatter = logging.Formatter(_meta.default_message_format, _meta.default_date_format)

        if _meta.file_enabled:
            self.file_path = os.path.join(_meta.files_path, name) +  _meta.file_suffix
            self.file_handler = self.addFileHandler(self.file_path, encoding=_meta.file_encoding)

        if _meta.stream_enabled:
            self.stream_handler = self.addStreamHandler()

    def addFileHandler(self, *args, **kwargs):
        '''
        Add logging.FileHandler(\*args, \*\*kwargs) to logger.
        Returns created handler.
        '''
        handler = logging.FileHandler(*args, **kwargs)
        handler.setLevel(self._meta.default_level)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)
        return handler

    def addStreamHandler(self, *args, **kwargs):
        '''
        Add logging.StreamHandler(\*args, \*\*kwargs) to logger.
        Returns created handler.
        '''
        handler = logging.StreamHandler(*args, **kwargs)
        handler.setLevel(self._meta.default_level)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)
        return handler



def LoggerClass(**kwargs):
    '''
    Return configured logger class.
    '''
    attr = {
        'Meta': type('Meta', (object, BaseLogger.Meta), kwargs)
    }

    from new import classobj
    logger_class=classobj('Logger',(BaseLogger,),attr)
    return logger_class
