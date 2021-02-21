import progressbar
import concurrent.futures

from entry import getArgs
from util import AllResults
from formatter import Formatter
from scan_util import checkPort

def main(args=None):
  hosts, ports, latex, verbose = getArgs(args)

  allResults = AllResults()

  with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    # add all port checking to the thread pool
    futures = []
    for host in hosts:
      pResults = []
      for port in ports:
        futures.append(executor.submit(checkPort, host, port, verbose))

    # add our result once the thread has finished
    i = 0
    if verbose: bar = progressbar.ProgressBar(max_value=len(futures))
    for future in concurrent.futures.as_completed(futures):
      result = future.result()
      if verbose: bar.update(i)
      allResults.addPortResult(result)
      i += 1
    if verbose: bar.finish()

  # output the results
  if latex is None: Formatter(allResults).print()
  else:             Formatter(allResults).latex(latex)

if __name__ == '__main__':
  main()
