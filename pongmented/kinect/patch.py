# noinspection PyProtectedMember
def patch_pykinect():
    import ctypes
    from pykinect.nui import PlanarImage
    from pykinect.nui.structs import _NuiSurfaceDesc
    from pongmented import log

    # noinspection PyProtectedMember
    @property
    def image_height_patch(self):
        desc = _NuiSurfaceDesc()
        PlanarImage._GetLevelDesc(self, 0, ctypes.byref(desc))
        return desc.height

    setattr(PlanarImage, 'height', image_height_patch)
    log.info('Successfully patched pykinect.PlanarImage.height')
