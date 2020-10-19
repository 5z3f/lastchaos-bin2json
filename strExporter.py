__author__          = 'agsvn'

from struct import unpack
from lib.reader import BinaryReader

import calendar
import time
import json

def readStr(file, fileType, encoding):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount, dataMax = br.ReadInt(), br.ReadInt()
        fileTypeLower = fileType.lower()

        #singleDesc = False
        doubleDesc, tripleDesc, emptyDesc = False, False, False

        emptyDescFiles = [
            'strclient_us.lod',
            'straffinity_us.lod',
            'strcombo_us.lod',
            'strrareoption_us.lod',
            'strsetitem_us.lod',
            'stroption_us.lod'
        ]

        if 'strskill_us.lod' in fileTypeLower:            doubleDesc = True
        elif 'strquest_us.lod' in fileTypeLower:          tripleDesc = True
        elif fileTypeLower in emptyDescFiles:    emptyDesc = True

        
        for i in range(0, dataCount):
            id = br.ReadInt()
            name = br.ReadString(encoding)

            if doubleDesc:      desc = [br.ReadString(encoding), br.ReadString(encoding)]
            elif tripleDesc:    desc = [br.ReadString(encoding), br.ReadString(encoding), br.ReadString(encoding)]
            elif emptyDesc:     desc = []
            else:               desc = [br.ReadString(encoding)]

            chunk = {   
                "stringId": id,
                "stringName": name,
                "stringDescription": None if emptyDesc else desc
            }

            data.append(chunk)

    return data

def main():
    fileType = input('string file [ex. strItem_us.lod]: ')
    folder = "D:\\Games\\LastChaosTestClient\\Local\\us\\String"
    file = "{0}\\{1}".format(folder, fileType)

    data = readStr(file, fileType, 'latin1')
            
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