
import mmap
import os
import re
import pandas as pd

walk_dir = "./SOURCE"
paste_dir = "./SOURCE-Intermediate"

##### ^(?!\w+:\s*")[^\n]*"$

##### (^@?\w+):\s*"([^"\\]*(?:\\[\s\S\n]+?[^"\\]*)*\s*)(")
# problematic files for this pattern:
#   intrface/english/RCS/OPTIONS.STR

for root, subdirs, files in os.walk(walk_dir):
    for file in files:
        if os.path.splitext(file)[1] == ".STR" or os.path.splitext(file)[1] == ".str":
            openfile = open(os.path.join(root, file), 'rb')
            print(root + file)
            with mmap.mmap(openfile.fileno(), length=0, access=mmap.ACCESS_READ) as mm:

                mo = re.findall(br'(^\w+):\s*"([^"\\]*(?:\\[\s\S\n]+?[^"\\]*)*\s*)(")', mm, re.MULTILINE)

                if mo:
                    for match in mo:
                        data["id"].append(match[0].decode("cp1252"))
                        data["string"].append(match[1].decode("cp1252"))

                data = {
                    "id": [],
                    "string": []
                }

                print(data)

                # save to excel file
                df = pd.DataFrame(data)
                df.to_excel(os.path.join(root, os.path.splitext(file)[0]) + ".xlsx", index=False)

                openfile.close()




