__author__          = 'agsvn'

from struct import unpack
from lib.reader import BinaryReader

import calendar
import time
import json
import bson

def readAction(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            data.append({
                "id": br.ReadInt(),
                "type": br.ByteToInt(br.ReadByte()),
                "job": br.ReadInt(),
                "iconPosition": br.ReadIntToList(3)
            })

    return data

def readAffinity(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            id = br.ReadInt()
            iconPosition = br.ReadIntToList(3)
            needItemId = br.ReadInt()
            needItemCount = br.ReadInt()
            needLevel = br.ReadInt()
            needId = br.ReadInt()
            needPoints = br.ReadInt()

            affinityNpcsData = []
            npcsRows = br.ReadInt()

            for j in range(npcsRows):
                affinityNpcsData.append({
                    "npcId": br.ReadInt(),
                    "npcFlag": br.ReadInt(),
                    "npcStringId": br.ReadInt()
                })

            affinityContributeItemData = []
            contributeItemRows = br.ReadInt()

            for k in range(contributeItemRows):                
                affinityContributeItemData.append({
                    "itemId": br.ReadInt(),
                    "points": br.ReadInt()
                })

            affinityContributeMonsterData = []
            contributeMonsterRows = br.ReadInt()

            for l in range(contributeMonsterRows):                
                affinityContributeMonsterData.append({
                    "npcId": br.ReadInt(),
                    "points": br.ReadInt(),
                    "iconPosition": br.ReadIntToList(3)
                })

            affinityContributeQuestData = []
            contributeQuestRows = br.ReadInt()

            for m in range(contributeQuestRows):                
                affinityContributeQuestData.append({
                    "questId": br.ReadInt(),
                    "points": br.ReadInt()
                })

            affinityRewardItemData = []
            rewardItemRows = br.ReadInt()

            for n in range(rewardItemRows):                
                affinityRewardItemData.append({
                    "itemId": br.ReadInt(),
                    "points": br.ReadInt()
                })

            data.append({
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
            })

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

        for i in range(dataCount):
            id = br.ReadInt()
            name = br.ReadBytesToString(DEF_APET_NAME_LENGTH, 'latin-1')
            type = br.ReadInt()
            itemId = br.ReadInt()
            aiSlot = br.ReadInt()
            mount = br.ReadIntToList(2)
            summonSkill = br.ReadIntToList(2)
            flag = br.ReadInt()
            smc = [br.ReadBytesToString(DEF_SMCFILE_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_SMCFILE_LENGTH, 'latin-1')]
            idle1 = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            idle2 = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            attack1 = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            attack2 = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            damage = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            die = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            walk = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            run = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]
            levelup = [br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1'), br.ReadBytesToString(DEF_APET_ANI_LENGTH, 'latin-1')]

            apetEvolutionData = []
            for j in range(DEF_MAX_EVOLUTION):                
                apetEvolutionData.append({
                    "level": br.ReadInt(),
                    "stamina": br.ReadInt(),
                    "faith": br.ReadInt(),
                    "evPetId": br.ReadInt()
                })

            data.append({
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
            })

    return data

def readCombo(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            data.append({
                "id": br.ReadInt(),
                "gold": br.ReadInt(),
                "iconPosition": br.ReadIntToList(3),
                "skill": br.ByteToInt(br.ReadByte()),
                "point": br.ReadInt()
            })

    return data

def readOption(file):
    DEF_OPTION_MAX_LEVEL = 36

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            data.append({
                "id": br.ReadInt(),
                "type": br.ReadInt(),
                "levels": br.ReadIntToList(DEF_OPTION_MAX_LEVEL)
            })

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

        for i in range(dataCount):
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
            for i in range(QUEST_MAX_CONDITION):
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

            data.append({
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
            })

    return data            

def readSMC(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            id = br.ReadInt()

            if id is not 0:
                meshClass = br.ReadBytesToString(br.ReadInt16(), 'latin1') 
                meshSize = br.ReadInt()

                meshData = []
                for j in range(meshSize):
                    meshNum = br.ReadInt()
                    meshTFNM = br.ReadBytesToString(br.ReadInt16(), 'latin1')
                    texSize = br.ReadInt()

                    meshData.append({
                        "meshNum": meshNum,
                        "meshPath": meshTFNM,
                    })

                    texData = []
                    for k in range(texSize):
                        textureName = br.ReadBytesToString(br.ReadInt16(), 'latin1')
                        texturePath = br.ReadBytesToString(br.ReadInt16(), 'latin1')

                        texData.append({
                            "texName": textureName,
                            "texPath": texturePath,
                        })

                data.append({
                    "id": id - 1,
                    "model": {
                        "modelName": meshClass,
                        "mesh": meshData,
                        "texture": texData
                    }
                })

    return data

def readItemCompose(file):
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()
        composeData = br.ReadIntToList(dataCount)

        return {
            "composeData": composeData
        }

def readLevelupGuide(file):
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()
        levelupData = br.ReadIntToList(dataCount)

        return {
            "levelupMsgData": levelupData
        }

def readNpcChannel(file):
    CHANNEL_ARRAY_SIZE = 16

    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        return {
            "npcIndex": br.ReadInt(),
            "channel": br.ReadIntToList(CHANNEL_ARRAY_SIZE)
        }

def readItemExchange(file):
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount, dataMax = br.ReadInt(), br.ReadInt()

        return {
            "tradeItemData": br.ReadIntToList(dataMax),
        }

def readItemFortune(file):
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        return {
            "itemFortuneData": br.ReadIntToList(dataCount),
        }

def readMoonstone(file):
    MOONSTONE_MAX_GAMIGO = 6
    MOONSTONE_MAX_OTHER = 5

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)

        for i in range(MOONSTONE_MAX_GAMIGO):
            itemCount = br.ReadInt()

            data.append({
                "id": i,
                "items": br.ReadIntToList(itemCount)
            })
            
    return data

def readNotice(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()
        
        for i in range(dataCount):
            id = br.ReadInt()
            enabled = br.ReadInt()
            title = br.ReadString('latin1')
            message = br.ReadString('latin1')
            startTime = br.ReadString('latin1')
            endTime = br.ReadString('latin1')
            cycle = br.ReadInt()
            color = [br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte())]

            data.append({
                "id": id,
                "enabled": enabled,
                "title": title,
                "message": message,
                "time": {
                    "start": startTime,
                    "end": endTime
                },
                "cycle": cycle,
                "color": color
            })
            
    return data

def readStatTooltip(file):
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        return {
            "statTooltipData": br.ReadIntToList(dataCount),
        }

def readRaidObjectList(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            id = br.ReadInt()
            assignZone = br.ReadInt()
            objectType = br.ReadInt()
            objectIndex = br.ReadInt()
            objectName = br.ReadString('latin1')

            data.append({
                "id": id,
                "assignZone": assignZone,
                "object": {
                    "id": objectIndex,
                    "type": objectType,
                    "name": objectName,
                }
            })
            
    return data

def readJewelCompos(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            level = br.ReadInt()
            norCompNas = br.ReadInt()
            caCompNas = br.ReadInt()
            caJewCreate = br.ReadInt()
            norCompVal = br.ReadInt()
            caCompVal = br.ReadInt()
            norUp2 = br.ReadInt()
            norUp3 = br.ReadInt()
            caUp2 = br.ReadInt()
            caUp3 = br.ReadInt()
            norDown1 = br.ReadInt()
            norDown2 = br.ReadInt()
            norDown3 = br.ReadInt()
            caDown1 = br.ReadInt()
            caDown2 = br.ReadInt()
            caDown3 = br.ReadInt()

            chunk = {
                "level": level,
                "gold": {
                    "normalGoldNeed": norCompNas,
                    "chaosGoldNeed": caCompNas
                },
                "normalToChaosComposeProb": caJewCreate,
                "normalComposeProb": norCompVal,
                "chaosComposeProb": caCompVal,
                "normal": {
                    "normalPlus2Prob": norUp2,
                    "normalPlus3Prob": norUp3,
                    "normalMinus1Prob": norDown1,
                    "normalMinus2Prob": norDown2,
                    "normalMinus3Prob": norDown3
                },
                "chaos": {
                    "chaosPlus2Prob": caUp2,
                    "chaosPlus3Prob": caUp3,
                    "chaosMinus1Prob": caDown1,
                    "chaosMinus2Prob": caDown2,
                    "chaosMinus3Prob": caDown3
                }
            }

            data.append(chunk)
            
    return data

def readZoneFlag(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            data.append({
                "npcId": br.ReadInt(),
                "zoneFlag": br.ReadInt64(),
                "extraFlag": br.ReadInt64()
            })

    return data

def readShop(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):
            id = br.ReadInt()
            shopName = br.ReadBytesToString(br.ReadInt(), 'latin1')
            sellRate = br.ReadInt()
            buyRate = br.ReadInt()
            itemCount = br.ReadInt()
            sellItems = br.ReadIntToList(itemCount)

            data.append({
               "npcId": id,
               "shopName": shopName,
               "rate": {
                   "sell": sellRate,
                   "buy": buyRate
               },
               "itemCount": itemCount,
               "items": sellItems
            })

            if dataCount == id:
                break;
                
    return data

def readZoneData(file):
    DEF_EXTRA_MAX = 30

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        zoneCount = br.ReadInt()

        zoneInfoChunk = []
        for i in range(zoneCount):
            zoneType = br.ReadInt()
            extraCnt = br.ReadInt()
            nString = br.ReadInt()
            wldFileName = br.ReadBytesToString(128, 'latin1')
            texName1 = br.ReadBytesToString(64, 'latin1')
            texName2 = br.ReadBytesToString(64, 'latin1')
            fLoadingStep = br.ReadFloat()
            fTer_Lodmul = br.ReadFloat()

            zoneInfoChunk.append({
                "zoneType": zoneType,
                "extraCnt": extraCnt,
                "nString": nString,
                "wldFileName": wldFileName,
                "texture": {
                    "texName1": texName1,
                    "texName2": texName2 
                },
                "loadingStep": fLoadingStep,
                "terLodmul": fTer_Lodmul
            })

        nExtraCnt = br.ReadInt()
        zoneExtraChunk = []
        for i in range(nExtraCnt):
            zoneExtraChunk.append(br.ReadIntToList(DEF_EXTRA_MAX))
            
        data.append({
            "zoneData": zoneInfoChunk,
            "zoneExtra": zoneExtraChunk
        })

    return data

def readChangeItem(file):
    with open(file, "rb") as f:
        br = BinaryReader(f)
        
        changeWeapon = br.ReadIntToList(br.ReadInt())
        changeHelmet = br.ReadIntToList(br.ReadInt())
        changeTop = br.ReadIntToList(br.ReadInt())
        changePants = br.ReadIntToList(br.ReadInt())
        changeGloves = br.ReadIntToList(br.ReadInt())
        changeBoots = br.ReadIntToList(br.ReadInt())

    return {
            "changeWeapon": changeWeapon,
            "changeArmor": {
                "helmet": changeHelmet,
                "top": changeTop,
                "pants": changePants,
                "gloves": changeGloves,
                "boots": changeBoots
            }
    }

def readEvent(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        localeId, dataCount = br.ReadInt(), br.ReadInt()
        
        for i in range(dataCount):
            data.append({
                "eventId": br.ReadInt(),
                "enable": br.ReadInt()
            })

    return {
        "localeId": localeId,
        "event": data
    }

def readTitletool(file):
    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()

        for i in range(dataCount):            
            data.append({
                "id": br.ReadInt(),
                "enable": br.ByteToInt(br.ReadByte()),
                "effect": {
                    "normal": br.ReadBytesToString(64, 'latin1'),
                    "attack": br.ReadBytesToString(64, 'latin1'),
                    "damage": br.ReadBytesToString(64, 'latin1')
                },
                "color": {
                    "text": "{:08x}".format(br.ReadInt()),
                    "background": "{:08x}".format(br.ReadInt()),
                },
                "option": {
                    "id": br.ReadIntToList(5),
                    "level": [br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte()), br.ByteToInt(br.ReadByte())]
                },
                "itemId": br.ReadInt()
            })

    return data

def readItem(file, isGamigo):
    MAX_MAKE_ITEM_MATERIAL = 10
    DEF_SMC_DEFAULT_LENGTH = 64
    DEF_MAX_ORIGIN_OPTION = 10
    DEF_EFFECT_DEFAULT_LENGTH = 32

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()
        print(dataCount)
        
        for i in range(dataCount):  
            data.append({
                "itemId": br.ReadInt(),
                "jobFlag": br.ReadInt(),
                "stack": br.ReadInt(),
                "fame/maxuse": br.ReadInt(),
                "level": br.ReadInt(),
                "flag": br.ReadInt64(),
                "wearing": br.ReadInt(),
                "type": br.ReadInt(),
                "subtype": br.ReadInt(),
                "crafting": {
                    "needItemId": br.ReadIntToList(MAX_MAKE_ITEM_MATERIAL),
                    "needItemCount": br.ReadIntToList(MAX_MAKE_ITEM_MATERIAL)
                },
                "specialSkill": {
                    "needSpecialSkill1": br.ReadIntToList(2),
                    "needSpecialSkill2": br.ReadIntToList(2),
                },
                "iconPosition": br.ReadIntToList(3),
                "num": br.ReadIntToList(4),
                "price": br.ReadInt(),
                "set": br.ReadIntToList(7 if isGamigo else 5),
                "smc": br.ReadBytesToString(DEF_SMC_DEFAULT_LENGTH, 'latin1'),
                "effect": {
                    "normal": br.ReadBytesToString(DEF_EFFECT_DEFAULT_LENGTH, 'latin1'),
                    "attack": br.ReadBytesToString(DEF_EFFECT_DEFAULT_LENGTH, 'latin1'),
                    "damage": br.ReadBytesToString(DEF_EFFECT_DEFAULT_LENGTH, 'latin1')
                },
                "rareOption": {
                    "id": br.ReadInt(),
                    "chance": br.ReadInt(),
                    "optionIds": br.ReadIntToList(DEF_MAX_ORIGIN_OPTION),
                    "optionLevels": br.ReadIntToList(DEF_MAX_ORIGIN_OPTION)
                },
                "rvr": {
                    "type": br.ReadInt(),
                    "grade": br.ReadInt()
                },
                "fortuneId": br.ByteToInt(br.ReadByte()),
                "castleWar": br.ReadInt()
            })
            
    return data

def readMob(file):
    DEF_SMC_LENGTH = 128
    DEF_ANI_LENGTH = 64

    data = []
    with open(file, "rb") as f:
        br = BinaryReader(f)
        dataCount = br.ReadInt()
        print(dataCount)
        
        for i in range(dataCount):
            data.append({
                "npcId": br.ReadInt(),
                "level": br.ReadInt(),
                "health": br.ReadInt(),
                "mana": br.ReadInt(),
                "flag": br.ReadInt(),
                "flag1": br.ReadInt(),
                "speed": {
                    "attack": br.ReadInt(),
                    "walk": br.ReadFloat(),
                    "run": br.ReadFloat(),
                },
                "scale": br.ReadFloat(),
                "attackArea": br.ReadFloat(),
                "size": br.ReadFloat(),
                "master": {
                    "skill": br.ByteToInt(br.ReadByte()),
                    "specialSkill": br.ByteToInt(br.ReadByte())
                },
                "skillEffect": br.ReadIntToList(5),
                "attackType": br.ByteToInt(br.ReadByte()),
                "fire": {
                    "delayCount": br.ByteToInt(br.ReadByte()),
                    "delay": br.ReadFloatToList(4),
                    "object": br.ByteToInt(br.ReadByte()),
                    "speed": br.ReadFloat()
                },
                "skill": {
                    "skill0": [br.ReadInt(), br.ByteToInt(br.ReadByte())],
                    "skill1": [br.ReadInt(), br.ByteToInt(br.ReadByte())]
                },
                "rvr": {
                    "grade": br.ReadInt(),
                    "value": br.ReadInt()
                },
                "bound": br.ReadFloat(),
                "model": {
                    "smc": br.ReadBytesToString(DEF_SMC_LENGTH, 'latin1'),
                    "animation": {
                        "idle": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "walk": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "damage": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "attack": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "die": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "run": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "idle2": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                        "attack2": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                    },
                },
                "fireEffect": {
                    "0": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                    "1": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1'),
                    "2": br.ReadBytesToString(DEF_ANI_LENGTH, 'latin1')
                }

            })

    return data            

def main():
    fileType = input('File [ex: itemAll.lod]: ')
    folder = "C:\\Users\\Administrator\\Desktop\\export"
    file = "{0}\\{1}".format(folder, fileType)
    fileTypeLower = fileType.lower()

    isGamigo = True

    if 'actions' in fileTypeLower:
        data = readAction(file)
    elif 'affinity' in fileTypeLower:
        data = readAffinity(file)
    elif 'bigpet' in fileTypeLower:
        data = readBigpet(file)
    elif 'combo' in fileTypeLower:
        data = readCombo(file)
    elif 'option' in fileTypeLower:
        data = readOption(file)
    elif 'quest' in fileTypeLower:
        data = readQuest(file)
    elif 'smc' in fileTypeLower:
        data = readSMC(file)
    elif 'itemcompose' in fileTypeLower:
        data = readItemCompose(file)
    elif 'levelup_guide' in fileTypeLower:
        data = readLevelupGuide(file)
    elif 'npc_channel' in fileTypeLower:
        data = readNpcChannel(file)
    elif 'item_exchange' in fileTypeLower:
        data = readItemExchange(file)
    elif 'itemfortune' in fileTypeLower:
        data = readItemFortune(file)
    elif 'moonstone' in fileTypeLower:
        data = readMoonstone(file)
    elif 'notice' in fileTypeLower:
        data = readNotice(file)
    elif 'stattooltip' in fileTypeLower:
        data = readStatTooltip(file)
    elif 'raidobjectlist' in fileTypeLower:
        data = readRaidObjectList(file)
    elif 'jewelcompos' in fileTypeLower:
        data = readJewelCompos(file)
    elif 'zoneflag' in fileTypeLower:
        data = readZoneFlag(file)
    elif 'shop' in fileTypeLower:
        data = readShop(file)
    elif 'zone_data' in fileTypeLower:
        data = readZoneData(file)
    elif 'change_item' in fileTypeLower:
        data = readChangeItem(file)
    elif 'event' in fileTypeLower:
        data = readEvent(file)
    elif 'titletool' in fileTypeLower:
        data = readTitletool(file)
    elif 'itemall' in fileTypeLower:
        data = readItem(file, isGamigo)
    elif 'moball' in fileTypeLower:
        data = readMob(file)

    tpl = {
        "exportInfo": {
            "gameVersion": None,
            "file": fileType,
            "fileType": 'bin/data' if '.bin' in fileType else "lod/data",
            "timestamp": calendar.timegm(time.gmtime())
        },
        "data": data
    }

    with open('exported/{0}.json'.format(fileType), 'w', encoding='utf8') as f:
       json.dump(tpl, f, indent=2, ensure_ascii=False)

    #with open('exported/{0}.bson'.format(fileType), 'wb') as bson_file:
    #    bson_file.write(bson.dumps(tpl))

    print("Exported to {0}.json".format(fileType))
            
if __name__ == '__main__':
    main()