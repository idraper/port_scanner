import json

class Formatter:
  def __init__(self, results):
    self.results = results

  def __repr__(self):
    return self.__str__()
  
  def __str__(self):
    return 'ResultsFormatter'

  def print(self):
    # print to stdout

    for _,hostR in self.results.hostResults.items():
      print(hostR.host)
      for portR in sorted(hostR.portResults, key=lambda r: r.port.port):
        print(f'  {portR.port.port}\\{portR.port.proto}'.ljust(20) + portR.status)
        if portR.status == 'trace':
          if type(portR.raw) == dict and portR.host in portR.raw:
            for k in sorted(portR.raw[portR.host].keys()):
              print(f'    {k}'.ljust(6) + f'{portR.raw[portR.host][k][0]}')

  def latex(self, fname):
    # print to latex document
    pass
