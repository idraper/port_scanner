# port_scanner

This is a tool for scanning hosts for ports to see if they are open.
It uses multi-threading for much faster results than sequential requests.

NOTE: All scripts have only been tested using Windows 10, and with
proper installation of requirements.

This includes things such as python, packages like `scapy`, `latex`, etc.
In order to use this script you will need to have all the python packages installed,
as well as `Winpcap`/`Npcap` (for scapy).

If you want to generate pdf reports (recommended), you will need to have latex installed on your machine
with the required packages installed (`geometry`, `microtype`, `amsmath`, `amsfonts`, and `graphicx`).

---

## Command-line

### Hosts

There are several ways to provide hosts.
You must provide hosts either explicitly, as a range, or from a file.
You may use all three options and it will combine and run for all hosts passed.

Here are some examples:

Running with 2 explicit hosts:
```
> python3 scan.py -p 80 -ho 192.168.86.24 192.168.86.27
```

Running with a range of hosts:
```
> python3 scan.py -p 80 -r 192.168.86.24-192.168.86.27
> python3 scan.py -p 80 -r 192.168.86.24-27
```

Running with hosts in a file (one host per line):
```
> python3 scan.py -p 80 -f config/hosts.txt
```

Running with hosts in a file as well as a different range:
```
> python3 scan.py -p 80 -f config/hosts.txt -r 192.168.86.24-27
```

---

### Ports

You may supply as many ports to check as you want with the `-p` flag.
Each port is configured independently and will be checked on every host.
The default for a port is to use TCP.
You can also configure it to use UDP, or traceroute with that port.

Here are examples of how to do each:

Scanning for port 80 with tcp:
```
> python3 scan.py -p 80 -ho 192.168.86.24
```

Scanning for port 80 with udp (NOTE: options are case-sensitive):
```
> python3 scan.py -p 80:udp -ho 192.168.86.24
```

Scanning for port 80 but running traceroute:
```
> python3 scan.py -p 80:tcp:t -ho 192.168.86.24
```


Scanning for multiple ports, some tcp some udp, and one traceroute:
```
> python3 scan.py -p 80:tcp 443:udp 1023:tcp:t -ho 192.168.86.24
```

Note that if you use traceroute, you must specify the protocol.

---

### Output

By default, this will print out results to stdout, but
if you have latex installed with the proper packages installed
and you can give it a pdf name to export to. Here is an example:

Generating a pdf report of findings:
```
> python3 scan.py -p 80:tcp:t -ho 8.8.8.8 -l report.pdf
```

---

## GUI

Instead of using the command-line, you can access the `scan.py` script through a web GUI (albeit very simple :D)
which acts as a wrapper around the command-line arguments.

You can run this service with the `scan_web.py` script, usage as follows:
```
> python3 scan_web
```

This will open a browser window connected to lightweight server which calls `scan.py` for you.
All arguments are the same, and you describe ports in the same way.
This GUI works for now, but in the future it would be nice to update it and make adding ports nicer.
