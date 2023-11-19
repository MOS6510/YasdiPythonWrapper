# YASDI Python Wrapper

This is a simple python 3.x wrapper for SMA's 'YASDI' (aka **Y**et **A**nother **S**MA **D**ata **I**mplementation).

**SMAData1** (version **1**, short **SD1**) is the name of the protocol SMA used with (older) string inverters. It can still be used in modern inverters
(in 2023) with a [RS485 data module](https://files.sma.de/downloads/485i-Module-IA-de-19W.pdf) if needed. 

YASDI does not implement the modern communication protocol **SMAData2+** (version **2+**, short **SD2+**) which is used in all modern SMA inverters and devices with ethernet (IP network).



### Get latest YASDI source code, compile and install it

Get the source directly from [SMA Solar Technology AG](https://www.sma.de/produkte/apps-software/yasdi) 
or my server [www.heiko-pruessing.de](https://www.heiko-pruessing.de/projects/yasdi/).

```bash
Bash> unzip yasdi-1.8.1build9-src.zip -d YASDI
Bash> cd YASDI/projects/generic-cmake
Bash> mkdir build-gcc
Bash> cd build-gcc
Bash> cmake ..
Bash> make
Bash> sudo make install    
Bash> sudo ldconfig
```
  
### Init YASDI Python Wrapper

Install all deps:

```
make init
```

### Edit YASDI configuration file

Edit the file <b>yasdi.ini</b> as needed and test it with 

```
yasdishell ./yasdi.ini
```

### Run Unit Tests

The unit tests can be started with:

```
make test
```

### Start the Sample Demon 

```
make demon
```

The sample demon searches for all connected devices (inverters) and starts data query with most important measurement values. 
It creates a data file which contains all requested data:

```
ChannelName;ChannelUnit;ValueTimestamp;ChannelValue
Pac;kW;1700388485;2.3
E-Tag;kWh;1700388485;1.4
E-Total;kWh;1700388485;2746876.4
```

