import mmap
import os
import re
import sys
from pathlib import Path

import pandas as pd

##### ^(?!\w+:\s*")[^\n]*"$

##### (^@?\w+):\s*"([^"\\]*(?:\\[\s\S\n]+?[^"\\]*)*\s*)(")
# problematic files for this pattern:
#   intrface/english/RCS/OPTIONS.STR

folder_from = sys.argv[1]
folder_to = sys.argv[2]

for root, subdirs, files in os.walk(folder_from):
    for file in files:
        if os.path.splitext(file)[1] == ".STR" or os.path.splitext(file)[1] == ".str":
            openfile = open(os.path.join(root, file), 'rb')
            # print(root + file)
            with mmap.mmap(openfile.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                mo = re.findall(br'(^\w+):\s*"([^"\\]*(?:\\[\s\S\n]+?[^"\\]*)*\s*)(")', mm, re.MULTILINE)
                if mo:
                    data = {
                        "id": [],
                        "string": []
                    }

                    for match in mo:
                        data["id"].append(match[0].decode("cp1252"))
                        data["string"].append(match[1].decode("cp1252"))

                        # print(data)

                    # save to excel file
                    df = pd.DataFrame(data)

                    relative = root.replace(folder_from, "")[1:]
                    absolute = os.path.join(folder_to, relative)

                    if not os.path.isdir(absolute):
                        Path(absolute).mkdir(parents=True)

                    target_file = os.path.join(absolute, os.path.splitext(file)[0] + ".xlsx")

                    df.to_excel(target_file, index=False)

                    openfile.close()
