#By LolHacksRule

#Only tested on iOS
from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Shrek Kart Texture (Offzip Dumped)", ".dat;.img")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1
    
def noepyCheckType(data):
    bs = NoeBitStream(data)
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    rawImgWidth = bs.readShort()
    rawImgHeight = bs.readShort()
    rawImgFmt = bs.readShort() #6: PVR, 8: 8888
    unk = bs.readShort() #1
    rawDataSize = bs.readInt()
    if rawImgFmt == 6: #Read PVR header
        PVRhdrSize = bs.readInt()
        PVRimgWidth = bs.readInt()
        PVRimgHeight = bs.readInt()
        PVRnumMips = bs.readInt()
        PVRimgFmt = bs.readByte()
        PVRflag1 = bs.readByte()
        PVRflag2 = bs.readByte()
        PVRflag3 = bs.readByte()
        print(hex(PVRimgFmt)+ ": format")
        PVRdataSize = bs.readInt()
        PVRbpp = bs.readInt();
        PVRred = bs.readInt();
        PVRgreen = bs.readInt();
        PVRblue = bs.readInt();
        PVRalpha = bs.readInt();
        PVRId = bs.readInt();
        PVRSurfaces = bs.readInt()
        data = bs.readBytes(PVRdataSize)
        imgWidth = PVRimgWidth
        imgHeight = PVRimgHeight
        imgFmt = PVRimgFmt
    else:
        data = bs.readBytes(rawDataSize)
        imgFmt = rawImgFmt
        imgWidth = rawImgWidth
        imgHeight = rawImgHeight
    #RGBA8888
    if imgFmt == 0x0008 or imgFmt == 0x0400: #Apparently 0x4000 is RGBA4444 but idk
        print("ARGB8888")
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif imgFmt == 0x19:
        print("PVRTC_4BPP_RGBA\nWIP!")
        data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    flippedImg = rapi.imageFlipRGBA32(data, imgWidth, imgHeight, 0, 1)
    texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, flippedImg, texFmt))
    return 1