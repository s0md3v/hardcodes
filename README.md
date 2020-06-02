<h2 align="center">
  <br>
  <a href="https://github.com/s0md3v/hardcodes"><img src="https://i.ibb.co/7p791wv/hardcodes-svg.png" alt="hardcodes"></a>
  <br>
  hardcodes
  <br>
</h2>

<h4 align="center">extract strings from source code</h4>

<p align="center">
  <img src="https://img.shields.io/badge/dependencies-0-3498db">
  <a href="https://github.com/s0md3v/hardcodes/releases">
    <img src="https://img.shields.io/pypi/v/hardcodes?color=3498db&label=version">
  </a>
  <a href="https://github.com/s0md3v/hardcodes/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/hardcodes.svg">
  </a>
</p>

**hardcodes** is a utility for searching strings hardcoded by developers in programs. It uses a modular tokenizer that can handle comments, any number of backslashes & nearly any syntax you throw at it.

Yes, it is designed to process any syntax and following languages are officially supported:

```
ada, applescript, c, c#, c++, coldfusion, golang, haskell, html, java, javascript,
jsp, lua, pascal, perl, php, powershell, python, ruby, scala, sql, swift, xml
```

#### Installation
##### with pip
```
pip3 install hardcodes
```
##### or build from source
```
git clone https://github.com/s0md3v/hardcodes && cd hardcodes && python3 setup.py install
```

<hr>

### Documentation
hardcodes is available as both a library as well as a command line program. The relevant documentation can be found below:

- [For developers](https://github.com/s0md3v/hardcodes#for-developers)
- [For users](https://github.com/s0md3v/hardcodes#for-users)

### For Developers
The sample program below demonstrates usage of `hardcodes` library

```python
from hardcodes import search

string = "console.log('hello there')"
result = search(string, lang="common", comments="parse")
print(result)
```
```python
Output: ['hello there']
```

The arguments `lang` and `comments` are optional. Their use is explained below in the user documentation section.

<hr>

### For Users
`cli.py` provides a grep-like command line interface to `hardcodes` library. You will need to install the library first to use it.

#### Find strings in a file
```bash
python cli.py /path/to/file.ext
```

#### Find strings in a directory, recursively
```bash
python cli.py -r /path/to/dir
```

#### Hide paths from output
```bash
python cli.py -o /path/to/file.ext
```

#### Specify programming language
Specifying a language is optional and should be used only when the programming language of source is already known.

```bash
python cli.py -l 'golang' /path/to/file.go
```

#### Specify comment behaviour
With `-c` option, you can specify 

- `ignore` ignore the comments completely
- `parse`  parse the comments like code
- `string` add comments to list of hardcoded strings

`python cli.py -o /path/to/file.ext`
