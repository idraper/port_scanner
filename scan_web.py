import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

import os
import sys
from io import StringIO

import scan

# HTML to return
titleHTML = '<body><h1>Port Scanner</h1></body>'
def hostsHTML(h):
  return f'<body><h3>Hosts</h3><div><textarea name="host" rows="5" cols="30">{h}</textarea></div></body>'
def hostRangeHTML(h):
  return f'<body><h3>Host Range</h3><div><br><input type="text" id="hostRange" name="hostRange" value="{h}"><br></div></body>'
def hostFileHTML(h):
  return f'<body><h3>Host File</h3><div><br><input type="text" id="hostFile" name="hostFile" value="{h}"><br></div></body>'
def portsHTML(p):
  return f'<body><h3>Ports</h3><div><textarea name="port" rows="5" cols="30">{p}</textarea></div></body>'
def latexHTML(l):
  return f'<body><h3>Create PDF Report (must have latex installed)</h3><div><br><input type="text" id="latex" name="latex" value="{l}"><br></div></body>'

# JS to trigger value to run
script = '''<script type="text/javascript">
function runFunc() {
  var myForm = document.getElementById('myForm');
  myForm.run.value = true;
  myForm.submit();
}
</script>
'''

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    # Extract query params
    hosts = ''
    hostRange = ''
    hostFile = ''
    ports = ''
    latex = ''
    run = False
    query_components = parse_qs(urlparse(self.path).query)
    if 'host' in query_components:
      hosts = query_components['host']
      hosts = '\n'.join(hosts)
    if 'hostRange' in query_components:
      hostRange = query_components['hostRange'][0]
    if 'hostFile' in query_components:
      hostFile = query_components['hostFile'][0]
    if 'port' in query_components:
      ports = query_components['port']
      ports = '\n'.join(ports)
    if 'latex' in query_components:
      latex = query_components['latex'][0]
    if 'run' in query_components:
      run = True if query_components['run'][0] == 'true' else False

    if run:
      # run the script (show different page with output)
      html = f'<html>{script}{titleHTML}Running...'
      self.wfile.write(bytes(html, "utf8"))

      args = ['-p', *(ports.split('\n'))]
      if len(hosts) > 0: args += ['-ho', *(hosts.split('\n'))]
      if len(hostRange) > 0: args += ['-r', hostRange]
      if len(hostFile) > 0: args += ['-f', hostFile]
      if len(latex) > 0: args += ['-l', latex]

      print(args)
      old_stdout = sys.stdout
      sys.stdout = mystdout = StringIO()

      output = ''
      try:
        scan.main(args)
      except:
        output = f'Error with args: {args}'

      sys.stdout = old_stdout
      output = output if output.startswith('Error') else mystdout.getvalue()
      if 'Summary' in output: output = output[output.index('Summary'):]
      elif output.startswith('Error'): pass
      else: output = 'Generated report'

      self.wfile.write(bytes(f'Done<br></br><div>Output:</div><div><textarea rows="40" cols="60">{output}</textarea></div><br></br><form><input type="submit" value="New Scan"></form></html>', "utf8"))
    else:
      # show normal page
      html = f'<html>{script}<head></head>{titleHTML}<form id="myForm" onsubmit="runFunc()">{hostsHTML(hosts)}{hostRangeHTML(hostRange)}{hostFileHTML(hostFile)}{portsHTML(ports)}{latexHTML(latex)}<input type="submit" value="Submit"><input type="hidden" name="run" value="false"/></form></html>'
      self.wfile.write(bytes(html, "utf8"))

    return

if __name__ == '__main__':
  print('Starting server on http://localhost:9922')
  httpd = http.server.HTTPServer(('localhost', 9922), MyHttpRequestHandler)
  os.system('start http://localhost:9922')
  httpd.serve_forever()
