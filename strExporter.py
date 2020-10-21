__author__          = 'agsvn'

from struct import unpack
from lib.reader import BinaryReader

import calendar
import time
import json

def readStr(file, fileType, encoding, isGamigo):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount, dataMax = br.ReadInt(), br.ReadInt()
        fileTypeLower = fileType.lower()

        descCount = 1

        emptyDescFiles = [
            'strclient',
            'straffinity',
            'strcombo',
            'strrareoption',
            'strsetitem',
            'stroption'
        ]

        if 'strskill' in fileTypeLower:            descCount = 2
        elif 'strquest' in fileTypeLower:          descCount = 3
        elif fileTypeLower[:-7] in emptyDescFiles: descCount = 0

        
        for i in range(dataCount):
            id = br.ReadInt()
            name = br.ReadString(encoding)

            desc = []
            for j in range(descCount):
                desc.append(br.ReadString(encoding))

            if 'stritem' in fileTypeLower and isGamigo:
                unknown0 = br.ReadInt()
                unknown1 = br.ReadBytesToString(unknown0, 'latin1') if unknown0 else None
            
            chunk = {   
                "id": id,
                "name": name
            }

            if descCount:
                chunk["description"] = desc

            data.append(chunk)

    return data

def main():
    fileType = input('string file [ex. strItem_us.lod]: ')
    folder = "C:\\Program Files (x86)\\gamigo AG\\LastChaosUK_VIP\\Local\\uk\\String"
    file = "{0}\\{1}".format(folder, fileType)

    isGamigo = True

    data = readStr(file, fileType, 'latin1', isGamigo)
            
    tpl = {
        "exportInfo": {
            "gameVersion": None,
            "file": fileType,
            "fileType": "lod/string",
            "timestamp": calendar.timegm(time.gmtime())
        },
        "data": data
    }

    with open('exported/{0}.json'.format(fileType), 'w', encoding='utf8') as f:
        json.dump(tpl, f, indent=2, ensure_ascii=False)

    print("Exported to %s.json" % fileType)
            
if __name__ == '__main__':
    main()