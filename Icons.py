from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import config

class Icons(object):
    """description of class"""

    _icons = None

    @classmethod
    def get_icon(cls, key = None):
        if cls._icons is None:
            cls._icons = {}
            cls._icons[config.NONE] = cls._set_icon_maps(config.NONE, config.NONE)
            cls._icons[config.ZERO] = cls._set_icon_maps(config.ZERO_ICON, config.ZERO_SELECT)
            cls._icons[config.ONE] = cls._set_icon_maps(config.ONE_ICON, config.ONE_SELECT)
            cls._icons[config.EMPTY] = cls._set_icon_maps(config.EMPTY_ICON, config.EMPTY_SELECT)
            cls._icons[config.EMPTY + config.MID] = cls._set_icon_maps(config.EMPTY_MID_ICON, config.EMPTY_MID_SELECT)
            cls._icons[config.HADAMARD] = cls._set_icon_maps(config.HADAMARD_ICON, config.HADAMARD_SELECT)
            cls._icons[config.HADAMARD + config.DOWN] = cls._set_icon_maps(config.HADAMARD_DOWN_ICON, config.HADAMARD_DOWN_SELECT)
            cls._icons[config.HADAMARD + config.MID] = cls._set_icon_maps(config.HADAMARD_MID_ICON, config.HADAMARD_MID_SELECT)
            cls._icons[config.HADAMARD + config.UP] = cls._set_icon_maps(config.HADAMARD_UP_ICON, config.HADAMARD_UP_SELECT)
            cls._icons[config.X] = cls._set_icon_maps(config.X_ICON, config.X_SELECT)
            cls._icons[config.X + config.DOWN] = cls._set_icon_maps(config.X_DOWN_ICON, config.X_DOWN_SELECT)
            cls._icons[config.X + config.MID] = cls._set_icon_maps(config.X_MID_ICON, config.X_MID_SELECT)
            cls._icons[config.X + config.UP] = cls._set_icon_maps(config.X_UP_ICON, config.X_UP_SELECT)
            cls._icons[config.Y] = cls._set_icon_maps(config.Y_ICON, config.Y_SELECT)
            cls._icons[config.Y + config.DOWN] = cls._set_icon_maps(config.Y_DOWN_ICON, config.Y_DOWN_SELECT)
            cls._icons[config.Y + config.MID] = cls._set_icon_maps(config.Y_MID_ICON, config.Y_MID_SELECT)
            cls._icons[config.Y + config.UP] = cls._set_icon_maps(config.Y_UP_ICON, config.Y_UP_SELECT)
            cls._icons[config.Z] = cls._set_icon_maps(config.Z_ICON, config.Z_SELECT)
            cls._icons[config.Z + config.DOWN] = cls._set_icon_maps(config.Z_DOWN_ICON, config.Z_DOWN_SELECT)
            cls._icons[config.Z + config.MID] = cls._set_icon_maps(config.Z_MID_ICON, config.Z_MID_SELECT)
            cls._icons[config.Z + config.UP] = cls._set_icon_maps(config.Z_UP_ICON, config.Z_UP_SELECT)
            cls._icons[config.S] = cls._set_icon_maps(config.S_ICON, config.S_SELECT)
            cls._icons[config.S + config.DOWN] = cls._set_icon_maps(config.S_DOWN_ICON, config.S_DOWN_SELECT)
            cls._icons[config.S + config.MID] = cls._set_icon_maps(config.S_MID_ICON, config.S_MID_SELECT)
            cls._icons[config.S + config.UP] = cls._set_icon_maps(config.S_UP_ICON, config.S_UP_SELECT)
            cls._icons[config.T] = cls._set_icon_maps(config.T_ICON, config.T_SELECT)
            cls._icons[config.T + config.DOWN] = cls._set_icon_maps(config.T_DOWN_ICON, config.T_DOWN_SELECT)
            cls._icons[config.T + config.MID] = cls._set_icon_maps(config.T_MID_ICON, config.T_MID_SELECT)
            cls._icons[config.T + config.UP] = cls._set_icon_maps(config.T_UP_ICON, config.T_UP_SELECT)
            cls._icons[config.SWAP] = cls._set_icon_maps(config.SWAP_ICON, config.SWAP_SELECT)
            cls._icons[config.SWAP + config.DOWN] = cls._set_icon_maps(config.SWAP_DOWN_ICON, config.SWAP_DOWN_SELECT)
            cls._icons[config.SWAP + config.MID] = cls._set_icon_maps(config.SWAP_MID_ICON, config.SWAP_MID_SELECT)
            cls._icons[config.SWAP + config.UP] = cls._set_icon_maps(config.SWAP_UP_ICON, config.SWAP_UP_SELECT)
            cls._icons[config.CONTROL + config.DOWN] = cls._set_icon_maps(config.CONTROL_DOWN_ICON, config.CONTROL_DOWN_SELECT)
            cls._icons[config.CONTROL + config.MID] = cls._set_icon_maps(config.CONTROL_MID_ICON, config.CONTROL_MID_SELECT)
            cls._icons[config.CONTROL + config.UP] = cls._set_icon_maps(config.CONTROL_UP_ICON, config.CONTROL_UP_SELECT)
        if key is not None:
            try:
                return cls._icons[key]
            except:
                return cls._icons[config.NONE]

    @classmethod
    def _set_icon_maps(self, normal, active = None):
        if active == None:
            active = normal
        icon = QIcon()
        icon.addFile(normal, QSize(48, 48), QIcon.Normal)
        icon.addFile(active, QSize(48, 48), QIcon.Active)
        return icon




