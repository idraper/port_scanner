import argparse
from netaddr import iter_iprange
from distutils.util import strtobool

from util import Port

def argToPort(arg):
  sp = arg.split(':')
  if len(sp) == 1: return Port(int(sp[0]))
  if len(sp) == 2: return Port(int(sp[0]), sp[1])
  if len(sp) == 3: return Port(int(sp[0]), sp[1], True)

def getHosts(args):
  hosts = set()
  if args.host is not None:
    hosts.update(args.host)
  if args.range is not None:
    rng = args.range.split('-')
    if len(rng) == 1: raise TypeError(f'Didn\'t get a range, received: {args.range}')
    if len(rng) > 2: raise TypeError(f'Cannot have more than 1 range, received: {args.range}')
    if len(rng) == 2 and rng[1].count('.') == 0: rng[1] = '.'.join(rng[0].split('.')[:-1]) + f'.{rng[1]}'
    hosts.update(map(lambda x: str(x), iter_iprange(*rng)))
  if args.file is not None:
    for fname in args.file:
      with open(fname, 'r') as f:
        hosts.update([line.strip() for line in f])
    if '' in hosts: hosts.remove('')

  return sorted(list(hosts))

def processArgs(parser, raw_args):
  args = parser.parse_args(raw_args)
  hosts = getHosts(args)
  if len(hosts) == 0: parser.error('No hosts provided')

  return hosts, [argToPort(arg) for arg in args.port], args.latex, args.verbose

def getArgs(raw_args):
  parser = argparse.ArgumentParser(description='Port scanner to scan either a specified set of TCP or UDP ports.')
  parser.add_argument('-p', '--port', nargs='+', required=True, help='the ports to search')
  parser.add_argument('-v', '--verbose', type=lambda x: bool(strtobool(x)), default=True, help='whether to print to stdout')
  parser.add_argument('-l', '--latex', default=None, help='generate pdf report at the given filename using latex (must have latex installed)')

  group = parser.add_argument_group()
  group.add_argument('-ho', '--host', nargs='+', help='the host to search on')
  group.add_argument('-r', '--range', help='a host range to search on')
  group.add_argument('-f', '--file', nargs='+', help='a file (or multiple) containing hosts to search (1 host per line)')

  return processArgs(parser, raw_args)
