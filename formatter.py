import os
import tempfile
import subprocess
from latex import build_pdf
from functools import reduce

class Formatter:
  def __init__(self, results):
    self.results = results

  def __repr__(self):
    return self.__str__()
  
  def __str__(self):
    return 'ResultsFormatter'

  def print(self):
    # print to stdout

    print('Summary:')
    print(f'UDP Ports Scanned:   {sum(map(lambda hr: sum(map(lambda x: x.port.proto == "udp", hr.portResults)), self.results.hostResults.values()))}')
    print(f'TCP Ports Scanned:   {sum(map(lambda hr: sum(map(lambda x: x.port.proto == "tcp", hr.portResults)), self.results.hostResults.values()))}')
    print(f'Total Ports Scanned: {sum(map(lambda hr: len(hr.portResults), self.results.hostResults.values()))}')
    print(f'Open Ports:          {sum(map(lambda hr: sum(map(lambda x: "open" in x.status, hr.portResults)), self.results.hostResults.values()))}')

    print('')
    print('Details:')
    for hostR in sorted(self.results.hostResults.values(), key=lambda hr: hr.host):
      print(hostR.host)
      for portR in sorted(hostR.portResults, key=lambda r: r.port.port):
        print(f'  {portR.port.port}\\{portR.port.proto}'.ljust(20) + portR.status)
        if portR.status == 'trace':
          if type(portR.raw) == dict and portR.host in portR.raw:
            for k in sorted(portR.raw[portR.host].keys()):
              print(f'    {k}'.ljust(6) + f'{portR.raw[portR.host][k][0]}')

  def latex(self, fname):
    # print to latex document

    def header():
      return r'''
\documentclass[paper=a4, fontsize=11pt,twoside]{scrartcl}	% KOMA

\usepackage[a4paper,pdftex]{geometry}	% A4paper margins
\setlength{\oddsidemargin}{5mm}			% Remove 'twosided' indentation
\setlength{\evensidemargin}{5mm}

\usepackage[english]{babel}
\usepackage[protrusion=true,expansion=true]{microtype}	
\usepackage{amsmath,amsfonts}
\usepackage{graphicx}

\RedeclareSectionCommand[beforeskip=-5.5ex plus -1ex minus -.2ex,afterskip=4.3ex plus -.2ex]{section}
\RedeclareSectionCommand[beforeskip=-5.5ex plus -1ex minus -.2ex,afterskip=4.3ex plus -.2ex]{subsection}

\newcommand{\HRule}[1]{\rule{\linewidth}{#1}} 	% Horizontal rule

\makeatletter							% Title
\def\printtitle{%						
    {\centering \@title\par}}
\makeatother									

\makeatletter							% Author
\def\printauthor{%					
    {\centering \large \@author}}				
\makeatother							

      '''

    def cover(title):
      return r'''
\title{	\normalsize \textsc{} 	% Subtitle
		 	\\[2.0cm]								% 2cm spacing
			\HRule{0.5pt} \\						% Upper rule
			\LARGE \textbf{\uppercase{'''+title+r'''}}	% Title
			\HRule{2pt} \\ [0.5cm]		% Lower rule + 0.5cm spacing
			\normalsize \today			% Todays date
		}

\author{
  This report was\\
  generated from the git repo:\\
  idraper/port\_scanner\\
}

\begin{document}
% ------------------------------------------------------------------------------
% Maketitle
% ------------------------------------------------------------------------------
\thispagestyle{empty}		% Remove page numbering on this page

\printtitle					% Print the title data as defined above
  	\vfill
\printauthor				% Print the author data as defined above
\newpage
% ------------------------------------------------------------------------------
% Begin document
% ------------------------------------------------------------------------------
\setcounter{page}{1}		% Set page numbering to begin on this page
      '''


    def done():
      return r'''
\end{document}
      '''

    document = ''
    document += header()
    document += cover('Port Scan Report')

    # print summary report
    document += '\n\\section*{Summary}\n\n'

    document += '{\n\LARGE\n'
    document += r'\begin{tabular}{ll}' + '\n'
    document += f'UDP Ports Scanned: & {sum(map(lambda hr: sum(map(lambda x: x.port.proto == "udp", hr.portResults)), self.results.hostResults.values()))} \\\\\n'
    document += f'TCP Ports Scanned: & {sum(map(lambda hr: sum(map(lambda x: x.port.proto == "tcp", hr.portResults)), self.results.hostResults.values()))} \\\\\n'
    document += f'Total Ports Scanned: & {sum(map(lambda hr: len(hr.portResults), self.results.hostResults.values()))} \\\\\n'
    document += f'Open Ports: & {sum(map(lambda hr: sum(map(lambda x: "open" in x.status, hr.portResults)), self.results.hostResults.values()))} \n'
    document += r'\end{tabular} \vfill' + '\n'
    document += '}\n\n'

    # print table with details report
    document += '\\section*{Details}\n\n'
    for hostR in sorted(self.results.hostResults.values(), key=lambda hr: hr.host):
      document += f'\\subsection*{{{hostR.host}}}\n\n'
      document += r'\begin{tabular}{lll}'
      document += '\\hline\n'
      document += r'Port & Protocol & Status \\'
      document += '\\hline\n'

      for portR in sorted(hostR.portResults, key=lambda r: r.port.port):
        document += f'{portR.port.port} & {portR.port.proto} & {portR.status} \\\\'

        if portR.status == 'trace':
          if type(portR.raw) == dict and portR.host in portR.raw:
            document += '\n' + r'& & \begin{tabular}{ll}'
            for k in sorted(portR.raw[portR.host].keys()):
              document += f'\n{k} & {portR.raw[portR.host][k][0]} \\\\'
            document += r'\end{tabular} \\' + '\n'

      document += '\\hline\n'
      document += r'\end{tabular} \vfill' + '\n\n'

    document += done()

    with open(fname, 'wb') as file:
      file.write(bytes(build_pdf(document)))
    os.system(f'start {fname}')
