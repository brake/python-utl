#Module utl

Utilities I use in many of my projects


##Sub-modules

- utl.file
- utl.hex
- utl.misc
- utl.text
- utl.version
- utl.wx_

##Module utl.file

File related utilities


###Functions

    binary_file(file_name)
    
Open binary file for reading

    writable_binary_file(file_name)
    
Open binary file for writing

    text_file(file_name)
    
Open text file for reading

    writable_text_file(file_name)
    
Open text file for writing

    utf8_bom_text_file(file_name)
    
Open UTF8 text file with BOM for reading


    file_lines_count(filename)
    
Count lines in a text file

    filelist_processor(iterable, parse_line, progress_co=None)
    
Generator of parsed lines from each text file (path) in iterable.

* iterable - sequence of file paths or None (there sys.argv[1:] will be used)
* parse_line - callable for processing of single line
* progress_co - coroutine with API like below:
        progress_co = progress_generator()
        progress_co.send((filename, lines_read, lines_total, lines_processed))
        ...
        progress_co.send(lines_saved)  # finalizing work

Generates output data in format produced by parse_line()

    offset_iter(fo)

Generator of pairs (offset_from_beginning_of_file, string) for file object 'fo'

    rlines(f, keepends=False)

Iterate through the lines of a file in reverse order.
If keepends is true, line endings are kept as part of the line.

Works only with files opened in binary mode.

##Module utl.hex

Hex string to binary conversions and vice versa

###Functions

    bin2hexstr(bindata)
# 
    hexstr2bin_list(hexstr)
# 
    is_hexstr(s)
Check a string s for presence a valid hexadecimal data

##Module utl.version

Application version management.

Basing on files:
- main_version.txt
- previous version of file app_version.py

create a new file app_version.py containing current application version.
Only a "build" code, which is responsible for version increment requires to import this module. Code reading
the application version depends only from automatically updated app_version.py

Version is a string consisting from three parts: major.minor.build
- major (0...255)
- minor (0...255)
- build (0...65535)

In case you need increment major and/or minor version numbers and reset a build number to zero, you have to:
- edit the 'main_version.txt' to set major and minor versions
- remove 'app_version.py'

#####Usage:
Inside each "build" code you have to call get_new_version()
In a code where there the version number is need
    
    import app_version
    ...
    version = app_version.version

###Functions
    
    get_current_version()
Return a full current version number.
If version information have not initialized yet it will be generated.

    get_new_version()
    
Return a new full version number

##Module utl.wx_

[wxPython](http://www.wxpython.org) utilities

###Functions

    modal_dialog(cls)

Decorator adding to classes derived from wx.Dialog feature of modal call via context manager protocol.

#####Example:

    @utl.wx_.modal_dialog
    class MyDialog extends wx.Dialog:
        pass
    ...

    with MyDialog() as dlg:
        dlg.ShowModal()

#     

    transparent_event_handler(fn)

Decorator for event handlers which should call event.Skip().
Prevents event handler from explict annoying call of event.Skip().

Assumes that handler receives event as second parameter.

##Module utl.text

Text utilities

###Functions

    chunk(s, p)
Split string/unicode into sections with size p

    lines_parser(iterable, parse_line)
Generator of pairs:

- ParseStats
- result of applying parse_line() function to text line from iterable.

parse_line() should return None if parsing of some line fails. In this case generator will not yield anything but will switch to next line.

    lines_stripped(iterable, chars=None)
Return Iterable object containing lines from input iterable with strip(chars) applied

    lines_uncommented(iterable, comments=(';', '#'))
Return Iterable object containing only lines from iterable which didn't begin with comment

    progress_co(justify=75)
Print some processing state to console. Return a generator.

#####Usage example:
    progress = progress_co()
    progress.send((filename, lines_read, lines_total, lines_processed))
    ...
    progress.send(lines_saved)

###Classes

    ParseStats(read, processed)
Named tuple containing numbers of read and processed lines of text

##Module utl.misc

Uncategorized utilities

###Functions
    flatten(iterable)
Generator of flattened sequence from input iterable.

iterable can contain scalars and another iterables.

    [1, 2, 3, 4, [[[5, 6], 7]], 8, [9]] -> [1, 2, 3, 4, 5, 6, 7, 8, 9]

#####Example:
    >>> list(flatten([1, 2, 3, 4, [[[5, 6], 7]], 8, [9]]))
    [1, 2, 3, 4, 5, 6, 7, 8, 9]

___

    ignored(*exceptions)
Create context manager ignoring exceptions from input sequence

    >>> with ignored(TypeError):
    ...     'aaa' / 4

###Classes 

    class Singleton

Meta class for Singleton creation:

    >>> class A(object):
    ...    __metaclass__ = Singleton

    >>> a1 = A()

    >>> a2 = A()

    >>> id(a1) == id(a2)
    True
