#Slight update by LHR, fixes reading RGBA8888 textures

from inc_noesis import *
from addrlib import *

#Thanks AboodXD. Wii U swizzling code https://github.com/aboood40091/GTX-Extractor/tree/master/addrlib
#GX2 format http://mk8.tockdom.com/wiki/GTX%5CGSH_(File_Format)

BCn_formats = [0x31, 0x431, 0x32, 0x432, 0x33, 0x433, 0x34, 0x234, 0x35, 0x235, 0x41A]
BCn_format = {  0x31    :noesis.FOURCC_BC1,
                0x431   :noesis.FOURCC_BC1,
                0x32    :noesis.FOURCC_BC2, 
                0x432   :noesis.FOURCC_BC2, 
                0x33    :noesis.FOURCC_BC3, 
                0x433   :noesis.FOURCC_BC3, 
                0x34    :noesis.FOURCC_BC4, 
                0x234   :noesis.FOURCC_BC4, 
                0x35    :noesis.FOURCC_BC5, 
                0x235   :noesis.FOURCC_BC5,
                0x41A   :noesis.NOESISTEX_RGBA32}
print_format = {0x31    :"GX2_SURFACE_FORMAT_T_BC1_UNORM",
                0x431   :"GX2_SURFACE_FORMAT_T_BC1_SRGB",
                0x32    :"GX2_SURFACE_FORMAT_T_BC2_UNORM", 
                0x432   :"GX2_SURFACE_FORMAT_T_BC2_SRGB", 
                0x33    :"GX2_SURFACE_FORMAT_T_BC3_UNORM", 
                0x433   :"GX2_SURFACE_FORMAT_T_BC3_SRGB", 
                0x34    :"GX2_SURFACE_FORMAT_T_BC4_UNORM", 
                0x234   :"GX2_SURFACE_FORMAT_T_BC4_SNORM", 
                0x35    :"GX2_SURFACE_FORMAT_T_BC5_UNORM", 
                0x235   :"GX2_SURFACE_FORMAT_T_BC5_SNORM",
                0x41A   :"GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB"}
def registerNoesisTypes():
    handle = noesis.register("FunLabs Wii U Texture", ".wut")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    idstring = noeStrFromBytes(bs.readBytes(4))
    if idstring != "MIPh":
        return 0
    return 1
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    bs.setEndian(NOE_BIGENDIAN)
    MIPhMagic = noeStrFromBytes(bs.readBytes(4))
    dataSize = bs.readInt()
    xoffset = bs.readShort()
    yoffset = bs.readShort()
    dataOfs = bs.readInt()
    width = bs.readInt()
    height = bs.readInt()
    unk0 = bs.readShort()
    unk1 = bs.readShort()
    wutIDString = noeStrFromBytes(bs.readBytes(4)) #"WUT "
    unk2 = bs.readShort()
    unk3 = bs.readShort()
    GX2SurfaceDim = bs.readInt()
    texWidth = bs.readInt()
    texHeight = bs.readInt()
    unk4 = bs.readInt()
    mipmaps = bs.readInt()
    texFormat = bs.readInt()
    AAmode = bs.readInt()
    GX2SurfaceUse = bs.readInt()
    pixelSize = bs.readInt()
    dataPointer = bs.readInt()
    mipmapsDataSize = bs.readInt()
    mipmapsPointer = bs.readInt()
    tileMode = bs.readInt()
    swizzleValue = bs.readInt()
    alignment = bs.readInt()
    pitch = bs.readInt()
    bs.seek(dataOfs)
    pixel = bs.readBytes(pixelSize)
    
    bpp = surfaceGetBitsPerPixel(texFormat)
    pixel = deswizzle(width, height, 1, texFormat, 0, GX2SurfaceUse,tileMode,swizzleValue,pitch, bpp, 0, 0, pixel)
    if (texFormat == 0x41a): #Do this instead if RGBA8888
        textureData = rapi.imageDecodeRaw(pixel,width,height,"r8 g8 b8 a8")
    else:
        textureData = rapi.imageDecodeDXT(pixel,width,height,BCn_format[texFormat])
    texList.append(NoeTexture("test", width, height, textureData, noesis.NOESISTEX_RGBA32))
    print("\nTex Format:",print_format[texFormat])
    
    return 1

