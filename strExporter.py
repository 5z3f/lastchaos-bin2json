__author__          = 'agsvn'

from struct import unpack
from lib.reader import BinaryReader

import calendar
import time
import json
import argparse
import os

def readStr(file, fileType, encoding, gamigo, simple):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount, dataMax = br.ReadInt() - 1, br.ReadInt()
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

        if 'strskill' in fileTypeLower:         descCount = 2
        elif 'strquest' in fileTypeLower:       descCount = 3
        elif fileTypeLower in emptyDescFiles:   descCount = 0

        for i in range(dataCount):

            if br.pos() >= br.size():
                break
                
            id = br.ReadInt()
            name = br.ReadString(encoding)
            
            desc = []
            for j in range(descCount):
                desc.append(br.ReadString(encoding))

            if 'stritem' in fileTypeLower and gamigo:
                unknown0 = br.ReadInt()
                unknown1 = br.ReadBytesToString(unknown0, encoding) if unknown0 else 'False'
            
            if not simple:
                chunk = {   
                    "id": id,
                    "name": name
                }
                
                if descCount:
                    chunk["description"] = desc
            else:
                chunk = []
                chunk.append(id)
                chunk.append(name)

                if descCount:
                    chunk.append(desc)

            data.append(chunk)

    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='infile', required=True)
    parser.add_argument('-g', '--gamigo', dest='gamigo', action='store_true')
    parser.add_argument('-s', '--simple', dest='simple', action='store_true', help="Export results as very simple array format")

    args = parser.parse_args()

    fileNameBase = os.path.basename(args.infile)
    fileName = fileNameBase.split('_')[0]
    fileDir = os.path.dirname(args.infile)

    data = readStr(args.infile, fileName, encoding = 'latin1', gamigo = args.gamigo, simple = args.simple)
            
    tpl = {
        "exportInfo": {
            "gameVersion": None,
            "file": fileNameBase,
            "fileType": "lod/string",
            "timestamp": calendar.timegm(time.gmtime())
        },
        "data": data
    }

    with open(f"{fileDir}\{fileNameBase}.json", 'w', encoding='utf8') as f:
        json.dump(tpl if not args.simple else data, f, indent=2, ensure_ascii=False)

    print(f"Exported to: {fileDir}\{fileNameBase}.json")
            
if __name__ == '__main__':
    main()
