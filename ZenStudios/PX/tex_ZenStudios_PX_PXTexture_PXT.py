from inc_noesis import *
from addrlib import *

def registerNoesisTypes():
    handle = noesis.register("Zen Studios PX Texture", ".pxt")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.logPopup()
    return 1

def noepyCheckType(texData):
    bs = NoeBitStream(texData)
    #Check for PXT header
    
    if noeStrFromBytes(bs.readBytes(2)) != "PX": return 0
    return 1
    
def noepyLoadRGBA(texData, texList):
    bs = NoeBitStream(texData)
    bs.seek(0x8)
    #ver = bs.readByte() #Afaik I only found 01
    texFmt = bs.readInt()
    texWidth = bs.readInt()
    texHeight = bs.readInt()
    mips = bs.readInt()
    print(texWidth, "x", texHeight)
    if texFmt != 0xE1 and texFmt != 0xF0 and texFmt != 352 and texFmt != 353 and texFmt != 368 and texFmt != 370:
        texData = texData[0x18:] #Do this so we read textures at 0x18
    if texFmt == 0x0160 or texFmt == 0x0161 or texFmt == 0x0170 or texFmt == 0x0172:
        print("H")
        texData = texData[0x1c:]
    NinTex_dataSz = bs.readInt();
    if texFmt == 0xE1 or texFmt == 0xF0:
        WiiUTex_unk = bs.readInt();
    texData = bs.readBytes(NinTex_dataSz)
    #bpp = surfaceGetBitsPerPixel(texFmt)
        
    #texData = texData[0x20:]
    #RGBA8888 texture
    if texFmt == 0x14: #Mobile
        print("RGB888")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x16:    
        print("RGBA8888") #Mobile
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x17:    
        print("RGBA8888 other one")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "a8 r8 g8 b8")
        texFmt = noesis.NOESISTEX_RGBA32
    #DXT?
    elif texFmt == 0x40:    
        print("Possibly DXT, TODO!")
        #texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x44:    
        print("Possibly BC4 DXT, TODO!")
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.FOURCC_BC4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x54:    
        print("Xbox 360 DXT Tiled\nUNKNOWN")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x82:    
        print("PVRTC4, TODO!")
        texData = rapi.imageDecodePVRTC(texData, texWidth, texHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x83:    
        print("PVRTC4A, TODO!")
        texData = rapi.imageDecodePVRTC(texData, texWidth, texHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x84:    
        print("Xbox 360 DXT Tiled\nUNKNOWN")
        #texData = rapi.imageDecodePVRTC(texData, texWidth, texHeight, 4)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xC0:    
        print("PS Vita Swizzled RGBA8888\nDeswizzling is WIP!")
        texData = rapi.imageFromMortonOrder(texData, texWidth, texHeight)
        texData = rapi.imageFlipRGBA32(texData, texWidth, texHeight, 1, 0)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x8A:    
        print("ETC") #this byte is inconsistent
        texData = rapi.callExtensionMethod("etc_decoderaw32", texData, texWidth, texHeight, "rgb")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0xE1:    
        #texData = deswizzle(texWidth, texHeight, 1, texFmt, 0, 1, 4, 4, 256, 32, 0, 0, texData)
        print("WiiU Swizzled RGBA8888\nCannot deswizzle currently!")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0160 or texFmt == 0x0161:
        #block_height = min(max(texHeight // 8, 1), 16)
        #texData = unswizzleNX(texData, texWidth, texHeight, 4, block_height)
        print("Switch Swizzled RGBA8888\nCannot deswizzle currently!")
        texData = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8 g8 b8 a8")
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0170:    
        #block_height = min(max(texHeight // 8, 1), 8)
        #texData = unswizzleNX(texData, texWidth, texHeight, 2, block_height)
        print("Switch Swizzled DXT1\nCannot deswizzle currently!")
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.NOESISTEX_DXT1)
        texFmt = noesis.NOESISTEX_RGBA32
    elif texFmt == 0x0172:    
        #block_height = min(max(texHeight // 8, 1), 8)
        #texData = unswizzleNX(texData, texWidth, texHeight, 4, block_height)
        print("Switch Swizzled DXT5\nCannot deswizzle currently!")
        texData = rapi.imageDecodeDXT(texData, texWidth, texHeight, noesis.NOESISTEX_DXT5)
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print(texFmt)
        print("UNKNOWN TEXTURE FORMAT DETECTED!")
        return 1
    texList.append(NoeTexture(rapi.getInputName(), texWidth, texHeight, texData, texFmt))
    return 1

# adaptation of Yuzu Nintendo Switch Emulator (https://github.com/yuzu-emu/yuzu) unswizzling by https://github.com/orgs/yuzu-emu/people
# https://git.metaa.io/mirror/yuzu/blob/a3e82e8e1f5cb39246f30cac045db8e243f0daee/src/video_core/textures/decoders.cpp
# original source: Tegra K1 Technical Reference Manual, p.1187-1188 (https://developer.nvidia.com/embedded/tegra-k1-reference)
# assume GPLv2+ License: https://github.com/yuzu-emu/yuzu/blob/master/license.txt

def unswizzleNX(buffer, width, height, bpb, block_height=16, width_pad=16, height_pad=16):
    # setup
    out = bytearray(len(buffer))
    if width % width_pad or height % height_pad:
        width_show = width
        height_show = height
        width = width_real = ((width + width_pad - 1) // width_pad) * width_pad
        height = height_real = ((height + height_pad - 1) // height_pad) * height_pad
    else:
        width_show = width_real = width
        height_show = height_real = height
    image_width_in_gobs = width * bpb // 64

    # unswizzling
    for Y in range(height):
        for X in range(width):
            Z = Y * width + X
            GOB_address = 0 + (Y // (8 * block_height)) * 512 * block_height * image_width_in_gobs + (X * bpb // 64) * 512 * block_height + (Y % (8 * block_height) // 8) * 512
            X *= bpb
            address = GOB_address + ((X % 64) // 32) * 256 + ((Y % 8) // 2) * 64 + ((X % 32) // 16) * 32 + (Y % 2) * 16 + (X % 16)
            out[Z * bpb:(Z + 1) * bpb] = buffer[address:address + bpb]

    # crop
    if width_show != width_real or height_show != height_real:
        crop = bytearray(width_show * height_show * bpb)
        for Y in range(height_show):
            OffsetIn = Y * width_real * bpb
            OffsetOut = Y * width_show * bpb
            crop[OffsetOut:OffsetOut + width_show * bpb] = out[OffsetIn:OffsetIn + width_show * bpb]
        out = crop

    return out