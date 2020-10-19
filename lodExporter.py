__author__          = 'agsvn'

from struct import unpack
from lib.reader import BinaryReader

import calendar
import time
import json

def readAction(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(0, dataCount):
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
        dataCount = br.ReadInt()

        for i in range(0, dataCount):
            id = br.ReadInt()
            iconPosition = br.ReadIntToList(3)
            needItemId = br.ReadInt()
            needItemCount = br.ReadInt()
            needLevel = br.ReadInt()
            needId = br.ReadInt()
            needPoints = br.ReadInt()

            affinityNpcsData = []
            npcsRows = br.ReadInt()

            for j in range(0, npcsRows):
                affinityNpc = {
                    "npcId": br.ReadInt(),
                    "npcFlag": br.ReadInt(),
                    "npcStringId": br.ReadInt()
                }

                affinityNpcsData.append(affinityNpc)

            affinityContributeItemData = []
            contributeItemRows = br.ReadInt()

            for k in range(0, contributeItemRows):
                affinityContributeItem = {
                    "itemId": br.ReadInt(),
                    "points": br.ReadInt()
                }
                
                affinityContributeItemData.append(affinityContributeItem)

            affinityContributeMonsterData = []
            contributeMonsterRows = br.ReadInt()

            for l in range(0, contributeMonsterRows):
                affinityContributeMonster = {
                    "npcId": br.ReadInt(),
                    "points": br.ReadInt(),
                    "iconPosition": br.ReadIntToList(3)
                }
                
                affinityContributeMonsterData.append(affinityContributeMonster)

            affinityContributeQuestData = []
            contributeQuestRows = br.ReadInt()

            for m in range(0, contributeQuestRows):
                affinityContributeQuest = {
                    "questId": br.ReadInt(),
                    "points": br.ReadInt()
                }
                
                affinityContributeQuestData.append(affinityContributeQuest)

            affinityRewardItemData = []
            rewardItemRows = br.ReadInt()

            for n in range(0, rewardItemRows):
                affinityRewardItem = {
                    "itemId": br.ReadInt(),
                    "points": br.ReadInt()
                }
                
                affinityRewardItemData.append(affinityRewardItem)

            chunk = {
                "id": id,
                "iconPosition": iconPosition,
                "itemRequirements": {
                    "itemId": needItemId,
                    "itemCount": needItemCount,
                },
                "requiredLevel": needLevel,
                "requirements": {
                    "affinityId": needId,
                    "affinityPoints": needPoints,
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
        dataCount = br.ReadInt()

        for i in range(0, dataCount):
            id = br.ReadInt()
            name = br.ReadBytes(DEF_APET_NAME_LENGTH, 'latin-1')
            type = br.ReadInt()
            itemId = br.ReadInt()
            aiSlot = br.ReadInt()
            mount = br.ReadIntToList(2)
            summonSkill = br.ReadIntToList(2)
            flag = br.ReadInt()
            smc = [br.ReadBytes(DEF_SMCFILE_LENGTH, 'latin-1'), br.ReadBytes(DEF_SMCFILE_LENGTH, 'latin-1')]
            idle1 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            idle2 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            attack1 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            attack2 = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            damage = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            die = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            walk = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            run = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]
            levelup = [br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytes(DEF_APET_ANI_LENGTH, 'latin-1')]

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
                "id": id,
                "name": name,
                "type": type,
                "itemId": itemId,
                "aiSlot": aiSlot,
                "mount": mount,
                "summonSkill": summonSkill,
                "flag": flag,
                "model": {
                    "smc": smc,
                    "animation": {
                        "idle1": idle1,
                        "idle2": idle2,
                        "attack1": attack1,
                        "attack2": attack2,
                        "damage": damage,
                        "die": die,
                        "walk": walk,
                        "run": run,
                        "levelup": levelup
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
        dataCount = br.ReadInt()

        for i in range(0, dataCount):
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
        dataCount = br.ReadInt()

        for i in range(0, dataCount):
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
        dataCount = br.ReadInt()

        for i in range(0, dataCount):
            id = br.ReadInt()
            type1 = br.ReadInt()
            type2 = br.ReadInt()
            startType = br.ReadInt()
            startData = br.ReadInt()
            prizeNpc = br.ReadInt()
            preQuestNo = br.ReadInt()
            startNpcZoneNo = br.ReadInt()
            prizeNpcZoneNo = br.ReadInt()
            needExp = br.ReadInt()
            needMinLevel = br.ReadInt()
            needMaxLevel = br.ReadInt()
            needJob = br.ReadInt()
            needMinPenalty = br.ReadInt()
            needMaxPenalty = br.ReadInt()
            needItemIndex = br.ReadIntToList(QUEST_MAX_NEED_ITEM)
            needItemCount = br.ReadIntToList(QUEST_MAX_NEED_ITEM)
            rvrType = br.ReadInt()
            rvrGrade = br.ReadInt()

            conditionType = br.ReadIntToList(QUEST_MAX_CONDITION)
            conditionIndex = br.ReadIntToList(QUEST_MAX_CONDITION)
            conditionNum = br.ReadIntToList(QUEST_MAX_CONDITION)

            conditionData = []
            for i in range(0, QUEST_MAX_CONDITION):
                conditionData.append(br.ReadIntToList(QUEST_MAX_CONDITION_DATA))
            
            prizeType = br.ReadIntToList(QUEST_MAX_PRIZE)
            prizeIndex = br.ReadIntToList(QUEST_MAX_PRIZE)
            prizeData = br.ReadInt64ToList(QUEST_MAX_PRIZE)
            
            optionPrize = br.ReadInt()
            optPrizeType = br.ReadIntToList(QUEST_MAX_OPTPRIZE)
            optPrizeIndex = br.ReadIntToList(QUEST_MAX_OPTPRIZE)
            optPrizeData = br.ReadIntToList(QUEST_MAX_OPTPRIZE)
            optPrizePlus = br.ReadIntToList(QUEST_MAX_OPTPRIZE)

            partyScale = br.ReadInt()
            onlyOptPrize = br.ReadInt()

            chunk = {
                "id": id,
                "questType": {
                    "type1": type1,
                    "type2": type2
                },
                "startType": startType,
                "startNpc": startData,
                "prizeNpc": prizeNpc,
                "preQuestId": preQuestNo,
                "startNpcZoneId": startNpcZoneNo,
                "prizeNpcZoneId": prizeNpcZoneNo,
                "needExp": needExp,
                "minLevel": needMinLevel,
                "maxLevel": needMaxLevel,
                "requiredJob": needJob,
                "pkPenaltyMin": needMinPenalty,
                "pkPenaltyMax": needMaxPenalty,
                "requiredItems": {
                    "itemIds": needItemIndex,
                    "itemCount": needItemCount
                },
                "rvrTypeId": rvrType,
                "rvrGradeId": rvrGrade,
                "condition": {
                    "types": conditionType,
                    "ids": conditionIndex,
                    "count": conditionNum,
                    "data": conditionData
                },
                "prize": {
                    "types": prizeType,
                    "ids": prizeIndex,
                    "data": prizeData,
                    "optionPrize": optionPrize,
                    "optionPrizeType": optPrizeType,
                    "optionPrizeIndex": optPrizeIndex,
                    "optionPrizeData": optPrizeData,
                    "optionPrizePlus": optPrizePlus
                },
                "groupType": partyScale,
                "onlyOptPrize": onlyOptPrize
            }

            data.append(chunk)

    return data            



def main():
    fileType = input('lod file type [itemAll.lod, actions.lod]: ')
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
            "file": fileType,
            "fileType": "lod/data",
            "timestamp": calendar.timegm(time.gmtime())
        },
        "data": data
    }

    with open('{0}.json'.format(fileType), 'w', encoding='utf8') as f:
       json.dump(tpl, f, indent=2, ensure_ascii=False)

    print("Exported to {0}.json".format(fileType))
            
if __name__ == '__main__':
    main()