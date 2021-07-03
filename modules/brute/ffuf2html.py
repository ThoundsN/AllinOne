#!/usr/bin/env python3

#legacy code 

import json
import csv
import config

from os import listdir
from os.path import isfile, join,abspath
from jinja2 import Template

import utils

template_fraction = """

        <div class="row center">
   <table id="ffufreport">
        <thead>
          <tr>
              <th>Status</th>
              <th>FUZZ</th>
              <th>URL</th>
              <th>Redirect location</th>
              <th>Position</th>
              <th>Length</th>
              <th>Words</th>
              <th>Lines</th>
          </tr>
        </thead>
        <tbody>
    {% for result in results %}
                <tr class="result-{{ result["status_code"] }}" style="background-color: {{result["HTMLColor"]}};">
                <td><font color="black" class="status-code">{{ result["status_code"] }}</font></td>
                <td>{{ result["FUZZ"] }}</td>
                <td><a href="{{ result["url"] }}">{{ result["url"] }}</a></td>
                <td>{{ result["redirectlocation"] }}</td>
                <td>{{ result["position"] }}</td>
                <td>{{ result["content_length"] }}</td>
                <td>{{ result["content_words"] }}</td>
                <td>{{ result['content_lines'] }}</td>
                </tr>
            {% endfor %}
        </tbody>
      </table>
  </div>
<br /><br />
<br /><br />
<br /><br />

"""

prefix_string ="""
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, maximum-scale=1.0"
    />
    <title>FFUF Report - </title>
    <!-- CSS  -->
    <link
      href="https://fonts.googleapis.com/icon?family=Material+Icons"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
	/>
	<link
	  rel="stylesheet"
	  type="text/css"
	  href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css"
	/>

  </head>


  <body>
    <nav>
      <div class="nav-wrapper">
        <a href="#" class="brand-logo">FFUF</a>
        <ul id="nav-mobile" class="right hide-on-med-and-down">
        </ul>
      </div>
    </nav>


    <main class="section no-pad-bot" id="index-banner">
      <div class="container">
        <br /><br />
        <h1 class="header center ">FFUF Report</h1>
"""

tail_string = """
<br /><br />
</div>
</main>
<!--JavaScript at end of body for optimized loading-->
<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
<script>
$(document).ready( function () {
$('#ffufreport').DataTable();
} );
</script>
<style>
body {
display: flex;
min-height: 100vh;
flex-direction: column;
}
main {
flex: 1 0 auto;
}
</style>
</body>
</html>
"""

def colorizeResults(results):
    for result in results:
        s = result.status_code
        if s >= 200 and s <= 299:
            result["HTMLColor"] = "#adea9e"
            continue
        if s >= 300 and s <= 399:
            result["HTMLColor"] = "#bbbbe6"
            continue
        if s >= 400 and s <= 499:
            result["HTMLColor"] = "#d2cb7e"
            continue
        if s >= 500 and s <= 599:
            result["HTMLColor"] = "#de8dc1"
            continue


def read_csv(input):
    results = [dict(d) for d in csv.DictReader(open(input))]
    # print("results          "   )
    # print('[%s]' % ', '.join(map(str, results)))
    return results

def get_files_list(dir):
    # for dirpath, _, filenames in os.walk(dir):
    #     for f in filenames:
    #         yield os.path.abspath(os.path.join(dirpath, f))
    csvfiles = utils.getFilesInDir(config.ffuf_runtime_processed_dir,".csv")

    return csvfiles

def write_martrix(matrix,output):
    template = Template(template_fraction)

    for results in matrix:
        output.write(template.render(results=results))


def csvfile2html(csvfile:str,html_output:str):
    matrix = [read_csv(csvfile)]
    output = open(html_output,'a')
    output.write(prefix_string)
    write_martrix(matrix, output)
    output.write(tail_string)

    output.close()

def main(input_path,output_html):

    files = get_files_list(input_path)
    # for file in files:
    #   print(file)
    # exit(0)
    matrix = [ read_csv(file) for file in files]

    # print("matrix             " )
    # print('[%s]' % ', '.join(map(str, matrix)))

    output = open(output_html,'a')
    output.write(prefix_string)
    write_martrix(matrix, output)
    output.write(tail_string)

    output.close()


if __name__ == '__main__':
    main()
