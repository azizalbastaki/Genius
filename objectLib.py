#Written by Abdulaziz Albastaki in January 2021
from panda3d.core import CollideMask,BitMask32, AmbientLight
class dock():
    def __init__(self,loader,location):
        self.loader = loader
        self.port = self.loader.loadModel("assets/environment/arctic/buildings/port.bam")
        self.port.setPos(location)
        self.port.setH(90)
        self.port.setCollideMask(BitMask32.bit(1))
        ambiet = AmbientLight('ambient')
        ambiet.setColor((0.2, 0.2, 0.2, 1))
        alight = self.port.attachNewNode(ambiet)
        self.port.setLight(alight)
        self.port.reparentTo(render)
class building1():
    def __init__(self,loader):
        self.loader = loader
        self.gameObject = self.loader.loadModel("assets/environment/arctic/buildings/building1.bam")
class tree1():
    def __init__(self,loader):
        self.loader = loader
        self.gameObject = self.loader.loadModel("assets/environment/arctic/nature/tree.bam")