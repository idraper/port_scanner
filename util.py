import json
import progressbar as pb

class Port:
  def __init__(self, port, proto='tcp', trace=False):
    self.port = port
    self.proto = proto
    self.trace = trace

  def __repr__(self):
    return self.__str__()
  
  def __str__(self):
    return f'Port({self.port}, {self.proto}, {self.trace})'

  def toJson(self):
    return json.dumps({'port': self.port, 'proto': self.proto, 'trace': self.trace})

class PortResults:
  def __init__(self, host, port, status, raw):
    self.host = host
    self.port = port
    self.status = status
    self.raw = raw

  def __repr__(self):
    return self.__str__()
  
  def __str__(self):
    return f'PortResults({self.port}, {self.status})'

  def toJson(self):
    return {'port': self.port.toJson(), 'status': self.status}
    # return {'port': self.port.toJson(), 'status': self.status, 'raw': self.raw}

  def toJsonStr(self):
    return json.dumps(self.toJson())

class HostResults:
  def __init__(self, host, portResults=None):
    self.host = host
    self.portResults = [] if portResults is None else portResults

  def __repr__(self):
    return self.__str__()
  
  def __str__(self):
    return f'HostResults({self.host}, {self.portResults})'

  def toJson(self):
    return {'host': self.host, 'portResults': list(map(lambda r: r.toJson(), self.portResults))}

  def toJsonStr(self):
    return json.dumps(self.toJson())

class AllResults:
  def __init__(self, hostResults=None):
    self.hostResults = {} if hostResults is None else hostResults
  
  def __getitem__(self, key):
    return self.hostResults[key]

  def __repr__(self):
    return self.__str__()
  
  def __str__(self):
    return f'AllResults({len(self.hostResults)})'

  def addPortResult(self, portResult):
    if portResult.host in self.hostResults:
      self.hostResults[portResult.host].portResults.append(portResult)
    else:
      self.hostResults[portResult.host] = HostResults(portResult.host, [portResult])
