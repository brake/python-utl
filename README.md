# Package `utl`

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://opensource.org/licenses/MIT)

Utilities I use in many of my projects.

## Sub-modules

  * [utl.file](#utlfile)
  * [utl.hex](#utlhex)
  * [utl.misc](#utlmisc)
  * [utl.version](#utlversion)
  * [utl.wx_](#utlwx_)
  * [utl.text](#utltext)
    
## utl.file

File related utilities

### utl.file Functions

`binary_file(name, *args, **kwargs)` Open file in binary mode for reading

`text_file(name, *args, **kwargs)` Open file in text mode for reading.

`utf8_bom_text_file(name, *args, **kwargs)` Open [UTF-8](https://en.wikipedia.org/wiki/UTF-8) text file with [BOM](https://en.wikipedia.org/wiki/Byte_order_mark) in text mode for reading.

`writable_binary_file(name, *args, **kwargs)` Open file in binary mode for writing.

`writable_text_file(nane, *args, **kwargs)` Open file in text mode for writing.

`file_lines_count(filename)` Count lines in a text file.

`filelist_processor(iterable, parse_line, progress_co=None)` Generator of parsed lines from each text file (path) in iterable.

 * `iterable` - sequence of file paths or None (there sys.argv[1:] will be used)
 * `parse_line` - callable for processing of single line
 * `progress_co` - coroutine with API like below:
 
   ```python
   progress_co = progress_generator()
   progress_co.send((filename, lines_read, lines_total, lines_processed))
   ...
   progress_co.send(lines_saved)  # finalizing work
   ```

   Generates output data in format produced by `parse_line()`

`offset_iter(fd)` Generator of pairs (offset_from_beginning_of_file, string) for file object 'fd'.

`reverse_lines(fd, keepends=False, block_size=4096)` Iterate through the lines of a file in reverse order.
If `keepends` is `True`, line endings are kept as part of the line. Return `generator`.

## utl.hex

Hex string to binary conversions and vice versa

### utl.hex Functions

`hexstr2bytes_list(hexstr)` Convert the hex string to list of bytes.

**Examples**:

```python
>>> hexstr2bytes_list('DDFFAA33')
[221, 255, 170, 51]

>>> hexstr2bytes_list('DDFFAA3')
Traceback (most recent call last):
...
TypeError: Odd-length string
```

`bytes_list2bin(bl)` Convert list of bytes to binary string.

**Example**:
```python
>>> bytes_list2bin([221, 255, 170, 51])
'\xdd\xff\xaa3'
```

`bytes_list2hexstr(bl, uppercase=True)` Convert list of bytes to hex string.

**Examples**:

```python
>>> bytes_list2hexstr([221, 255, 170, 51])
'DDFFAA33'

>>> bytes_list2hexstr([221, 255, 170, 51], True)
'DDFFAA33'

>>> bytes_list2hexstr([221, 255, 170, 51], False)
'ddffaa33'
```

`is_hexstr(s)` Check a string s for presence a valid hexadecimal data.

**Examples**:

```python
>>> is_hexstr('ddffaa33')
True

>>> is_hexstr('failing_test')
False
```

`swap_nibbles(s)` Swap nibbles in a hex string. `len(s)` must be even otherwise `ValueError` will be raised.

**Examples**:

```python
>>> swap_nibbles('d1c1a1b1')
'1d1c1a1b'

>>> swap_nibbles('d1c1a1b')
Traceback (most recent call last):
...
ValueError: Odd-length string

>>> swap_nibbles('D1NX')
'1DXN'
```

## utl.misc

Uncategorized utilities.

### utl.misc Functions

`flatten(iterable)` Generator of flattened sequence from input `iterable`. `iterable` can contain scalars and another iterables.

**Examples**:

```python
[1, 2, 3, 4, [[[5, 6], 7]], 8, [9]] ➔ [1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> list(flatten([1, 2, 3, 4, [[[5, 6], 7]], 8, [9]]))
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

`ignored(*exceptions)` Create context manager ignoring exceptions from input sequence. **Only for Python 2**

**Examples**:

```python
>>> with ignored(TypeError):
...     'aaa' / 4

>>> with ignored(ValueError):
...     'aaa' / 4                      
Traceback (most recent call last):
...
TypeError: unsupported operand type(s) ...
```

### utl.misc Classes

`class Singleton` Meta class for [Singleton](https://en.wikipedia.org/wiki/Singleton_pattern) creation.

**Example**:

```python
>>> class A(object):
...    __metaclass__ = Singleton

>>> a1 = A()

>>> a2 = A()

>>> id(a1) == id(a2)
True
```

## utl.version

Application version management.

Based on files:
  - `main_version.txt`
  - previous version of file - `app_version.py`

create a new file app_version.py containing current application version.
Only a "build" code, which is responsible for version increment requires to import this module. Code reading
the application version depends only from automatically updated `app_version.py`

Version is a string consisting from three parts: major.minor.build
  - major (0...255)
  - minor (0...255)
  - build (0...65535)

In case you need increment major and/or minor version numbers and reset a build number to zero, you have to:
  - edit the `main_version.txt` to set major and minor versions
  - remove `app_version.py`

### Usage:
Inside each "build" code (for example in `setup.pky`) you have to call `get_new_version()`
In a code where there the version number is need:
```python
import app_version
...
version = app_version.version
```

### utl.version Functions

`get_current_version()` Return a full current version number. If version information have not initialized yet it will be generated.

`get_new_version()` Return a new full version number

## utl.wx_

wx.Python utilities

### utl.wx_ Functions

`modal_dialog(cls)` Decorator adding to classes derived from wx.Dialog feature of modal call via context manager protocol.

**Example**:
```python
@utl.wx_.modal_dialog
class MyDialog extends wx.Dialog:
    pass
...

with MyDialog() as dlg:
    dlg.ShowModal()
```

`transparent_event_handler(fn)` Decorator for event handlers which should call `event.Skip()`. Prevents event handler from explict annoying call of `event.Skip()`. 
Assumes that handler receives event as second parameter.

**Example**:
```python
@utl.wx_.transparent_event_handler
def on_button_click(self, event):
    # do not need to call event.Skip() here
    do_one()
    do_two()
```

## utl.text

Text utilities

### utl.text Functions

`chunk(s, p)` Split string s into sections with size p.

```python
>>> chunk('aaabbbcccdddeee', 3)
[u'aaa', u'bbb', u'ccc', u'ddd', u'eee']

>>> chunk('aaaabbbbccccee', 4)
[u'aaaa', u'bbbb', u'cccc', u'ee']

>>> chunk('aaa', 4)
[u'aaa']
```

`lines_parser(iterable, parse_line)` 

Generator of pairs: 
   - `ParseStats` 
   - result of applying `parse_line()` function to text line from iterable.

  `ParseStats` - object with fields:
  - `read` - total lines read
  - `processed` - lines where `parse_line` doesn't return `None`
  
  `parse_line()` should return None if parsing of some line fails. In this case generator will not yield
  anything but will switch to next line.

**Examples**:

```python
>>> def parse_line(line):
...     if line.startswith(' '):
...         return None
...     return True if line else False
>>> lines = ('', 'aaa', 'bbb', ' ccc')
>>> list(lines_parser(lines, parse_line))
[(ParseStats(read=1, processed=1), False), (ParseStats(read=2, processed=2), True), (ParseStats(read=3, processed=3), True)]

>>> def parse_line(line):
...     if line.startswith(' '):
...         return None
...     return True if line else False
>>> lines = ('', 'aaa', ' ccc', 'bbb')
>>> list(lines_parser(lines, parse_line))
[(ParseStats(read=1, processed=1), False), (ParseStats(read=2, processed=2), True), (ParseStats(read=4, processed=3), True)]
```

`lines_stripped(iterable, chars=None)` Return Iterable object containing lines from input iterable with strip(chars) applied.

**Examples**:
```python
>>> list(lines_stripped([' aaa ', '\tbbb\n', 'ccc']))
[u'aaa', u'bbb', u'ccc']

>>> list(lines_stripped(['xaaax', '  bbb', '__ccc__'], 'x_'))
[u'aaa', u'  bbb', u'ccc']
```

`lines_uncommented(iterable, comments=(u';', u'#'))` Return Iterable object containing only lines from iterable which didn't begin with comment.

**Examples**:
```python
>>> lines = ('aaa', '; bbb', '#ccc ', 'ddd')
>>> list(lines_uncommented(lines))
[u'aaa', u'ddd']

>>> lines = ('** aaa', '*bbb', '#ccc ', ' ddd')
>>> list(lines_uncommented(lines, ('**', ' ')))
[u'*bbb', u'#ccc ']
```

`progress_co(justify=75)` Print some processing state to console. Return a generator.

**Example**:

```python
>>> progress = progress_co(0)
>>> progress.send(('file.txt', 3, 7, 1))   
file.txt 3/7 (processed: 1)  Lines saved: 0
>>> progress.send(100)                     
file.txt 3/7 (processed: 1)  Lines saved: 100
>>> progress.send(('another_file.txt', 0, 10, 0)) 
     Done!
another_file.txt 0/10 (processed: 0)  Lines saved: 100
```
