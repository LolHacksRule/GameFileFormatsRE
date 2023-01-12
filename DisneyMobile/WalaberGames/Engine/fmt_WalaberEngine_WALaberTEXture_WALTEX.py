#Where's My Water? (2013+ entries) *.WALTEX
#By LolHacksRule, my first Noesis script! Ideas taken from Exient XGS (Engine) Texture script.

#Fixed texture offset read from 2020
USE_HACK = True

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Where's My Water? (2013+) [WALaber (Engine) TEXture]", ".waltex")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    bs = NoeBitStream(texData)
    #Check for WALT header
    if noeStrFromBytes(bs.readBytes(4)) != "WALT": return 0
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    bs.seek(0x4)
    ver = bs.readByte() #Afaik I only found 01
    texFmt = bs.readByte()
    texWidth = bs.readUShort()
    texHeight = bs.readUShort()
    print(texWidth, "x", texHeight)
    texData = texData[0x10:] #Do this so we read textures at 0x10
    #Idk how to fix a portion of individual textures without bruteforcing so here's a hack, maybe this might break other textures idk
    if USE_HACK:
        if (texWidth != 32 and texWidth != 64 and texWidth != 128 and texWidth != 256 and texWidth != 512 and texWidth != 1024 and texWidth != 2048 and texWidth != 4096): #Don't break WMM
            print("Applying hack!")
            #if (texWidth == 84 or texWidth == 203 or texWidth == 205 or texWidth == 245):
            if (texWidth < 32):
                texWidth = 32
            if (texWidth > 32 and texWidth < 64):
                texWidth = 64
            #if (texWidth == 257 or texWidth == 271 or texWidth == 288 or texWidth == 361 or texWidth == 362 or texWidth == 415 or texWidth == 439 or texWidth == 444 or texWidth == 459 or texWidth == 490):
            if (texWidth > 64 and texWidth < 128):
                texWidth = 128
            if (texWidth > 128 and texWidth < 256):
                texWidth = 256
            if (texWidth > 256 and texWidth < 512):
                texWidth = 512
            #if (texWidth == 513 or texWidth == 576 or texWidth == 542 or texWidth == 545 or texWidth == 721 or texWidth == 723 or texWidth == 724 or texWidth == 725 or texWidth == 750 or texWidth == 794 or texWidth == 831 or texWidth == 888 or texWidth == 878 or texWidth == 917 or texWidth == 1000):
            if (texWidth > 512 and texWidth < 1024):
                texWidth = 1024
            #if (texWidth == 1025 or texWidth == 1089 or texWidth == 1443 or texWidth == 1501 or texWidth == 2000 or texWidth == 2001):
            if (texWidth > 1024 and texWidth < 2048): #Don't break WMM
                texWidth = 2048
            print("HACKED:", texWidth, "x", texHeight)
    #RGBA8888 texture
    if texFmt == 0x0:    
        print("RGBA8888: format detected")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGB565 texture
    ##elif texFmt == 0x?:    
        #print("RGB565: format detected")
        ##texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "b5 g6 r5")
        ##texFmt = noesis.NOESISTEX_RGB24
    #RGBA5551 texture
    ##elif texFmt == 0x?:    
        #print("RGBA5551: format detected")
        ##texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a1 b5 g5 r5")
        ##texFmt = noesis.NOESISTEX_RGBA32
    #RGBA4444 texture
    elif texFmt == 0x3:    
        print("RGBA4444: format detected") #this byte is inconsistent
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a4 b4 g4 r4")
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return None
    #print("If the image doesn't look right, set the swap flag and try again.")
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1