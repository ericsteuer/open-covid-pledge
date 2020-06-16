import os
import re
import sys


input_file_name = "patents.html"

if not os.path.isfile(input_file_name):
  print("File not found: {}\n".format(input_file_name))
  print("1.  Navigate to https://ip.sandia.gov/category.do/categoryID=31")
  print("2.  Under \"Show Advanced Options\" change \"Results Per Page\" to \"all\"")
  print("3.  Press search and wait for the page to reload")
  print("4.  Save the file as {} and try running this script again".format(input_file_name))
  sys.exit(1)


pattern = re.compile(r'<a href="/patent.do/ID=\d+">([\d,]+)')

with open(input_file_name) as f:
  html = f.read()

patent_id_matches = pattern.findall(html)

if (len(patent_id_matches) < 1000):
  print("Change to \"Results Per Page: all\" under \"Show Advanced Options\" on https://ip.sandia.gov/category.do/categoryID=31")

patent_ids = []

for match in patent_id_matches[:]:

  patent_id = match.replace(",", "")
  patent_ids.append(patent_id)


with open("../../../data/patent_ids/sandia.csv", "w") as f:
  f.write(",\n".join(patent_ids) + ",")
