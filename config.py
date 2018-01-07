from PyQ import configuration
from PyQ.Gatename import Gatename

#..........results display............
label_width = 96
label_height = 36
label_line_width = 1
figure_dpi = 96

#..........resolution..........
win_width = 1024
win_height = 768

#..........icon relations.................
icon_path = "./resources/"
icon_select = "_select"
icon_extension = ".bmp"

#...........circuit settings..............
INITIAL_QUBITS = configuration.DEFAULT_SIZE
INITIAL_LAYERS_COUNT = configuration.DEFAULT_LAYER_COUNT
SIZE_RESTRICTION = configuration.SIZE_RESTRICTION

#...............slot states...............
HADAMARD = Gatename.HADAMARD
X = Gatename.PAULI_X
Y = Gatename.PAULI_Y
Z = Gatename.PAULI_Z
S = Gatename.S
T = Gatename.T
SWAP = Gatename.SWAP
# do przerobienia na uwzględnianie różnych control icons'
CONTROL = "CRTL"
UP = "_U"
DOWN = "_D"
MID = "_M"
EMPTY = "EMPTY"
ZERO = "0"
ONE = "1"
NONE = ""
HERM = "*"

#................icons...................
HADAMARD_ICON = icon_path + "hadamard" + icon_extension
HADAMARD_DOWN_ICON = icon_path + "hadamard_down" + icon_extension
HADAMARD_MID_ICON = icon_path + "hadamard_mid" + icon_extension
HADAMARD_UP_ICON = icon_path + "hadamard_up" + icon_extension
X_ICON = icon_path + "x" + icon_extension
X_DOWN_ICON = icon_path + "x_down" + icon_extension 
X_MID_ICON = icon_path + "x_mid" + icon_extension
X_UP_ICON = icon_path + "x_up" + icon_extension 
Y_ICON = icon_path + "y" + icon_extension
Y_DOWN_ICON = icon_path + "y_down" + icon_extension 
Y_MID_ICON = icon_path + "y_mid" + icon_extension 
Y_UP_ICON = icon_path + "y_up" + icon_extension 
Z_ICON = icon_path + "z" + icon_extension
Z_DOWN_ICON = icon_path + "z_down" + icon_extension 
Z_MID_ICON = icon_path + "z_mid" + icon_extension 
Z_UP_ICON = icon_path + "z_up" + icon_extension 
S_ICON = icon_path + "s" + icon_extension 
S_DOWN_ICON = icon_path + "s_down" + icon_extension 
S_MID_ICON = icon_path + "s_mid" + icon_extension
S_UP_ICON = icon_path + "s_up" + icon_extension

S_HERM_ICON = icon_path + "s_herm" + icon_extension
S_HERM_DOWN_ICON = icon_path + "s_herm_down" + icon_extension
S_HERM_MID_ICON = icon_path + "s_herm_mid" + icon_extension
S_HERM_UP_ICON = icon_path + "s_herm_up" + icon_extension

T_ICON = icon_path + "t" + icon_extension
T_DOWN_ICON = icon_path + "t_down" + icon_extension
T_MID_ICON = icon_path + "t_mid" + icon_extension
T_UP_ICON = icon_path + "t_up" + icon_extension

T_HERM_ICON = icon_path + "t_herm" + icon_extension
T_HERM_DOWN_ICON = icon_path + "t_herm_down" + icon_extension
T_HERM_MID_ICON = icon_path + "t_herm_mid" + icon_extension
T_HERM_UP_ICON = icon_path + "t_herm_up" + icon_extension

SWAP_ICON = icon_path + "swap" + icon_extension
SWAP_DOWN_ICON = icon_path + "swap_down" + icon_extension
SWAP_MID_ICON = icon_path + "swap_mid" + icon_extension
SWAP_UP_ICON = icon_path + "swap_up" + icon_extension
CONTROL_DOWN_ICON = icon_path + "control_down" + icon_extension 
CONTROL_MID_ICON = icon_path + "control_mid" + icon_extension
CONTROL_UP_ICON = icon_path + "control_up" + icon_extension
EMPTY_ICON = icon_path + "empty" + icon_extension 
EMPTY_MID_ICON = icon_path + "empty_mid" + icon_extension
ZERO_ICON = icon_path + "zero" + icon_extension 
ONE_ICON = icon_path + "one" + icon_extension 

#..........icons select................
HADAMARD_SELECT = icon_path + "hadamard" + icon_select + icon_extension
HADAMARD_DOWN_SELECT = icon_path + "hadamard_down" + icon_select + icon_extension 
HADAMARD_MID_SELECT = icon_path + "hadamard_mid" + icon_select + icon_extension
HADAMARD_UP_SELECT = icon_path + "hadamard_up" + icon_select + icon_extension 
X_SELECT = icon_path + "x" + icon_select + icon_extension
X_DOWN_SELECT = icon_path + "x_down" + icon_select + icon_extension 
X_MID_SELECT = icon_path + "x_mid" + icon_select + icon_extension
X_UP_SELECT = icon_path + "x_up" + icon_select + icon_extension 
Y_SELECT = icon_path + "y" + icon_select + icon_extension
Y_DOWN_SELECT = icon_path + "y_down" + icon_select + icon_extension 
Y_MID_SELECT = icon_path + "y_mid" + icon_select + icon_extension 
Y_UP_SELECT = icon_path + "y_up" + icon_select + icon_extension 
Z_SELECT = icon_path + "z" + icon_select + icon_extension
Z_DOWN_SELECT = icon_path + "z_down" + icon_select + icon_extension 
Z_MID_SELECT = icon_path + "z_mid" + icon_select + icon_extension 
Z_UP_SELECT = icon_path + "z_up" + icon_select + icon_extension
S_SELECT = icon_path + "s" + icon_select + icon_extension 
S_DOWN_SELECT = icon_path + "s_down" + icon_select + icon_extension 
S_MID_SELECT = icon_path + "s_mid" + icon_select + icon_extension
S_UP_SELECT = icon_path + "s_up" + icon_select + icon_extension

S_HERM_SELECT = icon_path + "s_herm" + icon_select + icon_extension
S_HERM_DOWN_SELECT = icon_path + "s_herm_down" + icon_select + icon_extension
S_HERM_MID_SELECT = icon_path + "s_herm_mid" + icon_select + icon_extension
S_HERM_UP_SELECT = icon_path + "s_herm_up" + icon_select + icon_extension

T_SELECT = icon_path + "t" + icon_select + icon_extension 
T_DOWN_SELECT = icon_path + "t_down" + icon_select + icon_extension 
T_MID_SELECT = icon_path + "t_mid" + icon_select + icon_extension 
T_UP_SELECT = icon_path + "t_up" + icon_select + icon_extension

T_HERM_SELECT = icon_path + "t_herm" + icon_select + icon_extension
T_HERM_DOWN_SELECT = icon_path + "t_herm_down" + icon_select + icon_extension
T_HERM_MID_SELECT = icon_path + "t_herm_mid" + icon_select + icon_extension
T_HERM_UP_SELECT = icon_path + "t_herm_up" + icon_select + icon_extension

SWAP_SELECT = icon_path + "swap" + icon_select + icon_extension
SWAP_DOWN_SELECT = icon_path + "swap_down" + icon_select + icon_extension
SWAP_MID_SELECT = icon_path + "swap_mid" + icon_select + icon_extension
SWAP_UP_SELECT = icon_path + "swap_up" + icon_select + icon_extension
CONTROL_DOWN_SELECT = icon_path + "control_down" + icon_select + icon_extension
CONTROL_MID_SELECT = icon_path + "control_mid" + icon_select + icon_extension
CONTROL_UP_SELECT = icon_path + "control_up" + icon_select + icon_extension
EMPTY_SELECT = icon_path + "empty" + icon_select + icon_extension
EMPTY_MID_SELECT = icon_path + "empty_mid" + icon_select + icon_extension
ZERO_SELECT = icon_path + "zero" + icon_select + icon_extension
ONE_SELECT = icon_path + "one" + icon_select + icon_extension