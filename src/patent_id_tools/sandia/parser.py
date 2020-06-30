import os
import re
import sys


class PatentsHTMLFile:
  def __init__(self, input_file_name, hint_source_url, min_expected_patent_count):
    self.input_file_name = input_file_name
    self.hint_source_url = hint_source_url
    self.min_expected_patent_count = min_expected_patent_count


public_patents = PatentsHTMLFile(
  input_file_name="2020-06-30 Sandia public patents.html",
  hint_source_url="https://ip.sandia.gov/category.do/categoryID=32",
  min_expected_patent_count=43)

RTDP_patents = PatentsHTMLFile(
  input_file_name="2020-06-30 Sandia RTDP patents.html",
  hint_source_url="https://ip.sandia.gov/category.do/categoryID=31",
  min_expected_patent_count=1048)


def check_has_file(patents):
  if not os.path.isfile(patents.input_file_name):
    print("File not found: {}\n".format(patents.input_file_name))
    print("1.  Navigate to {}".format(patents.hint_source_url))
    print("2.  Under \"Show Advanced Options\" change \"Results Per Page\" to \"all\"")
    print("3.  Press search and wait for the page to reload")
    print("4.  Save the file as {} and try running this script again".format(patents.input_file_name))
    sys.exit(1)

check_has_file(public_patents)
check_has_file(RTDP_patents)


pattern = re.compile(r'<a href="/patent.do/ID=\d+">([\d,]+)')

def parse_file(patents):
  with open(patents.input_file_name) as f:
    html = f.read()

  patent_id_matches = pattern.findall(html)

  expected = patents.min_expected_patent_count
  actual = len(patent_id_matches)
  if (actual < expected):
    print("Fewer than expected ({} vs {}) patents parsed from {}.\nChange to \"Results Per Page: all\" under \"Show Advanced Options\".".format(actual, expected, patents.hint_source_url))
    sys.exit(1)

  patent_ids = []

  for match in patent_id_matches[:]:

    patent_id = match.replace(",", "")
    patent_ids.append(patent_id)

  # Find duplicates
  deduped_patent_ids = []
  duplicates = []

  for patent_id in patent_ids:
    if patent_id not in deduped_patent_ids:
      deduped_patent_ids.append(patent_id)
    else:
      duplicates.append(patent_id)

  if duplicates:
    print("INFO: Found {} duplicates in {}: {}".format(len(duplicates), patents.input_file_name, duplicates))

  return deduped_patent_ids


public_patent_ids = parse_file(public_patents)
RTDP_patent_ids = parse_file(RTDP_patents)

# Write to file
with open("../../../data/patent_ids/sandia.csv", "w") as f:
  f.write("patent_id,public,")

  for patent_id in public_patent_ids:
    f.write("\n{},1,".format(patent_id))

  for patent_id in RTDP_patent_ids:
    f.write("\n{},0,".format(patent_id))
