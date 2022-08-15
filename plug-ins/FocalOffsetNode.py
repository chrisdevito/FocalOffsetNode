from __future__ import division

from maya.api import OpenMaya


def maya_useNewAPI():
    pass


class FocalOffset(OpenMaya.MPxNode):
    """
    :class:`FocalOffset` MPxNode class
    """
    kPluginNodeId = OpenMaya.MTypeId(0x82163)
    kPluginNodeName = "FocalOffset"

    m_input_cam_matrix = OpenMaya.MObject()
    m_input_obj_matrix = OpenMaya.MObject()

    m_input_focal = OpenMaya.MObject()
    m_output_focal = OpenMaya.MObject()

    # translate
    m_output_translate = OpenMaya.MObject()
    m_output_translateX = OpenMaya.MObject()
    m_output_translateY = OpenMaya.MObject()
    m_output_translateZ = OpenMaya.MObject()

    def __init__(self):
        super(FocalOffset, self).__init__()

    @classmethod
    def nodeCreator(cls):
        return cls()

    def compute(self, plug, datablock):
        """
        Computes the node

        :param plug: attribute plug
        :type plug: OpenMaya.MPlug
        :param datablock: Data
        :type datablock: OpenMaya.MDataBlock

        :return: None
        :rtype: NoneType
        """
        plugs = [self.m_output_translate,
                 self.m_output_translateX,
                 self.m_output_translateY,
                 self.m_output_translateZ]

        if plug in plugs:

            # get input matrices
            input_camera_mat = datablock.inputValue(
                self.m_input_cam_matrix).asMatrix()
            input_obj_mat = datablock.inputValue(
                self.m_input_obj_matrix).asMatrix()

            input_focal = datablock.inputValue(self.m_input_focal).asDouble()
            output_focal = datablock.inputValue(self.m_output_focal).asDouble()
            focal_scalar = output_focal / input_focal

            cam_tmat = OpenMaya.MTransformationMatrix(input_camera_mat)
            obj_tmat = OpenMaya.MTransformationMatrix(input_obj_mat)

            cam_point = cam_tmat.translation(OpenMaya.MSpace.kWorld)
            cam_dir = OpenMaya.MVector(
                0.0, 0.0, -1.0) * cam_tmat.asRotateMatrix()
            obj_point = obj_tmat.translation(OpenMaya.MSpace.kWorld)

            obj_vec = obj_point - cam_point

            dot = obj_vec * cam_dir

            project_dist = 0.0

            if dot != 0.0:
                project_dist = dot / cam_dir.length()

            view_normal_vec = cam_dir.normal()
            project_vec = OpenMaya.MVector((project_dist * view_normal_vec.x),
                                           (project_dist * view_normal_vec.y),
                                           (project_dist * view_normal_vec.z))
            project_vec += cam_point

            result_vec = cam_point - project_vec
            new_length = result_vec.length() * focal_scalar
            result_vec.normalize()
            result_vec *= new_length
            result_vec += project_vec

            # get all outputs
            # get output a translate
            output_translate_x = datablock.outputValue(
                self.m_output_translateX)
            output_translate_y = datablock.outputValue(
                self.m_output_translateY)
            output_translate_z = datablock.outputValue(
                self.m_output_translateZ)

            # set output translation
            output_translate_x.setMDistance(OpenMaya.MDistance(result_vec.x))
            output_translate_y.setMDistance(OpenMaya.MDistance(result_vec.y))
            output_translate_z.setMDistance(OpenMaya.MDistance(result_vec.z))

            output_translate_x.setClean()
            output_translate_y.setClean()
            output_translate_z.setClean()

            datablock.setClean(plug)

    @classmethod
    def nodeInitializer(cls):
        '''
        Initializes attributes for the node.
        '''
        attr_c = OpenMaya.MFnCompoundAttribute()
        attr_u = OpenMaya.MFnUnitAttribute()
        attr_m = OpenMaya.MFnMatrixAttribute()
        attr_n = OpenMaya.MFnNumericAttribute()

        cls.m_input_cam_matrix = attr_m.create(
            "input_camera_matrix",
            "icm",
            OpenMaya.MFnMatrixAttribute.kDouble)
        cls.addAttribute(cls.m_input_cam_matrix)

        cls.m_input_obj_matrix = attr_m.create(
            "input_object_matrix",
            "iom",
            OpenMaya.MFnMatrixAttribute.kDouble)
        cls.addAttribute(cls.m_input_obj_matrix)

        cls.m_input_focal = attr_n.create(
            "input_focalLength",
            "ifl",
            OpenMaya.MFnNumericData.kDouble,
            35.0)
        attr_n.storable = True
        attr_n.keyable = True
        attr_n.readable = True
        attr_n.writable = True
        attr_n.setMin(0.001)
        cls.addAttribute(cls.m_input_focal)

        cls.m_output_focal = attr_n.create(
            "output_focalLength",
            "ofl",
            OpenMaya.MFnNumericData.kDouble,
            35.0)
        attr_n.storable = True
        attr_n.keyable = True
        attr_n.readable = True
        attr_n.writable = True
        attr_n.setMin(0.001)
        cls.addAttribute(cls.m_output_focal)

        # translate a
        cls.m_output_translateX = attr_u.create(
            "output_translateX", "otx", OpenMaya.MFnUnitAttribute.kDistance)
        cls.m_output_translateY = attr_u.create(
            "output_translateY", "oty", OpenMaya.MFnUnitAttribute.kDistance)
        cls.m_output_translateZ = attr_u.create(
            "output_translateZ", "otz", OpenMaya.MFnUnitAttribute.kDistance)

        cls.m_output_translate = attr_c.create(
            "output_translate", "oat")
        attr_c.addChild(cls.m_output_translateX)
        attr_c.addChild(cls.m_output_translateY)
        attr_c.addChild(cls.m_output_translateZ)
        cls.addAttribute(cls.m_output_translate)

        cls.attributeAffects(cls.m_input_obj_matrix, cls.m_output_translate)
        cls.attributeAffects(cls.m_input_cam_matrix, cls.m_output_translate)
        cls.attributeAffects(cls.m_input_focal, cls.m_output_translate)
        cls.attributeAffects(cls.m_output_focal, cls.m_output_translate)


def initializePlugin(mobject):
    """
    Function for initializing the plugin

    :param mobject: MObject for the plugin object
    :type mobject: OpenMaya.MObject

    :return: None
    :rtype: NoneType
    """
    mplugin = OpenMaya.MFnPlugin(mobject)

    try:
        mplugin.registerNode(FocalOffset.kPluginNodeName,
                             FocalOffset.kPluginNodeId,
                             FocalOffset.nodeCreator,
                             FocalOffset.nodeInitializer)
    except BaseException:
        raise RuntimeError(
            "Failed to register node: {0}".format(
                FocalOffset.kPluginNodeName))


def uninitializePlugin(mobject):
    """
    Function for uninitializing the plugin

    :param mobject: MObject for the plugin object
    :type mobject: OpenMaya.MObject

    :return: None
    :rtype: NoneType
    """
    mplugin = OpenMaya.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode(FocalOffset.kPluginNodeId)
    except BaseException:
        raise RuntimeError(
            "Failed to deregister node: {0}".format(
                FocalOffset.kPluginNodeName))
