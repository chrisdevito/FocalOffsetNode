FocalOffsetNode
=================
Maintains camera focal point when changing focal length.

Installation:
-------------
The FocalOffsetNode is a Maya module that can be installed like all other Maya modules. You can do one of the following:

* Drag and drop the setup.mel file in this directory into maya and it'll do the work of installation
* Add the focaloffsetnode root directory to the MAYA_MODULE_PATH environment variable.
* Add the focaloffsetnode root directory to the MAYA_MODULE_PATH in your Maya.env. e.g. MAYA_MODULE_PATH += /path/to/focaloffsetnode
* Edit the focaloffset.mod file, and replace the ./ with the full path to the cmt root directory, then copy the cmt.mod file to where your modules are loaded from.

To Run
-------
```
import FocalOffset
FocalOffset.main()
```