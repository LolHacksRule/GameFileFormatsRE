#Rewrite by LHR

from inc_noesis import *
import noesis
import rapi
import os
import lib_zq_nintendo_tex as nintex

#Thanks Zhenёq, Nintendo wii code reference : https://github.com/Zheneq/Noesis-Plugins
#Format reference ：http://wiki.tockdom.com/wiki/Image_Formats


def registerNoesisTypes():
    handle = noesis.register("Rovio Fusion GameCube Texture (not really)", ".gct")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    idstring = noeStrFromBytes(bs.readBytes(4))
    if idstring != "MIPh":
        return 0
    return 1

gctfmts = {
    0x00: nintex.NINTEX_IA8,
    0x09: nintex.NINTEX_C4,
    0x0e: nintex.NINTEX_CMPR,
}

def readMIPHeader(bs):
    return {
        'MIPhMagic' : bs.readUInt(),
        'dataSize'   : bs.readUInt(),
        'xoffset'  : bs.readShort(),
        'yoffset'    : bs.readShort(),
        'dataOfs'    : bs.readUInt(),
        'texWidth' : bs.readUInt(),
        'texHeight'    : bs.readUInt(),
        'unk1'    : bs.readShort(),
        'unk2'    : bs.readShort(),
        'unk3'    : bs.readInt(),
    }

def readGCT(bs):
    return {
        'gctMagic' : bs.readUInt(), #"GCT "
        'texWidth' : bs.readShort(),
        'texHeight' : bs.readShort(),
        'texFormat' : bs.readShort(),
        'palFormat' : bs.readShort(), #-1=not use; 0=IA8; 1=RGB565; 2=RGB5A3;
        'unk3' : bs.readInt(),
        'pixelSize' : bs.readInt(),
        'palSize' : bs.readInt(),
        'unk14' : bs.readInt(),
        'unk15' : bs.readInt(),
    }

def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data, NOE_BIGENDIAN)
    MIPh_hdr = readMIPHeader(bs)
    GCT = readGCT(bs)
    tex = nintex.readTexture(bs, GCT['texWidth'], GCT['texHeight'], gctfmts[GCT['texFormat']])
    tex.name = rapi.getInputName()
    texList.append(tex)
    return len(texList)