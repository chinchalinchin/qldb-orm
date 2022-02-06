# Configuration

## Log Level

The log level can be set through the environment variable **LOG_LEVEL** to the values: `NOTSET`, `INFO`, `DEBUG` and `ERROR`,

```shell
export LOG_LEVEL='INFO'
innoldb --table table-name --all
```

```python
import os
from innoldb.qldb import Query

os.environ['LOG_LEVEL'] = 'DEBUG'
Query('table-name').all()
```

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