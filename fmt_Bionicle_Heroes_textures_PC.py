from inc_noesis import *
import noesis
import rapi

def registerNoesisTypes():
    handle = noesis.register("Bionicle Heroes textures", ".nup")
    noesis.setHandlerTypeCheck(handle, bioHCheckType)
    noesis.setHandlerLoadRGBA(handle, bioHLoadRGBA)
    handle = noesis.register("Bionicle Heroes textures", ".hgp")
    noesis.setHandlerTypeCheck(handle, bioHCheckType)
    noesis.setHandlerLoadRGBA(handle, bioHLoadRGBA)
    noesis.logPopup()
    return 1

def bioHCheckType(data):
    return 1

def bioHLoadRGBA(data, texList):
    texCount = 0
    bs = NoeBitStream(data)
    fileSize = bs.getSize()
    fileSizeDiv4 = fileSize // 4
    for i in range(0, fileSizeDiv4 - 1):
        temp = bs.readInt()

        if (temp == 0x20534444):
            texCount += 1
            print(texCount)
            offset = bs.tell()
            print ("Found texture header at: " + hex(offset - 0x04))
            bs.seek(0x08, NOESEEK_REL)
            height = bs.readInt()
            width = bs.readInt()
            print ("Height: " + str(height))
            print ("Width: " + str(width))
            bs.seek(0x08, NOESEEK_REL)
            mipCount = bs.readInt()
            print ("Mips: " + str(mipCount))
            bs.seek(-0x20, NOESEEK_REL)

            if mipCount == 0x00:
                textureSize = (height * width * 0x06) + 0x80
            else:
                textureSize = (height * width) + 0x80

                for i in range(1, mipCount):
                    height //= 0x02
                    width //= 0x02
                    textureSize += max(0x01, ((width + 0x03) // 0x04)) * max(0x01, ((height + 0x03) // 0x04)) * 0x10

            img = rapi.loadTexByHandler(bs.readBytes(textureSize), ".dds")
            img.name = str(texCount)
            texList.append(img)
    return 1
