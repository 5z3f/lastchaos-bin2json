__author__          = 'agsvn'

from struct import unpack
import array
import calendar
import time
import json

class BinaryReader:
    def __init__(self, file):
        self.f = file

    def ReadInt(self):
        i = unpack('@I', self.f.read(4))[0]
        return -1 if i == 4294967295 else i

    def ReadInt64(self):
        return unpack('@q', self.f.read(8))[0]

    def ReadIntToList(self, i):
        return [-1 if i == 4294967295 else i for i in list(unpack("@%dI" % i, self.f.read(4*i)))]

    def ReadInt64ToList(self, i):
        return list(unpack("@%dq" % i, self.f.read(8*i)))

    def ReadFloat(self):
        return unpack('@f', self.f.read(4))[0]

    def ReadString(self):
        return self.f.read(unpack('@I', self.f.read(4))[0])

    def ReadByte(self):
        return self.f.read(1)

    def ReadBytes(self, count, encoding):
        return self.f.read(count).decode(encoding).rstrip('\x00')

    def ByteToInt(self, bytes):
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result

def readAction(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        intDataCount = br.ReadInt()

        for i in range(0, intDataCount):
            chunk = {
                "id": br.ReadInt(),
                "type": br.ByteToInt(br.ReadByte()),
                "job": br.ReadInt(),
                "iconPosition": br.ReadIntToList(3)
            }

            data.append(chunk)

    return data

def readAffinity(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        intDataCount = br.ReadInt()

        for i in range(0, intDataCount):
            intId = br.ReadInt()
            intIconPosition = br.ReadIntToList(3)
            intNeedItemId = br.ReadInt()
            intNeedItemCount = br.ReadInt()
            intNeedLevel = br.ReadInt()
            intNeedId = br.ReadInt()
            intNeedPoints = br.ReadInt()

            affinityNpcsData = []
            intNpcsRows = br.ReadInt()

            for j in range(0, intNpcsRows):
                affinityNpc = {
                    "npcId": br.ReadInt(),
                    "npcFlag": br.ReadInt(),
                    "npcStringId": br.ReadInt()
                }

                affinityNpcsData.append(affinityNpc)

            affinityContributeItemData = []
            intContributeItemRows = br.ReadInt()

            for k in range(0, intContributeItemRows):
                affinityContributeItem = {
                    "itemId": br.ReadInt(),
                    "points": br.ReadInt()
                }
                
                affinityContributeItemData.append(affinityContributeItem)

            affinityContributeMonsterData = []
            intContributeMonsterRows = br.ReadInt()

            for l in range(0, intContributeMonsterRows):
                affinityContributeMonster = {
                    "npcId": br.ReadInt(),
                    "points": br.ReadInt(),
                    "iconPosition": br.ReadIntToList(3)
                }
                
                affinityContributeMonsterData.append(affinityContributeMonster)

            affinityContributeQuestData = []
            intContributeQuestRows = br.ReadInt()

            for m in range(0, intContributeQuestRows):
                affinityContributeQuest = {
                    "questId": br.ReadInt(),
                    "points": br.ReadInt()
                }
                
                affinityContributeQuestData.append(affinityContributeQuest)

            affinityRewardItemData = []
            intRewardItemRows = br.ReadInt()

            for n in range(0, intRewardItemRows):
                affinityRewardItem = {
                    "itemId": br.ReadInt(),
                    "points": br.ReadInt()
                }
                
                affinityRewardItemData.append(affinityRewardItem)

            chunk = {
                "id": intId,
                "iconPosition": intIconPosition,
                "itemRequirements": {
                    "itemId": intNeedItemId,
                    "itemCount": intNeedItemCount,
                },
                "requiredLevel": intNeedLevel,
                "requirements": {
                    "affinityId": intNeedId,
                    "affinityPoints": intNeedPoints,
                },
                "npcs": affinityNpcsData,
                "contributeItems": affinityContributeItemData,
                "contributeMonsters": affinityContributeMonsterData,
                "contributeQuests": affinityContributeQuestData,
                "rewardItems": affinityRewardItemData
            }

            data.append(chunk)

    return data

def readBigpet(file):
    DEF_APET_NAME_LENGTH = 20
    DEF_SMCFILE_LENGTH = 64
    DEF_APET_ANI_LENGTH = 32
    DEF_MAX_EVOLUTION = 4

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        intDataCount = br.ReadInt()

        for i in range(0, intDataCount):
            intId = br.ReadInt()
            strName = br.ReadBytes(DEF_APET_NAME_LENGTH, 'latin-1')
            intType = br.ReadInt()
            intItemId = br.ReadInt()
            intAISlot = br.ReadInt()
            intMount = br.ReadIntToList(2)
            intSummonSkill = br.ReadIntToList(2)
            intFlag = br.ReadInt()
            strSMC = [br.ReadBytes(DEF_SMCFILE_LENGTH, 'latin-1'), br.ReadBytes(DEF_SMCFILE_LENGTH, 'latin-1')]
            strIdle1 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strIdle2 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strAttack1 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strAttack2 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strDamage = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strDie = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strWalk = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strRun = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            strLevelup = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]

            apetEvolutionData = []

            for j in range(0, DEF_MAX_EVOLUTION):
                apetEvolution = {
                    "level": br.ReadInt(),
                    "stamina": br.ReadInt(),
                    "faith": br.ReadInt(),
                    "evPetId": br.ReadInt()
                }
                
                apetEvolutionData.append(apetEvolution)

            chunk = {
                "id": intId,
                "name": strName,
                "type": intType,
                "itemId": intItemId,
                "aiSlot": intAISlot,
                "mount": intMount,
                "summonSkill": intSummonSkill,
                "flag": intFlag,
                "model": {
                    "smc": strSMC,
                    "animation": {
                        "idle1": strIdle1,
                        "idle2": strIdle2,
                        "attack1": strAttack1,
                        "attack2": strAttack2,
                        "damage": strDamage,
                        "die": strDie,
                        "walk": strWalk,
                        "run": strRun,
                        "levelup": strLevelup
                    }
                },
                "evolutionData": apetEvolutionData,
                # DEF_MAX_ACCEXP = 1
                "accExpData": {
                    "maxAccParam1": br.ReadInt(),
                    "maxAccParam2": br.ReadInt(),
                    "accRateParam1": br.ReadInt(),
                    "accRateParam2": br.ReadInt()
                }
            }

            #br.ReadInt()
            
            #print(chunk)
            data.append(chunk)

    return data

def readCombo(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        intDataCount = br.ReadInt()

        for i in range(0, intDataCount):
            chunk = {
                "id": br.ReadInt(),
                "gold": br.ReadInt(),
                "iconPosition": br.ReadIntToList(3),
                "skill": br.ByteToInt(br.ReadByte()),
                "point": br.ReadInt()
            }

            data.append(chunk)

    return data

def readOption(file):
    DEF_OPTION_MAX_LEVEL = 36

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        intDataCount = br.ReadInt()

        for i in range(0, intDataCount):
            chunk = {
                "id": br.ReadInt(),
                "type": br.ReadInt(),
                "levels": br.ReadIntToList(DEF_OPTION_MAX_LEVEL)
            }

            data.append(chunk)

    return data            

def readQuest(file):
    QUEST_MAX_NEED_ITEM = 5
    QUEST_MAX_CONDITION = 3
    QUEST_MAX_CONDITION_DATA = 4
    QUEST_MAX_PRIZE = 5
    QUEST_MAX_OPTPRIZE = 7

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        intDataCount = br.ReadInt()

        for i in range(0, intDataCount):
            intId = br.ReadInt()
            intType1 = br.ReadInt()
            intType2 = br.ReadInt()
            intStartType = br.ReadInt()
            intStartData = br.ReadInt()
            intPrizeNpc = br.ReadInt()
            intPreQuestNo = br.ReadInt()
            intStartNpcZoneNo = br.ReadInt()
            intPrizeNpcZoneNo = br.ReadInt()
            intNeedExp = br.ReadInt()
            intNeedMinLevel = br.ReadInt()
            intNeedMaxLevel = br.ReadInt()
            intNeedJob = br.ReadInt()
            intNeedMinPenalty = br.ReadInt()
            intNeedMaxPenalty = br.ReadInt()
            arrNeedItemIndex = br.ReadIntToList(QUEST_MAX_NEED_ITEM)
            arrNeedItemCount = br.ReadIntToList(QUEST_MAX_NEED_ITEM)
            intRVRType = br.ReadInt()
            intRVRGrade = br.ReadInt()

            arrConditionType = br.ReadIntToList(QUEST_MAX_CONDITION)
            arrConditionIndex = br.ReadIntToList(QUEST_MAX_CONDITION)
            arrConditionNum = br.ReadIntToList(QUEST_MAX_CONDITION)

            arrConditionData = []
            for i in range(0, QUEST_MAX_CONDITION):
                arrConditionData.append(br.ReadIntToList(QUEST_MAX_CONDITION_DATA))
            
            arrPrizeType = br.ReadIntToList(QUEST_MAX_PRIZE)
            arrPrizeIndex = br.ReadIntToList(QUEST_MAX_PRIZE)
            arrPrizeData = br.ReadInt64ToList(QUEST_MAX_PRIZE)
            
            intOptionPrize = br.ReadInt()
            arrOptPrizeType = br.ReadIntToList(QUEST_MAX_OPTPRIZE)
            arrOptPrizeIndex = br.ReadIntToList(QUEST_MAX_OPTPRIZE)
            arrOptPrizeData = br.ReadIntToList(QUEST_MAX_OPTPRIZE)
            arrOptPrizePlus = br.ReadIntToList(QUEST_MAX_OPTPRIZE)

            intPartyscale = br.ReadInt()
            intOnlyOptPrize = br.ReadInt()

            chunk = {
                "id": intId,
                "questType": {
                    "type1": intType1,
                    "type2": intType2
                },
                "startType": intStartType,
                "startNpc": intStartData,
                "prizeNpc": intPrizeNpc,
                "preQuestId": intPreQuestNo,
                "startNpcZoneId": intStartNpcZoneNo,
                "prizeNpcZoneId": intPrizeNpcZoneNo,
                "needExp": intNeedExp,
                "minLevel": intNeedMinLevel,
                "maxLevel": intNeedMaxLevel,
                "requiredJob": intNeedJob,
                "pkPenaltyMin": intNeedMinPenalty,
                "pkPenaltyMax": intNeedMaxPenalty,
                "requiredItems": {
                    "itemIds": arrNeedItemIndex,
                    "itemCount": arrNeedItemCount
                },
                "rvrTypeId": intRVRType,
                "rvrGradeId": intRVRGrade,
                "condition": {
                    "types": arrConditionType,
                    "ids": arrConditionIndex,
                    "count": arrConditionNum,
                    "data": arrConditionData
                },
                "prize": {
                    "types": arrPrizeType,
                    "ids": arrPrizeIndex,
                    "data": arrPrizeData,
                    "optionPrize": intOptionPrize,
                    "optionPrizeType": arrOptPrizeType,
                    "optionPrizeIndex": arrOptPrizeIndex,
                    "optionPrizeData": arrOptPrizeData,
                    "optionPrizePlus": arrOptPrizePlus
                },
                "groupType": intPartyscale,
                "onlyOptPrize": intOnlyOptPrize
            }

            data.append(chunk)

    return data            



def main():
    fileType = input('\t lod file type [itemAll.lod, actions.lod]: ')
    folder = "C:\\Users\\Administrator\\Desktop\\export"
    file = "{0}\\{1}".format(folder, fileType)

    if 'actions' in fileType:
        data = readAction(file)
    elif 'affinity' in fileType:
        data = readAffinity(file)
    elif 'bigpet' in fileType:
        data = readBigpet(file)
    elif 'combo' in fileType:
        data = readCombo(file)
    elif 'option' in fileType:
        data = readOption(file)
    elif 'quest' in fileType:
        data = readQuest(file)
        
    tpl = {
        "exportInfo": {
            "gameVersion": None,
            "fileType": '{0}'.format(fileType),
            "date": calendar.timegm(time.gmtime())
        },
        "data": data
    }

    with open('{0}.json'.format(fileType), 'w', encoding='utf8') as f:
       json.dump(tpl, f, indent=2, ensure_ascii=False)

    print("[{0}] Exported to {0}.json".format(fileType))
            
if __name__ == '__main__':
    main()