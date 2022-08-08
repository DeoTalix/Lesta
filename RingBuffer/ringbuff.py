#!RingBuffer/venv/bin/python
import sys
if sys.version.startswith("2.7") != True:
    raise Exception(
        "This file has no support for python version ({}). Supported version is 2.7 only."
        .format(sys.version))

from collections import deque


class MethodNotImplemented(Exception):
    def __init__(self, *args):
        super(NotImplemented, self).__init__("This method is not implemented yet!")


class RingBuffIsEmpty(Exception):
    def __init__(self, *args):
        super(RingBuffIsEmpty, self).__init__("RingBuffer is empty!")


class RingBuffOverflow(Exception):
    def __init__(self, *args):
        super(RingBuffOverflow, self).__init__("RingBuffer is full!")


class RingBuffInvalidMaxsize(Exception):
    def __init__(self, message, *args):
        message = "Invalid maxsize for RingBuff. " + message
        super(RingBuffInvalidMaxsize, self).__init__(message, *args)


class RingBuffTemplate(object):
    __slots__ = ("_maxsize", "_size", "_overwritable", "_resolve_overflow")

    def __init__(self, maxsize, overwritable=False):
        self._maxsize = self._check_maxsize(maxsize)
        self._size = 0
        self._overwritable = bool(overwritable)
        if self._overwritable == True:
            self._resolve_overflow = self.get
        else:
            self._resolve_overflow = self._raise_overflow

    def __iter__(self):
        "Iterate through buffer and get values until it is empty"
        while self.isempty == False:
            yield self.get()

    def __str__(self):
        return "[{}]".format(", ".join(map(repr, self._q)))

    def __repr__(self):
        return "RingBuff({})".format(self.__str__())

    def put(self, value):
        """
        Checks if buffer is full.
        If True:
            In case is overwritable:
            - overwrites oldest value
            - updates head and tail indexes.
            Else:
            - raises RingBuffOverflow exception.
        Else:
        - puts values in the buffer.
        - updates tail and size indexes.
        """
        if self.isfull:
            self._resolve_overflow()
    
    def _resolve_overflow(self, *args):
        """
        Method is replaced on instance initialization.
        Replacement depends on whether ring buffer is 
        overwritable or not.
        """
        raise MethodNotImplemented()

    def _raise_overflow(self):
        raise RingBuffOverflow()

    def get(self):
        """
        Checks if buffer is empty.
        If True:
        - raises RingBuffIsEmpty exception.
        Else:
        - gets next value from the buffer.
        - updates head and size indexes.
        - returns value.
        """
        if self.isempty:
            raise RingBuffIsEmpty()

    def _check_maxsize(self, maxsize):
        """
        Checks if provided maxsize is valid.
        If True:
        - returns maxsize
        Else:
        - raise exception
        """
        try:
            maxsize = int(maxsize)
        except ValueError:
            raise RingBuffInvalidMaxsize("Can't be converted to integer.")

        if maxsize < 1:
            raise RingBuffInvalidMaxsize("Must be >= 1.")

        return maxsize

    @property
    def state(self):
        return {
            "size": self._size, 
            "maxsize": self._maxsize,
            "overwritable": self._overwritable
            }

    @property
    def isempty(self):
        return self._size <= 0

    @property
    def isfull(self):
        return self._size >= self._maxsize


class RingBuffQueue(RingBuffTemplate):
    __slots__ = RingBuffTemplate.__slots__ + ("_q", )

    def __init__(self, maxsize, overwritable=False):
        super(RingBuffQueue, self).__init__(maxsize, overwritable)
        self._q = deque()

    def put(self, value):
        super(RingBuffQueue, self).put(value)
        self._q.append(value)

    def get(self):
        super(RingBuffQueue, self).get()
        return self._q.popleft()

    @property
    def isempty(self):
        return len(self._q) == 0

    @property
    def isfull(self):
        return len(self._q) == self._maxsize


class RingBuffList(RingBuffTemplate):
    __slots__ = RingBuffTemplate.__slots__ + ("_head", "_tail", "_q")

    def __init__(self, maxsize, overwritable=False):
        super(RingBuffList, self).__init__(maxsize, overwritable)
        self._q = [None] * self._maxsize
        self._head = 0
        self._tail = 0

    def put(self, value):
        super(RingBuffList, self).put(value)
        self._q[self._tail] = value
        self._tail = (self._tail + 1) % self._maxsize
        self._size += 1

    def get(self):
        super(RingBuffList, self).get()
        value = self._q[self._head]
        self._head = (self._head + 1) % self._maxsize
        self._size -= 1
        return value

    @property
    def state(self):
        st = super(RingBuffList, self).state
        st.update({
            "head": self._head,
            "tail": self._tail,
        })
        return st

