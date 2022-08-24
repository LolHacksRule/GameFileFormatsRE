#By LolHacksRule

#Please tell me if a format that is listed isn't decoded properly
#There's format 26 but I don't remember what file has it
#Conversion of r channel in LA88 (https://zenhax.com/viewtopic.php?t=7573)
#Added and modified 3DS deswizzle code (https://raw.githubusercontent.com/Zheneq/Noesis-Plugins/master/fmt_mtframework_3ds_tex.py)
#Added code to flip the image data

from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Exient XGS Engine Texture (Nintendo 3DS)", ".t3d")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    if noeStrFromBytes(bs.readBytes(3)) != "T3D": return 0
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    #unknown = bs.readByte()
    bs.seek(0x4)
    imgWidth = bs.readUShort()
    imgHeight = bs.readUShort()
    imgWidth2 = bs.readUShort()
    imgHeight2 = bs.readUShort()
    unknown2 = bs.readInt();
    imgFmt = bs.readInt()
    dataSize = bs.readInt()
    print(hex(imgFmt)+ ": format")
    unknown3 = bs.readUShort();
    unknown4 = bs.readUShort();
    unknown3 = bs.readInt();
    data = bs.readBytes(dataSize)
    if dataSize == 0:
        print("Texture is empty!")
        return 1
    if imgFmt == 0x0 or imgFmt == 0x1 or imgFmt == 0x2:
        data = unswizzleGeneric(data, imgWidth, imgHeight)
    elif imgFmt == 0x3:
        data = unswizzle8888(data, imgWidth, imgHeight)
    elif imgFmt == 0xD:
        data = unswizzleLA88(data, imgWidth, imgHeight)
    elif imgFmt == 0x19:
        data = unswizzleLA44(data, imgWidth, imgHeight)
    #RGB565
    if imgFmt == 0x0:
        print("RGB565 (WIP!)")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
        texFmt = noesis.NOESISTEX_RGBA32
    #ARGB1555
    if imgFmt == 0x1:
        print("ARGB1555")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a1 b5 g5 r5")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGBA4444
    if imgFmt == 0x2:
        print("RGBA4444")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
        texFmt = noesis.NOESISTEX_RGBA32
    #RGBA8888
    if imgFmt == 0x3:
        print("RGBA8888")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8 b8 g8 r8")
        texFmt = noesis.NOESISTEX_RGBA32
    #LA88
    if imgFmt == 0xD:
        print("LA88")
        #add to convert
        In = bytearray(data)
        Out = bytearray(2*len(data))
        for i in range(3): Out[i::4] = In[0::2]
        Out[3::4] = In[1::2]
        data = Out
        Out = rapi.imageFlipRGBA32(data, imgWidth, imgHeight, "r8 a8") #TODO#
        texFmt = noesis.NOESISTEX_RGBA32
    #LA44
    if imgFmt == 0x19:
        print("LA44\nWIP")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r4 a4")
        texFmt = noesis.NOESISTEX_RGBA32
    #ETC1
    if imgFmt == 0xFC:
        print("ETC1\nWIP")
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
    #ETC1_RGB_SPLITALPHA_ZORDERON
    if imgFmt == 0xFD:
        print("ETC1_RGB_SPLITALPHA_ZORDERON\nWIP")
        data = rapi.callExtensionMethod("etc_decoderaw32", data, imgWidth, imgHeight, "rgba")
        texFmt = noesis.NOESISTEX_RGBA32
    flippedImg = rapi.imageFlipRGBA32(data, imgWidth, imgHeight, 0, 1)
    texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, flippedImg, texFmt))
    return 1

def unswizzleGeneric(buffer, width, height):
    bpp = 16
    l = 8
    m = 4
    s = 2
    stripSize = bpp * s // 8

    result = bytearray(width * height * bpp // 8)
    ptr = 0

    for y in range(0, height, l):
        for x in range(0, width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * width) + x + x1 + x2) * bpp // 8
                                result[idx : idx+stripSize] = buffer[ptr : ptr+stripSize]
                                ptr += stripSize

    return result

def unswizzle8888(buffer, width, height):
    bpp = 32
    l = 8
    m = 4
    s = 2
    stripSize = bpp * s // 8

    result = bytearray(width * height * bpp // 8)
    ptr = 0

    for y in range(0, height, l):
        for x in range(0, width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * width) + x + x1 + x2) * bpp // 8
                                result[idx : idx+stripSize] = buffer[ptr : ptr+stripSize]
                                ptr += stripSize

    return result
    
def unswizzleLA44(buffer, width, height):
    bpp = 8
    l = 8
    m = 4
    s = 2
    stripSize = bpp * s // 8

    result = bytearray(width * height * bpp // 8)
    ptr = 0

    for y in range(0, height, l):
        for x in range(0, width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * width) + x + x1 + x2) * bpp // 8
                                result[idx : idx+stripSize] = buffer[ptr : ptr+stripSize]
                                ptr += stripSize

    return result
      
def unswizzleLA88(buffer, width, height):
    bpp = 16
    l = 8
    m = 4
    s = 2
    stripSize = bpp * s // 8

    result = bytearray(width * height * bpp // 8)
    ptr = 0

    for y in range(0, height, l):
        for x in range(0, width, l):
            for y1 in range(0, l, m):
                for x1 in range(0, l, m):
                    for y2 in range(0, m, s):
                        for x2 in range(0, m, s):
                            for y3 in range(s):
                                idx = (((y + y1 + y2 + y3) * width) + x + x1 + x2) * bpp // 8
                                result[idx : idx+stripSize] = buffer[ptr : ptr+stripSize]
                                ptr += stripSize

    return result