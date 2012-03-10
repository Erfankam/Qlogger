#!/usr/bin/python

import sys
import os
import inspect
import traceback
import threading
import re
import string
import time
import datetime

'''
    Idias:
1. add cron like process to class to report live ack proidically
2. add child object to inform them with custom event
3. add self observer for logger class
4. add a mechanism to set permission of logging files of streams
5. add mode to priodically delete of compress log file of pass them to other handlers
6. add localization time and other fields to class
7. add calculation time to base time for accuracy
8. add static method or even class to support global logging 
9. add shared file of other attributes as a global attrs.
10. add ability to accept some external method or field to get other user defined log attributes
11. add exception handling to module and rename module to Qlogger
12. add rotation machanizm to avoid file system overloading
13. add network status to log if it s needed and is not insane.!
14. use defaut values it threr is no proper value for an attribute like: "There is no doc for %ds"      ... has done.
15. add ability to change logFormat by user log string violently.
************************
time qlog format
    Qlogger("$tid %h %f %d %q ... %pid")
'''
'''
To Fix:
    1- user regular expression instead of replace for each statement                        ... has done.
    2- let user use special characters like % and other followers                            ... had done.
    3- Dynamic assinment of calculation functions.                                          ... had done.
    4- fix log name(object) and log type fields in class
    5- add get code detail class or function to attrdict to get attributes.
    6- big and huge empty space or string when use %%dt%d.
    7. Emitting space in regullar expresion substituation                                   ... has done.
'''

attrDict = {}
# --------------------->key -----------> Non static elements list -----------------> rest of static elemet list -----<
# attrDict.__setItem__('group name', [ ['description', 'value', gertter function], r'''reqular expression string'''] )
attrDict.__setitem__('ti'    ,[\
        ['thread id'           , '', None],\
        re.compile(r'''(?<=[^%])%ti(?Lmsux)''')] )

attrDict.__setitem__('pi'    , [\
        ['process id'          , '', None],\
        re.compile(r'''(?<=[^%])%pi(?Lmsux)''')] )

attrDict.__setitem__('dt'    , [\
        ['date time'           , '', None],\
        re.compile(r'''(?<=[^%])%dt(?Lmsux)''')] )

attrDict.__setitem__('ds'    , [\
        ['document string'     , '', None],\
        re.compile(r'''(?<=[^%])%ds(?Lmsux)''')] )

attrDict.__setitem__('fn'    , [\
        ['function name'       , '', None],\
        re.compile(r'''(?<=[^%])%fn(?Lmsux)''')] )

attrDict.__setitem__('cn'    , [\
        ['class name'          , '', None],\
        re.compile(r'''(?<=[^%])%cn(?Lmsux)''')] )

attrDict.__setitem__('mn'    , [\
        ['module name'         , '', None],\
        re.compile(r'''(?<=[^%])%mn(?Lmsux)''')] )

attrDict.__setitem__('fa'    , [\
        ['file address'        , '', None],\
        re.compile(r'''(?<=[^%])%fa(?Lmsux)''')] )

attrDict.__setitem__('ln'    , [\
        ['line number'         , '', None],\
        re.compile(r'''(?<=[^%])%ln(?Lmsux)''')] )

attrDict.__setitem__('pn'    , [\
        ['platform name'       , '', None],\
        re.compile(r'''(?<=[^%])%pn(?Lmsux)''')] )

attrDict.__setitem__('si'    , [\
        ['standard input'      , '', None],\
        re.compile(r'''(?<=[^%])%si(?Lmsux)''')] )

attrDict.__setitem__('so'    , [\
        ['standard output'     , '', None],\
        re.compile(r'''(?<=[^%])%so(?Lmsux)''')] )

attrDict.__setitem__('se'    , [\
        ['standard error'      , '', None],\
        re.compile(r'''(?<=[^%])%se(?Lmsux)''')] )

attrDict.__setitem__('on'    , [\
        ['os name'             , '', None],\
        re.compile(r'''(?<=[^%])%on(?Lmsux)''')] )

attrDict.__setitem__('of'    , [\
        ['os family'           , '', None],\
        re.compile(r'''(?<=[^%])%of(?Lmsux)''')] )

attrDict.__setitem__('oa'    , [\
        ['os architecture'     , '', None],\
        re.compile(r'''(?<=[^%])%oa(?Lmsux)''')] )

attrDict.__setitem__('hn'    , [\
        ['host name'           , '', None],\
        re.compile(r'''(?<=[^%])%hn(?Lmsux)''')] )

attrDict.__setitem__('ov'    , [\
        ['os version'          , '', None],\
        re.compile(r'''(?<=[^%])%ov(?Lmsux)''')] )

attrDict.__setitem__('ul'    , [\
        [ 'user log'           , '', None],\
        re.compile(r'''(?<=[^%])%ul(?Lmsux)''')] )

attrDict.__setitem__('lt'    , [\
        ['log type'            , '', None],\
        re.compile(r'''(?<=[^%])%lt(?Lmsux)''')] )

attrDict.__setitem__('lo'    , [\
        ['log object'          , '', None],\
        re.compile(r'''(?<=[^%])%lo(?Lmsux)''')] )

regexPatern = re.compile(r"""(
                    (?=(?P<ti>.*[^%]%ti))*    # thread id 
                    (?=(?P<pi>.*[^%]%pi))*    # process id 
                    (?=(?P<ul>.*[^%]%ul))*    # process id
                    (?=(?P<dt>.*[^%]%dt))*    # date time
                    (?=(?P<ds>.*[^%]%ds))*    # document string
                    (?=(?P<mn>.*[^%]%mn))*    # method name
                    (?=(?P<fn>.*[^%]%fn))*    # funtion name
                    (?=(?P<cn>.*[^%]%cn))*    # class name
                    (?=(?P<fa>.*[^%]%fa))*    # file address
                    (?=(?P<ln>.*[^%]%ln))*    # line number
                    (?=(?P<pn>.*[^%]%pn))*    # platform name
                    (?=(?P<se>.*[^%]%se))*    # standard error
                    (?=(?P<si>.*[^%]%si))*    # standard input
                    (?=(?P<so>.*[^%]%so))*    # standard output
                    (?=(?P<on>.*[^%]%on))*    # os name
                    (?=(?P<ov>.*[^%]%ov))*    # os version
                    (?=(?P<oa>.*[^%]%oa))*    # os architecture
                    (?=(?P<of>.*[^%]%of))*    # os family
                    (?=(?P<hn>.*[^%]%hn))*    # host name
                    (?=(?P<lt>.*[^%]%lt))*    # log type
                    (?=(?P<lo>.*[^%]%lo))*    # log object
                    (?Lmsux)                # >>> regex options
                )*""", re.DOTALL) 

# Define builtin loglevel for compalibility
loglevelDef = \
    {
        'DEBUG' : 0,
        'ERROR' : 1,
        'OK'    : 2,
        'WARN'  : 3,
        'EXCEPT': 4,
        'QLOG'  : 5,
    }
                                
class EKlogger:
    def __new__(self):
        pass

    def __init__(self, logName = None):
        if not logName:
            logName = "EKlogger__main__" + '<' + str(id(self)) + '>'
        self.__logName = logName
        self.__handler = []

        # level of all handler means total log level self.__level = None
        # means sublog self.__child = {}
        self.__name = None
        self.__counter = 0
        
    def __del__(self):
        pass

    def __str__(self):
        return self.__logName

    def addHandler(self, handler):
        self.__handler.append(handler)

    def addChild(self, logName=None):
        """ Add child logger to main instance with the name of logName.
            if logName not given, logName will generate name with format 
            like this:
                example@logger__child__(0)
        """
        # FIXME
        if not logName:
            logName = self.logName + "__child__" +\
                        '<' + str(self.__child.__len__()) + '>'
        newChild = EKlogger( logName )
        self.__child.__setitem__(logName, newChild)

    def Qlog(self, message=None, argTuple=None, logLevel=None):
        """
        Use under multi perpose log.
        """
        logStack = inspect.stack()[-1]
        for handler in self.__handler:
            handler.log(self.__logName + message, argTuple, logStack, logLevel)
        # delete and destructor the stack avoiding crash
        del logStack

    # FIXME
    def INFO(self, message):
        for handler in self.__handler:
            handler.log("Info: " + self.__logName + ": " + message)

    # FIXME
    def WARN(self, message):
        """
        Use when situation is what exactly you want.
        """
        pass

    # FIXME
    def ERROR(self, message):
        """
        Use when have error in your operation.
        """
        pass

    # FIXME
    def EXCEPT(self, message):
        """
        Use under geting exception.
        """
        pass

    # FIXME
    def OK(self, message):
        """
        Use when situation is what exactly you want.
        """
        pass

    # FIXME
    def DEBUG(self, message):
        """
        Use under debuging level.
        """
        pass
    # FIXME

    def setLogName(self, logName):
        self.__logName = logName
    def setLogLevel(self, logLevel):
        for handler in self.__handlers:
            handler.setLogLevel(logLevel)

class Handler:

    def __new__(self):
        pass

    def __init__(self):
        self.__logLevel = None
        self.__mode = None
        self.__seperator = None
        self.__priority = None
        self.__logFormatter = None
        self.__logSchduler = None

    def setPriority(self, priority):
        self.__priority = priority

    def setLogLevel(self, logLevel):
        self.__logLevel = logLevel

    def setMode(self, mode):
        self.__mode = mode
    # TODO
    def setLogFormatter(self, logFormatter):
        self.__logFormatter = logFormatter
    # TODO
    def setLogFormatter(self, logSchaduler):
        self.__logSchduler = logSchaduler
    
class StreamHandler(Handler):
    pass

class FileHandler(Handler):
    """ global values """
    __HandlerType = "FileHandler"

    """ Shared values among other instances """
    __descr = None
    __nowTime = None
    __elapsedTime = None

    def __new__(*args, **kwargs):
        pass

    def __init__(self, path=None, descr=None, logFormat=None):
        Handler.__init__(self)
        self.__path = path
        self.__descr = descr
        self.__logFormatter = None
        self.__shared = False
        self.__thread = None
        # define max access to this file descriptor
        self.__maxConnection = 1
        # lock for mutual exclusion
        self.__lock = None
        self.__initialize(path, descr, logFormat)
        pass

    def __str__(self):
        pass

    def __del__(self):
        pass

    def __call__(self):
        pass

    def __initialize(self, path, descr, logFormat):
        if self.__shared:
            if not __descr:
                __descr =  open(self.__path, 'w+t')
                self.__descr = __descr
        else:
            self.__descr =  open(self.__path, 'w+t')
        self.__thread = threading.Thread()
        self.__thread.setDaemon(False)
        self.__logFormatter = LogFormatter(logFormat)
        try:
            self.__lock = threading.BoundedSemaphore(self.__maxConnection)
        except:
            try:
                self.__lock = threading.RLock(self.__maxConnection)
            except:
                self.__lock = threading.Lock()

    def log(self, logString, argTuple, logStack, logLevel):
        self.__thread = threading.Thread(
                                group=None,\
                                target=self.__log,\
                                args=(logString, argTuple, logStack, logLevel))
        self.__thread.start()

    def __log(self, logString, argTuple, logStack, logLevel):
        # check log level. If not passed, will return
        # it works even with None
        if logLevel > self.__logLevel:
            return
        if logString:
            self.__logFormatter.setUserLog(logString, argTuple, logStack)
        self.__logFormatter.parseLogFormat()
        self.__lock.acquire()
        self.__descr.write(self.__logFormatter.getParsedFormat())
        self.__descr.flush()
        self.__lock.release()

class HTTPHandler(Handler):
    pass

class SMTPHandler(Handler):
    pass

class EventHandler(Handler):
    pass

class LogFormatter:

    def __new__(*args, **kwargs):
        pass

    def __init__(self, formatString, lsep="\n"):
        self.__formatString = formatString
        self.__parsedFormat = ''
        self.__regexPatern = regexPatern    
        self.__regexObject = None 
        self.__timeFormatter = ''
        self.__attrDict = {}
        self.__logSeperator = lsep
        self.__initialize(formatString)
        self.__userLog = None

    def __str__(self):    
        pass

    def __initialize(self, formatString):
        self.__timeFormatter = TimeFormatter(formatString)
        self.__regexObject = self.__regexPatern.match(self.__formatString)
        for _attrKey, _attrVal in self.__regexObject.groupdict().items():
            if _attrVal:
                exec("attrDict[_attrKey][0][2] = self.get_%s" %_attrKey)
                self.__attrDict.__setitem__(_attrKey, attrDict[_attrKey][0])

    def __updateLogFormatAttributes(self):
        for _attrKey in self.__attrDict.keys():
            # assigning self attribute list from global variable "attrDict"
            self.__attrDict[_attrKey][1] = self.__attrDict[_attrKey][2]()

    def parseLogFormat(self):
        self.__updateLogFormatAttributes()
        __tempString = self.__formatString
        for (_attrKey, _attrVal) in self.__attrDict.items():    
            # execute key fuction in to obtain it s value
            _attrVal = self.__attrDict[_attrKey][1]
            # check wether attrkey is inside element by value or not
            if not _attrVal:
                _attrVal = 'None'
            print "key = %s, val= %s"%(_attrKey, _attrVal)
            # substitute each element by proper value using attrDict global variable
            __tempString = attrDict[_attrKey][1].sub(_attrVal, __tempString)
        self.__timeFormatter.setFormatString(__tempString)
        self.__timeFormatter.parseTimeFormat()
        self.__parsedFormat = self.__timeFormatter.getParsedTimeFormat()
        self.__parsedFormat = self.__parsedFormat + (self.__logSeperator)

    def setFormatString(self, formatString):
        self.__formatString = formatString

    def setLogSeparator(self, logSeperator):
        self.__logSeperator = seperator

    def getFormatString(self):
        return self.__formatString

    def getParsedFormat(self):
        return self.__parsedFormat

    def setUserLog(self, userLog, argTuple, logStack):
        # Get requirement from top level and asign them to local.
        self.__logStack = logStack
        self.__argTuple = argTuple
        self.__userLog = userLog
        self.__argSep = "\n"
        self.__argDepth = 0
        self.__argIndentSize = 1 
        self.__argIndent = '-' * self.__argIndentSize 
        self.__firstSep = '>'
        self.__nonFirstSep = ' '
        #print " inside setUserLog argTuple = ", self.__argTuple
        self.__argReObj = re.compile(r"""(?<=[^%])%q(?Lmsux)""")
        argIndent = self.__argIndent
        self.__argParsed = ""

        def argParser(argRaw, argDepth = 0, elemCounter = 0):
            # Parse args passed by user into log string.
            print "elemCounter = ", elemCounter
            argSep = self.__argSep
            if not argDepth:
                argSep = ''
            if elemCounter == 0:
                prec = self.__firstSep
                elemCounter += 1
            elif elemCounter > 0:
                prec = self.__nonFirstSep
            elif elemCounter < 0:
                prec = ''
            try:
                argIter = argRaw.__iter__()
            except AttributeError:
                # Found argRaw is not iterable
                argIter = None
            if argIter:
                    nestFlag = False
                    inElemCounter = 0
                    while True:
                        try:
                            argKey = argIter.next()
                            if nestFlag:
                                inElemCounter += 1
                            else:
                                inElemCounter = 0
                                nestFlag = True
                            argParser(argKey, argDepth + 1, inElemCounter)
                            # Test whether argKey is a key of dict or not
                            try:
                                argVal = argRaw.get(argKey)
                            except AttributeError:
                                argVal = None
                            if argVal:
                                self.__argParsed += " : "
                                #argSep = ''
                                argParser(argVal, 0, -1)
                            #self.__argParsed += self.__argSep 
                        except StopIteration:
                            break
            else:
                self.__argParsed += argSep + \
                                (self.__argIndent * argDepth) + \
                                prec + str(argRaw)
        if self.__argTuple:
            for argCounter in xrange(self.__argTuple.__len__()):
                self.__argParsed = ""
                argRaw = self.__argTuple[argCounter]
                argParser(argRaw)       
                self.__userLog = self.__argReObj.sub(\
                                        self.__argParsed,\
                                        self.__userLog, 1)

    def setTimeFormatter(timeFormatter):
        self.__timeFormatter = timeFormatter

# ****************** Property functions ********************
    def get_fn(self):
        # parse and return function name.
        return self.__logStack[3]

    def get_cn(self):
        # parse and return class name.
        return "class Name"

    def get_ln(self):
        # parse and return line number of executing.
        return str(self.__logStack[2])

    def get_mn(self):
        # parse and return method of class name.
        return "Module Name"

    def get_ti(self):
        # parse and return thread name or identifier.
        return threading.current_thread().__str__()

    def get_pi(self):
        # parse and return process number.
        return os.getpid().__str__()

    def get_fa(self):
        # parse and return .
        return self.__logStack[1]

    def get_lt(self):
        # parse and return function name.
        return "Log Type"

    def get_on(self):
        # parse and return function name.
        return os.uname()[0]

    def get_oa(self):
        # parse and return function name.
        return os.uname()[4]
        pass

    def get_hn(self):
        # parse and return function name.
        return os.uname()[1]

    def get_ov(self):
        # parse and return function name.
        return os.uname()[2]

    def get_ul(self):
        # parse and return function name.
        return self.__userLog

    def get_ds(self):
        # parse and return function name.
        return self.__doc__

    def get_si(self):
        # parse and return function name.
        return sys.stdin.__str__()

    def get_so(self):
        # parse and return function name.
        return sys.stdout.__str__()

    def get_se(self):
        # parse and return function name.
        return sys.stderr.__str__()

    def get_dt(self):
        # parse and return function name.
        return datetime.datetime.now().__str__()

    def get_lo(self):
        # parse and return function name.
        return self.__str__()

    def get_of(self):
        # parse and return function name.
        return os.name

    def get_pn(self):
        # parse and return function name.
        return sys.platform
# *****************************************************       

class LogSchaduler:
    pass

class TimeFormatter:
    '''
    Used for detemining the time of logging based on
    strftime arguments in datetime module.
    '''
    def __init__(self, formatString):
        self.__formatString = formatString
        self.__parsedTimeFormat = ''
        self.__rawTimeString = ''
        self.__rawTimeObject = ''

        # time format attributes
        self.__tf_year = ''
        self.__tf_month = ''
        self.__tf_day = ''
        self.__tf_weekday = ''
        self.__tf_hour = ''
        self.__tf_minute = ''
        self.__tf_second = ''
        self.__tf_microsecond = ''
        self.__initialize(formatString)

    def __initialize(self, formatString):    
        self.__rawTimeObject = datetime.datetime.now()
        self.__rawTimeString = self.__rawTimeObject.__str__()

    def setFormatString(self, formatString):
        self.__formatString = formatString

    def __updateTimeFormatAttributes(self):
        self.__rawTimeObject = datetime.datetime.now()
        self.__tf_year = self.__rawTimeObject.year

    def __timeIsUpdate(self):
        pass

    def getRawTimeString(self):
        return self.__rawTimeString

    def parseTimeFormat(self):
        self.__updateTimeFormatAttributes()
        self.__parsedTimeFormat = self.__rawTimeObject.strftime(\
                                                self.__formatString)
    
    def getParsedTimeFormat(self):
       return self.__parsedTimeFormat
       
