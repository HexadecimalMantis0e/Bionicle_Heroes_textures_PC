from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Bionicle Heroes textures", ".nup")
    noesis.setHandlerTypeCheck(handle, bhCheckType)
    noesis.setHandlerLoadRGBA(handle, bhLoadRGBA)
    handle = noesis.register("Bionicle Heroes textures", ".hgp")
    noesis.setHandlerTypeCheck(handle, bhCheckType)
    noesis.setHandlerLoadRGBA(handle, bhLoadRGBA)
    noesis.logPopup()
    return 1

def bhCheckType(data):
    return 1

def bhLoadRGBA(data, texList):
    texCount = 0
    bs = NoeBitStream(data)
    fileSizeDiv4 = bs.getSize() // 4
    
    for i in range(0, fileSizeDiv4 - 1):
        temp = bs.readUInt()

        if (temp == 0x20534444):
            texCount += 1
            print(texCount)
            address = bs.tell()
            print("Found texture header at: " + hex(address - 0x04))
            bs.seek(0x08, NOESEEK_REL)
            height = bs.readUInt()
            width = bs.readUInt()
            print("Height: " + str(height))
            print("Width: " + str(width))
            bs.seek(0x08, NOESEEK_REL)
            mips = bs.readUInt()
            print("Mips: " + str(mips))
            bs.seek(0x34, NOESEEK_REL)
            type = bs.readBytes(0x04).decode()
            print("Type: " + str(type))
            bs.seek(-0x58, NOESEEK_REL)

            if mips == 0x00:
                textureSize = (height * width * 0x06) + 0x80
            else:
                textureSize = (height * width) + 0x80

                for i in range(1, mips):
                    height //= 0x02
                    width //= 0x02
                    textureSize += max(0x01, ((width + 0x03) // 0x04)) * max(0x01, ((height + 0x03) // 0x04)) * 0x10

            img = rapi.loadTexByHandler(bs.readBytes(textureSize), ".dds")
            img.name = str(texCount)
            texList.append(img)
            bs.seek(address, NOESEEK_ABS)
    return 1
