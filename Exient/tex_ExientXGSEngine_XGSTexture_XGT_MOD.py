#Mod by LolHacksRule, Acewell for original script https://www.zenhax.com/download/file.php?id=8466
#Added support for RGB565, RGBA4444, PVRTC4BPP, ETC2_RGB
#TODO: Add code to detect swizzle
#It's not possible to detect Wii U/legacy textures right away so I commented sections that are moddable

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Exient XGS Engine Texture", ".xgt_dxt;.xgt;.xgt_etc;.xgt_pvr")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    if noeStrFromBytes(bs.readBytes(4)) != "XGST": return 0
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    bs.seek(0x4)
    dataOffset = bs.readUShort()
    headerSZ = bs.readUShort()
    numMips = bs.readUByte()
    flag1 = bs.readByte()
    flag2 = bs.readByte()
    flag3 = bs.readByte()
    imgFmt = bs.readUShort()
    print(hex(imgFmt)+ ": format")
    UNKNOWN = bs.readShort()
    imgWidth = bs.readUShort()
    imgHeight = bs.readUShort()
    imgWidth2 = bs.readUShort()
    imgHeight2 = bs.readUShort()
    bs.readInt()
    datasize = bs.readUInt()
    data = bs.readBytes(datasize) 
    #RGB565_ABSW_WII
    if imgFmt == 0x0:
        print("RGB565_Swizzled (WIP!)")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x1:
        print("RGB565")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGB565
    elif imgFmt == 0x2:
        print("RGBA4444")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGBA4444
    elif imgFmt == 0x3:
        print("RGBA4444 OR RGBA8888\nIf it doesn't look right, look at the below comment!")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4") #COMMENT AND REPLACE WITH "r8 g8 b8 a8" TO WORK WITH WII U/LEGACY RGBA8888 TEXTURES
        texFmt = noesis.NOESISTEX_RGBA32
    #RGBA8888
    elif imgFmt == 0x4:
        print("RGBA8888")    
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x5:    
        print("UNKNOWN!")
        #data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "l8 a8")
        #texFmt = noesis.NOESISTEX_RGBA32
        return 1
    #R8A8 ???
    elif imgFmt == 0x8:    
        print("L8A8 OR DXT1 (WIP!)\nIf it doesn't look right, look at the below comment!")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "l8 a8") #COMMENT THIS AND THE BELOW LINE AND REPLACE THE BELOW WITH "texFmt = noesis.NOESISTEX_DXT1" (No quotes) TO WORK WITH WII U TEXTURES
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x0d:    
        print("LA88_BE (WIP!)")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "l8 a8") #TODO#
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT1
    elif imgFmt == 0x18:
        print("DXT1")
        texFmt = noesis.NOESISTEX_DXT1
    #DXT5
    elif imgFmt == 0x1a:
        print("DXT5")
        texFmt = noesis.NOESISTEX_DXT5
    #PVRTC_4BPP_RGB_v3
    elif imgFmt == 0x1e:    
        print("PVRTC4BPP_RGB (WIP!)")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x1f:
        print("PVRTC4BPP_RGBA (WIP!)")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    #ETC RGB
    elif imgFmt == 0x23:
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
        print("ETC")
    elif imgFmt == 0xFC:
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgba")
        texFmt = noesis.NOESISTEX_RGBA32
        print("ETC2_RGB")
    texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt))
    return 1