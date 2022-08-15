from maya import cmds


def main():

    # make the plugin load first
    cmds.loadPlugin("FocalOffsetNode", quiet=True)

    # list selection
    selected = cmds.ls(selection=True)

    if not selected:
        raise RuntimeError("Nothing selected!")

    if not len(selected) == 2:
        raise RuntimeError("Please select two transforms.")

    camera = selected[0]
    camera_shape = cmds.listRelatives(camera, children=True)[0]

    if not cmds.nodeType(camera_shape) == "camera":
        raise RuntimeError("Please first select your camera then object")

    focal_point = selected[1]

    # remove namespaces
    nice_camera_name = camera.split(":")[-1]
    nice_focal_name = focal_point.split(":")[-1]

    focal_node = cmds.createNode(
        "FocalOffset", name="{0}_{1}_focaloffset".format(
            nice_camera_name, nice_focal_name))

    out_camera = cmds.duplicate(
        camera, name="{0}_result".format(nice_camera_name))[0]

    if cmds.listRelatives(out_camera, parent=True):
        cmds.parent(out_camera, world=True)

    out_camera_shape = cmds.listRelatives(out_camera, children=True)[0]

    # input
    cmds.connectAttr(
        camera + ".worldMatrix", focal_node + ".input_camera_matrix")
    cmds.connectAttr(
        camera_shape + ".focalLength", focal_node + ".input_focalLength")
    cmds.connectAttr(
        focal_point + ".worldMatrix", focal_node + ".input_object_matrix")

    # output
    cmds.connectAttr(
        focal_node + ".output_translate", out_camera + ".translate")
    cmds.connectAttr(
        focal_node + ".output_focalLength", out_camera_shape + ".focalLength")

    cmds.orientConstraint(camera, out_camera)


if __name__ == "__main__":
    main()
