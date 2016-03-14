# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab
"""
pipe2py.modules.pipedateformat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides functions for formatting timetuples.

A wide range of format specifiers can be used to create the output text string.
The specifiers all begin with a percent sign followed by a single character.

Here are a few specifiers and how they each format the date/time February 12th,
2008 at 8:45 P.M.

    Specifier                   Formatted Date
    -------------------------   -------------------------------
    %m-%d-%Y                    02-12-2008
    %A, %b %d, %y at %I:%M %p   Tuesday, Feb 12, 08 at 08:45 PM
    %D 	                        02/12/08
    %R 	                        20:45
    %B 	                        February

Examples:
    basic usage::

        >>> from pipe2py.modules.pipedateformat import pipe
        >>> from datetime import date
        >>> pipe({'tuple': date(2015, 5, 4).timetuple()}).next()['content']
        '05/04/2015 00:00:00'

Attributes:
    OPTS (dict): The default pipe options
    DEFAULTS (dict): The default parser options
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from time import strftime
from . import processor
from pipe2py.lib.log import Logger

OPTS = {}
DEFAULTS = {'format': '%m/%d/%Y %H:%M:%S', 'field': 'tuple'}
logger = Logger(__name__).logger


def parser(timetuple, objconf, skip, **kwargs):
    """ Obtains the user input

    Args:
        timetuple (obj): datime.timetuple
        objconf (obj): The pipe configuration (an Objectify instance)
        skip (bool): Don't parse the content

    Returns:
        Tuple(dict, bool): Tuple of (the formatted date, skip)

    Examples:
        >>> from datetime import date
        >>> from pipe2py.lib.utils import Objectify
        >>>
        >>> timetuple = date(2015, 5, 4).timetuple()
        >>> objconf = Objectify({'format': '%m/%d/%Y'})
        >>> parser(timetuple, objconf, False)[0]
        '05/04/2015'
    """
    parsed = kwargs['feed'] if skip else strftime(objconf.format, timetuple)
    return parsed, skip


@processor(DEFAULTS, async=True, **OPTS)
def asyncPipe(*args, **kwargs):
    """A processor module that asynchronously formats a timetuple.

    Args:
        item (dict): The entry to process
        kwargs (dict): The keyword arguments passed to the wrapper

    Kwargs:
        conf (dict): The pipe configuration. May contain the keys 'format',
            'assign', or 'field'.

            format (str): Format string passed to time.strftime (default:
                '%m/%d/%Y %H:%M:%S', i.e., '02/12/2008 20:45:00')

            assign (str): Attribute to assign parsed content (default: content)
            field (str): Item attribute from which to obtain the string to be
                formatted (default: 'tuple')

    Returns:
        Deferred: twisted.internet.defer.Deferred item with formatted date

    Examples:
        >>> from datetime import date
        >>> from twisted.internet.task import react
        >>> from pipe2py.twisted import utils as tu
        >>>
        >>> def run(reactor):
        ...     callback = lambda x: print(x.next()['content'])
        ...     item = {'tuple': date(2015, 5, 4).timetuple()}
        ...     d = asyncPipe(item)
        ...     return d.addCallbacks(callback, logger.error)
        >>>
        >>> try:
        ...     react(run, _reactor=tu.FakeReactor())
        ... except SystemExit:
        ...     pass
        ...
        05/04/2015 00:00:00
    """
    return parser(*args, **kwargs)


@processor(DEFAULTS, **OPTS)
def pipe(*args, **kwargs):
    """A processor module that formats a timetuple.

    Args:
        item (dict): The entry to process
        kwargs (dict): The keyword arguments passed to the wrapper

    Kwargs:
        conf (dict): The pipe configuration. May contain the keys 'format',
            'assign', or 'field'.

            format (str): Format string passed to time.strftime (default:
                '%m/%d/%Y %H:%M:%S', i.e., '02/12/2008 20:45:00')

            assign (str): Attribute to assign parsed content (default: content)
            field (str): Item attribute from which to obtain the string to be
                formatted (default: 'tuple')

    Returns:
        dict: an item with formatted date string

    Examples:
        >>> from datetime import date
        >>> item = {'tuple': date(2015, 5, 4).timetuple()}
        >>> pipe(item).next()['content']
        '05/04/2015 00:00:00'
        >>> pipe(item, conf={'format': '%Y'}).next()['content']
        '2015'
    """
    return parser(*args, **kwargs)

