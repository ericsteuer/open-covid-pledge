import os


input_patent_ids_file_name = "../../../data/patent_ids/sandia.csv"
input_lens_patent_ids_file_name = "./lens-export.csv"

if not os.path.isfile(input_patent_ids_file_name):
  print("File not found: {}\n".format(input_patent_ids_file_name))
  print("Please follow instructions in parser.py file first to generate the {} file".format(input_patent_ids_file_name))
  sys.exit(1)

if not os.path.isfile(input_lens_patent_ids_file_name):
  print("File not found: {}\n".format(input_lens_patent_ids_file_name))
  print("Please follow these instructions:")
  print("1. Go to lens.org and export all of the Sandia related patents using the following search: https://www.lens.org/lens/search?q=applicant:Sandia%%20OR%%20owner:Sandia&l=en&st=true&preview=true")
  print("2. Place the export file at {}".format(input_lens_patent_ids_file_name))
  sys.exit(1)


with open(input_patent_ids_file_name, "r") as f:
  sandia_patent_ids_text = f.read()

with open(input_lens_patent_ids_file_name, "r") as f:
  lens_export_text = f.read().strip()

#
# This manual map was created by:
#
# 1. Running script with empty manual map to get non matching ids
# 2. Going to https://ip.sandia.gov/category.do/categoryID=31 and searching for the id.  Needs to be comma seperated.  E.g. if 10330657 is not matching then search for: 10,330,657
# 3. Copy the title and use in search on lens.org page: https://www.lens.org/lens/search?l=en&st=true&preview=true&view=boolean&q=(applicant:Sandia%20%20OR%20owner:Sandia)%20AND%20title:(Estimation%20of%20conductivity%20for%20nanoporous%20materials)
# 4. Copy and paste the other patent id (recorded for reference) and the given lens_id
#
# n.b. if you don't find it then search by title in case the owner & applicant is not recorded as Sandia in lens.org database e.g.: https://www.lens.org/lens/search?l=en&st=true&preview=true&view=boolean&q=title:(THIOPHOSPHORYLATING%20A%20SATURATED%20HYDROCARBON%20GROUP)
#
manual_map = {
  "10330657": { "other_id": "WO 2016/094153 A2", "lens_id": "112-021-245-517-125" },
  "8439534":  { "other_id": "US 8439534 B1", "lens_id": "117-762-823-930-633" },
  "8103045":  { "other_id": "US 8103045 B2", "lens_id": "035-385-935-894-127" },
  "6427791":  { "other_id": "US 2002/0096369 A1", "lens_id": "105-370-233-952-21X" },
  "5049791":  { "other_id": "US 5049791 A", "lens_id": "088-400-361-418-206" },
  "4237433":  { "other_id": "US 4237433 A", "lens_id": "145-928-852-002-329" },
  "3855105":  { "other_id": "US 3855105 A", "lens_id": "049-900-135-519-881" },
}

lens_export_rows = [r.split(",") for r in lens_export_text.split("\n")]
lens_data = [{"lens_id": l[4], "id": l[3]} for l in lens_export_rows]

lens_id_by_patent_id = {}
for data in lens_data:
  only_number = data["id"].split(" ")[1]
  lens_id_by_patent_id[only_number] = data


# drop the header line
sandia_patent_id_lines = sandia_patent_ids_text.split("\n")[1:]
# remove the trailing `,1,` or `,0,` from each line
sandia_patent_ids = [i[:-3] for i in sandia_patent_id_lines]
matched = []
not_matched = []
for patent_id in sandia_patent_ids:
  if patent_id in lens_id_by_patent_id:
    matched.append(lens_id_by_patent_id[patent_id]["lens_id"])
  elif patent_id in manual_map:
    matched.append(manual_map[patent_id]["lens_id"])
  else:
    not_matched.append(patent_id)

# Note when this are uploaded to lens they must be uploaded without the newlines, the final trailing comma, and no whitespace between the ids
# e.g.: 148-042-950-998-250,087-269-695-607-325,085-796-496-379-851
matched_ids_str = ",\n".join(matched) + ","

with open("../../../data/lens_org_patent_ids/sandia.csv", "w") as f:
  f.write(matched_ids_str)

print("Matched:")
print(matched_ids_str)
print("---")

count_per_lens_id = {}
duplicate_lens_ids = set()
for patent_id in matched:
  if patent_id not in count_per_lens_id:
    count_per_lens_id[patent_id] = 0
  count_per_lens_id[patent_id] += 1
  if count_per_lens_id[patent_id] > 1:
    duplicate_lens_ids.add(patent_id)

if duplicate_lens_ids:
  print("Warning: {} duplicates: {}".format(len(duplicate_lens_ids), duplicate_lens_ids))

print("---")

print("Not matched {}:".format(len(not_matched)))
print(",\n".join(not_matched))
