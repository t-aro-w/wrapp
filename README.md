# wrapp: Making a CLI Application by wrapping


## INSTALL

```
pip install wrapp
```

## USAGE

### Create your Python script under a few rules

In short, just use `wrapp.new`.

```
wrapp.new > YOURS.py
```

`wrapp.new` outputs template code at stdout.

```
cat YOURS.py
#!/usr/bin/env python3
from logging import getLogger


logger = getLogger(__name__)


def add_arguments(parser):
    ...


def main(args):
    ...
```

Starting with this template, add program options in `add_arguments()`.

The type of `parser` is assumed as `argparse.ArgumentParser` class.

for details, your Python script must contain `add_arguments(parser)` and `main(args)`.
`logger` is optional. Also `logger` can be replaced its name as `_LOG` or `LOG`.
For `logger`, it's OK to use any other 3rd-party logging modules like [`loguru`](https://github.com/Delgan/loguru).


### Run your Python script as an CLI app

Assume your Python script is `YOURS.py`.

```
wrapp YOURS.py --your-options ...
```

That is, just replace `python` to `wrapp`.
Then your script may keep simple:

- `if __name__ == '__main__':` is not needed.
- Also you don't need any noisy modules such as `argparse`.


## FEATURES

- No dependencies. wrapp only depends on Python standard libraries.
- It's like [python-fire](https://github.com/google/python-fire). But for wrapp, you don't need to import any other module in your Python code.


## LICENSE

MIT License.


## BACKGROUNDS

TBD.
