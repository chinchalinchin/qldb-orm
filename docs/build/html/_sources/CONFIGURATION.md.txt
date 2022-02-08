# Configuration

## Log Level

The log level can be set through the environment variable **LOG_LEVEL** to the values: `NOTSET`, `INFO`, `DEBUG` and `ERROR`,

```shell
export LOG_LEVEL='INFO'
innoldb --table table-name --all
```

```python
import os

os.environ['LOG_LEVEL'] = 'DEBUG'

from innoldb.qldb import Query

Query('table-name').get_all()
```

.. note::
  The environment must be set before the `innoldb` import. During the import, `innoldb` will scan the environment and use the value it finds on its initial load. 

## Build From Source

The `innoldb` library can be built from source with the following script,

```shell
git clone https://github.com/Makpar-Innovation-Laboratory/innoldb
cd innoldb
python -m build
VERSION=$(cat version.txt)
cd dist
pip install innoldb-${VERSION}-py3-none-any.whl
```

Or use the pre-packaged helper script,

```shell
git clone https://github.com/Makpar-Innovation-Laboratory/innoldb
./innoldb/scripts/install
```