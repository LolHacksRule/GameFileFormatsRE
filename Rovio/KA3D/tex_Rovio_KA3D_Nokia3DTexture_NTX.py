#By LHR, ONLY TESTED ON BOUNCE NGAGE
from inc_noesis import *
from addrlib import *

def registerNoesisTypes():
    handle = noesis.register("Rovio KA3D Nokia 3D Texture", ".ntx")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    bs = NoeBitStream(texData)
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    version = bs.readShort();
    texWidth = bs.readShort()
    texHeight = bs.readShort();
    texFmt = bs.readShort();
    if (texFmt == 0x01):
        print("R8G8B8");
        texFmtStr = "b8g8r8";
    elif (texFmt == 0x02):
        print("B8G8R8");
        texFmtStr = "r8g8b8";
    elif (texFmt == 0x03):
        print("A8R8G8B8");
        texFmtStr = "b8g8r8a8";
    elif (texFmt == 0x04):
        print("X8R8G8B8");
        texFmtStr = "b8g8r8a8";
    elif (texFmt == 0x05):
        print("X8B8G8R8");
        texFmtStr = "r8g8b8a8";
    elif (texFmt == 0x06):
        print("A8B8G8R8");
        texFmtStr = "r8g8b8a8";
    elif (texFmt == 0x07):
        print("R5G6B5");
        texFmtStr = "b5g6r5";
    elif (texFmt == 0x08):
        print("R5G5B5");
        texFmtStr = "b5g5r5a1";
    elif (texFmt == 0x09):
        print("R6G6B6");
        texFmtStr = "b6g6r6a14";
    #elif (texFmt == 0x0B):
        #print("P8");
        #texFmtStr = "p8";
    elif (texFmt == 0x0C):
        print("L8 (WIP!)");
        texFmtStr = "l8";
    elif (texFmt == 0x0D):
        print("A1R5G5B5");
        texFmtStr = "b5g5r5a1";
    elif (texFmt == 0x0E):
        print("X4R4G4B4");
        texFmtStr = "b4g4r4a4";
    elif (texFmt == 0x0F):
        print("A4R4G4B4");
        texFmtStr = "b4g4r4a4";
    elif (texFmt == 0x10):
        print("A4B4G4R4");
        texFmtStr = "r4g4b4a4";
    elif (texFmt == 0x11):
        print("R4G4B4A4");
        texFmtStr = "a4b4g4r4";
    elif (texFmt == 0x12):
        print("A1B5G5R5");
        texFmtStr = "r5g5b5a1";
    elif (texFmt == 0x13):
        print("R5G5B5A1");
        texFmtStr = "a1b5g5r5";
    elif (texFmt == 0x14):
        print("R3G3B2");
        texFmtStr = "b2g3r3";
    elif (texFmt == 0x15):
        print("R3G2B3");
        texFmtStr = "b3g2r3";
    elif (texFmt == 0x16):
        print("A8");
        texFmtStr = "a8";
    elif (texFmt == 0x17):
        print("A8R3G3B2");
        texFmtStr = "b2g3r3a8";
    elif (texFmt == 0x18):
        print("A8R3G2B3");
        texFmtStr = "b3g2r3a8";
    #elif (texFmt == 0x1C):
        #print("R16F");
        #texFmtStr = "r16";
    #elif (texFmt == 0x1D):
        #print("G16R16F");
        #texFmtStr = "r16g16";
    #elif (texFmt == 0x1E):
        #print("A16B16G16R16F");
        #texFmtStr = "r16g16b16a16";
    elif (texFmt == 0x1F):
        print("R32F (WIP!)");
        texFmtStr = "r32";
    elif (texFmt == 0x20):
        print("G32R32F (WIP!)");
        texFmtStr = "r32g32";
    elif (texFmt == 0x21):
        print("A32B32G32R32F (WIP!)");
        texFmtStr = "r32g32b32a32";
    #elif (texFmt == 0x22):
        #print("D32 (WIP!)");
        #texFmtStr = "d32";
    #elif (texFmt == 0x23):
        #print("D24 (WIP!)");
        #texFmtStr = "d24";
    #elif (texFmt == 0x24):
        #print("D16 (WIP!)");
        #texFmtStr = "d16";
    #elif (texFmt == 0x25):
        #print("D24S8 (WIP!)");
        #texFmtStr = "d24s8";
    else:
        #0x0B
        print("TEXTURE FORMAT", texFmt, "IS AN UNKNOWN/UNSUPPORTED TEXTURE FORMAT!");
        return 1
    palSz = bs.readShort();
    if (palSz > 0):
        dmy = bs.readInt();
        pal = bs.readBytes(palSz*2);
    flags = bs.readShort();
    userFlags = bs.readShort();
    if (palSz > 0):
        print("Palette textures are WIP!");
        if (texFmt == 0x1F or texFmt == 0x20 or texFmt == 0x24):
            texData = texData[(palSz*4 + 14):]
        else:
            texData = texData[(palSz*2 + 14):]
        texData = rapi.imageDecodeRawPal(texData, pal, texWidth, texHeight, 8, texFmtStr)
    else:
        texData = texData[0x0e:]
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, texFmtStr)
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, noesis.NOESISTEX_RGBA32))
    return 1