__author__          = 'agsvn'

from struct import unpack
import array
import calendar
import time
import json

class BinaryReader:
    def ReadInt(self, f):
        return unpack('I', f.read(4))[0]

    def ReadFloat(self, f):
        return unpack('f', f.read(4))[0]

    def ReadString(self, f):
        return f.read(unpack('I', f.read(4))[0])

    def ReadShort(self, f):
        return unpack('h', f.read(2))[0]

def readStr(file, fileType):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader()
        rows, max = br.ReadInt(f), br.ReadInt(f)
        
        print("[item] reading {0} {1} string rows".format(rows, fileType))
        for i in range(0, rows):
            idx = br.ReadInt(f)
            name = br.ReadString(f).decode('latin-1')

            if fileType == 'skill':
                desc = [br.ReadString(f).decode('latin-1'), br.ReadString(f).decode('latin-1')]
            elif fileType == 'quest':
                desc = [br.ReadString(f).decode('latin-1'), br.ReadString(f).decode('latin-1'), br.ReadString(f).decode('latin-1')]
            elif fileType == 'client' or fileType == 'affinity' or fileType == 'combo' or fileType == 'rareoption' or fileType == 'setitem' or fileType == 'option':
                desc = []
            else:
                desc = br.ReadString(f).decode('latin-1')


            chunk = {   
                "stringId": idx,
                "stringName": name,
                "stringDescription": desc if len(desc) else None
            }

            data.append(chunk)

    return data
    


def main():
    fileType = input('\t string file type [item, npcname, skill, quest]: ')
    folder = "D:\\Games\\LastChaosTestClient\\Local\\us\\String"
    file = "{0}\\str{1}_us.lod".format(folder, fileType)

    data = readStr(file, fileType)
            
    tpl = {
        "exportInfo": {
            "gameVersion": 'branch-03.413.392',
            "fileType": '{0}String'.format(fileType),
            "date": calendar.timegm(time.gmtime())
        },
        "data": data
    }

    with open('str{0}_us.json'.format(fileType.capitalize()), 'w', encoding='utf8') as f:
        json.dump(tpl, f, indent=2, ensure_ascii=False)

    print("[{0}] Exported to str{1}_us.json".format(fileType, fileType.capitalize()))
            
if __name__ == '__main__':
    main()