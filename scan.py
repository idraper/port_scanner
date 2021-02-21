
import progressbar
import concurrent.futures
from scan_util import checkPort
from entry import getHosts, processArgs, getArgs

from util import HostResults

def main(args=None):
  hosts, ports, verbose = getArgs(args)

  with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    futures = []
    for host in hosts:
      pResults = []
      for port in ports:
        futures.append(executor.submit(checkPort, host, port, verbose))

    i = 0
    if verbose: bar = progressbar.ProgressBar(max_value=len(futures))
    for future in concurrent.futures.as_completed(futures):
      result = future.result()
      if verbose: bar.update(i)
      # print(result.raw)
      i += 1


if __name__ == '__main__':
  main()
