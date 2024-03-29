__author__          = 'agsvn'

from struct import unpack
from math import floor

class BinaryReader:
    def __init__(self, file):
        self.f = file

        self.f.seek(0, 2)
        self.fileBytes = self.f.tell()
        self.f.seek(0, 0)

    def pos(self):
        return self.f.tell()
        
    def size(self):
        return self.fileBytes
    
    def ReadInt(self):
        i = unpack('@I', self.f.read(4))[0]
        return -1 if i == 4294967295 else i

    def ReadInt16(self):
        return unpack('@h', self.f.read(2))[0]

    def ReadInt64(self):
        return unpack('@q', self.f.read(8))[0]

    def ReadIntToList(self, i):
        return [-1 if i == 4294967295 else i for i in list(unpack("@%dI" % i, self.f.read(4*i)))]

    def ReadInt64ToList(self, i):
        return list(unpack("@%dq" % i, self.f.read(8*i)))

    def ReadFloat(self):
        return (floor(unpack('@f', self.f.read(4))[0]*pow(10, 3)+0.5))/pow(10, 3)

    def ReadFloat8(self):
        return round(unpack('@f', self.f.read(4))[0], 8)#(floor(unpack('@f', self.f.read(4))[0]*pow(10, 8)+0.5))/pow(10, 8)

    def ReadPreciseFloat(self):
        return round(unpack('@f', self.f.read(4))[0], 8)

    def ReadFloatToList(self, i):
        return list(unpack('@%df' % i, self.f.read(4*i)))

    def ReadString(self, encoding):
        return self.f.read(unpack('@I', self.f.read(4))[0]).decode(encoding)

    def ReadByte(self):
        return self.f.read(1)

    def ReadBytes(self, i):
        return self.f.read(i)

    def ReadBytesToString(self, count, encoding):
        return self.f.read(count).decode(encoding).rstrip('\x00')

    def ByteToInt(self, bytes):
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result