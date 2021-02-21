
from scapy.all import sr, sr1, traceroute, IP, TCP, UDP, ICMP

from util import PortResults

# runs a scapy trace and returns the result
def tryTrace(host, port, verbose=False):
  def getProtoObj():
    if port.proto == 'udp': return UDP(dport=port.port)
    if port.proto == 'tcp': return TCP(dport=port.port)

  rtn = None
  resp,_ = traceroute(host, dport=port.port, timeout=3, l4=getProtoObj(), verbose=False)

  if resp is None: 
    rtn = PortResults(host, port, 'closed', 'None')
  else:
    rtn = PortResults(host, port, 'trace', resp.get_trace())

  return rtn

# runs a scapy TCP send/receive and returns the result
def tryTCP(host, port, verbose=False):
  rtn = None
  resp = sr1(IP(dst=host)/TCP(dport=port.port,flags='S'),timeout=3, verbose=False)

  if resp is None: 
    rtn = PortResults(host, port, 'closed', 'None')
  elif resp.haslayer(TCP):
    if resp.getlayer(TCP).flags == 0x12:
      send_rst = sr(IP(dst=host)/TCP(dport=port.port,flags='AR'),timeout=3, verbose=False)
      rtn = PortResults(host, port, 'open', resp.show(dump=True))
    elif resp.getlayer(TCP).flags == 0x14:
      rtn = PortResults(host, port, 'closed', resp.show(dump=True))
  else: 
    rtn = PortResults(host, port, 'closed', 'None')

  return rtn

# runs a scapy UDP send/receive and returns the result
def tryUDP(host, port, verbose=False):
  rtn = None
  resp = sr1(IP(dst=host)/UDP(dport=port.port),timeout=3, verbose=False)

  if resp is None:
    rtn = PortResults(host, port, 'open/filtered', 'None')
  elif resp.haslayer(ICMP):
    if resp.getlayer(ICMP).code == 0x3:
      rtn = PortResults(host, port, 'closed', resp.show(dump=True))
    if resp.getlayer(ICMP).code == 0x1 or \
      resp.getlayer(ICMP).code == 0x2 or \
      resp.getlayer(ICMP).code == 0x9 or \
      resp.getlayer(ICMP).code == 0xa or \
      resp.getlayer(ICMP).code == 0xd:
      rtn = PortResults(host, port, 'filtered', resp.show(dump=True))
  else: 
    rtn = PortResults(host, port, 'closed', 'None')

  return rtn

# checks a given port to see if it is open (or trace it)
def checkPort(host, port, verbose=False):
  rtn = None
  if port.trace:            rtn = tryTrace(host, port, verbose)
  elif port.proto == 'tcp': rtn = tryTCP(host, port, verbose)
  elif port.proto == 'udp': rtn = tryUDP(host, port, verbose)
  else: raise TypeError(f'Unsupported protocol for {host}:{port.port} - {port.proto}')
  return rtn
