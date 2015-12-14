# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from PyQt5.QtCore import QObject, QCoreApplication, pyqtSlot, QUrl, pyqtSignal

from UM.Application import Application
from UM.Scene.SceneNode import SceneNode
from UM.Scene.BoxRenderer import BoxRenderer
from UM.Operations.AddSceneNodeOperation import AddSceneNodeOperation
from UM.Scene.Selection import Selection
from UM.Operations.RemoveSceneNodeOperation import RemoveSceneNodeOperation
from UM.Operations.GroupedOperation import GroupedOperation

import os.path

class ControllerProxy(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._controller = Application.getInstance().getController()
        self._controller.contextMenuRequested.connect(self._onContextMenuRequested)
        self._selection_pass = None

    @pyqtSlot(str)
    def setActiveView(self, view):
        self._controller.setActiveView(view)

    @pyqtSlot(str)
    def setActiveTool(self, tool):
        self._controller.setActiveTool(tool)

    @pyqtSlot()
    def removeSelection(self):
        if not Selection.hasSelection():
            return

        op = GroupedOperation()
        for node in Selection.getAllSelectedObjects():
            op.addOperation(RemoveSceneNodeOperation(node))
        op.push()
        Selection.clear()

    contextMenuRequested = pyqtSignal("quint64", arguments=["objectId"])

    def _onContextMenuRequested(self, x, y):
        if not self._selection_pass:
            self._selection_pass =  Application.getInstance().getRenderer().getRenderPass("selection")

        id = self._selection_pass.getIdAtPosition(x, y)

        if id:
            self.contextMenuRequested.emit(id)
        else:
            self.contextMenuRequested.emit(0)
