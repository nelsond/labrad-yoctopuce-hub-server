# LabRAD Yoctopuce Hub server

Hub server for reading values from [Yoctopuce](http://www.yoctopuce.com/) modules.

**Currently only the Yocto-3D-V2 and Yocto-Meteo modules are
supported.**

## Requirements

### pylabrad

Make sure you install `pylabrad` before you run the server, e.g. using `pip`:

```shell
$ pip install labrad
```

You should also set the required environment variables, e.g. in `bash`:

```shell
$ export LABRADHOST=<hostname or ip>
$ export LABRADPASSWORD=<password>
```

## Configuration

### `modules.json`

Copy [`modules.example.json`](modules.example.json) to get started:

```shell
$ cp modules.example.json modules.json
```

Edit `modules.json` according to the modules connected to your computer:

```json
[
  {
    "name": "magnetometer",
    "uid": "Y3DMK002-XXXXX",
    "class": "Magnetometer"
  },
  {
    "name": "meteo",
    "uid": "METEOMK1-XXXXX",
    "class": "Meteo"
  }
]
```

## Example usage

First, start the server:

```shell
$ python yhub_server.py
```

Then start an (i)python console ...

```shell
$ ipython
```

... and use the settings:

```python
import labrad

cxn = labrad.connection()
yhub = cxn.yoctopuce_hub

yhub.modules.available()
# => [('Yocto-Meteo', 'METEOMK1-XXXX'), ('Yocto-3D-V2', 'Y3DMK002-XXXX')]

yhub.modules_enabled()
# => [('meteo', 'Meteo'), ('magnetometer', 'Magnetometer')]

yhub.get_reading('meteo')
# => [('p', 959.44), ('RH', 51.7), ('T', 23.59)]

yhub.get_reading('magnetometer')
# => [('y', -0.288), ('x', 0.6), ('z', 0.152)]
```
