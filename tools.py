#Written by Abdulaziz Albastaki in February 2021
from panda3d.core import BitMask32,CollisionRay,CollisionTraverser,CollisionNode,CollideMask,CollisionHandlerQueue
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import OnscreenText
from random import randint
from objectLib import building1, tree1, collisions
class buildingTool():
    def __init__(self,models,player,loader,accept):
        self.gameObjects = [building1(loader),tree1(loader),collisions(loader)]
        for i in self.gameObjects:
            i.gameObject.reparentTo(render)
            i.gameObject.hide()
        self.player = player
        self.loader = loader
        self.setupGUI()
        self.frame.hide()

        self.rotation = 0
        self.index = 0
        self.currentGameObject = self.gameObjects[self.index].gameObject
        self.currentSizeFactor = 1
        self.currentGameObject.show()
        self.toggle = False
        self.placedObjects = []
        self.pressedKey = False

        #Collisions
        self.cTrav = CollisionTraverser()
        self.groundRay = CollisionRay()
        self.groundRay.setDirection(0, 0, -1)
        self.groundRayCol = CollisionNode('playerRay')
        self.groundRayCol.addSolid(self.groundRay)
        self.groundRayCol.setFromCollideMask(CollideMask.bit(1))
        self.groundRayCol.setIntoCollideMask(CollideMask.allOff())
        self.groundColNp = self.currentGameObject.attachNewNode(self.groundRayCol)
        self.groundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.groundColNp, self.groundHandler)

        self.keymap = {
            "b": False,
            "up": False,
            "down": False,
            "right": False,
            "left": False,
            "R": False,
            "sizeup": False,
            "sizedown": False,
            "P": False,
            "changenext": False,
            "changeprevious": False
        }
        accept("b", self.updateKey, ["b", True])  #
        accept("b-up", self.updateKey, ["b", False])

        accept("arrow_left", self.updateKey, ["left", True])
        accept("arrow_left-up", self.updateKey, ["left", False])

        accept("arrow_right", self.updateKey, ["right", True])
        accept("arrow_right-up", self.updateKey, ["right", False])

        accept("arrow_up", self.updateKey, ["up", True])
        accept("arrow_up-up", self.updateKey, ["up", False])

        accept("arrow_down", self.updateKey, ["down", True])
        accept("arrow_down-up", self.updateKey, ["down", False])

        accept("r", self.updateKey, ["R", True])
        accept("r-up", self.updateKey, ["R", False])

        accept("]", self.updateKey, ["sizeup", True])
        accept("]-up", self.updateKey, ["sizeup", False])

        accept("[", self.updateKey, ["sizedown", True])
        accept("[-up", self.updateKey, ["sizedown", False])

        accept("enter", self.updateKey, ["P", True])
        accept("enter-up", self.updateKey, ["P", False])

        accept(",", self.updateKey, ["changeprevious", True])
        accept(",-up", self.updateKey, ["changeprevious", False])

        accept(".", self.updateKey, ["changenext", True])
        accept(".-up", self.updateKey, ["changenext", False])

        self.updateTask = taskMgr.add(self.update, "update")

    def updateKey(self, key, value):
        self.keymap[key] = value

        if (value==False)and(key=="P" or "b" or "R" or "sizeup" or "sizedown"):
            self.pressedKey = False

    def update(self,task):
        deltatime = globalClock.getDt()
        if (self.keymap["b"] and self.toggle == False) and self.pressedKey == False:
            self.toggleOn()
        elif (self.keymap["b"] and self.toggle == True) and self.pressedKey == False:
            self.toggleOff()
        if self.toggle == True:
            def updatePosition():
                self.positionText.text = "Position: " + str(int(self.currentGameObject.getX())) + "," + str(int(self.currentGameObject.getX())) + "," + str(int(self.currentGameObject.getZ()))
            def updateSize():
                self.scaleText.text = "Scale: " + str(self.currentSizeFactor)
            self.moveFactor = 5
            if self.keymap["up"]:
                self.setHeight()
                self.currentGameObject.setX(self.currentGameObject,self.moveFactor)
                updatePosition()
            if self.keymap["down"]:
                self.setHeight()
                self.currentGameObject.setX(self.currentGameObject,-self.moveFactor)
                updatePosition()
            if self.keymap["left"]:
                self.setHeight()
                self.currentGameObject.setY(self.currentGameObject,-self.moveFactor)
                updatePosition()
            if self.keymap["right"]:
                self.setHeight()
                self.currentGameObject.setY(self.currentGameObject,self.moveFactor)
                updatePosition()
            if self.keymap["sizeup"] and self.pressedKey == False:
                self.currentSizeFactor+=1
                updateSize()
                self.currentGameObject.setScale(self.currentSizeFactor)
            if self.keymap["sizedown"] and self.pressedKey == False:
                self.currentSizeFactor-=1
                updateSize()
                self.currentGameObject.setScale(self.currentSizeFactor)
            if self.keymap["R"] and self.pressedKey==False:
                self.currentGameObject.setH(self.currentGameObject, 90)
                self.rotation = self.currentGameObject.getH()
                self.pressedKey = True
                self.setHeight()
            if self.keymap["P"] and self.pressedKey == False:
                self.placeObject(self.loader,self.gameObjects,self.index,self.currentGameObject,self.currentSizeFactor)
                self.pressedKey = True
            def changeObject():
                self.currentGameObject = self.gameObjects[self.index].gameObject
                self.currentGameObject.show()
                self.currentGameObject.setPos(self.currentPosition)
                self.currentGameObject.setScale(self.currentSizeFactor)
                self.currentGameObject.setH(self.rotation)
            if self.keymap["changenext"]:
                self.currentPosition = self.currentGameObject.getPos()
                self.currentGameObject.hide()
                self.index+=1
                if self.index == len(self.gameObjects):
                    self.index = 0
                changeObject()
            if self.keymap["changeprevious"]:
                self.currentPosition = self.currentGameObject.getPos()
                self.currentGameObject.hide()
                self.index-=1
                if self.index == -1:
                    self.index = len(self.gameObjects)-1
                changeObject()
        return task.cont

    def setupGUI(self):
        self.frame = DirectFrame(parent=render2d ,frameColor=(0, 0,0, 1),
                              frameSize=(-0.2, 0.4, -0.4, 0.2),
                              pos=(-1, -1, 0))
        self.devMode = OnscreenText(parent= self.frame, text='DEVELOPER MODE', pos=(0.2, 0.1), scale=0.04, fg=(1,1,1,1))
        self.scaleText = OnscreenText(parent= self.frame, text='Scale: 1', pos=(0.2, 0), scale=0.04, fg=(1,1,1,1))
        self.positionText = OnscreenText(parent= self.frame, text='Position: 0,0,0', pos=(0.2, -0.1), scale=0.04, fg=(1,1,1,1))

    class placeObject():
        def __init__(self,loader,gameObjects,index,currentGameObject,currentSizeFactor):
            object = gameObjects[index]
            model = loader.loadModel(object.file)
            model.setPos(currentGameObject.getPos())
            model.setScale(currentSizeFactor)
            model.setH(currentGameObject.getH())

            model.setCollideMask(BitMask32.bit(0))
            model.reparentTo(render)
            file = open("newbuildings","a")
            self.objectNumber = str(randint(0,9999))
            self.variableName = "self."+ str(object.name) + self.objectNumber
            code = "\n" + self.variableName + " = self.loader.loadModel('" + object.file + "')"
            code += "\n" + self.variableName + ".setScale(" + str(currentSizeFactor) + ")"
            code += "\n" + self.variableName + ".setPos(" + str(currentGameObject.getX())+ ", " +str(currentGameObject.getY()) + ", " + str(currentGameObject.getZ()) + ")"
            code += "\n" + self.variableName + ".setH(" + str(currentGameObject.getH()) + ")"
            try:
                if "hide" in object.otherCommands:
                    code += "\n" + self.variableName + ".hide()"
            except:
                pass
            code += "\n" + self.variableName + '.reparentTo(render)\n'
            file.write(code)
            file.close()
    def toggleOn(self):
        self.currentGameObject.setPos(self.player.getPos())
        self.currentGameObject.setX(self.player,10)
        self.currentGameObject.show()
        self.frame.show()
        self.toggle = True
    def toggleOff(self):
        self.currentGameObject.hide()
        self.frame.hide()
        self.toggle = False

    def setHeight(self):
        self.cTrav.traverse(render)
        entries = list(self.groundHandler.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())
        for entry in entries:
            self.currentGameObject.setZ(entry.getSurfacePoint(render).getZ() + 1)