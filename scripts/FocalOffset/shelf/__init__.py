import os
from maya import mel, cmds
from functools import partial
from collections import OrderedDict

buttons = OrderedDict(
    {
        "FocalOffsetNode": {
            "command": ("import FocalOffset\n", "FocalOffset.main()"),
            "sourceType": "python",
            "style": "iconOnly",
            "image": "maya_focaloffset_icon.png",
            "annotation": "Focal Offset Node",
            "enableCommandRepeat": False,
            "flat": True,
            "width": 32,
            "height": 32,
            "enableBackground": False,
        },
    }
)


def create_shelf():
    """
    Create the OBB shelf

    Raises:
        None

    Returns:
        None
    """

    tab_layout = mel.eval("$pytmp=$gShelfTopLevel")
    shelf_exists = cmds.shelfLayout("FocalOffset", exists=True)

    if shelf_exists:
        cmds.deleteUI("FocalOffset", layout=True)

    shelf = cmds.shelfLayout("FocalOffset", parent=tab_layout)

    for button, kwargs in buttons.items():
        cmds.shelfButton(label=button, parent=shelf, **kwargs)

    # Fix object 0 error.
    shelves = cmds.shelfTabLayout(tab_layout, query=True, tabLabelIndex=True)

    for index, shelf in enumerate(shelves):
        cmds.optionVar(stringValue=("shelfName%d" % (index + 1), str(shelf)))


create_shelf()
