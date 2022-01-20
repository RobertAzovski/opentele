
from __future__ import annotations
from typing import List, Dict, Tuple, TypeVar, Type
from .utils import *
import hashlib, os

_T = TypeVar("_T")

class DeviceInfo(object):
    def __init__(self, model, version) -> None:
        self.model = model
        self.version = version
    def __str__(self) -> str:
        return f"{self.model} {self.version}"

class SystemInfo(BaseObject):

    
    deviceList : List[DeviceInfo] = []
    device_modesl : List[str] = []
    system_versions : List[str] = []

    def __init__(self) -> None:
        pass
    
    @classmethod
    def RandomDevice(cls : Type[SystemInfo], unique_id : str = None) -> DeviceInfo:
        hash_id = cls._strtohashid(unique_id)
        return cls._RandomDevice(hash_id)

    @classmethod
    def _RandomDevice(cls, hash_id : int):
        cls.__gen__()
        return cls._hashtovalue(hash_id, cls.deviceList)

    @classmethod
    def __gen__(cls):
        raise NotImplementedError(f"{cls.__name__} device not supported for randomize yet")

    @classmethod
    def _strtohashid(cls, unique_id : str = None):

        if unique_id != None and not isinstance(unique_id, str):
            unique_id = str(unique_id)

        byteid = os.urandom(32) if unique_id == None else unique_id.encode("utf-8")
        
        return int(hashlib.sha1(byteid).hexdigest(), 16) % (10 ** 12)

    @classmethod
    def _hashtorange(cls, hash_id : int, max, min = 0):
        return hash_id % (max - min) + min

    @classmethod
    def _hashtovalue(cls, hash_id : int, values : List[_T]) -> _T:
        return values[hash_id % len(values)]
    
    @classmethod
    def _CleanAndSimplify(cls, text : str) -> str:
        return " ".join(word for word in text.split(" ") if word)

class GeneralDesktopDevice(SystemInfo):
    
    # Total: 794 devices, update Jan 10th 2022
    # Real device models that I crawled myself from the internet
    #
    # This is the values in HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\BIOS
    # including SystemFamily, SystemProductName, BaseBoardProduct
    #
    # Filtered any models that exceed 15 characters
    # just like tdesktop does in lib_base https://github.com/desktop-app/lib_base/blob/master/base/platform/win/base_info_win.cpp#L173
    #
    # Feel free to use
    #
    # Sources: https://answers.microsoft.com/, https://www.techsupportforum.com/ and https://www.bleepingcomputer.com/

    device_models = [
        '0000000000', '0133D9', '03X0MN', '04GJJT', '04VWF2', '04WT2G', '05DN3X', '05FFDN', '0679', '0692FT',
        '06CDVY', '07JNH0', '0841B1A', '0874P6', '08VFX1', '095TWY', '09DKKT', '0C1D71', '0GDG8Y', '0H0CC0',
        '0H869M', '0J797R', '0JC474', '0KM92T', '0KP0FT', '0KV3RP', '0KWVT8', '0M277C', '0M332H', '0M9XW4',
        '0MYG77', '0N7TVV', '0NWWY0', '0P270J', '0PD9KD', '0PPYW4', '0R1203', '0R849J', '0T105W', '0TP406',
        '0U785D', '0UU795', '0WCNK6', '0Y2MRG', '0YF8P5', '1005P', '1005PE', '10125', '103C_53307F', '103C_53307F G=D',
        '103C_53311M HP', '103C_53316J', '103C_53316J G=D', '103C_5335KV', '103C_5336AN', '1066AWU', '110-050eam',
        '122-YW-E173', '131-GT-E767', '1425', '1494', '1496', '1633', '181D', '1849', '18F9', '198C', '1998',
        '20060', '20216', '20245', '20250', '20266', '20351', '20384', '20ATCTO1WW', '20AWA161TH', '20BECTO1WW',
        '20HD005EUS', '20HES2SF00', '20V9', '2166', '216C', '2248', '22CD', '2349G5P', '2378DHU', '2A9A', '2AB1',
        '2AC8', '2AE0', '304Bh', '3060', '30B9', '30DC', '30F7', '3600', '3624', '3627', '3642', '3646h', '3679CTO',
        '3717', '4157RC2', '4313CTO', '500-056', '600-1305t', '600-1370', '60073', '740U5L', '765802U', '80B8',
        '80C4', '80D0', '80E3', '80E5', '80E9', '80FC', '80RU', '80S7', '80Y7', '8114', '81DE', '81EF', '81H9',
        '81MU', '81VV', '8216', '8217', '82KU', '838F', '843B', '844C', '84A6', '84DA', '8582', '86F9', '8786',
        '8I945PL-G', '90NC001MUS', '90NC00JBUS', '945GT-GN', '965P-S3', '970A-G/3.1', '980DE3/U3S3', '990FXA-UD3',
        'A320M-S2H', 'A320M-S2H-CF', 'A55M-DGS', 'A58MD', 'A78XA-A2T', 'A7DA 3 series', 'A88X-PLUS', 'AB350 Gaming K4',
        'AO533', 'ASUS MB', 'AX3400', 'Acer Desktop', 'Acer Nitro 5', 'Alienware', 'Alienware 17', 'Alienware 17 R2',
        'Alienware 18', 'Alienware X51', 'Alienware m15', 'All Series', 'Aspire 4520', 'Aspire 4736Z', 'Aspire 5',
        'Aspire 5250', 'Aspire 5252', 'Aspire 5536', 'Aspire 5538G', 'Aspire 5732Z', 'Aspire 5735', 'Aspire 5738',
        'Aspire 5740', 'Aspire 6930G', 'Aspire 8950G', 'Aspire A515-51G', 'Aspire E5-575G', 'Aspire M3641',
        'Aspire M5-581T', 'Aspire M5-581TG', 'Aspire M5201', 'Aspire M5802', 'Aspire M5811', 'Aspire M7300',
        'Aspire R5-571TG', 'Aspire T180', 'Aspire V3-574G', 'Aspire V5-473G', 'Aspire V5-552P', 'Aspire VN7-792G',
        'Aspire X1301', 'Aspire X1700', 'Aspire X3400G', 'Aspire one', 'Asterope', 'Aurora', 'Aurora R5', 'Aurora-R4',
        'B360M D3H-CF', 'B360M-D3H', 'B450M DS3H', 'B450M DS3H-CF', 'B550 MB', 'B550M DS3H', 'B560 MB', 'B560M DS3H',
        'B85M-D2V', 'B85M-G', 'BDW', 'Boston', 'Burbank', 'C40', 'CELSIUS R640', 'CG1330', 'CG5290', 'CG8270',
        'CM1630', 'CathedralPeak', 'Charmander_KL', 'CloverTrail', 'Cuba MS-7301', 'D102GGC2', 'D900T', 'D945GCL',
        'DG41WV', 'DH61WW', 'DH67CL', 'DH77EB', 'DP55WB', 'DT1412', 'DX4300', 'DX4831', 'DX4860', 'DX58SO',
        'Dazzle_RL', 'Default string', 'Dell DM061', 'Dell DV051', 'Dell DXC061', 'Dell XPS420', 'Dell XPS720',
        'Desktop', 'Dimension 3000', 'Dimension 4700', 'Dimension E521', 'Durian 7A1', 'EP35-DS3', 'EP35-DS3R',
        'EP35-DS4', 'EP35C-DS3R', 'EP43-DS3L', 'EP45-DS3L', 'EP45-UD3L', 'EP45-UD3LR', 'EP45-UD3P', 'EP45-UD3R',
        'EP45T-UD3LR', 'ET1831', 'EX58-UD3R', 'Eee PC', 'Eureka3', 'Extensa 5620', 'Extensa 7620', 'F2A88X-D3HP',
        'F5SL', 'F71IX1', 'FJNB215', 'FM2A88X Pro3+', 'FMCP7AM&#160;', 'Freed_CFS', 'G1.Assassin2', 'G31M-ES2L',
        'G31MVP', 'G31T-M2', 'G33M-DS2R', 'G41M-Combo', 'G41M-ES2L', 'G41MT-S2P', 'G53JW', 'G53SW', 'G55VW',
        'G60JX', 'G73Sw', 'GA-73PVM-S2H', 'GA-770T-USB3', 'GA-78LMT-S2P', 'GA-78LMT-USB3', 'GA-790FXTA-UD5',
        'GA-870A-UD3', 'GA-880GM-D2H', 'GA-880GM-UD2H', 'GA-880GM-USB3', 'GA-880GMA-USB3', 'GA-890GPA-UD3H',
        'GA-890XA-UD3', 'GA-970A-D3', 'GA-EA790X-DS4', 'GA-MA74GM-S2H', 'GA-MA770-UD3', 'GA-MA770T-UD3', 'GA-MA770T-UD3P',
        'GA-MA785GM-US2H', 'GA-MA785GT-UD3H', 'GA-MA78G-DS3H', 'GA-MA78LM-S2H', 'GA-MA790FX-DQ6', 'GA-MA790X-DS4',
        'GA-MA790X-UD4', 'GA401IV', 'GA502IU', 'GE60 2OC\\2OE', 'GF8200E', 'GL502VMK', 'GL502VML', 'GL552VW',
        'GL553VD', 'GT5636E', 'GT5654', 'GT5674', 'GT70 2OC/2OD', 'Gateway Desktop', 'Gateway M280', 'Godzilla-N10',
        'H110M-A/M.2', 'H110M-DVS R3.0', 'H55-USB3', 'H55M-S2V', 'H61M-C', 'H61M-HVS', 'H61MXL/H61MXL-K', 'H67M-D2-B3',
        'H81H3-AM', 'H81M-D PLUS', 'H87-D3H', 'H87-D3H-CF', 'H87-HD3', 'H97-D3H', 'H97M Pro4', 'HP 15', 'HP 620',
        'HP All-in-One 22-c1xx', 'HP Compaq 6720s', 'HP Compaq 8000 Elite SFF', 'HP Compaq 8100 Elite CMT',
        'HP Compaq 8200 Elite CMT', 'HP Compaq 8200 Elite USDT', 'HP Compaq dc7800p Convertible', 'HP ENVY',
        'HP ENVY 14', 'HP ENVY 14 Sleekbook', 'HP ENVY TS m6 Sleekbook', 'HP ENVY x360 Convertible', 'HP ENVY x360 m6 Convertible',
        'HP Elite x2 1012 G1', 'HP EliteBook 6930p', 'HP EliteBook 8540w', 'HP EliteDesk 800 G1 SFF', 'HP G62',
        'HP G70', 'HP G7000', 'HP HDX18', 'HP Laptop 15-da0xxx', 'HP Pavilion', 'HP Pavilion 15', 'HP Pavilion Gaming 690-0xxx',
        'HP Pavilion Gaming 790-0xxx', 'HP Pavilion P6000 Series', 'HP Pavilion Sleekbook 14', 'HP Pavilion dm4',
        'HP Pavilion dv2700', 'HP Pavilion dv3', 'HP Pavilion dv4', 'HP Pavilion dv5', 'HP Pavilion dv6', 'HP Pavilion dv7',
        'HP Pavilion g6', 'HP ProBook 4320s', 'HP ProBook 450 G2', 'HP ProBook 4520s', 'HP ProBook 4530s', 'HP Spectre x360 Convertible',
        'HPE-498d', 'HPE-560Z', 'IDEAPAD', 'IMEDIA MC 2569', 'INVALID', 'ISKAA', 'IdeaCentre K330', 'Infoway',
        'Inspiron', 'Inspiron 1525', 'Inspiron 1526', 'Inspiron 1545', 'Inspiron 1564', 'Inspiron 1750', 'Inspiron 3891',
        'Inspiron 518', 'Inspiron 5570', 'Inspiron 560', 'Inspiron 570', 'Inspiron 6000', 'Inspiron 620', 'Inspiron 660',
        'Inspiron 7559', 'Inspiron 7720', 'Inspiron N5010', 'Inspiron N7010', 'Intel_Mobile', 'Ironman_SK',
        'K40ID', 'K43SA', 'K46CM', 'K50AB', 'K52JB', 'K53SV', 'K55VD', 'K56CM', 'KL3', 'KM400A-8237', 'Kabini CRB',
        'LENOVO', 'LEONITE', 'LH700', 'LIFEBOOK SH561', 'LNVNB161216', 'LX6810-01', 'LY325', 'Lancer 5A2', 'Lancer 5B2',
        'Latitude', 'Latitude 3410', 'Latitude 5400', 'Latitude 6430U', 'Latitude 7420', 'Latitude 7490', 'Latitude D630',
        'Latitude E4300', 'Latitude E5450', 'Latitude E6330', 'Latitude E6430', 'Latitude E6510', 'Latitude E6520',
        'Lenovo B50-70', 'Lenovo G50-80', 'Livermore8', 'M11x R2', 'M14xR2', 'M15x', 'M17x', 'M2N-E', 'M2N-SLI',
        'M2N-X', 'M3A-H/HDMI', 'M3A770DE', 'M3N78-AM', 'M4A785TD-M EVO', 'M4A785TD-V EVO', 'M4A78LT-M', 'M4A78T-E',
        'M4A79 Deluxe', 'M4A79XTD EVO', 'M4A87TD/USB3', 'M4A89GTD-PRO', 'M4N68T', 'M4N98TD EVO', 'M5640/M3640',
        'M570U', 'M5A78L LE', 'M5A78L-M LE', 'M5A78L-M/USB3', 'M5A87', 'M5A88-V EVO', 'M5A97', 'M5A97 LE R2.0',
        'M5A97 R2.0', 'M68MT-S2', 'M750SLI-DS4', 'M771CUH Lynx', 'MA51_HX', 'MAXIMUS V GENE', 'MCP61PM-AM',
        'MCP73PV', 'MJ-7592', 'MS-16GC', 'MS-1727', 'MS-17K3', 'MS-6714', 'MS-7094', 'MS-7325', 'MS-7327', 'MS-7350',
        'MS-7360', 'MS-7366', 'MS-7502', 'MS-7514', 'MS-7519', 'MS-7522', 'MS-7529', 'MS-7549', 'MS-7577', 'MS-7583',
        'MS-7586', 'MS-7592', 'MS-7599', 'MS-7637', 'MS-7640', 'MS-7641', 'MS-7673', 'MS-7678', 'MS-7680', 'MS-7681',
        'MS-7751', 'MS-7752', 'MS-7793', 'MS-7816', 'MS-7817', 'MS-7821', 'MS-7850', 'MS-7917', 'MS-7972', 'MS-7977',
        'MS-7A34', 'MS-7A62', 'MS-7B00', 'MS-7B46', 'MS-7C02', 'MS-7C75', 'MX8734', 'Makalu', 'Mi Laptop', 'N53SV',
        'N552VX', 'N55SF', 'N61Jq', 'N68-GS3 UCC', 'N68C-S UCC', 'N76VZ', 'N81Vp', 'NFORCE 680i SLI', 'NL8K_NL9K',
        'NL9K', 'NP740U5L-Y03US', 'NT500R5H-X51M', 'NUC7i7DNB', 'NUC7i7DNHE', 'NV52 Series', 'NV54 Series',
        'NWQAE', 'Narra6', 'Nettle2', 'Nitro AN515-52', 'Not Applicable', 'Notebook PC', 'OEM', 'OptiPlex 330',
        'OptiPlex 745', 'OptiPlex 755', 'OptiPlex 9010', 'OptiPlex GX520', 'P170EM', 'P170HMx', 'P35-DS3L',
        'P43-A7', 'P4M90-M7A', 'P4P800', 'P4S-LA', 'P55-UD4', 'P55-US3L', 'P55-USB3', 'P55A-UD3', 'P55A-UD3R',
        'P55A-UD4', 'P55A-UD4P', 'P55M-UD2', 'P5E-VM HDMI', 'P5K PRO', 'P5N32-E SLI', 'P5Q SE2', 'P5Q-PRO',
        'P5QL PRO', 'P5QL-E', 'P5QPL-AM', 'P67A-UD3-B3', 'P67A-UD4-B3', 'P67A-UD5-B3', 'P6T', 'P6T DELUXE V2',
        'P6T SE', 'P6X58D PREMIUM', 'P6X58D-E', 'P7477A-ABA 751n', 'P7P55D', 'P7P55D-E', 'P7P55D-E LX', 'P8610',
        'P8H61-M LE/USB3', 'P8H67-M PRO', 'P8P67', 'P8P67 PRO', 'P8P67-M PRO', 'P8Z68-V LE', 'P8Z68-V LX', 'P8Z68-V PRO',
        'P8Z77-V', 'P8Z77-V LX', 'P9X79 LE', 'PM800-8237', 'PORTEGE R705', 'PRIME A320M-K', 'PRIME B450M-A',
        'PRIME X470-PRO', 'PRIME Z270-A', 'PRIME Z390-A', 'PRIME Z490-V', 'PWWAA', 'Polaris_HW', 'Portable PC',
        'PowerEdge 2950', 'PowerEdge R515', 'PowerEdge T420', 'Precision', 'Precision 7530', 'Precision M6500',
        'Proteus IV', 'QL5', 'Qosmio X505', 'R560-LAR39E', 'ROG', 'RS690M2MA', 'RS780HVF', 'RV415/RV515', 'S500CA',
        'S550CM', 'SABERTOOTH P67', 'SABERTOOTH X58', 'SAMSUNG ATIV', 'SG41', 'SJV50PU', 'SKL', 'SM80_HR', 'SQ9204',
        'STRIKER II NSE', 'SVE14125CLB', 'SVE14A25CVW', 'SX2801', 'SX2802', 'Satellite A200', 'Satellite A215',
        'Satellite A300D', 'Satellite A500', 'Satellite A505', 'Satellite A665', 'Satellite A665D', 'Satellite C660',
        'Satellite C855D', 'Satellite L635', 'Satellite L650', 'Satellite P205D', 'Satellite R630', 'Shark 2.0',
        'Studio 1458', 'Studio 1555', 'Studio 1558', 'Studio 1747', 'Studio XPS 1640', 'Studio XPS 7100', 'Studio XPS 9100',
        'Suntory_KL', 'Swift 3', 'Swift SF314-52', 'T5212', 'T5226', 'T9408UK', 'TA790GX 128M', 'TA790GX A3+',
        'TA790GXB3', 'TA790GXE', 'TA790GXE 128M', 'TA990FXE', 'TM1963', 'TPower I55', 'TZ77XE3', 'ThinkPad L440',
        'ThinkPad T430', 'ThinkPad T440p', 'ThinkPad T470', 'ThinkPad T510', 'ThinkPad T540p', 'Type1Family',
        'U50F', 'UD3R-SLI', 'UL30VT', 'USOPP_BH', 'UX303UB', 'UX32VD', 'VAIO', 'VGN-NR498E', 'VGN-NW265F', 'VGN-SR45H_B',
        'VIOLET6', 'VPCEB27FD', 'VPCEE31FX', 'VPCF11QFX', 'VPCF1290X', 'VPCF22C5E', 'VPCF22J1E', 'VPCS111FM',
        'Veriton E430', 'VivoBook', 'Vostro', 'Vostro 1520', 'Vostro 1720', 'Vostro1510', 'W35xSS_370SS', 'W55xEU',
        'X421JQ', 'X510UNR', 'X550CA', 'X550JX', 'X555LAB', 'X556UB', 'X556UF', 'X570 GAMING X', 'X570 MB',
        'X58-USB3', 'X58A-UD3R', 'X58A-UD5', 'X58A-UD7', 'XPS', 'XPS 13 9305', 'XPS 13 9370', 'XPS 15 9550',
        'XPS 15 9560', 'XPS 630i', 'XPS 730', 'XPS 730X', 'XPS 8300', 'XPS 8700', 'XPS 8940', 'XPS A2420', 'XPS L501X',
        'XPS L701X', 'XPS M1530', 'YOGA 530-14ARR', 'YOGA 920-13IKB', 'YOGATablet2', 'Yoga2', 'Z10PE-D8 WS',
        'Z170 PRO GAMING', 'Z170-E', 'Z170X-Gaming 5', 'Z170X-UD3', 'Z170X-UD3-CF', 'Z370P D3', 'Z370P D3-CF',
        'Z68 Pro3', 'Z68A-D3-B3', 'Z68A-D3H-B3', 'Z68AP-D3', 'Z68MA-D2H-B3', 'Z68X-UD3H-B3', 'Z68XP-UD3', 'Z68XP-UD4',
        'Z77 Pro4', 'Z77X-D3H', 'Z87 Extreme6', 'Z87-D3HP', 'Z87-D3HP-CF', 'Z87M Extreme4', 'Z87N-WIFI', 'Z87X-OC',
        'Z87X-OC-CF', 'Z87X-UD4H', 'Z97-A', 'Z97-A-USB31', 'Z97-AR', 'Z97-C', 'Z97-PRO GAMER', 'Z97X-Gaming 7',
        'eMachines E725', 'h8-1070t', 'h8-1534', 'imedia S3720', 'ixtreme M5800', 'p6654y', 'p6710f'
    ]

class WindowsDevice(GeneralDesktopDevice):
    system_versions = [
        "Windows 10", "Windows 8", "Windows 8.1", "Windows 7"
    ]
    
    deviceList : List[DeviceInfo] = []

    @classmethod
    def __gen__(cls : Type[WindowsDevice]) -> None:
        
        if len(cls.deviceList) == 0:


            results : List[DeviceInfo]= []
            
            for model in cls.device_models:
                model = cls._CleanAndSimplify(model.replace("_", ""))
                for version in cls.system_versions:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results

class LinuxDevice(GeneralDesktopDevice):

    system_versions : List[str] = []
    deviceList : List[DeviceInfo] = []

    @classmethod
    def __gen__(cls : Type[LinuxDevice]) -> None:
        
        if len(cls.system_versions) == 0:
            # https://github.com/desktop-app/lib_base/blob/master/base/platform/linux/base_info_linux.cpp#L129

            # ? Purposely reduce the amount of devices parameter to generate deviceList more quickly
            enviroments = [
                "GNOME", "MATE", "XFCE", "Cinnamon", "Unity", "ubuntu", "LXDE"
            ]

            wayland = ["Wayland", "XWayland", "X11"]

            libcNames = ["glibc"]
            libcVers = ["2.31", "2.32", "2.33", "2.34"]

            # enviroments = [
            #     "GNOME", "MATE", "XFCE", "Cinnamon", "X-Cinnamon",
            #     "Unity", "ubuntu", "GNOME-Classic", "LXDE"
            # ]

            # wayland = ["Wayland", "XWayland", "X11"]

            # libcNames = ["glibc", "libc"]
            # libcVers = [
            #     "2.20", "2.21", "2.22", "2.23", "2.24", "2.25", "2.26", "2.27",
            #     "2.28", "2.29", "2.30", "2.31", "2.32", "2.33", "2.34"
            # ]
            
            def getitem(group : List[List[str]], prefix : str = "") -> List[str]:

                prefix = "" if prefix == "" else prefix + " "
                results = []
                if len(group) == 1:
                    for item in group[0]:
                        results.append(prefix  + item)
                    return results
                        
                for item in group[0]:
                    results.extend(getitem(group[1:], prefix + item))
                

                return results

            libcFullNames = getitem([libcNames, libcVers], "")

            cls.system_versions = getitem([enviroments, wayland, libcFullNames], "Linux")

            results : List[DeviceInfo]= []
            
            for version in cls.system_versions:
                for model in cls.device_models:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results

class macOSDevice(GeneralDesktopDevice):

    deviceList : List[DeviceInfo] = []

    # Total: 54 device models, update Jan 10th 2022
    # Only list device models since 2013
    #
    # Sources:
    # Thanks to: https://mrmacintosh.com/list-of-mac-boardid-deviceid-model-identifiers-machine-models/
    #       and: https://github.com/brunerd/jamfTools/blob/main/EAs/macOSCompatibility.sh
    #
    # Remark: https://www.innerfence.com/howto/apple-ios-devices-dates-versions-instruction-sets

    device_models = [
        'MacBookPro16,4', 'MacBookPro16,3', 'MacBookPro16,2', 'MacBookPro16,1', 'MacBookPro15,4',
        'MacBookPro15,3', 'MacBookPro15,2', 'MacBookPro15,1', 'MacBookPro14,3', 'MacBookPro14,2',
        'MacBookPro14,1', 'MacBookPro13,3', 'MacBookPro13,2', 'MacBookPro13,1', 'MacBookPro12,1',
        'MacBookPro11,5', 'MacBookPro11,4', 'MacBookPro11,3', 'MacBookPro11,2', 'MacBookPro11,1',
        'MacBookPro10,2', 'MacBookPro10,1',

        'MacBookAir9,1', 'MacBookAir8,2', 'MacBookAir8,1', 'MacBookAir7,2', 'MacBookAir7,2',
        'MacBookAir7,1', 'MacBookAir6,2', 'MacBookAir6,1', 'MacBookAir6,2',

        'MacBook10,1', 'MacBook9,1', 'MacBook8,2', 'MacBook8,1', 'MacPro7,1', 'MacPro6,1',

        'iMac20,2', 'iMac20,1', 'iMac19,1', 'iMac18,3', 'iMac18,2', 'iMac18,1', 'iMac17,1', 'iMac17,1',
        'iMac17,1', 'iMac16,2', 'iMac16,1', 'iMac15,2', 'iMac15,1', 'iMac14,4', 'iMac14,3', 'iMac14,2',
        'iMac14,1', 'iMacPro1,1'
    ]

    # Source: https://support.apple.com/en-us/HT201222
    system_versions = [
        'macOS 10.12', 'macOS 10.12.1', 'macOS 10.12.2', 'macOS 10.12.3', 'macOS 10.12.4',
        'macOS 10.12.5', 'macOS 10.12.6', 'macOS 10.13', 'macOS 10.13.1', 'macOS 10.13.2',
        'macOS 10.13.3', 'macOS 10.13.4', 'macOS 10.13.5', 'macOS 10.13.6', 'macOS 10.14', 
        'macOS 10.14.1', 'macOS 10.14.2', 'macOS 10.14.3', 'macOS 10.14.4', 'macOS 10.14.5', 
        'macOS 10.14.6', 'macOS 10.15', 'macOS 10.15.1', 'macOS 10.15.2', 'macOS 10.15.3', 
        'macOS 10.15.4', 'macOS 10.15.5', 'macOS 10.15.6', 'macOS 10.15.7', 'macOS 11.0', 
        'macOS 11.0.1', 'macOS 11.1', 'macOS 11.2', 'macOS 11.2.1', 'macOS 11.2.2', 'macOS 11.2.3', 
        'macOS 11.3', 'macOS 11.3.1', 'macOS 11.4', 'macOS 11.5', 'macOS 11.5.1', 'macOS 11.5.2', 
        'macOS 11.6', 'macOS 11.6.1', 'macOS 11.6.2', 'macOS 12.0', 'macOS 12.0.1', 'macOS 12.1'
    ]

    deviceList : List[DeviceInfo] = []

    @classmethod
    def __gen__(cls : Type[macOSDevice]) -> None:
        
        if len(cls.deviceList) == 0:
            
            # https://github.com/desktop-app/lib_base/blob/master/base/platform/mac/base_info_mac.mm#L42
            
            def FromIdentifier(model : str):
                words = []
                word = ""

                for ch in model:
                    if not ch.isalpha(): continue
                    if ch.isupper():
                        if word != "":
                            words.append(word)
                            word = ""
                    word += ch
                
                if word != "": words.append(word)
                result = ""
                for word in words:
                    if result != "" and word != "Mac" and word != "Book":
                        result += " "
                    result += word
                
                return result
                    
            new_devices_models = []
            for model in cls.device_models:
                model = cls._CleanAndSimplify(FromIdentifier(model))
                if not model in new_devices_models:
                    new_devices_models.append(model)
                    
            cls.device_models = new_devices_models

            results : List[DeviceInfo]= []
            
            for model in cls.device_models:
                for version in cls.system_versions:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results

class AndroidDevice(SystemInfo):

    device_models = [
        'Samsung GT-I5510M', 'Samsung GT-I5800L', 'Samsung SCH-I559', 'Samsung SCH-i559', 'Samsung Behold II', 
        'Samsung GT-I9260', 'Samsung SM-A710XZ', 'Samsung GT-B9120', 'Samsung SCH-R880', 'Samsung SCH-R720', 
        'Samsung SGH-S730M', 'Samsung SHV-E270L', 'Samsung SAMSUNG-SGH-I927', 'Samsung SGH-I927', 'Samsung SCH-I699I', 
        'Samsung Samsung Chromebook 3', 'Samsung Samsung Chromebook Plus', 'Samsung kevin', 'Samsung Samsung Chromebook Plus (V2)', 
        'Samsung nautilus', 'Samsung Samsung Chromebook Pro', 'Samsung caroline', 'Samsung SPH-D600', 'Samsung SAMSUNG-SGH-I857', 
        'Samsung SCH-I510', 'Samsung SM-G1600', 'Samsung SM-G1650', 'Samsung GT-I5500B', 'Samsung GT-I5500L', 
        'Samsung GT-I5500M', 'Samsung GT-I5503T', 'Samsung GT-I5510L', 'Samsung SGH-T759', 'Samsung EK-GC100', 
        'Samsung GT-B9062', 'Samsung YP-GI2', 'Samsung SHW-M100S', 'Samsung archer', 'Samsung SM-A716S', 'Samsung SM-A015A', 
        'Samsung SM-A015AZ', 'Samsung SM-A015F', 'Samsung SM-A015G', 'Samsung SM-A015M', 'Samsung SM-A015T1', 
        'Samsung SM-A015U', 'Samsung SM-A015U1', 'Samsung SM-A015V', 'Samsung SM-S111DL', 'Samsung SM-A013F', 
        'Samsung SM-A013G', 'Samsung SM-A013M', 'Samsung SM-A022F', 'Samsung SM-A022G', 'Samsung SM-A022M', 'Samsung SM-A025A', 
        'Samsung SM-A025AZ', 'Samsung SM-A025F', 'Samsung SM-A025G', 'Samsung SM-A025M', 'Samsung SM-A025U', 
        'Samsung SM-A025U1', 'Samsung SM-A025V', 'Samsung SM-A105F', 'Samsung SM-A105FN', 'Samsung SM-A105G', 
        'Samsung SM-A105M', 'Samsung SM-A105N', 'Samsung SM-A102U', 'Samsung SM-A102U1', 'Samsung SM-A102W', 
        'Samsung SM-S102DL', 'Samsung SM-A102N', 'Samsung SM-A107F', 'Samsung SM-A107M', 'Samsung SM-A115A', 
        'Samsung SM-A115AP', 'Samsung SM-A115AZ', 'Samsung SM-A115F', 'Samsung SM-A115M', 'Samsung SM-A115U', 
        'Samsung SM-A115U1', 'Samsung SM-A115W', 'Samsung SM-A125F', 'Samsung SM-A125M', 'Samsung SM-A125N', 
        'Samsung SM-A125U', 'Samsung SM-A125U1', 'Samsung SM-S127DL', 'Samsung SM-A260F', 'Samsung SM-A260G', 
        'Samsung SC-02M', 'Samsung SCV46', 'Samsung SCV46-j', 'Samsung SCV46-u', 'Samsung SM-A205F', 'Samsung SM-A205FN', 
        'Samsung SM-A205G', 'Samsung SM-A205GN', 'Samsung SM-A205W', 'Samsung SM-A205YN', 'Samsung SM-A205U', 
        'Samsung SM-A205U1', 'Samsung SM-S205DL', 'Samsung SM-A202F', 'Samsung SM-A2070', 'Samsung SM-A207F', 
        'Samsung SM-A207M', 'Samsung SC-42A', 'Samsung SCV49', 'Samsung SM-A215U', 'Samsung SM-A215U1', 'Samsung SM-A215W', 
        'Samsung SM-S215DL', 'Samsung SM-A217F', 'Samsung SM-A217M', 'Samsung SM-A217N', 'Samsung SM-A226B', 
        'Samsung SM-A226B', 'Samsung SM-A300H', 'Samsung SM-A300F', 'Samsung SM-A300M', 'Samsung SM-A300XZ', 
        'Samsung SM-A300YZ', 'Samsung SM-A3000', 'Samsung SM-A300X', 'Samsung SM-A3009', 'Samsung SM-A300G', 
        'Samsung SM-A300F', 'Samsung SM-A3000', 'Samsung SM-A300YZ', 'Samsung SM-A300FU', 'Samsung SM-A300XU', 
        'Samsung SM-A300Y', 'Samsung SM-A320Y', 'Samsung SM-A013G', 'Samsung SM-A310F', 'Samsung SM-A310M', 'Samsung SM-A310X', 
        'Samsung SM-A310Y', 'Samsung SM-A310N0', 'Samsung SM-A320F', 'Samsung SM-A320FL', 'Samsung SM-A320X', 
        'Samsung SCV43', 'Samsung SCV43-j', 'Samsung SCV43-u', 'Samsung SM-A305F', 'Samsung SM-A305FN', 'Samsung SM-A305G', 
        'Samsung SM-A305GN', 'Samsung SM-A305GT', 'Samsung SM-A305N', 'Samsung SM-A305YN', 'Samsung SM-A307FN', 
        'Samsung SM-A307G', 'Samsung SM-A307GN', 'Samsung SM-A307GT', 'Samsung SM-A315F', 'Samsung SM-A315G', 
        'Samsung SM-A315N', 'Samsung SM-A325F', 'Samsung SM-A325M', 'Samsung SCG08', 'Samsung SM-A326B', 'Samsung SM-A326BR', 
        'Samsung SM-A326U', 'Samsung SM-A326U1', 'Samsung SM-A326W', 'Samsung SM-S326DL', 'Samsung SM-A405FM', 
        'Samsung SM-A405FN', 'Samsung SM-A405S', 'Samsung SM-A3050', 'Samsung SM-A3051', 'Samsung SM-A3058', 
        'Samsung SC-41A', 'Samsung SCV48', 'Samsung SM-A415F', 'Samsung SM-A4260', 'Samsung SM-A426B', 'Samsung SM-A426N', 
        'Samsung SM-A426U', 'Samsung SM-A426U1', 'Samsung SM-A500H', 'Samsung SM-A500F', 'Samsung SM-A500G', 
        'Samsung SM-A500M', 'Samsung SM-A500XZ', 'Samsung SM-A5000', 'Samsung SM-A500X', 'Samsung SM-A5009', 
        'Samsung SM-A5000', 'Samsung SM-A500YZ', 'Samsung SM-A500FU', 'Samsung SM-A500Y', 'Samsung SM-A500W', 
        'Samsung SM-A500K', 'Samsung SM-A500L', 'Samsung SM-A500F1', 'Samsung SM-A500S', 'Samsung SM-A510Y', 
        'Samsung SM-A510F', 'Samsung SM-A510M', 'Samsung SM-A510X', 'Samsung SM-A510Y', 'Samsung SM-A5108', 'Samsung SM-A510K', 
        'Samsung SM-A510L', 'Samsung SM-A510S', 'Samsung SM-A510Y', 'Samsung SM-A5100', 'Samsung SM-A5100X', 
        'Samsung SM-A510XZ', 'Samsung SM-A520F', 'Samsung SM-A520X', 'Samsung SM-A520W', 'Samsung SM-A520K', 
        'Samsung SM-A520L', 'Samsung SM-A520S', 'Samsung SM-A505F', 'Samsung SM-A505FM', 'Samsung SM-A505FN', 
        'Samsung SM-A505G', 'Samsung SM-A505GN', 'Samsung SM-A505GT', 'Samsung SM-A505N', 'Samsung SM-A505U', 
        'Samsung SM-A505U1', 'Samsung SM-A505W', 'Samsung SM-A505YN', 'Samsung SM-S506DL', 'Samsung SM-A5070', 
        'Samsung SM-A507FN', 'Samsung SM-A515F', 'Samsung SM-A515U', 'Samsung SM-A515U1', 'Samsung SM-A515W', 
        'Samsung SM-S515DL', 'Samsung SC-54A', 'Samsung SCG07', 'Samsung SM-A5160', 'Samsung SM-A516B', 'Samsung SM-A516N', 
        'Samsung SM-A516U', 'Samsung SM-A516U1', 'Samsung SM-A516V', 'Samsung SM-A525F', 'Samsung SM-A5260', 
        'Samsung SM-A526B', 'Samsung SM-A526N', 'Samsung SM-A526U', 'Samsung SM-A526U1', 'Samsung SM-A526W', 
        'Samsung SM-A600AZ', 'Samsung SM-A600A', 'Samsung SM-A600T1', 'Samsung SM-A600P', 'Samsung SM-A600T', 
        'Samsung SM-A600U', 'Samsung SM-A600F', 'Samsung SM-A600FN', 'Samsung SM-A600G', 'Samsung SM-A600GN', 
        'Samsung SM-A600N', 'Samsung SM-A605F', 'Samsung SM-A605FN', 'Samsung SM-A605G', 'Samsung SM-A605GN', 
        'Samsung SM-A6050', 'Samsung SM-A6060', 'Samsung SM-A606Y', 'Samsung SM-A700H', 'Samsung SM-A700F', 'Samsung SM-A700FD', 
        'Samsung SM-A700X', 'Samsung SM-A7000', 'Samsung SM-A700YD', 'Samsung SM-A7009', 'Samsung SM-A700K', 
        'Samsung SM-A700L', 'Samsung SM-A700S', 'Samsung SM-A750C', 'Samsung SM-A750F', 'Samsung SM-A750FN', 
        'Samsung SM-A750G', 'Samsung SM-A750GN', 'Samsung SM-A750N', 'Samsung SM-A710F', 'Samsung SM-A710M', 
        'Samsung SM-A710X', 'Samsung SM-A7108', 'Samsung SM-A710K', 'Samsung SM-A710L', 'Samsung SM-A710S', 'Samsung SM-A710Y', 
        'Samsung SM-A7100', 'Samsung SM-A720F', 'Samsung SM-A720S', 'Samsung SM-A7050', 'Samsung SM-A705F', 'Samsung SM-A705FN', 
        'Samsung SM-A705GM', 'Samsung SM-A705MN', 'Samsung SM-A705U', 'Samsung SM-A705W', 'Samsung SM-A705YN', 
        'Samsung SM-A7070', 'Samsung SM-A707F', 'Samsung SM-A715F', 'Samsung SM-A715W', 'Samsung SM-A7160', 'Samsung SM-A716B', 
        'Samsung SM-A716U', 'Samsung SM-A716U1', 'Samsung SM-A716V', 'Samsung SM-A725F', 'Samsung SM-A725M', 
        'Samsung SCV32', 'Samsung SM-A800F', 'Samsung SM-A800YZ', 'Samsung SM-A800S', 'Samsung SM-A800I', 'Samsung SM-A800IZ', 
        'Samsung SM-A8000', 'Samsung SM-A800X', 'Samsung SM-G885F', 'Samsung SM-G885Y', 'Samsung SM-G8850', 'Samsung SM-G885S', 
        'Samsung SM-A810F', 'Samsung SM-A810YZ', 'Samsung SM-A810S', 'Samsung SM-A530F', 'Samsung SM-A530X', 
        'Samsung SM-A530W', 'Samsung SM-A530N', 'Samsung SM-A730F', 'Samsung SM-A730X', 'Samsung SM-A8050', 'Samsung SM-A805F', 
        'Samsung SM-A805N', 'Samsung SM-G887F', 'Samsung SM-G8870', 'Samsung SM-A920F', 'Samsung SM-A920N', 'Samsung SM-A9200', 
        'Samsung SM-G887N', 'Samsung SM-A9100', 'Samsung SM-A910F', 'Samsung SM-G8850', 'Samsung SM-G8858', 'Samsung SM-A6050', 
        'Samsung SM-A605XC', 'Samsung SM-A6058', 'Samsung SM-A9000', 'Samsung SM-A9080', 'Samsung SM-A908B', 
        'Samsung SM-A908N', 'Samsung SM-A9200', 'Samsung GT-S5830', 'Samsung GT-S5830B', 'Samsung GT-S5830C', 
        'Samsung GT-S5830D', 'Samsung GT-S5830F', 'Samsung GT-S5830G', 'Samsung GT-S5830L', 'Samsung GT-S5830M', 
        'Samsung GT-S5830T', 'Samsung GT-S5830i', 'Samsung GT-S5831i', 'Samsung GT-S5838', 'Samsung GT-S5839i', 
        'Samsung GT-S6358', 'Samsung SCH-I619', 'Samsung SHW-M240S', 'Samsung SM-G310R5', 'Samsung SM-G357M', 
        'Samsung SM-G313HU', 'Samsung SM-G313HY', 'Samsung SM-G313M', 'Samsung SM-G313MY', 'Samsung SM-G313U', 
        'Samsung GT-S6800', 'Samsung GT-S6352', 'Samsung GT-S6802', 'Samsung GT-S6802B', 'Samsung SCH-i579', 
        'Samsung SCH-I589', 'Samsung SCH-i589', 'Samsung SCH-i579', 'Samsung SCH-i589', 'Samsung GT-S7500', 'Samsung GT-S7500L', 
        'Samsung GT-S7500T', 'Samsung GT-S7500W', 'Samsung GT-S7508', 'Samsung SGH-I827D', 'Samsung SM-S765C', 
        'Samsung SM-S766C', 'Samsung SM-G310HN', 'Samsung SM-G357FZ', 'Samsung GT-I8160', 'Samsung GT-I8160L', 
        'Samsung GT-I8160P', 'Samsung GT-S7560', 'Samsung GT-S7560M', 'Samsung GT-S7270', 'Samsung GT-S7270L', 
        'Samsung SCH-I679', 'Samsung GT-S7278', 'Samsung GT-S7272', 'Samsung GT-S7275', 'Samsung GT-S7275B', 
        'Samsung GT-S7275R', 'Samsung GT-S7275T', 'Samsung GT-S7275Y', 'Samsung GT-S7272C', 'Samsung GT-S7278U', 
        'Samsung GT-S7273T', 'Samsung SM-G313ML', 'Samsung SM-G316H', 'Samsung SM-G316HU', 'Samsung SM-G316M', 
        'Samsung SM-G316MY', 'Samsung SM-G313F', 'Samsung SM-G313MU', 'Samsung SM-G313HN', 'Samsung SM-G3139D', 
        'Samsung SM-G313H', 'Samsung SM-G316U', 'Samsung SM-G318H', 'Samsung SM-G318ML', 'Samsung SM-G318HZ', 
        'Samsung SM-G318MZ', 'Samsung SM-G316ML', 'Samsung SC-01H', 'Samsung SCH-R820', 'Samsung SCH-R830C', 
        'Samsung SM-G850F', 'Samsung SM-G850FQ', 'Samsung SM-G850M', 'Samsung SM-G850X', 'Samsung SM-G850Y', 
        'Samsung SAMSUNG-SM-G850A', 'Samsung SM-G850W', 'Samsung SM-G8508S', 'Samsung SM-G850K', 'Samsung SM-G850L', 
        'Samsung SM-G850S', 'Samsung SAMSUNG-SGH-I407', 'Samsung GT-I5800', 'Samsung GT-I5800L', 'Samsung GT-I5800D', 
        'Samsung GT-I5801', 'Samsung SAMSUNG-SGH-I827', 'Samsung SCH-R920', 'Samsung SM-G386T', 'Samsung SCH-R830', 
        'Samsung GT-I8250', 'Samsung GT-I8530', 'Samsung SM-C5000', 'Samsung SM-C500X', 'Samsung SM-C5000', 'Samsung SM-C5010', 
        'Samsung SM-C5018', 'Samsung SM-C7000', 'Samsung SM-C700X', 'Samsung SM-C701X', 'Samsung SM-C701F', 'Samsung SM-C7010', 
        'Samsung SM-C7018', 'Samsung SM-C7100', 'Samsung SM-C710X', 'Samsung SM-C7108', 'Samsung SM-C900F', 'Samsung SM-C900Y', 
        'Samsung SM-C9000', 'Samsung SM-C9008', 'Samsung SM-C900X', 'Samsung EK-GC100', 'Samsung SAMSUNG-EK-GC100', 
        'Samsung EK-GC100', 'Samsung EK-KC100K', 'Samsung EK-KC120L', 'Samsung EK-KC120S', 'Samsung EK-GC120', 
        'Samsung EK-KC100S', 'Samsung EK-GC110', 'Samsung EK-GC110', 'Samsung EK-GN100', 'Samsung EK-GN120', 
        'Samsung EK-GC200', 'Samsung SCH-S738C', 'Samsung GT-B5330', 'Samsung GT-B5330B', 'Samsung GT-B5330L', 
        'Samsung SM-G386T1', 'Samsung SM-G386W', 'Samsung GT-I8262', 'Samsung GT-I8260', 'Samsung GT-I8260L', 
        'Samsung SM-G355H', 'Samsung GT-I8580', 'Samsung SHW-M570S', 'Samsung SM-G386F', 'Samsung SM-G3518', 
        'Samsung SM-G3586V', 'Samsung SM-G3589W', 'Samsung SM-G5108', 'Samsung SM-G5108Q', 'Samsung SM-G350', 
        'Samsung SM-G3502', 'Samsung SM-G3502L', 'Samsung SM-G3502T', 'Samsung SM-G350L', 'Samsung SM-G350M', 
        'Samsung SM-G360H', 'Samsung SM-G360HU', 'Samsung SM-G360F', 'Samsung SM-G360FY', 'Samsung SM-G360M', 
        'Samsung SAMSUNG-SM-G360AZ', 'Samsung SM-G360R6', 'Samsung SM-G360P', 'Samsung SM-S820L', 'Samsung SM-G360V', 
        'Samsung SM-G361H', 'Samsung SM-G361HU', 'Samsung SM-G361F', 'Samsung SM-G361M', 'Samsung SM-G360T1', 
        'Samsung SM-G360T', 'Samsung SM-G3606', 'Samsung SM-G3608', 'Samsung SM-G3609', 'Samsung SM-G360GY', 
        'Samsung GT-I8260E', 'Samsung SHW-M580D', 'Samsung SHW-M585D', 'Samsung SM-G355H', 'Samsung SM-G355HQ', 
        'Samsung SM-G355M', 'Samsung SM-G3556D', 'Samsung SM-G3558', 'Samsung SM-G3559', 'Samsung SM-G355HN', 
        'Samsung SCH-R740C', 'Samsung SCH-S735C', 'Samsung GT-I8268', 'Samsung SM-E500H', 'Samsung SM-E500F', 
        'Samsung SM-E500M', 'Samsung SM-S978L', 'Samsung SM-E500YZ', 'Samsung SM-E700H', 'Samsung SM-E700F', 
        'Samsung SM-E700M', 'Samsung SM-E7000', 'Samsung SM-E7009', 'Samsung SM-E7000', 'Samsung SM-G165N', 'Samsung GT-I5500', 
        'Samsung GT-I5503', 'Samsung GT-I5508', 'Samsung GT-I5510', 'Samsung SGH-T599N', 'Samsung SGH-T599', 
        'Samsung SGH-T599V', 'Samsung SGH-T679', 'Samsung SAMSUNG-SGH-I577', 'Samsung SAMSUNG-SGH-I437', 'Samsung SAMSUNG-SGH-I437P', 
        'Samsung GT-I8730', 'Samsung GT-I8730T', 'Samsung SAMSUNG-SGH-I437Z', 'Samsung SM-G3815', 'Samsung SM-E025F', 
        'Samsung SM-F127G', 'Samsung SM-F415F', 'Samsung SM-E5260', 'Samsung SM-E625F', 'Samsung SCH-I629', 'Samsung GT-S6810', 
        'Samsung GT-S6810B', 'Samsung GT-S6810E', 'Samsung GT-S6810L', 'Samsung GT-S6812i', 'Samsung GT-S6818', 
        'Samsung GT-S6818V', 'Samsung GT-S6812', 'Samsung GT-S6812B', 'Samsung GT-S6790N', 'Samsung GT-S6810M', 
        'Samsung GT-S6810P', 'Samsung GT-S6790', 'Samsung GT-S6790E', 'Samsung GT-S6790L', 'Samsung GT-S6812C', 
        'Samsung GT-S6792L', 'Samsung SC-04J', 'Samsung SC-02L', 'Samsung GT-S5670', 'Samsung GT-S5670B', 'Samsung GT-S5670L', 
        'Samsung SCV44', 'Samsung SM-F9000', 'Samsung SM-F900F', 'Samsung SM-F900U', 'Samsung SM-F900U1', 'Samsung SM-F900W', 
        'Samsung SM-F907B', 'Samsung SM-F907N', 'Samsung SM-G155S', 'Samsung SM-G150NK', 'Samsung SM-G150N0', 
        'Samsung SM-G150NL', 'Samsung SM-G150NS', 'Samsung SM-G160N', 'Samsung SM-G1650', 'Samsung GT-S7390', 
        'Samsung GT-S7390E', 'Samsung GT-S7390G', 'Samsung GT-S5660', 'Samsung GT-S5660B', 'Samsung GT-S5660L', 
        'Samsung GT-S5660M', 'Samsung GT-S5660V', 'Samsung SCH-i569', 'Samsung SHW-M290K', 'Samsung SHW-M290S', 
        'Samsung SAMSUNG-SM-G530A', 'Samsung GT-I9230', 'Samsung GT-I9235', 'Samsung SHV-E400K', 'Samsung SHV-E400S', 
        'Samsung SM-W2015', 'Samsung SCH-I879', 'Samsung GT-I9128', 'Samsung GT-I9128V', 'Samsung SHV-E270K', 
        'Samsung SHV-E270S', 'Samsung GT-I9118', 'Samsung GT-I9080E', 'Samsung GT-I9080L', 'Samsung SHV-E275K', 
        'Samsung SHV-E275S', 'Samsung GT-I9128E', 'Samsung GT-I9128I', 'Samsung GT-I9082', 'Samsung GT-I9082L', 
        'Samsung SM-G7202', 'Samsung SM-G7200', 'Samsung SM-G720AX', 'Samsung GT-I9060', 'Samsung GT-I9060L', 
        'Samsung GT-I9082C', 'Samsung GT-I9063T', 'Samsung GT-I9168', 'Samsung GT-I9168I', 'Samsung GT-I9060C', 
        'Samsung GT-I9060I', 'Samsung GT-I9060M', 'Samsung SCH-I879E', 'Samsung SM-G530H', 'Samsung SM-G530BT', 
        'Samsung SM-G5306W', 'Samsung SM-G5308W', 'Samsung SM-G530F', 'Samsung SM-G530M', 'Samsung SM-G5309W', 
        'Samsung SM-G5308W', 'Samsung SM-G530MU', 'Samsung SM-G530Y', 'Samsung SM-G530H', 'Samsung SM-G530R7', 
        'Samsung gprimelteacg', 'Samsung SM-G530W', 'Samsung SM-G530T1', 'Samsung SM-G530P', 'Samsung SM-S920L', 
        'Samsung SM-G530T', 'Samsung SM-G530R4', 'Samsung SM-G530FZ', 'Samsung SAMSUNG-SM-G530AZ', 'Samsung SM-G531H', 
        'Samsung SM-G531BT', 'Samsung SM-G531F', 'Samsung SM-G531M', 'Samsung SM-G531Y', 'Samsung SM-G532F', 
        'Samsung SM-G532MT', 'Samsung SM-J250F', 'Samsung GT-I9082i', 'Samsung SM-G720N0', 'Samsung SM-G7102', 
        'Samsung SM-G7106', 'Samsung SM-G7108', 'Samsung SM-G7109', 'Samsung SM-G7102T', 'Samsung SM-G710', 'Samsung SM-G7105', 
        'Samsung SM-G7105H', 'Samsung SM-G7105L', 'Samsung SM-G710K', 'Samsung SM-G710L', 'Samsung SM-G710S', 
        'Samsung SCH-R910', 'Samsung SCH-R915', 'Samsung SCH-I759', 'Samsung SGH-N075T', 'Samsung SM-J100H', 
        'Samsung SM-J100ML', 'Samsung SM-S777C', 'Samsung SM-J100F', 'Samsung SM-J100G', 'Samsung SM-J100M', 
        'Samsung SM-J100FN', 'Samsung SM-J100MU', 'Samsung SM-J100Y', 'Samsung SM-J100VPP', 'Samsung SM-J120F', 
        'Samsung SM-J120FN', 'Samsung SM-J120M', 'Samsung SAMSUNG-SM-J120AZ', 'Samsung SAMSUNG-SM-J120A', 'Samsung SM-J120W', 
        'Samsung SM-J120P', 'Samsung SM-S120VL', 'Samsung SM-J120F', 'Samsung SM-J110F', 'Samsung SM-J110G', 
        'Samsung SM-J110M', 'Samsung SM-J111F', 'Samsung SM-J111M', 'Samsung SM-J110H', 'Samsung SM-J110L', 'Samsung SM-J105B', 
        'Samsung SM-J105H', 'Samsung SM-J105B', 'Samsung SM-J105H', 'Samsung SM-J105F', 'Samsung SM-J105M', 'Samsung SM-J105Y', 
        'Samsung SM-J106B', 'Samsung SM-J106H', 'Samsung SM-J106B', 'Samsung SM-J106M', 'Samsung SM-J120H', 'Samsung SM-J120G', 
        'Samsung SM-J120ZN', 'Samsung SM-J200H', 'Samsung SM-J260T1', 'Samsung SM-S260DL', 'Samsung SM-J200F', 
        'Samsung SM-J200G', 'Samsung SM-J200GU', 'Samsung SM-J200M', 'Samsung SM-J200Y', 'Samsung SM-J200BT', 
        'Samsung SM-J250F', 'Samsung SM-J250Y', 'Samsung SM-J260F', 'Samsung SM-J260G', 'Samsung SM-J260M', 'Samsung SM-J260Y', 
        'Samsung SM-J260FU', 'Samsung SM-J260GU', 'Samsung SM-J260MU', 'Samsung SM-G532G', 'Samsung SM-G532M', 
        'Samsung SM-J210F', 'Samsung SM-J250F', 'Samsung SM-J250G', 'Samsung SM-J250M', 'Samsung SM-J260AZ', 
        'Samsung SM-J210F', 'Samsung SM-J3109', 'Samsung SM-J320P', 'Samsung SM-J327U', 'Samsung SM-J327R7', 
        'Samsung SM-J327R6', 'Samsung SM-J327R4', 'Samsung SM-J337R7', 'Samsung SM-J337VPP', 'Samsung SM-J337U', 
        'Samsung SM-J320H', 'Samsung SM-J3300', 'Samsung SM-J3308', 'Samsung SM-J337P', 'Samsung SM-J337R4', 
        'Samsung SM-J327V', 'Samsung SM-J327P', 'Samsung SM-J327VPP', 'Samsung SM-S367VL', 'Samsung SM-S357BL', 
        'Samsung SAMSUNG-SM-J326AZ', 'Samsung SAMSUNG-SM-J327AZ', 'Samsung SAMSUNG-SM-J327A', 'Samsung SM-S337TL', 
        'Samsung SM-S327VL', 'Samsung SM-J327W', 'Samsung SM-J327T1', 'Samsung SM-J327T', 'Samsung SM-J3110', 
        'Samsung SM-J3119', 'Samsung SM-J330G', 'Samsung SM-J337T', 'Samsung SM-J337V', 'Samsung SM-J320N0', 
        'Samsung SM-S320VL', 'Samsung SM-J320Y', 'Samsung SM-J320YZ', 'Samsung SM-J320R4', 'Samsung SM-J320V', 
        'Samsung SM-J320VPP', 'Samsung SM-J320ZN', 'Samsung SM-J320F', 'Samsung SM-J320G', 'Samsung SM-J320M', 
        'Samsung SAMSUNG-SM-J320AZ', 'Samsung SAMSUNG-SM-J321AZ', 'Samsung SAMSUNG-SM-J320A', 'Samsung SM-J320W8', 
        'Samsung SM-J320FN', 'Samsung SM-J330F', 'Samsung SM-J330FN', 'Samsung SM-J330N', 'Samsung SM-J330L', 
        'Samsung SM-J337W', 'Samsung SM-J400F', 'Samsung SM-J400G', 'Samsung SM-J400M', 'Samsung SM-J410F', 'Samsung SM-J410G', 
        'Samsung SM-J415F', 'Samsung SM-J415FN', 'Samsung SM-J415G', 'Samsung SM-J415GN', 'Samsung SM-J415N', 
        'Samsung SM-J500H', 'Samsung SM-J5007', 'Samsung SM-J500F', 'Samsung SM-J500G', 'Samsung SM-J500M', 'Samsung SM-J5008', 
        'Samsung SM-J500N0', 'Samsung SM-J500FN', 'Samsung SM-J530F', 'Samsung SM-J530FM', 'Samsung SM-J530K', 
        'Samsung SM-J530L', 'Samsung SM-J530S', 'Samsung SM-J500Y', 'Samsung SM-G570F', 'Samsung SM-G570M', 'Samsung SM-G570Y', 
        'Samsung SM-G570F', 'Samsung SM-G5700', 'Samsung SM-J530G', 'Samsung SM-J530GM', 'Samsung SM-J530Y', 
        'Samsung SM-J530YM', 'Samsung SM-J510H', 'Samsung SM-J5108', 'Samsung SM-J510F', 'Samsung SM-J510FN', 
        'Samsung SM-J510FQ', 'Samsung SM-J510GN', 'Samsung SM-J510MN', 'Samsung SM-J510UN', 'Samsung SM-J510K', 
        'Samsung SM-J510L', 'Samsung SM-J510S', 'Samsung SM-J600F', 'Samsung SM-J600FN', 'Samsung SM-J600G', 
        'Samsung SM-J600GT', 'Samsung SM-J600N', 'Samsung SM-J600L', 'Samsung SM-J610F', 'Samsung SM-J610FN', 
        'Samsung SM-J610G', 'Samsung SM-J700K', 'Samsung SM-J700H', 'Samsung SM-J700F', 'Samsung SM-J700M', 'Samsung SM-J7008', 
        'Samsung SM-J727U', 'Samsung SM-J727R4', 'Samsung SM-J727VPP', 'Samsung SM-J737VPP', 'Samsung SM-J737A', 
        'Samsung SM-J737U', 'Samsung SM-J730F', 'Samsung SM-J730FM', 'Samsung SM-J737R4', 'Samsung SM-S767VL', 
        'Samsung SM-S757BL', 'Samsung SM-J720F', 'Samsung SM-J720M', 'Samsung SM-G615F', 'Samsung SM-J701F', 
        'Samsung SM-J701M', 'Samsung SM-J701MT', 'Samsung SM-J727P', 'Samsung SAMSUNG-SM-J727AZ', 'Samsung SAMSUNG-SM-J727A', 
        'Samsung SM-S727VL', 'Samsung SM-J727T1', 'Samsung SM-J727T', 'Samsung SM-G610F', 'Samsung SM-G610M', 
        'Samsung SM-G610Y', 'Samsung SM-G6100', 'Samsung SM-G611M', 'Samsung SM-G611MT', 'Samsung SM-G611FF', 
        'Samsung SM-J730G', 'Samsung SM-J730GM', 'Samsung SM-J737P', 'Samsung SM-S737TL', 'Samsung SM-J737T1', 
        'Samsung SM-J737T', 'Samsung SM-J727V', 'Samsung SM-J737V', 'Samsung SM-J700P', 'Samsung SM-J700T1', 
        'Samsung SM-J700T', 'Samsung SM-J710F', 'Samsung SM-J710FQ', 'Samsung SM-J710GN', 'Samsung SM-J710MN', 
        'Samsung SM-J7108', 'Samsung SM-J710K', 'Samsung SM-J7109', 'Samsung SM-J730K', 'Samsung SM-C710F', 'Samsung SM-J810F', 
        'Samsung SM-J810G', 'Samsung SM-J810M', 'Samsung SM-J810Y', 'Samsung SM-A605K', 'Samsung SM-A202K', 'Samsung SM-A326K', 
        'Samsung SHW-M130K', 'Samsung SM-C111', 'Samsung SM-C111M', 'Samsung SM-C115', 'Samsung SM-C115M', 'Samsung SM-C115W', 
        'Samsung SM-C115L', 'Samsung GT-B7810', 'Samsung SHW-M340L', 'Samsung SHW-M340S', 'Samsung GT-I8258', 
        'Samsung SM-M015F', 'Samsung SM-M015G', 'Samsung SM-M013F', 'Samsung SM-M017F', 'Samsung SM-M022F', 'Samsung SM-M022G', 
        'Samsung SM-M022M', 'Samsung SM-M025F', 'Samsung SM-M105F', 'Samsung SM-M105G', 'Samsung SM-M105M', 'Samsung SM-M105Y', 
        'Samsung SM-M107F', 'Samsung SM-M115F', 'Samsung SM-M115M', 'Samsung SM-M127F', 'Samsung SM-M127G', 'Samsung SM-M127N', 
        'Samsung SM-M205N', 'Samsung SM-M205F', 'Samsung SM-M205FN', 'Samsung SM-M205G', 'Samsung SM-M205M', 
        'Samsung SM-M215F', 'Samsung SM-M305F', 'Samsung SM-M305M', 'Samsung SM-M3070', 'Samsung SM-M307F', 'Samsung SM-M307FN', 
        'Samsung SM-M315F', 'Samsung SM-M317F', 'Samsung SM-M405F', 'Samsung SM-M426B', 'Samsung SM-M515F', 'Samsung SM-M625F', 
        'Samsung SM-G750H', 'Samsung GT-I9152', 'Samsung SCH-P709', 'Samsung GT-I9150', 'Samsung GT-I9158', 'Samsung GT-I9200', 
        'Samsung GT-I9208', 'Samsung SCH-P729', 'Samsung GT-I9205', 'Samsung SGH-M819N', 'Samsung SAMSUNG-SGH-I527', 
        'Samsung SGH-I527M', 'Samsung SHV-E310K', 'Samsung SHV-E310L', 'Samsung SHV-E310S', 'Samsung SPH-L600', 
        'Samsung SCH-R960', 'Samsung GT-I9152P', 'Samsung GT-I9158P', 'Samsung GT-I9158V', 'Samsung SM-G750F', 
        'Samsung SAMSUNG-SM-G750A', 'Samsung SM-G750H', 'Samsung SM-G7508Q', 'Samsung SM-G7508Q', 'Samsung GT-S5570', 
        'Samsung GT-S5570B', 'Samsung GT-S5570I', 'Samsung GT-S5570L', 'Samsung GT-S5578', 'Samsung SGH-T499', 
        'Samsung SGH-T499V', 'Samsung SGH-T499Y', 'Samsung GT-S6500', 'Samsung GT-S6500D', 'Samsung GT-S6500L', 
        'Samsung GT-S6500T', 'Samsung GT-S6010', 'Samsung GT-S6010L', 'Samsung GT-S6012', 'Samsung GT-S6012B', 
        'Samsung EK-GN120', 'Samsung EK-GN120A', 'Samsung EK-GN120A', 'Samsung SHW-M220L', 'Samsung Galaxy Nexus', 
        'Samsung Galaxy X', 'Samsung Galaxy Nexus', 'Samsung Galaxy Nexus', 'Samsung GT-I9220', 'Samsung GT-I9228', 
        'Samsung GT-N7000', 'Samsung GT-N7005', 'Samsung SC-05D', 'Samsung SCH-i889', 'Samsung SAMSUNG-SGH-I717', 
        'Samsung SGH-I717', 'Samsung SGH-I717D', 'Samsung SGH-I717M', 'Samsung SGH-I717R', 'Samsung SGH-T879', 
        'Samsung SHV-E160K', 'Samsung SHV-E160L', 'Samsung SHV-E160S', 'Samsung SM-P601', 'Samsung SM-P602', 
        'Samsung SM-P605K', 'Samsung SM-P605L', 'Samsung SM-P605S', 'Samsung GT-N8020', 'Samsung SHV-E230K', 
        'Samsung SHV-E230L', 'Samsung SHV-E230S', 'Samsung SPH-P600', 'Samsung SCH-I925U', 'Samsung SCH-I925', 
        'Samsung GT-N8000', 'Samsung GT-N8005', 'Samsung SHW-M480K', 'Samsung GT-N8013', 'Samsung SHW-M486W', 
        'Samsung SHW-M480W', 'Samsung SHW-M485W', 'Samsung GT-N8010', 'Samsung SM-P601', 'Samsung SM-P605', 'Samsung SM-P605M', 
        'Samsung SM-P607T', 'Samsung SM-P605V', 'Samsung SM-P600', 'Samsung SM-P600', 'Samsung SM-P600', 'Samsung GT-N5100', 
        'Samsung GT-N5105', 'Samsung GT-N5120', 'Samsung SAMSUNG-SGH-I467', 'Samsung SGH-I467M', 'Samsung GT-N5110', 
        'Samsung SHW-M500W', 'Samsung SC-01G', 'Samsung SCL24', 'Samsung SM-N915K', 'Samsung SM-N915L', 'Samsung SM-N915S', 
        'Samsung SM-N9150', 'Samsung SM-N915F', 'Samsung SM-N915FY', 'Samsung SM-N915G', 'Samsung SM-N915X', 
        'Samsung SAMSUNG-SM-N915A', 'Samsung SM-N915W8', 'Samsung SM-N9150', 'Samsung SM-N915P', 'Samsung SM-N915T', 
        'Samsung SM-N915T3', 'Samsung SM-N915R4', 'Samsung SM-N915V', 'Samsung SM-N935F', 'Samsung SM-N935K', 
        'Samsung SM-N935L', 'Samsung SM-N935S', 'Samsung SAMSUNG-SGH-I317', 'Samsung SM-P900', 'Samsung SM-P901', 
        'Samsung SM-P900', 'Samsung SM-P900', 'Samsung SM-P905', 'Samsung SM-P905M', 'Samsung SAMSUNG-SM-P907A', 
        'Samsung SM-P905F0', 'Samsung SM-P905V', 'Samsung SM-N970F', 'Samsung SM-N9700', 'Samsung SM-N970U', 
        'Samsung SM-N970U1', 'Samsung SM-N970W', 'Samsung SM-N971N', 'Samsung SM-N770F', 'Samsung SC-01M', 'Samsung SCV45', 
        'Samsung SM-N9750', 'Samsung SM-N975C', 'Samsung SM-N975U', 'Samsung SM-N975U1', 'Samsung SM-N975W', 
        'Samsung SM-N975F', 'Samsung SM-N976B', 'Samsung SM-N976N', 'Samsung SM-N9760', 'Samsung SM-N976Q', 'Samsung SM-N976V', 
        'Samsung SM-N976U', 'Samsung SC-02E', 'Samsung GT-N7100', 'Samsung GT-N7100T', 'Samsung GT-N7100', 'Samsung GT-N7102', 
        'Samsung GT-N7102i', 'Samsung GT-N7108', 'Samsung SCH-N719', 'Samsung GT-N7102', 'Samsung GT-N7102i', 
        'Samsung GT-N7105', 'Samsung GT-N7105T', 'Samsung SAMSUNG-SGH-I317', 'Samsung SGH-I317M', 'Samsung SGH-T889V', 
        'Samsung GT-N7108D', 'Samsung SC-02E', 'Samsung SHV-E250K', 'Samsung SHV-E250L', 'Samsung SHV-E250S', 
        'Samsung SPH-L900', 'Samsung SGH-T889', 'Samsung SCH-R950', 'Samsung SCH-I605', 'Samsung SM-N980F', 'Samsung SM-N9810', 
        'Samsung SM-N981N', 'Samsung SM-N981U', 'Samsung SM-N981U1', 'Samsung SM-N981W', 'Samsung SM-N981B', 
        'Samsung SM-N985F', 'Samsung SC-53A', 'Samsung SCG06', 'Samsung SM-N9860', 'Samsung SM-N986N', 'Samsung SM-N986U', 
        'Samsung SM-N986U1', 'Samsung SM-N986W', 'Samsung SM-N986B', 'Samsung SC-01F', 'Samsung SC-02F', 'Samsung SCL22', 
        'Samsung SM-N900', 'Samsung SM-N9000Q', 'Samsung SM-N9005', 'Samsung SM-N9006', 'Samsung SM-N9007', 'Samsung SM-N9008V', 
        'Samsung SM-N9009', 'Samsung SM-N900U', 'Samsung SAMSUNG-SM-N900A', 'Samsung SM-N900W8', 'Samsung SM-N900K', 
        'Samsung SM-N900L', 'Samsung SM-N900S', 'Samsung SM-N900P', 'Samsung SM-N900T', 'Samsung SM-N900R4', 
        'Samsung SM-N900V', 'Samsung SM-N9007', 'Samsung SM-N9002', 'Samsung SM-N9008', 'Samsung SM-N750K', 'Samsung SM-N750L', 
        'Samsung SM-N750S', 'Samsung SM-N750', 'Samsung SM-N7500Q', 'Samsung SM-N7502', 'Samsung SM-N7505', 'Samsung SM-N7505L', 
        'Samsung SM-N7507', 'Samsung SM-N916K', 'Samsung SM-N910H', 'Samsung SM-N910C', 'Samsung SM-N910K', 'Samsung SM-N910L', 
        'Samsung SM-N910S', 'Samsung SM-N910U', 'Samsung SM-N910F', 'Samsung SM-N910G', 'Samsung SM-N910X', 'Samsung SAMSUNG-SM-N910A', 
        'Samsung SM-N910F', 'Samsung SM-N910W8', 'Samsung SM-N9100', 'Samsung SM-N9106W', 'Samsung SM-N9108V', 
        'Samsung SM-N9109W', 'Samsung SM-N9100', 'Samsung SM-N910P', 'Samsung SM-N910T', 'Samsung SM-N910T2', 
        'Samsung SM-N910T3', 'Samsung SM-N910R4', 'Samsung SM-N910V', 'Samsung SM-N916L', 'Samsung SM-N916S', 
        'Samsung SM-N9208', 'Samsung SM-N920C', 'Samsung SM-N920F', 'Samsung SM-N920G', 'Samsung SM-N920I', 'Samsung SM-N920X', 
        'Samsung SM-N920R7', 'Samsung SAMSUNG-SM-N920A', 'Samsung SM-N920W8', 'Samsung SM-N9200', 'Samsung SM-N9208', 
        'Samsung SM-N9200', 'Samsung SM-N920K', 'Samsung SM-N920L', 'Samsung SM-N920R6', 'Samsung SM-N920S', 
        'Samsung SM-N920P', 'Samsung SM-N920T', 'Samsung SM-N920R4', 'Samsung SM-N920V', 'Samsung SC-01J', 'Samsung SCV34', 
        'Samsung SM-N930F', 'Samsung SM-N930X', 'Samsung SM-N930K', 'Samsung SM-N930L', 'Samsung SM-N930S', 'Samsung SM-N930R7', 
        'Samsung SAMSUNG-SM-N930A', 'Samsung SM-N930W8', 'Samsung SM-N9300', 'Samsung SGH-N037', 'Samsung SM-N930R6', 
        'Samsung SM-N930P', 'Samsung SM-N930VL', 'Samsung SM-N930T', 'Samsung SM-N930U', 'Samsung SM-N930R4', 
        'Samsung SM-N930V', 'Samsung SC-01K', 'Samsung SCV37', 'Samsung SM-N950F', 'Samsung SM-N950N', 'Samsung SM-N950XN', 
        'Samsung SM-N950U', 'Samsung SM-N9500', 'Samsung SM-N9508', 'Samsung SM-N950W', 'Samsung SM-N950U1', 
        'Samsung SC-01L', 'Samsung SCV40', 'Samsung SM-N960F', 'Samsung SM-N960N', 'Samsung SM-N9600', 'Samsung SM-N960W', 
        'Samsung SM-N960U', 'Samsung SM-N960U1', 'Samsung SM-G615FU', 'Samsung SM-G610F', 'Samsung SM-G550FY', 
        'Samsung SM-G5500', 'Samsung SM-G550T1', 'Samsung SM-S550TL', 'Samsung SM-G550T', 'Samsung SM-G550T2', 
        'Samsung SM-G5520', 'Samsung SM-G5528', 'Samsung SM-G5510', 'Samsung SM-G550FY', 'Samsung SM-G5700', 
        'Samsung SM-J600GF', 'Samsung SM-G600FY', 'Samsung SM-G6000', 'Samsung SM-G600F', 'Samsung SM-G611F', 
        'Samsung SM-G611K', 'Samsung SM-G611L', 'Samsung SM-G611S', 'Samsung SM-G600FY', 'Samsung SM-G610K', 
        'Samsung SM-G610L', 'Samsung SM-G610S', 'Samsung SM-G6100', 'Samsung SM-J710FN', 'Samsung SM-J810GF', 
        'Samsung YP-GB70', 'Samsung YP-GS1', 'Samsung YP-GB1', 'Samsung YP-G1', 'Samsung YP-GI1', 'Samsung YP-G70', 
        'Samsung YP-GP1', 'Samsung YP-GP1', 'Samsung YP-GP1', 'Samsung YP-G50', 'Samsung GT-S5300', 'Samsung GT-S5300B', 
        'Samsung GT-S5300L', 'Samsung GT-S5302', 'Samsung GT-S5302B', 'Samsung GT-S5301', 'Samsung GT-S5303', 
        'Samsung GT-S5312', 'Samsung GT-S5312B', 'Samsung GT-S5312L', 'Samsung GT-S5310', 'Samsung GT-S5310B', 
        'Samsung GT-S5310E', 'Samsung GT-S5310G', 'Samsung GT-S5310L', 'Samsung GT-S5310T', 'Samsung GT-S5310I', 
        'Samsung GT-S5310N', 'Samsung GT-S5312C', 'Samsung GT-S5312M', 'Samsung SAMSUNG-SGH-I747Z', 'Samsung GT-S5301', 
        'Samsung GT-S5301B', 'Samsung GT-S5301L', 'Samsung GT-S5310C', 'Samsung GT-S5310M', 'Samsung SM-G110B', 
        'Samsung SM-G110M', 'Samsung SM-G110H', 'Samsung SHV-E220S', 'Samsung SCH-i559', 'Samsung SCH-M828C', 
        'Samsung GT-I9260', 'Samsung GT-I9268', 'Samsung SPH-M820-BST', 'Samsung SPH-M840', 'Samsung GT-B7510', 
        'Samsung GT-B7510B', 'Samsung GT-B7510L', 'Samsung SCH-S720C', 'Samsung SGH-T589', 'Samsung SGH-T589R', 
        'Samsung SGH-T589W', 'Samsung SM-A826S', 'Samsung SHV-E170K', 'Samsung SHV-E170L', 'Samsung SHV-E170S', 
        'Samsung SPH-M950', 'Samsung SM-G910S', 'Samsung SGH-I547C', 'Samsung SAMSUNG-SGH-I547', 'Samsung SPH-M830', 
        'Samsung GT-I9000', 'Samsung GT-I9000B', 'Samsung GT-I9000M', 'Samsung GT-I9000T', 'Samsung GT-I9003', 
        'Samsung GT-I9003L', 'Samsung GT-I9008L', 'Samsung GT-I9010', 'Samsung GT-I9018', 'Samsung GT-I9050', 
        'Samsung SC-02B', 'Samsung SCH-I500', 'Samsung SCH-S950C', 'Samsung SCH-i909', 'Samsung SAMSUNG-SGH-I897', 
        'Samsung SGH-T959V', 'Samsung SGH-T959W', 'Samsung SHW-M110S', 'Samsung SHW-M190S', 'Samsung SPH-D700', 
        'Samsung GT-S7275', 'Samsung GT-I9070', 'Samsung GT-I9070P', 'Samsung SCH-R930', 'Samsung SGH-T769', 
        'Samsung SGH-T699', 'Samsung SAMSUNG-SGH-I896', 'Samsung SGH-I896', 'Samsung SCH-I400', 'Samsung GT-S7562', 
        'Samsung GT-S7562L', 'Samsung GT-S7562', 'Samsung GT-S7562', 'Samsung GT-S7568', 'Samsung GT-S7582', 
        'Samsung GT-S7582L', 'Samsung SM-G313HZ', 'Samsung SPH-D700', 'Samsung SGH-T959P', 'Samsung SAMSUNG-SGH-I927R', 
        'Samsung SCH-R940', 'Samsung GT-I9001', 'Samsung SCH-I405', 'Samsung SGH-T959', 'Samsung SGH-T959D', 
        'Samsung GT-S7566', 'Samsung SM-G8750', 'Samsung SC-03L', 'Samsung SCV41', 'Samsung SM-G973F', 'Samsung SM-G973N', 
        'Samsung SM-G9730', 'Samsung SM-G9738', 'Samsung SM-G973C', 'Samsung SM-G973U', 'Samsung SM-G973U1', 
        'Samsung SM-G973W', 'Samsung SM-G977B', 'Samsung SM-G977N', 'Samsung SM-G977P', 'Samsung SM-G977T', 'Samsung SM-G977U', 
        'Samsung SM-G770F', 'Samsung SM-G770U1', 'Samsung SC-04L', 'Samsung SCV42', 'Samsung SM-G975F', 'Samsung SM-G975N', 
        'Samsung SM-G9750', 'Samsung SM-G9758', 'Samsung SM-G975U', 'Samsung SM-G975U1', 'Samsung SM-G975W', 
        'Samsung SC-05L', 'Samsung SM-G970F', 'Samsung SM-G970N', 'Samsung SM-G9700', 'Samsung SM-G9708', 'Samsung SM-G970U', 
        'Samsung SM-G970U1', 'Samsung SM-G970W', 'Samsung GT-I9100', 'Samsung GT-I9100M', 'Samsung GT-I9100P', 
        'Samsung GT-I9100T', 'Samsung GT-I9103', 'Samsung GT-I9108', 'Samsung GT-I9210T', 'Samsung SC-02C', 'Samsung SCH-R760X', 
        'Samsung SAMSUNG-SGH-I777', 'Samsung SGH-S959G', 'Samsung SGH-T989', 'Samsung SHV-E110S', 'Samsung SHW-M250K', 
        'Samsung SHW-M250L', 'Samsung SHW-M250S', 'Samsung GT-I9108', 'Samsung SCH-i929', 'Samsung GT-S7273T', 
        'Samsung SCH-R760', 'Samsung SPH-D710', 'Samsung SPH-D710BST', 'Samsung SPH-D710VMUB', 'Samsung SGH-I757M', 
        'Samsung SHV-E120K', 'Samsung SHV-E120L', 'Samsung SHV-E120S', 'Samsung GT-I9210', 'Samsung SC-03D', 
        'Samsung SGH-I727R', 'Samsung GT-I9100G', 'Samsung GT-I9105', 'Samsung GT-I9105P', 'Samsung SAMSUNG-SGH-I727', 
        'Samsung SGH-I727', 'Samsung ISW11SC', 'Samsung SGH-T989D', 'Samsung SM-G980F', 'Samsung SC-51A', 'Samsung SC51Aa', 
        'Samsung SCG01', 'Samsung SM-G9810', 'Samsung SM-G981N', 'Samsung SM-G981U', 'Samsung SM-G981U1', 'Samsung SM-G981V', 
        'Samsung SM-G981W', 'Samsung SM-G981B', 'Samsung SM-G780G', 'Samsung SM-G780F', 'Samsung SM-G7810', 'Samsung SM-G781B', 
        'Samsung SM-G781N', 'Samsung SM-G781U', 'Samsung SM-G781U1', 'Samsung SM-G781V', 'Samsung SM-G781W', 
        'Samsung SCG03', 'Samsung SM-G9880', 'Samsung SM-G988N', 'Samsung SM-G988Q', 'Samsung SM-G988U', 'Samsung SM-G988U1', 
        'Samsung SM-G988W', 'Samsung SM-G988B', 'Samsung SM-G985F', 'Samsung SC-52A', 'Samsung SCG02', 'Samsung SM-G9860', 
        'Samsung SM-G986N', 'Samsung SM-G986U', 'Samsung SM-G986U1', 'Samsung SM-G986W', 'Samsung SM-G986B', 
        'Samsung SC-51B', 'Samsung SCG09', 'Samsung SM-G9910', 'Samsung SM-G991U1', 'Samsung SM-G991W', 'Samsung SM-G991B', 
        'Samsung SM-G991N', 'Samsung SC-52B', 'Samsung SM-G9980', 'Samsung SM-G998U', 'Samsung SM-G998U1', 'Samsung SM-G998W', 
        'Samsung SM-G998B', 'Samsung SM-G998N', 'Samsung SCG10', 'Samsung SM-G9960', 'Samsung SM-G996U1', 'Samsung SM-G996W', 
        'Samsung SM-G996B', 'Samsung SM-G996N', 'Samsung SC-03E', 'Samsung SGH-I748', 'Samsung SHV-E210K', 'Samsung SHV-E210L', 
        'Samsung SHV-E210S', 'Samsung SAMSUNG-SGH-I747', 'Samsung SGH-I747M', 'Samsung SGH-T999V', 'Samsung SCH-R530C', 
        'Samsung Gravity', 'Samsung SC-06D', 'Samsung SGH-T999N', 'Samsung SPH-L710T', 'Samsung SGH-T999L', 'Samsung SCH-R530M', 
        'Samsung SCH-L710', 'Samsung SPH-L710', 'Samsung SCH-S960L', 'Samsung SCH-S968C', 'Samsung SGH-T999', 
        'Samsung SCH-R530U', 'Samsung SPH-L710', 'Samsung SCH-I535', 'Samsung SCH-I535PP', 'Samsung SCH-R530X', 
        'Samsung GT-I9300', 'Samsung GT-I9300T', 'Samsung SCH-I939', 'Samsung GT-I9300', 'Samsung GT-I9308', 
        'Samsung SCH-I939', 'Samsung SCH-I939D', 'Samsung SHW-M440S', 'Samsung GT-I9305', 'Samsung GT-I9305N', 
        'Samsung GT-I9305T', 'Samsung GravityQuad', 'Samsung SC-03E', 'Samsung GT-I8262B', 'Samsung GT-I8190', 
        'Samsung GT-I8190L', 'Samsung GT-I8190N', 'Samsung GT-I8190T', 'Samsung SAMSUNG-SM-G730A', 'Samsung SM-G730W8', 
        'Samsung SM-G730V', 'Samsung GT-I8200L', 'Samsung GT-I8200N', 'Samsung GT-I8200', 'Samsung GT-I8200Q', 
        'Samsung GT-I9300I', 'Samsung GT-I9301I', 'Samsung GT-I9301Q', 'Samsung GT-I9300I', 'Samsung GT-I9300I', 
        'Samsung GT-I9300I', 'Samsung GT-I9300I', 'Samsung GT-I9308I', 'Samsung SCL21', 'Samsung SM-G3812B', 
        'Samsung SC-04E', 'Samsung GT-I9500', 'Samsung SCH-I959', 'Samsung SHV-E300K', 'Samsung SHV-E300L', 'Samsung SHV-E300S', 
        'Samsung GT-I9505', 'Samsung GT-I9508', 'Samsung GT-I9508C', 'Samsung SGH-M919N', 'Samsung SAMSUNG-SGH-I337Z', 
        'Samsung SAMSUNG-SGH-I337', 'Samsung SGH-I337M', 'Samsung SGH-M919V', 'Samsung SCH-R970C', 'Samsung SCH-R970X', 
        'Samsung SCH-I545L', 'Samsung SPH-L720T', 'Samsung SPH-L720', 'Samsung SM-S975L', 'Samsung SGH-S970G', 
        'Samsung SGH-M919', 'Samsung SCH-R970', 'Samsung SCH-I545', 'Samsung SCH-I545PP', 'Samsung GT-I9507', 
        'Samsung GT-I9507V', 'Samsung GT-I9515', 'Samsung GT-I9515L', 'Samsung GT-I9505X', 'Samsung GT-I9508V', 
        'Samsung GT-I9506', 'Samsung SHV-E330K', 'Samsung SHV-E330L', 'Samsung GT-I9295', 'Samsung SAMSUNG-SGH-I537', 
        'Samsung SGH-I537', 'Samsung SHV-E470S', 'Samsung GT-I9502', 'Samsung GT-I9505G', 'Samsung SHV-E330S', 
        'Samsung GT-I9190', 'Samsung GT-I9192', 'Samsung GT-I9195', 'Samsung GT-I9195L', 'Samsung GT-I9195T', 
        'Samsung GT-I9195X', 'Samsung GT-I9197', 'Samsung SGH-I257M', 'Samsung SHV-E370K', 'Samsung SHV-E370D', 
        'Samsung SCH-I435L', 'Samsung SPH-L520', 'Samsung SCH-R890', 'Samsung SCH-I435', 'Samsung GT-I9192I', 
        'Samsung GT-I9195I', 'Samsung SAMSUNG-SGH-I257', 'Samsung SM-C101', 'Samsung SAMSUNG-SM-C105A', 'Samsung SM-C105K', 
        'Samsung SM-C105L', 'Samsung SM-C105S', 'Samsung SM-C105', 'Samsung SC-04F', 'Samsung SCL23', 'Samsung SM-G900H', 
        'Samsung SM-G9008W', 'Samsung SM-G9009W', 'Samsung SM-G900F', 'Samsung SM-G900FQ', 'Samsung SM-G900I', 
        'Samsung SM-G900M', 'Samsung SM-G900MD', 'Samsung SM-G900T1', 'Samsung SM-G900T4', 'Samsung SM-G900R7', 
        'Samsung SAMSUNG-SM-G900AZ', 'Samsung SAMSUNG-SM-G900A', 'Samsung SM-G900W8', 'Samsung SM-G9006W', 'Samsung SM-G900K', 
        'Samsung SM-G900L', 'Samsung SM-G900R6', 'Samsung SM-G900S', 'Samsung SM-G900P', 'Samsung SM-S903VL', 
        'Samsung SM-G900T', 'Samsung SM-G900T3', 'Samsung SM-G900R4', 'Samsung SM-G900V', 'Samsung SM-G900X', 
        'Samsung SM-G906K', 'Samsung SM-G906L', 'Samsung SM-G906S', 'Samsung SC-02G', 'Samsung SM-G870F0', 'Samsung SM-G870F', 
        'Samsung SAMSUNG-SM-G870A', 'Samsung SM-G870W', 'Samsung SM-G900FD', 'Samsung SM-G900FG', 'Samsung SM-G860P', 
        'Samsung SM-G901F', 'Samsung SM-G800H', 'Samsung SM-G800R4', 'Samsung SM-G903F', 'Samsung SM-G903M', 
        'Samsung SM-G903W', 'Samsung SM-G800HQ', 'Samsung SM-G800F', 'Samsung SM-G800M', 'Samsung SM-G800Y', 
        'Samsung SAMSUNG-SM-G800A', 'Samsung SM-G800X', 'Samsung SC-05G', 'Samsung SM-G920F', 'Samsung SM-G920I', 
        'Samsung SM-G920X', 'Samsung SM-G920R7', 'Samsung SAMSUNG-SM-G920AZ', 'Samsung SAMSUNG-SM-G920A', 'Samsung SM-G920W8', 
        'Samsung SM-G9200', 'Samsung SM-G9208', 'Samsung SM-G9209', 'Samsung SM-G920K', 'Samsung SM-G920L', 'Samsung SM-G920R6', 
        'Samsung SM-G920T1', 'Samsung SM-G920S', 'Samsung SM-G920P', 'Samsung SM-S906L', 'Samsung SM-S907VL', 
        'Samsung SM-G920T', 'Samsung SM-G920R4', 'Samsung SM-G920V', 'Samsung SAMSUNG-SM-G890A', 'Samsung 404SC', 
        'Samsung SC-04G', 'Samsung SCV31', 'Samsung SM-G925I', 'Samsung SM-G925X', 'Samsung SM-G925R7', 'Samsung SAMSUNG-SM-G925A', 
        'Samsung SM-G925W8', 'Samsung SM-G9250', 'Samsung SM-G925K', 'Samsung SM-G925R6', 'Samsung SM-G925S', 
        'Samsung SM-G925P', 'Samsung SM-G925T', 'Samsung SM-G925R4', 'Samsung SM-G925V', 'Samsung SM-G9287C', 
        'Samsung SM-G928C', 'Samsung SM-G928G', 'Samsung SM-G928I', 'Samsung SM-G928X', 'Samsung SAMSUNG-SM-G928A', 
        'Samsung SM-G928W8', 'Samsung SM-G9280', 'Samsung SM-G928K', 'Samsung SM-G928N0', 'Samsung SM-G928L', 
        'Samsung SM-G928S', 'Samsung SM-G928P', 'Samsung SM-G928T', 'Samsung SM-G928R4', 'Samsung SM-G928V', 
        'Samsung SM-G925F', 'Samsung SM-G925L', 'Samsung SM-G9287', 'Samsung SM-G928F', 'Samsung SM-G928G', 'Samsung SM-G930F', 
        'Samsung SM-G930X', 'Samsung SM-G930W8', 'Samsung SM-G930K', 'Samsung SM-G930L', 'Samsung SM-G930S', 
        'Samsung SM-G930R7', 'Samsung SAMSUNG-SM-G930AZ', 'Samsung SAMSUNG-SM-G930A', 'Samsung SM-G930VC', 'Samsung SM-G9300', 
        'Samsung SM-G9308', 'Samsung SM-G930R6', 'Samsung SM-G930T1', 'Samsung SM-G930P', 'Samsung SM-G930VL', 
        'Samsung SM-G930T', 'Samsung SM-G930U', 'Samsung SM-G930R4', 'Samsung SM-G930V', 'Samsung SAMSUNG-SM-G891A', 
        'Samsung SC-02H', 'Samsung SCV33', 'Samsung SM-G935X', 'Samsung SM-G935W8', 'Samsung SM-G935K', 'Samsung SM-G935S', 
        'Samsung SAMSUNG-SM-G935A', 'Samsung SM-G935VC', 'Samsung SM-G935P', 'Samsung SM-G935T', 'Samsung SM-G935R4', 
        'Samsung SM-G935V', 'Samsung SM-G935F', 'Samsung SM-G935L', 'Samsung SM-G9350', 'Samsung SM-G935U', 'Samsung SC-02J', 
        'Samsung SCV36', 'Samsung SM-G950F', 'Samsung SM-G950N', 'Samsung SM-G950W', 'Samsung SM-G9500', 'Samsung SM-G9508', 
        'Samsung SM-G950U', 'Samsung SM-G950U1', 'Samsung SM-G892A', 'Samsung SM-G892U', 'Samsung SC-03J', 'Samsung SCV35', 
        'Samsung SM-G955F', 'Samsung SM-G955N', 'Samsung SM-G955W', 'Samsung SM-G9550', 'Samsung SM-G955U', 'Samsung SM-G955U1', 
        'Samsung SC-02K', 'Samsung SCV38', 'Samsung SM-G960F', 'Samsung SM-G960N', 'Samsung SM-G9600', 'Samsung SM-G9608', 
        'Samsung SM-G960W', 'Samsung SM-G960U', 'Samsung SM-G960U1', 'Samsung SC-03K', 'Samsung SCV39', 'Samsung SM-G965F', 
        'Samsung SM-G965N', 'Samsung SM-G9650', 'Samsung SM-G965W', 'Samsung SM-G965U', 'Samsung SM-G965U1', 
        'Samsung GT-I5700', 'Samsung GT-I5700L', 'Samsung GT-I5700R', 'Samsung GT-I5700L', 'Samsung GT-I5700', 
        'Samsung GT-I5700L', 'Samsung GT-I5700R', 'Samsung GT-i5700', 'Samsung GT-S5282', 'Samsung GT-S5280', 
        'Samsung GT-S7262', 'Samsung GT-S5283B', 'Samsung SM-G350E', 'Samsung SCH-I200', 'Samsung SCH-I200PP', 
        'Samsung SCH-I415', 'Samsung SCH-I829', 'Samsung SM-T397U', 'Samsung SM-T116IR', 'Samsung GT-P1000', 
        'Samsung GT-P1000L', 'Samsung GT-P1000M', 'Samsung GT-P1000N', 'Samsung GT-P1000R', 'Samsung GT-P1000T', 
        'Samsung GT-P1010', 'Samsung GT-P1013', 'Samsung SC-01C', 'Samsung SCH-I800', 'Samsung SGH-T849', 'Samsung SHW-M180K', 
        'Samsung SHW-M180L', 'Samsung SHW-M180S', 'Samsung SHW-M180W', 'Samsung SMT-i9100', 'Samsung GT-P7500', 
        'Samsung GT-P7500D', 'Samsung GT-P7503', 'Samsung GT-P7510', 'Samsung SC-01D', 'Samsung SCH-I905', 'Samsung SGH-T859', 
        'Samsung SHW-M300W', 'Samsung SHW-M380K', 'Samsung SHW-M380S', 'Samsung SHW-M380W', 'Samsung GT-P7501', 
        'Samsung GT-P7511', 'Samsung GT-P7100', 'Samsung SM-T116IR', 'Samsung SM-T116NY', 'Samsung SM-T330X', 
        'Samsung SM-T330', 'Samsung SPH-P100', 'Samsung GT-P6200', 'Samsung GT-P6200L', 'Samsung GT-P6201', 'Samsung GT-P6210', 
        'Samsung GT-P6211', 'Samsung SC-02D', 'Samsung SGH-T869', 'Samsung SHW-M430W', 'Samsung GT-P6800', 'Samsung GT-P6810', 
        'Samsung SCH-I815', 'Samsung SC-01E', 'Samsung GT-P7300', 'Samsung GT-P7310', 'Samsung GT-P7320', 'Samsung SCH-P739', 
        'Samsung SAMSUNG-SGH-I957', 'Samsung SAMSUNG-SGH-I957D', 'Samsung SGH-I957D', 'Samsung SAMSUNG-SGH-I957M', 
        'Samsung SGH-I957M', 'Samsung SAMSUNG-SGH-I957R', 'Samsung SGH-I957R', 'Samsung SHV-E140K', 'Samsung SHV-E140L', 
        'Samsung SHV-E140S', 'Samsung SHW-M305W', 'Samsung SM-T555', 'Samsung SM-T550', 'Samsung SM-T355C', 'Samsung SM-P555M', 
        'Samsung SM-P550', 'Samsung SM-P355M', 'Samsung SM-P355C', 'Samsung SM-T515', 'Samsung SM-T515N', 'Samsung SM-T517P', 
        'Samsung SM-T510', 'Samsung SM-T387R4', 'Samsung SM-T587P', 'Samsung SM-T597P', 'Samsung SM-T597V', 'Samsung SM-T597W', 
        'Samsung SM-T585', 'Samsung SM-T585C', 'Samsung SM-T585N0', 'Samsung SM-T580', 'Samsung SM-T580', 'Samsung SM-P585', 
        'Samsung SM-P585M', 'Samsung SM-P585Y', 'Samsung SM-P587', 'Samsung SM-P588C', 'Samsung SM-P585N0', 'Samsung SM-P583', 
        'Samsung SM-P580', 'Samsung SM-T385', 'Samsung SM-T385M', 'Samsung SM-T385C', 'Samsung SM-T385K', 'Samsung SM-T385L', 
        'Samsung SM-T385S', 'Samsung SM-T380', 'Samsung SM-T380C', 'Samsung SM-T595', 'Samsung SM-T597', 'Samsung SM-T595C', 
        'Samsung SM-T595N', 'Samsung SM-T590', 'Samsung SM-T590', 'Samsung SM-T295', 'Samsung SM-T295C', 'Samsung SM-T295N', 
        'Samsung SM-T297', 'Samsung SM-T290', 'Samsung SM-T295', 'Samsung SM-T307U', 'Samsung SM-T585M', 'Samsung SM-T587', 
        'Samsung SM-T580X', 'Samsung SM-T580X', 'Samsung SM-T285', 'Samsung SM-T285M', 'Samsung SM-T287', 'Samsung SM-T285YD', 
        'Samsung SM-T280', 'Samsung SM-T387AA', 'Samsung SM-T387P', 'Samsung SM-T387T', 'Samsung SM-T355', 'Samsung SM-T355Y', 
        'Samsung SM-T357T', 'Samsung SM-T350', 'Samsung SM-T350X', 'Samsung SM-T350', 'Samsung SM-T350X', 'Samsung SM-P355', 
        'Samsung SM-P355Y', 'Samsung SM-P350', 'Samsung SM-P350', 'Samsung SM-T387W', 'Samsung SM-T387V', 'Samsung SM-T555C', 
        'Samsung SM-T550X', 'Samsung SM-T550', 'Samsung SM-T550X', 'Samsung SM-P555', 'Samsung SM-P555C', 'Samsung SM-P555Y', 
        'Samsung SM-P555K', 'Samsung SM-P555L', 'Samsung SM-P555S', 'Samsung SM-P550', 'Samsung SM-P550', 'Samsung SM-T290', 
        'Samsung SM-T357W', 'Samsung SM-P205', 'Samsung SM-P200', 'Samsung SM-T517', 'Samsung SM-T280', 'Samsung SM-T505', 
        'Samsung SM-T505C', 'Samsung SM-T505N', 'Samsung SM-T507', 'Samsung SM-T500', 'Samsung SM-T225', 'Samsung SM-T225C', 
        'Samsung SM-T225N', 'Samsung SM-T220', 'Samsung SM-T365', 'Samsung SM-T365Y', 'Samsung SM-T545', 'Samsung SM-T547', 
        'Samsung SM-T547U', 'Samsung SM-T540', 'Samsung SM-T395', 'Samsung SM-T395C', 'Samsung SM-T395N', 'Samsung SM-T397U', 
        'Samsung SM-T390', 'Samsung SM-T575', 'Samsung SM-T575N', 'Samsung SM-T577', 'Samsung SM-T577U', 'Samsung SM-T570', 
        'Samsung SM-T583', 'Samsung SM-T561M', 'Samsung SM-T560', 'Samsung SAMSUNG-SM-T377A', 'Samsung SM-T377W', 
        'Samsung SM-T375L', 'Samsung SM-T375S', 'Samsung SM-T377T', 'Samsung SM-T3777', 'Samsung SM-T377V', 'Samsung SM-T377P', 
        'Samsung SM-T377R4', 'Samsung SM-T561', 'Samsung SM-T561Y', 'Samsung SM-T562', 'Samsung SM-T567V', 'Samsung SM-T560', 
        'Samsung SM-T560', 'Samsung SM-T560NU', 'Samsung SM-T378V', 'Samsung SM-T116BU', 'Samsung SM-T525', 'Samsung SM-T520', 
        'Samsung SM-T520CC', 'Samsung SM-T905', 'Samsung SM-T900', 'Samsung SM-T900X', 'Samsung SM-T325', 'Samsung SM-T320', 
        'Samsung SM-T320X', 'Samsung SM-T320', 'Samsung SM-T320', 'Samsung SM-T320NU', 'Samsung SM-T2519', 'Samsung SM-T800', 
        'Samsung SC-03G', 'Samsung SM-T705', 'Samsung SM-T705C', 'Samsung SM-T705Y', 'Samsung SM-T707V', 'Samsung SM-T700', 
        'Samsung SM-T815', 'Samsung SM-T815C', 'Samsung SM-T815Y', 'Samsung SM-T819', 'Samsung SM-T819Y', 'Samsung SM-T819C', 
        'Samsung SM-T813', 'Samsung SM-T813', 'Samsung SM-T810', 'Samsung SM-T715', 'Samsung SM-T719', 'Samsung SM-T719Y', 
        'Samsung SM-T719C', 'Samsung SM-T713', 'Samsung SM-T713', 'Samsung SM-T710', 'Samsung SM-T715Y', 'Samsung SM-T715C', 
        'Samsung SM-T715N0', 'Samsung SM-T713', 'Samsung SM-T710', 'Samsung SM-T710X', 'Samsung SM-T710', 'Samsung SM-T817', 
        'Samsung SAMSUNG-SM-T817A', 'Samsung SM-T817W', 'Samsung SM-T815N0', 'Samsung SM-T817P', 'Samsung SM-T817T', 
        'Samsung SM-T817R4', 'Samsung SM-T817V', 'Samsung SM-T818', 'Samsung SAMSUNG-SM-T818A', 'Samsung SM-T818W', 
        'Samsung SM-T818T', 'Samsung SM-T813', 'Samsung SM-T810', 'Samsung SM-T810X', 'Samsung SM-T825', 'Samsung SM-T825C', 
        'Samsung SM-T825X', 'Samsung SM-T827', 'Samsung SM-T825N0', 'Samsung SM-T827R4', 'Samsung SM-T827V', 
        'Samsung SM-T820', 'Samsung SM-T820X', 'Samsung SM-T820', 'Samsung SM-T835', 'Samsung SM-T837', 'Samsung SM-T837A', 
        'Samsung SM-T835C', 'Samsung SM-T835N', 'Samsung SM-T837P', 'Samsung SM-T837T', 'Samsung SM-T837R4', 
        'Samsung SM-T837V', 'Samsung SM-T830', 'Samsung SM-T830', 'Samsung SM-T725', 'Samsung SM-T725C', 'Samsung SM-T725N', 
        'Samsung SM-T727', 'Samsung SM-T727A', 'Samsung SM-T727R4', 'Samsung SM-T727U', 'Samsung SM-T727V', 'Samsung SM-T720', 
        'Samsung SM-T720', 'Samsung SM-T865', 'Samsung SM-T865N', 'Samsung SM-T867', 'Samsung SM-T867R4', 'Samsung SM-T867U', 
        'Samsung SM-T867V', 'Samsung SM-T860', 'Samsung SM-T866N', 'Samsung SM-P615', 'Samsung SM-P615C', 'Samsung SM-P615N', 
        'Samsung SM-P617', 'Samsung SM-P610', 'Samsung SM-P610X', 'Samsung SM-T875', 'Samsung SM-T875N', 'Samsung SM-T870', 
        'Samsung SM-T878U', 'Samsung SM-T735', 'Samsung SM-T735C', 'Samsung SM-T735N', 'Samsung SM-T737', 'Samsung SM-T730', 
        'Samsung SM-T736B', 'Samsung SM-T736N', 'Samsung SM-T975', 'Samsung SM-T975N', 'Samsung SM-T970', 'Samsung SM-T976B', 
        'Samsung SM-T976N', 'Samsung SM-T978U', 'Samsung SAMSUNG-SGH-I497', 'Samsung SGH-I497', 'Samsung GT-P5100', 
        'Samsung SPH-P500', 'Samsung SGH-T779', 'Samsung SCH-I915', 'Samsung GT-P5110', 'Samsung GT-P5113', 'Samsung GT-P3100', 
        'Samsung GT-P3100B', 'Samsung GT-P3105', 'Samsung SCH-I705', 'Samsung SCH-i705', 'Samsung GT-P3110', 
        'Samsung GT-P3113', 'Samsung SM-T310', 'Samsung GT-P5200', 'Samsung GT-P5220', 'Samsung GT-P5210', 'Samsung GT-P5210XD1', 
        'Samsung SM-T211', 'Samsung SM-T212', 'Samsung SM-T211M', 'Samsung SM-T215', 'Samsung SAMSUNG-SM-T217A', 
        'Samsung SM-T217S', 'Samsung SM-T217T', 'Samsung SM-T210', 'Samsung SM-T210R', 'Samsung SM-T210L', 'Samsung SM-T311', 
        'Samsung SM-T312', 'Samsung SM-T315', 'Samsung SM-T315T', 'Samsung SM-T310', 'Samsung SM-T310X', 'Samsung SM-T210X', 
        'Samsung SM-T2105', 'Samsung SM-T111', 'Samsung SM-T111M', 'Samsung SM-T110', 'Samsung SM-T116NQ', 'Samsung SM-T113', 
        'Samsung SM-T116', 'Samsung SM-T116NU', 'Samsung SM-T113NU', 'Samsung SM-T530NN', 'Samsung SM-T531', 
        'Samsung SM-T535', 'Samsung SAMSUNG-SM-T537A', 'Samsung SM-T537R4', 'Samsung SM-T537V', 'Samsung SM-T536', 
        'Samsung SM-T533', 'Samsung SM-T530', 'Samsung SM-T530X', 'Samsung SM-T530', 'Samsung SM-T530NU', 'Samsung SM-T230NZ', 
        'Samsung 403SC', 'Samsung SM-T230NW', 'Samsung SM-T230NW', 'Samsung SM-T231', 'Samsung SM-T232', 'Samsung SM-T235', 
        'Samsung SM-T235Y', 'Samsung SM-T237P', 'Samsung SM-T237V', 'Samsung SM-T239', 'Samsung SM-T2397', 'Samsung SM-T239M', 
        'Samsung SM-T239C', 'Samsung SM-T230', 'Samsung SM-T230NY', 'Samsung SM-T230X', 'Samsung SM-T230NY', 
        'Samsung SM-T230NT', 'Samsung SM-T230NU', 'Samsung SM-T230NU', 'Samsung SM-T331', 'Samsung SM-T335', 
        'Samsung SAMSUNG-SM-T337A', 'Samsung SM-T335K', 'Samsung SM-T335L', 'Samsung SM-T337T', 'Samsung SM-T337V', 
        'Samsung SM-T330', 'Samsung SM-T330NU', 'Samsung SM-T365', 'Samsung SM-T365M', 'Samsung SM-T365F0', 'Samsung SM-T360', 
        'Samsung SM-T360', 'Samsung SM-T530NU', 'Samsung SM-P580X', 'Samsung SM-T378K', 'Samsung SM-T378L', 'Samsung SM-T378S', 
        'Samsung SCT21', 'Samsung SM-T805K', 'Samsung SM-T805L', 'Samsung SM-T805S', 'Samsung SM-T805', 'Samsung SM-T805C', 
        'Samsung SM-T805M', 'Samsung SM-T805Y', 'Samsung SM-T807', 'Samsung SAMSUNG-SM-T807A', 'Samsung SM-T805W', 
        'Samsung SM-T807P', 'Samsung SM-T807T', 'Samsung SM-T807R4', 'Samsung SM-T807V', 'Samsung SM-T800', 'Samsung SM-T800X', 
        'Samsung SM-T800', 'Samsung SM-T705', 'Samsung SM-T705M', 'Samsung SAMSUNG-SM-T707A', 'Samsung SM-T705W', 
        'Samsung SM-T700', 'Samsung SM-T700', 'Samsung SM-T818V', 'Samsung SM-T825', 'Samsung SM-T825Y', 'Samsung SM-T825C', 
        'Samsung SM-T525', 'Samsung SM-T320', 'Samsung GT-S7392', 'Samsung GT-S7392L', 'Samsung GT-S7568I', 'Samsung GT-S7562i', 
        'Samsung GT-S7572', 'Samsung GT-S7390', 'Samsung GT-S7392', 'Samsung GT-S7562C', 'Samsung GT-S7390', 
        'Samsung GT-S7390L', 'Samsung GT-S7580', 'Samsung GT-S7580E', 'Samsung GT-S7580L', 'Samsung GT-S7583T', 
        'Samsung GT-S7898', 'Samsung GT-S7898I', 'Samsung SCH-I739', 'Samsung SM-G3502U', 'Samsung SM-G3508', 
        'Samsung SM-G3509', 'Samsung SM-G3508I', 'Samsung SM-G3502C', 'Samsung SM-G3502I', 'Samsung SM-G3508J', 
        'Samsung SM-G3509I', 'Samsung SHW-M130L', 'Samsung SPH-L300', 'Samsung SPH-L300', 'Samsung SM-T677', 
        'Samsung SAMSUNG-SM-T677A', 'Samsung SM-T677V', 'Samsung SM-T677', 'Samsung SM-T670', 'Samsung SM-T670', 
        'Samsung SM-T927A', 'Samsung GT-I8150', 'Samsung GT-I8150B', 'Samsung GT-I8150T', 'Samsung SGH-T679M', 
        'Samsung SM-T255S', 'Samsung SM-G600S', 'Samsung SM-J727S', 'Samsung SM-J737S', 'Samsung SM-A205S', 'Samsung GT-I8558', 
        'Samsung SCH-I869', 'Samsung GT-I8552', 'Samsung GT-I8552B', 'Samsung GT-I8550E', 'Samsung SHV-E500L', 
        'Samsung SHV-E500S', 'Samsung GT-I8552', 'Samsung SM-G3818', 'Samsung SM-G3819', 'Samsung SM-G3819D', 
        'Samsung SM-G3812', 'Samsung SM-G360BT', 'Samsung SM-G398FN', 'Samsung SM-G525F', 'Samsung SM-G889F', 
        'Samsung SM-G889G', 'Samsung SM-G889A', 'Samsung SM-G889YB', 'Samsung SM-G715A', 'Samsung SM-G715FN', 
        'Samsung SM-G715U', 'Samsung SM-G715U1', 'Samsung SM-G715W', 'Samsung SM-G390F', 'Samsung GT-S5690', 
        'Samsung GT-S5690L', 'Samsung GT-S5690M', 'Samsung GT-S5690R', 'Samsung GT-S7710', 'Samsung GT-S7710L', 
        'Samsung SM-G388F', 'Samsung SM-G389F', 'Samsung SM-G390Y', 'Samsung SM-G390W', 'Samsung GT-S5360', 'Samsung GT-S5360B', 
        'Samsung GT-S5360L', 'Samsung GT-S5360T', 'Samsung GT-S5363', 'Samsung GT-S5368', 'Samsung GT-S5369', 
        'Samsung SCH-I509', 'Samsung SCH-i509', 'Samsung GT-S6102', 'Samsung GT-S6102B', 'Samsung GT-S6102E', 
        'Samsung GT-S5303', 'Samsung GT-S5303B', 'Samsung GT-S6108', 'Samsung GT-B5510', 'Samsung GT-B5510B', 
        'Samsung GT-B5510L', 'Samsung GT-B5512', 'Samsung GT-B5512B', 'Samsung GT-S5367', 'Samsung GT-S6312', 
        'Samsung GT-S6313T', 'Samsung GT-S6310', 'Samsung GT-S6310B', 'Samsung GT-S6310L', 'Samsung GT-S6310T', 
        'Samsung GT-S6313T', 'Samsung GT-S6310N', 'Samsung SM-G130H', 'Samsung SM-G130M', 'Samsung SM-G130U', 
        'Samsung SM-G130BT', 'Samsung SM-G130E', 'Samsung SM-G130HN', 'Samsung SM-G130BU', 'Samsung SCV47', 'Samsung SM-F7000', 
        'Samsung SM-F700F', 'Samsung SM-F700N', 'Samsung SM-F700U', 'Samsung SM-F700U1', 'Samsung SM-F700W', 
        'Samsung SCG04', 'Samsung SM-F7070', 'Samsung SM-F707B', 'Samsung SM-F707N', 'Samsung SM-F707U', 'Samsung SM-F707U1', 
        'Samsung SM-F707W', 'Samsung SM-F9160', 'Samsung SM-F916B', 'Samsung SM-F916N', 'Samsung SM-F916Q', 'Samsung SM-F916U', 
        'Samsung SM-F916U1', 'Samsung SM-F916W', 'Samsung YP-GB70D', 'Samsung SM-T677NK', 'Samsung SM-T677NL', 
        'Samsung GT-I8550L', 'Samsung SM-A9000', 'Samsung SGH-T399N', 'Samsung SGH-T399', 'Samsung Gear Live', 
        'Samsung SCH-I100', 'Samsung SM-T387VK', 'Samsung SCH-W789', 'Samsung GT-B9150', 'Samsung GT-B9150', 
        'Samsung YP-GH1', 'Samsung SCH-I110', 'Samsung SAMSUNG-SGH-I997', 'Samsung SAMSUNG-SGH-I997R', 'Samsung SM-J106F', 
        'Samsung SPH-M900', 'Samsung SM-W2014', 'Samsung Nexus 10', 'Samsung Nexus S', 'Samsung Nexus S 4G', 
        'Samsung samsung-printer-tablet', 'Samsung SPH-M580', 'Samsung SPH-M580BST', 'Samsung SCH-R680', 'Samsung GT-S6293T', 
        'Samsung GT-S6293T', 'Samsung SAMSUNG-SGH-I847', 'Samsung SM-G6200', 'Samsung SM-G9198', 'Samsung SM-J260A', 
        'Samsung SM-J336AZ', 'Samsung SM-J337A', 'Samsung SM-J337AZ', 'Samsung SM-T230NZ', 'Samsung SM-W2018', 
        'Samsung SM-W2018X', 'Samsung SGH-T839', 'Samsung SCH-R730', 'Samsung SPH-M920', 'Samsung SPH-M930', 
        'Samsung SPH-M930BST', 'Samsung SPH-M910', 'Samsung SPH-M910', 'Samsung SM-W2016', 'Samsung SM-W2017',
        
        'HTC HTC Flyer', 'HTC HTC_P515E', 'HTC HTC_X515E', 'HTC HTC Incredible E S715e', 'HTC HTC One X9 dual sim', 
        'HTC ADR6325', 'HTC HTC_0P3P5', 'HTC HTC_0P4E2', 'HTC HTC 0P9C8', 'HTC HTC Desire 816 dual sim', 'HTC HTC_0PFJ50', 
        'HTC HTC 0PK72', 'HTC HTC One M9PLUS', 'HTC HTC 10', 'HTC HTC 10 Lifestyle', 'HTC HTC 2PS63', 'HTC HTC M10u', 
        'HTC HTC 10', 'HTC HTC 2PS6200', 'HTC HTC M10h', 'HTC HTC_M10h', 'HTC HTV32', 'HTC 2PS64', 'HTC HTC 10', 
        'HTC HTC6545LVW', 'HTC MSM8996 for arm64', 'HTC HTC 10 evo', 'HTC HTC_M10f', 'HTC HTC 10 evo', 'HTC HTC Desire 500 dual sim', 
        'HTC HTC 601e', 'HTC HTC 606w', 'HTC HTC Desire 600', 'HTC HTC Desire 600 dual sim', 'HTC HTC PO49120', 
        'HTC HTC 608t', 'HTC HTC 609d', 'HTC HTC 6160', 'HTC HTC 619d', 'HTC HTC_7060', 'HTC 710C', 'HTC HTC 802d', 
        'HTC HTC 803e', 'HTC HTC 8060', 'HTC HTC 8088', 'HTC HTC 809d', 'HTC HTC 8160', 'HTC HTC 901e', 'HTC HTC 801e', 
        'HTC HTC 802w', 'HTC HTC 9088', 'HTC HTC 919d', 'HTC HTC_A510c', 'HTC ADR6330VW', 'HTC ADR6425LVW', 'HTC HTC EVARE_UL', 
        'HTC HTC One X+', 'HTC HTC Amaze 4G', 'HTC HTC Ruby', 'HTC HTC_Amaze_4G', 'HTC HTC Aria', 'HTC HTC Aria A6380', 
        'HTC HTC Gratia A6380', 'HTC HTC Liberty', 'HTC HTC Butterfly', 'HTC HTC DLX_U', 'HTC HTC X920e', 'HTC HTC Butterfly', 
        'HTC HTC DLXUB1', 'HTC HTC Butterfly 2', 'HTC HTC_B810x', 'HTC HTC_B830x', 'HTC HTC Butterfly s', 'HTC HTC_Butterfly_s_901s', 
        'HTC HTC 9060', 'HTC HTC ChaCha A810b', 'HTC HTC ChaCha A810e', 'HTC HTC ChaChaCha A810e', 'HTC HTC Status', 
        'HTC HTC D10w', 'HTC HTC D316d', 'HTC HTC D610t', 'HTC HTC D626t', 'HTC HTC Desire 626 dual sim', 'HTC HTC_D626q', 
        'HTC HTC D626t', 'HTC HTC_D628u', 'HTC HTC D728w', 'HTC HTC Desire 728 dual sim', 'HTC HTC_D728x', 'HTC HTC D816d', 
        'HTC HTC_D816d', 'HTC HTC D816e', 'HTC HTC D816h', 'HTC HTC D816t', 'HTC HTC D816v', 'HTC HTC D816w', 
        'HTC HTC D820mt', 'HTC HTC_D820f', 'HTC HTC D820t', 'HTC HTC D820u', 'HTC HTC_D820u', 'HTC HTC_D820ts', 
        'HTC HTC_D820ys', 'HTC HTC_D820ys', 'HTC HTC D826t', 'HTC HTC6435LRA', 'HTC ADR6410LRA', 'HTC ADR6410LVW', 
        'HTC ADR6410OM', 'HTC HTC Desire', 'HTC X06HT', 'HTC PB99400', 'HTC HTC 2PZS1', 'HTC HTC Desire 10 compact', 
        'HTC a37dj dugl', 'HTC HTC Desire 10 lifestyle', 'HTC HTC Desire 10 lifestyle', 'HTC HTC_D10u', 'HTC HTC Desire 10 lifestyle', 
        'HTC HTC Desire 10 pro', 'HTC HTC Desire 10 pro', 'HTC HTC_D10i', 'HTC HTC 2PYA3', 'HTC HTC Desire 10 pro', 
        'HTC HTC 2Q5V1', 'HTC HTC Desire 12', 'HTC HTC 2Q5V200', 'HTC HTC Desire 12 (2Q5V200)', 'HTC HTC 2Q5W1', 
        'HTC HTC 2Q5W2', 'HTC HTC Desire 12+', 'HTC HTC ZQ5W10000', 'HTC HTC Desire 12+', 'HTC HTC 2Q721', 'HTC HTC Desire 12s', 
        'HTC EXODUS 1s', 'HTC HTC Desire 12s', 'HTC 2Q9J100', 'HTC HTC Desire 20 Pro', 'HTC HTC Desire 200', 
        'HTC HTC_Desire_200', 'HTC HTC Desire 210 dual sim', 'HTC HTC 301e', 'HTC HTC Desire 300', 'HTC HTC_0P6A1', 
        'HTC HTC_Desire_300', 'HTC HTC D310w', 'HTC HTC Desire 310 dual sim', 'HTC HTC Desire 310', 'HTC HTC_D310n', 
        'HTC HTC_V1', 'HTC HTC 0PF11', 'HTC HTC 0PF120', 'HTC HTC Desire 320', 'HTC HTC 2PNT1', 'HTC HTC Desire 326G dual sim', 
        'HTC HTC Desire 500', 'HTC HTC_Desire_500', 'HTC HTC 5060', 'HTC HTC Desire 500 dual sim', 'HTC HTC Desire 501', 
        'HTC HTC_603h', 'HTC HTC Desire 501 dual sim', 'HTC HTC 5088', 'HTC 0PCV1', 'HTC HTC 0PCV20', 'HTC HTC Desire 510', 
        'HTC HTC_0PCV2', 'HTC HTC Desire 510', 'HTC HTC Desire 512', 'HTC HTC D516d', 'HTC HTC D516t', 'HTC HTC C2', 
        'HTC HTC D516w', 'HTC HTC V2', 'HTC HTC Desire 516 dual sim', 'HTC HTC Desire 516 dual sim', 'HTC HTC V2', 
        'HTC HTC 0PGQ1', 'HTC HTC 0PM31', 'HTC HTC Desire 526', 'HTC HTCD100LVW', 'HTC HTCD100LVWPP', 'HTC HTC 0PL41', 
        'HTC HTC 0PL4100', 'HTC HTC Desire 526G dual sim', 'HTC HTC Desire 526GPLUS dual sim', 'HTC HTC_D526h', 
        'HTC HTC 0PL41', 'HTC HTC Desire 526G', 'HTC HTC 2PST1', 'HTC HTC 2PST2', 'HTC HTC Desire 530', 'HTC HTC_D530u', 
        'HTC HTC 2PST3', 'HTC HTC Desire 530', 'HTC HTCD160LVW', 'HTC HTCD160LVWPP', 'HTC HTC Desire 550', 'HTC HTC Desire 555', 
        'HTC HTC Desire 600', 'HTC HTC Desire 600 dual sim', 'HTC HTC 609d', 'HTC HTC Desire 600c dual sim', 
        'HTC HTC Desire 601', 'HTC HTC_0P4E2', 'HTC HTC Desire 601', 'HTC HTC0P4E1', 'HTC HTC Desire 601 dual sim', 
        'HTC HTC 606w', 'HTC HTC 609d', 'HTC HTC Desire 610', 'HTC HTC_0P9O2', 'HTC HTC_D610x', 'HTC HTC Desire 610', 
        'HTC HTC 0P9O30', 'HTC HTC Desire 612', 'HTC HTC D616w', 'HTC HTC Desire 616 dual sim', 'HTC HTC V3', 
        'HTC HTC 0PE64', 'HTC HTC Desire 620', 'HTC HTC_D620u', 'HTC HTC 0PE65', 'HTC HTC Desire 620G dual sim', 
        'HTC HTC_D620h', 'HTC HTC D626d', 'HTC HTCD200LVW', 'HTC HTCD200LVWPP', 'HTC HTC Desire 626', 'HTC HTC_D626x', 
        'HTC HTC_D630x', 'HTC HTC Desire 626', 'HTC HTC_0PKX2', 'HTC HTC Desire 626 dual sim', 'HTC HTC 0PM11', 
        'HTC HTC Desire 626G dual sim', 'HTC HTC Desire 626GPLUS dual sim', 'HTC HTC_D626ph', 'HTC HTC Desire 625', 
        'HTC HTC Desire 626s', 'HTC HTC Desire 626s', 'HTC 0PM92', 'HTC HTC 0PM92', 'HTC HTC Desire 626s', 'HTC HTC Desire 628', 
        'HTC HTC Desire 628 dual sim', 'HTC HTC 2PST5', 'HTC HTC Desire 630 dual sim', 'HTC HTC 2PYR1', 'HTC HTC Desire 650', 
        'HTC HTC_D650h', 'HTC A37 DUGL', 'HTC HTC Desire 650 dual sim', 'HTC HTC Desire 700 dual sim', 'HTC HTC Desire 700 dual sim', 
        'HTC HTC_709d', 'HTC HTC_7060', 'HTC HTC 7088', 'HTC HTC 709d', 'HTC HTC 2PQ84', 'HTC HTC Desire 728', 
        'HTC HTC Desire 728 dual sim', 'HTC HTC 2PQ83', 'HTC HTC Desire 728G dual sim', 'HTC HTC Desire 816', 
        'HTC HTC Desire 816', 'HTC HTC_0P9C2', 'HTC HTC_D816x', 'HTC HTC Desire 816 dual sim', 'HTC HTC Desire 816 dual sim', 
        'HTC HTC Desire 816G dual sim', 'HTC HTC Desire 816G dual sim', 'HTC HTC D816h', 'HTC HTC Desire 816G dual sim', 
        'HTC HTC 0PFJ4', 'HTC HTC Desire 820', 'HTC HTC Desire 820 dual sim', 'HTC HTC Desire 820G PLUS dual sim', 
        'HTC HTC Desire 820G dual sim', 'HTC HTC_D820pi', 'HTC HTC Desire 820q dual sim', 'HTC HTC D820ts', 'HTC HTC D820us', 
        'HTC HTC Desire 820s dual sim', 'HTC HTC Desire 820s dual sim', 'HTC HTC 2PUK2', 'HTC HTC Desire 825', 
        'HTC HTC_D825u', 'HTC HTC 2PUK1', 'HTC HTC Desire 825 dual sim', 'HTC HTC D826w', 'HTC HTC D826d', 'HTC HTC_D826y', 
        'HTC HTC D826t', 'HTC HTC Desire 826 dual sim', 'HTC HTC Desire 826 dual sim', 'HTC HTC D828w', 'HTC HTC_D828x', 
        'HTC HTC 2PRE4', 'HTC HTC Desire 828', 'HTC HTC_D828g', 'HTC HTC Desire 828 dual sim', 'HTC HTC 2PRE2', 
        'HTC HTC Desire 828 dual sim', 'HTC HTC Desire 830', 'HTC HTC_D830x', 'HTC HTC 2PVD1', 'HTC HTC D830u', 
        'HTC HTC Desire 830 dual sim', 'HTC HTC Desire C', 'HTC HTC Desire C', 'HTC HTC D626w', 'HTC HTC D820mt', 
        'HTC HTC D820mu', 'HTC HTC D826d', 'HTC HTC 0PFH2', 'HTC HTC Desire EYE', 'HTC HTC_M910x', 'HTC HTC 0PFH11', 
        'HTC HTC Desire EYE', 'HTC HTC Desire Eye', 'HTC 001HT', 'HTC Desire HD', 'HTC HTC Desire HD A9191', 
        'HTC Inspire HD', 'HTC Desire L by HTC', 'HTC HTC Desire L dual sim', 'HTC HTC Desire P', 'HTC HTC Desire S', 
        'HTC HTC Desire SV', 'HTC HTC Desire Q', 'HTC HTC Desire U', 'HTC HTC Desire U dual sim', 'HTC HTC Desire V', 
        'HTC HTC PROMIN_U', 'HTC HTC PRO_DS', 'HTC HTC T327w', 'HTC HTC T328w', 'HTC HTC Desire VC', 'HTC HTC Desire VC T328d', 
        'HTC HTC PRO_DD', 'HTC HTC T328d', 'HTC HTC Desire X', 'HTC HTC POO_U', 'HTC HTC Desire X dual sim', 
        'HTC HTC Desire XC dual sim', 'HTC HTC_Desire_320', 'HTC HTC 0PKX2', 'HTC HTC Desire 626', 'HTC HTC 0PM912', 
        'HTC HTC Desire 626', 'HTC HTC Desire 816G', 'HTC HTC 2PST1', 'HTC HTC Desire 530', 'HTC HTC6435LRA', 
        'HTC HTC6435LVW', 'HTC Eris', 'HTC Pulse', 'HTC ADR6300', 'HTC HTC E9pt', 'HTC HTC E9pw', 'HTC HTC_E9pw', 
        'HTC HTC E9t', 'HTC HTC E9w', 'HTC HTC_E9x', 'HTC HTCEVOV4G', 'HTC PG86100', 'HTC ISW12HT', 'HTC HTC EVO 3D X515a', 
        'HTC HTC EVO 3D X515m', 'HTC HTC Inspire 3D', 'HTC EVO', 'HTC EVO', 'HTC PG06100', 'HTC EXODUS 1', 'HTC EXODUS 1', 
        'HTC PC36100', 'HTC HTC Explorer', 'HTC HTC Explorer A310b', 'HTC HTC Explorer A310e', 'HTC HTC Flyer', 
        'HTC HTC Flyer P510e', 'HTC HTC Flyer P511e', 'HTC HTC Flyer P512', 'HTC HTC_Flyer_P512_NA', 'HTC HTC Dream', 
        'HTC HTC Vision', 'HTC T-Mobile G2', 'HTC HTC 10 evo', 'HTC HTC 5G Hub', 'HTC HTC 5G Hub', 'HTC HTC 5G Hub', 
        'HTC HTC 5G Hub', 'HTC HTC A100', 'HTC 2Q8L10000', 'HTC HTC Desire 19s', 'HTC HTC 2Q9J10000', 'HTC HTC Desire 20 Pro', 
        'HTC 2Q9U100', 'HTC HTC Desire 20+', 'HTC 2QAG100', 'HTC HTC Desire 21 pro 5G', 'HTC 2QAG100', 'HTC HTC Desire 21 pro 5G', 
        'HTC HTC Desire 610', 'HTC HTC 2PVG2', 'HTC HTC Desire 628 dual sim', 'HTC 2Q74100', 'HTC HTC Desire 19+', 
        'HTC HTC One', 'HTC HTC One mini', 'HTC HTC 2PZC100', 'HTC HTC 2Q4R400', 'HTC HTC 2Q4R300', 'HTC HTC 2Q4R400', 
        'HTC HTC 2Q4R1', 'HTC HTC 2Q4R100', 'HTC HTC U11 EYEs', 'HTC HTC U11 life', 'HTC HTC U11 Life', 'HTC HTC U11 life', 
        'HTC HTC 2Q4D200', 'HTC HTC U11 plus', 'HTC HTC_2Q4D100', 'HTC HTC 2Q7A100', 'HTC HTC Wildfire X', 'HTC HTC6435LVW', 
        'HTC HTC 919d', 'HTC HTC331ZLVW', 'HTC HTC331ZLVWPP', 'HTC HTC Acquire', 'HTC HTC EVO Design C715e', 
        'HTC HTC Hero S', 'HTC HTC Kingdom', 'HTC HTCEVODesign4G', 'HTC PH44100', 'HTC HTC6600LVW', 'HTC HTL23', 
        'HTC HTV31', 'HTC ERA G2 Touch', 'HTC HTC Hero', 'HTC T-Mobile G2 Touch', 'HTC T-Mobile_G2_Touch', 'HTC dopod A6288', 
        'HTC HERO200', 'HTC ISW13HT', 'HTC ADR6350', 'HTC HTC IncredibleS S710d', 'HTC HTC Incredible S', 'HTC HTC_S710E', 
        'HTC HTL21', 'HTC HTL22', 'HTC HTC J Z321e', 'HTC HTX21', 'HTC HTC Legend', 'HTC HTC 10', 'HTC HTC M8si', 
        'HTC HTC M8t', 'HTC HTC One M9', 'HTC HTC M9e', 'HTC HTC One M9_Prime Camera Edition', 'HTC HTC One M9s', 
        'HTC HTC_M9e', 'HTC HTC M9et', 'HTC HTC M9ew', 'HTC HTC_M9ew', 'HTC HTC M9pw', 'HTC HTC M9pw', 'HTC HTC_M9px', 
        'HTC HTC M9w', 'HTC Nexus 9', 'HTC Nexus 9', 'HTC Nexus One', 'HTC HTC One dual sim', 'HTC HTC One M8s', 
        'HTC HTC_0PKV1', 'HTC HTC One S', 'HTC HTC K2_U', 'HTC HTC One SV', 'HTC HTC One SV', 'HTC HTC 801e', 
        'HTC HTC One', 'HTC HTC One 801e', 'HTC HTC_PN071', 'HTC HTC 802t', 'HTC HTC 802t 16GB', 'HTC HTC 802w', 
        'HTC HTC One dual sim', 'HTC HTC 802d', 'HTC HTC One dual 802d', 'HTC HTC One dual sim', 'HTC HTC One', 
        'HTC HTCONE', 'HTC HTC One', 'HTC HTC6500LVW', 'HTC HTC M8Sd', 'HTC HTC M8St', 'HTC HTC One_E8', 'HTC HTC One_E8', 
        'HTC HTC_M8Sx', 'HTC 0PAJ5', 'HTC HTC One_E8 dual sim', 'HTC HTC_M8Sy', 'HTC HTC 0PAJ4', 'HTC HTC M8Sd', 
        'HTC HTC One_E8 dual sim', 'HTC HTC M8St', 'HTC HTC M8Sw', 'HTC HTC M8Ss', 'HTC HTC 0P6B900', 'HTC HTC One_M8 Eye', 
        'HTC HTC 0P6B9', 'HTC HTC One_M8 Eye', 'HTC HTC M8w', 'HTC HTC One_M8', 'HTC HTC_0P6B', 'HTC HTC_0P6B6', 
        'HTC HTC_M8x', 'HTC HTC One_M8 dual sim', 'HTC HTC M8d', 'HTC 831C', 'HTC HTC One_M8', 'HTC HTC6525LVW', 
        'HTC HTC M8e', 'HTC HTC One 801e', 'HTC HTC One 801s', 'HTC HTC A9w', 'HTC HTC One A9', 'HTC HTC_A9u', 
        'HTC HTC One A9', 'HTC 2PQ93', 'HTC HTC 2PWD1', 'HTC HTC One A9s', 'HTC HTC_A9sx', 'HTC HTC 2PWD2', 'HTC HTC One A9s', 
        'HTC HTC One dual 802d', 'HTC HTC One dual sim', 'HTC HTC_M8Sd', 'HTC HTC 0PL31', 'HTC HTC One E9 dual sim', 
        'HTC HTC One E9PLUS dual sim', 'HTC HTC D826sw', 'HTC HTC One E9s dual sim', 'HTC HTC_E9sx', 'HTC HTC One', 
        'HTC HTC M8Et', 'HTC HTC M8Ew', 'HTC 0PJA10', 'HTC HTC 0PJA10', 'HTC HTC One M9', 'HTC HTC_0PJA10', 'HTC HTC_M9u', 
        'HTC HTC One M9', 'HTC HTC One M9', 'HTC 0PJA2', 'HTC HTC One M9', 'HTC HTC6535LRA', 'HTC HTC6535LVW', 
        'HTC HTC 0PK71', 'HTC HTC M9pt', 'HTC HTC One M9PLUS', 'HTC HTC_M9pw', 'HTC HTC 0PK71', 'HTC HTC One M9PLUS_Prime Camera Edition', 
        'HTC HTC One M9PLUS', 'HTC HTC 0PLA1', 'HTC HTC One ME dual sim', 'HTC HTC One S', 'HTC HTC VLE_U', 'HTC HTC One S', 
        'HTC HTC Z560e', 'HTC HTC One S Special Edition', 'HTC HTC 2PRG100', 'HTC HTC One S9', 'HTC HTC_S9u', 
        'HTC HTC One SC', 'HTC HTC One SC T528d', 'HTC C525c', 'HTC HTC One SV', 'HTC HTC K2_UL', 'HTC HTC One SV', 
        'HTC HTC One SV', 'HTC HTC One SV BLK', 'HTC HTC One V', 'HTC HTC ONE V', 'HTC HTC One V', 'HTC HTC One VX', 
        'HTC HTC One X', 'HTC HTC S720e', 'HTC HTC One X', 'HTC HTC One X+', 'HTC HTC One X+', 'HTC HTC 2PXH1', 
        'HTC HTC One X10', 'HTC HTC 2PXH2', 'HTC HTC One X10', 'HTC HTC_X10u', 'HTC HTC 2PXH3', 'HTC HTC 2PS5200', 
        'HTC HTC One X9 dual sim', 'HTC HTC X9u', 'HTC HTC_X9u', 'HTC HTC One X', 'HTC HTC One XL', 'HTC HTC_One_XL', 
        'HTC HTC EVA_UTL', 'HTC HTC One max', 'HTC HTC_One_max', 'HTC HTC0P3P7', 'HTC HTC One mini', 'HTC HTC One mini', 
        'HTC HTC_One_mini_601e', 'HTC HTC_PO582', 'HTC HTC One mini 2', 'HTC HTC_M8MINx', 'HTC HTC_One_mini_2', 
        'HTC HTC_One_mini_601e', 'HTC HTC6515LVW', 'HTC HTC One_E8', 'HTC HTC One X', 'HTC HTC PO091', 'HTC HTC PG09410', 
        'HTC HTC-P715a', 'HTC HTC Rhyme S510b', 'HTC HTC S720e', 'HTC HTC Salsa C510b', 'HTC HTC Salsa C510e', 
        'HTC HTC Sensation', 'HTC HTC Sensation 4G', 'HTC HTC Sensation XE with Beats Audio', 'HTC HTC Sensation XE with Beats Audio Z715a', 
        'HTC HTC Sensation XE with Beats Audio Z715e', 'HTC HTC Sensation Z710a', 'HTC HTC Sensation Z710e', 
        'HTC HTC-Z710a', 'HTC HTC Sensation XL with Beats Audio X315b', 'HTC HTC Sensation XL with Beats Audio X315e', 
        'HTC HTC-X315E', 'HTC Sensation XL with Beats Audio', 'HTC HTC T329d', 'HTC HTC Desire L dual sim', 'HTC HTC 2PQ910', 
        'HTC ADR6400L', 'HTC HTC Mecha', 'HTC HTC U Play', 'HTC HTC_U-2u', 'HTC HTC 2PZM3', 'HTC HTC U Play', 
        'HTC HTC 2PWD1', 'HTC HTC U-1w', 'HTC HTC U Ultra', 'HTC HTC_U-1u', 'HTC HTC 2PZF1', 'HTC HTC U Ultra', 
        'HTC HTC U-3w', 'HTC HTC U11', 'HTC HTC_U-3u', 'HTC HTC 2PZC100', 'HTC HTC U11', 'HTC 601HT', 'HTC HTC U11', 
        'HTC HTV33', 'HTC 2PZC5', 'HTC HTC U11', 'HTC HTC U11 Life', 'HTC HTC U11 life', 'HTC HTC 2Q55300', 'HTC HTC 2Q6E1', 
        'HTC HTC U12 life', 'HTC HTC 2Q551', 'HTC HTC 2Q551+', 'HTC HTC 2Q55100', 'HTC HTC U12+', 'HTC HTC 2Q552', 
        'HTC HTC U12+', 'HTC HTC U12+', 'HTC 2Q9F100', 'HTC HTC U20 5G', 'HTC HTC PH39100', 'HTC HTC Raider X710e', 
        'HTC HTC Velocity 4G', 'HTC HTC Velocity 4G X710s', 'HTC HTC-X710a', 'HTC HTC WF5w', 'HTC HTC Wildfire', 
        'HTC HTC Bee', 'HTC HTC Wildfire', 'HTC Wildfire E', 'HTC Wildfire E Lite', 'HTC Wildfire E ultra', 'HTC HTC Wildfire E1', 
        'HTC Wildfire E1', 'HTC Wildfire E1 Plus', 'HTC Wildfire E2', 'HTC Wildfire E2 plus', 'HTC Wildfire E3', 
        'HTC HTC Wildfire S', 'HTC HTC Wildfire S A510b', 'HTC HTC Wildfire S A510e', 'HTC HTC-A510a', 'HTC HTC Wildfire S A515c', 
        'HTC HTC-PG762', 'HTC USCCADR6230US', 'HTC Wildfire E1 Plus', 'HTC Wildfire R70', 'HTC X2-HT', 'HTC HTC Desire 400 dual sim', 
        'HTC HTC 608t', 'HTC HTC Desire 610', 'HTC HTC Desire X', 'HTC HTC first', 'HTC HTC Magic', 'HTC T-Mobile myTouch 3G', 

        'Huawei Huawei Ideos X1', 'Huawei IDEOS X1', 'Huawei Kyivstar Terra', 'Huawei Pulse', 'Huawei HUAWEI T8300', 
        'Huawei HUAWEI T8600', 'Huawei HUAWEI T8828', 'Huawei EQ U8110', 'Huawei Huawei', 'Huawei Huawei U8110', 
        'Huawei MTC_A', 'Huawei Pulse Mini', 'Huawei Turkcell T10', 'Huawei life:) Android', 'Huawei HUAWEI IDEOS U8500', 
        'Huawei MTC_EVO', 'Huawei dtab01', 'Huawei HUAWEI C8813Q', 'Huawei HUAWEI C8860E', 'Huawei HUAWEI G520-T10', 
        'Huawei HUAWEI C8650+', 'Huawei HUAWEI C8655', 'Huawei HUAWEI C8810', 'Huawei HUAWEI C8812E', 'Huawei HUAWEI C8813', 
        'Huawei HUAWEI C8825D', 'Huawei HUAWEI C8860E', 'Huawei HUAWEI C8950D', 'Huawei HUAWEI H866C', 'Huawei HUAWEI H868C', 
        'Huawei HUAWEI H881C', 'Huawei HUAWEI M866', 'Huawei HUAWEI P2-0000', 'Huawei HUAWEI P2-6011', 'Huawei HUAWEI P2-6011-orange', 
        'Huawei MediaPad 10 FHD', 'Huawei MediaPad 10 FHD', 'Huawei MediaPad 10 LINK', 'Huawei HUAWEI MediaPad', 
        'Huawei HUAWEI MediaPad', 'Huawei Huawei S7-312u', 'Huawei HUAWEI MediaPad', 'Huawei MediaPad 7 Lite', 
        'Huawei HUAWEI T8833', 'Huawei HUAWEI T8950', 'Huawei HUAWEI T8950N', 'Huawei HUAWEI T8951', 'Huawei Netphone 501', 
        'Huawei U8230', 'Huawei GM FOX', 'Huawei MTC Pro', 'Huawei Personal U8350', 'Huawei Grameenphone Crystal', 
        'Huawei HUAWEI_IDEOS_U8500', 'Huawei MTC Evo', 'Huawei MegaFon U8500', 'Huawei Beeline_E500', 'Huawei GM Ultimate Slim', 
        'Huawei Huawei IDEOS X3', 'Huawei MTC Bravo', 'Huawei HUAWEI SONIC', 'Huawei HUAWEI_IDEOS_U8650', 'Huawei Kyivstar Aqua', 
        'Huawei MTC 955', 'Huawei Turkcell T20', 'Huawei HUAWEI IDEOS Y 200', 'Huawei Personal U8655-51', 'Huawei STARTRAIL II', 
        'Huawei HUAWEI U8661', 'Huawei MTC Fit', 'Huawei HUAWEI U8666E', 'Huawei MegaFon SP-A3', 'Huawei HUAWEI U8666E', 
        'Huawei HUAWEI U8666E-51', 'Huawei HUAWEI U8666N', 'Huawei T-Mobile myTouch', 'Huawei HUAWEI U8681', 
        'Huawei T-Mobile myTouch Q', 'Huawei IDEOS X5', 'Huawei MTC Neo', 'Huawei U8800', 'Huawei u8800', 'Huawei HUAWEI_IDEOS_X5', 
        'Huawei IDEOS X5', 'Huawei MTC Neo', 'Huawei RBM_HD', 'Huawei U8800 Pro', 'Huawei HUAWEI Ascend G 300', 
        'Huawei HUAWEI U8815', 'Huawei HUAWEI_Ascend G 300', 'Huawei Personal U8815-51', 'Huawei HUAWEI U8815N', 
        'Huawei MTC Viva', 'Huawei HUAWEI U8818', 'Huawei Bs 401', 'Huawei HUAWEI Ascend G 330', 'Huawei HUAWEI U8825-1', 
        'Huawei HUAWEI U8825D', 'Huawei HUAWEI_U8860', 'Huawei TURKCELL MaxiPRO5', 'Huawei HUAWEI U8950-1', 'Huawei HUAWEI U8950-51', 
        'Huawei HUAWEI U8950D', 'Huawei HUAWEI U8950N-1', 'Huawei HUAWEI U8950N-51', 'Huawei HUAWEI U9508', 'Huawei HUAWEI U9510', 
        'Huawei HUAWEI U9510E', 'Huawei HUAWEI Y210-0010', 'Huawei HUAWEI Ascend Y 210', 'Huawei HUAWEI Y210-0100', 
        'Huawei HUAWEI Y210-0151', 'Huawei HUAWEI Ascend Y 210D', 'Huawei HUAWEI Asend Y 210D', 'Huawei HUAWEI Y210-0200', 
        'Huawei Leopard MF808', 'Huawei NATCOM N8302', 'Huawei VIETTEL V8404', 'Huawei HUAWEI Y210-0251', 'Huawei HUAWEI Y210-2010', 
        'Huawei Pulse', 'Huawei U8230', 'Huawei Beeline_E300', 'Huawei Grameenphone Crystal', 'Huawei HUAWEI IDEOS U8500', 
        'Huawei HUAWEI_IDEOS_U8500', 'Huawei Huawei', 'Huawei Ideos', 'Huawei MTC Evo', 'Huawei Pulse Mini', 
        'Huawei RBM C', 'Huawei Tactile internet', 'Huawei Turkcell T10', 'Huawei Vodafone 845', 'Huawei IDEOS X5', 
        'Huawei u8800', 'Huawei Ideos', 'Huawei M860', 'Huawei ORINOQUIA C8688V', 'Huawei IDEOS S7', 'Huawei Ideos S7', 
        'Huawei Oysters SmaKit S7', 'Huawei IDEOS S7 Slim', 'Huawei u8800', 'Huawei HUAWEI A199', 'Huawei ATH-TL00', 
        'Huawei ATH-TL00H', 'Huawei ATH-UL00', 'Huawei U9500', 'Huawei HUAWEI G510-0251', 'Huawei HUAWEI Ascend G525', 
        'Huawei HUAWEI G525-U00', 'Huawei HUAWEI B199', 'Huawei HUAWEI C199', 'Huawei HUAWEI C199s', 'Huawei HUAWEI C8812', 
        'Huawei HUAWEI C8813D', 'Huawei HUAWEI C8813DQ', 'Huawei HUAWEI C8815', 'Huawei HUAWEI C8816', 'Huawei HUAWEI C8816D', 
        'Huawei C8817D', 'Huawei HUAWEI C8817E', 'Huawei HUAWEI C8817L', 'Huawei HUAWEI C8818', 'Huawei HUAWEI C8826D', 
        'Huawei HUAWEI-C8850', 'Huawei CHC-U03', 'Huawei CHC-U23', 'Huawei CHM-CL00', 'Huawei CHM-U01', 'Huawei CM990', 
        'Huawei CUN-AL00', 'Huawei CUN-TL00', 'Huawei Che1-CL10', 'Huawei Che1-CL20', 'Huawei Che1-L04', 'Huawei Che2-L11', 
        'Huawei Che2-L23', 'Huawei Che2-TL00', 'Huawei Che2-TL00H', 'Huawei Che2-TL00M', 'Huawei Che2-UL00', 
        'Huawei CHC-U01', 'Huawei M330', 'Huawei H1611', 'Huawei HUAWEI H1611', 'Huawei HUAWEI D2-0082', 'Huawei HUAWEI D2-2010', 
        'Huawei HUAWEI D2-6070', 'Huawei HUAWEI P8max', 'Huawei HUAWEI LUA-L03', 'Huawei HUAWEI LUA-L13', 'Huawei HUAWEI LUA-L23', 
        'Huawei HUAWEI LUA-U03', 'Huawei HUAWEI LUA-U23', 'Huawei ES8100', 'Huawei HuaweiES8500', 'Huawei FIG-LX1', 
        'Huawei FRD-L02', 'Huawei Huawei-U8665', 'Huawei HUAWEI G350', 'Huawei HUAWEI G350-U00', 'Huawei HUAWEI G350-U20', 
        'Huawei HUAWEI G506-U151', 'Huawei HUAWEI G510-0010', 'Huawei HUAWEI G510-0100', 'Huawei HuaweiG510-0100', 
        'Huawei HuaweiG510-0100-orange', 'Huawei HUAWEI Ascend G510', 'Huawei HUAWEI G510-0200', 'Huawei Orange Daytona', 
        'Huawei HUAWEI G520-5000', 'Huawei HUAWEI G521-L076', 'Huawei HUAWEI G521-L176', 'Huawei G526-L11', 'Huawei G526-L22', 
        'Huawei G526-L33', 'Huawei G527-U081', 'Huawei HUAWEI G535-L11', 'Huawei Kestrel', 'Huawei Orange Gova', 
        'Huawei Speedsurfer', 'Huawei Ultym5', 'Huawei HUAWEI G6-T00', 'Huawei HUAWEI G6-C00', 'Huawei HUAWEI G6-L11', 
        'Huawei HUAWEI G6-L22', 'Huawei HUAWEI G6-L33', 'Huawei HUAWEI G6-U00', 'Huawei HUAWEI G6-U10', 'Huawei HUAWEI G6-U251', 
        'Huawei HUAWEI G6-U34', 'Huawei HUAWEI G606-T00', 'Huawei HUAWEI G606-T00', 'Huawei HUAWEI G610-T00', 
        'Huawei G610-U00', 'Huawei HUAWEI G610-U00', 'Huawei HUAWEI G610-U30', 'Huawei HUAWEI G610-T01', 'Huawei HUAWEI G610-T11', 
        'Huawei HUAWEI G610-U15', 'Huawei HUAWEI G610-U20', 'Huawei HUAWEI G610-C00', 'Huawei G615-U10', 'Huawei HUAWEI G615-U10', 
        'Huawei HUAWEI G616-L076', 'Huawei HUAWEI G620-A2', 'Huawei HUAWEI G620-L72', 'Huawei G620-L75', 'Huawei G620S-L01', 
        'Huawei G620S-L02', 'Huawei G620S-L03', 'Huawei HUAWEI G620', 'Huawei Personal Huawei G620S', 'Huawei G620S-UL00', 
        'Huawei G621-TL00', 'Huawei G621-TL00M', 'Huawei HUAWEI G628-TL00', 'Huawei HUAWEI G629-UL00', 'Huawei HUAWEI G630-T00', 
        'Huawei HUAWEI G630-U00', 'Huawei G630-U10', 'Huawei G630-U20', 'Huawei G630-U251', 'Huawei HUAWEI G630-U251', 
        'Huawei HUAWEI G660-L075', 'Huawei HUAWEI RIO-TL00', 'Huawei HUAWEI RIO-UL00', 'Huawei G7-L01', 'Huawei HUAWEI G7-L01', 
        'Huawei HUAWEI G7-L02', 'Huawei G7-L03', 'Huawei HUAWEI G7', 'Huawei HUAWEI G7-L03', 'Huawei HUAWEI G7-L11', 
        'Huawei G7-TL00', 'Huawei HUAWEI G7-TL00', 'Huawei HUAWEI G7-UL20', 'Huawei HUAWEI G700-T00', 'Huawei HUAWEI G700-U00', 
        'Huawei HUAWEI G700-T01', 'Huawei HUAWEI G700-U10', 'Huawei HUAWEI G700-U20', 'Huawei HUAWEI G716-L070', 
        'Huawei HUAWEI G718', 'Huawei HUAWEI G730-C00', 'Huawei HUAWEI G730-T00', 'Huawei HUAWEI G730-U00', 'Huawei HUAWEI G730-L075', 
        'Huawei HUAWEI G730-U10', 'Huawei HUAWEI G730-U251', 'Huawei HUAWEI G730-U27', 'Huawei HUAWEI G730-U30', 
        'Huawei G735-L03', 'Huawei G735-L12', 'Huawei G735-L23', 'Huawei G740-L00', 'Huawei Orange Yumo', 'Huawei HUAWEI G750-T00', 
        'Huawei HUAWEI G750-T01', 'Huawei HUAWEI G750-T01M', 'Huawei HUAWEI G750-T20', 'Huawei HUAWEI G750-U10', 
        'Huawei HUAWEI G7500', 'Huawei HUAWEI RIO-L02', 'Huawei HUAWEI RIO-L03', 'Huawei RIO-L03', 'Huawei HUAWEI RIO-L02', 
        'Huawei HUAWEI RIO-L03', 'Huawei HUAWEI MLA-TL00', 'Huawei HUAWEI MLA-TL10', 'Huawei HUAWEI MLA-UL00', 
        'Huawei MLA-TL00', 'Huawei MLA-UL00', 'Huawei HUAWEI VNS-AL00', 'Huawei HUAWEI TAG-L01', 'Huawei HUAWEI TAG-L03', 
        'Huawei HUAWEI TAG-L13', 'Huawei HUAWEI TAG-L21', 'Huawei HUAWEI TAG-L22', 'Huawei HUAWEI TAG-L23', 'Huawei DIG-L01', 
        'Huawei DIG-L21', 'Huawei DIG-L22', 'Huawei HUAWEI TAG-L32', 'Huawei HUAWEI KII-L03', 'Huawei HUAWEI KII-L05', 
        'Huawei HUAWEI KII-L21', 'Huawei HUAWEI KII-L22', 'Huawei HUAWEI KII-L23', 'Huawei HUAWEI KII-L33', 'Huawei KII-L21', 
        'Huawei H1621', 'Huawei HUAWEI NMO-L21', 'Huawei HUAWEI NMO-L22', 'Huawei HUAWEI NMO-L23', 'Huawei HUAWEI NMO-L31', 
        'Huawei HUAWEI', 'Huawei HUAWEI RIO-L01', 'Huawei Orinoquia Gran Roraima + S7-722u', 'Huawei H30-C00', 
        'Huawei HONOR H30-L01', 'Huawei HONOR H30-L01M', 'Huawei H30-L02', 'Huawei HONOR H30-L02', 'Huawei H30-T00', 
        'Huawei H60-L01', 'Huawei HW-H60-J1', 'Huawei H60-L01', 'Huawei H60-L02', 'Huawei H60-L03', 'Huawei H60-L04', 
        'Huawei H60-L11', 'Huawei H60-L12', 'Huawei H60-L21', 'Huawei H60-L21', 'Huawei HUAWEI H871G', 'Huawei H882L', 
        'Huawei HUAWEI H891L', 'Huawei HUAWEI H892L', 'Huawei CAG-L22', 'Huawei HRY-LX1T', 'Huawei YAL-AL00', 
        'Huawei YAL-L21', 'Huawei YAL-TL00', 'Huawei MAR-LX1R', 'Huawei YAL-AL10', 'Huawei YAL-L41', 'Huawei MAR-LX1H', 
        'Huawei HRY-LX1T', 'Huawei HRY-AL00Ta', 'Huawei Che2-L12', 'Huawei JAT-L29', 'Huawei JAT-L41', 'Huawei JAT-LX1', 
        'Huawei JAT-LX3', 'Huawei KSA-LX2', 'Huawei KSA-LX3', 'Huawei KSA-LX9', 'Huawei DUB-LX1', 'Huawei STK-L22', 
        'Huawei STK-LX1', 'Huawei STK-LX3', 'Huawei JSN-L21', 'Huawei JSN-L21', 'Huawei JSN-L22', 'Huawei JSN-L23', 
        'Huawei PCT-TL10', 'Huawei PCT-AL10', 'Huawei PCT-L29', 'Huawei SLA-L03', 'Huawei BLL-L21', 'Huawei BLL-L22', 
        'Huawei HUAWEI BLL-L21', 'Huawei HUAWEI BLL-L22', 'Huawei HMA-L09', 'Huawei HMA-L29', 'Huawei LYA-L0C', 
        'Huawei LYA-L29', 'Huawei EVR-AN00', 'Huawei EVR-N29', 'Huawei SNE-LX1', 'Huawei BLL-L23', 'Huawei HUAWEI BLL-L23', 
        'Huawei BND-L34', 'Huawei 701HW', 'Huawei 702HW', 'Huawei CPN-AL00', 'Huawei CPN-L09', 'Huawei CPN-W09', 
        'Huawei HDN-L09', 'Huawei HDN-W09', 'Huawei CMR-AL09', 'Huawei CMR-W09', 'Huawei SHT-AL09', 'Huawei SHT-W09', 
        'Huawei CMR-AL19', 'Huawei CMR-W19', 'Huawei BAH2-L09', 'Huawei BAH2-W19', 'Huawei JDN2-L09', 'Huawei JDN2-W09', 
        'Huawei AGS-L03', 'Huawei AGS-L09', 'Huawei AGS-W09', 'Huawei BG2-U03', 'Huawei AGS2-W09', 'Huawei INE-LX1', 
        'Huawei FIG-LA1', 'Huawei FIG-LX2', 'Huawei FIG-LX3', 'Huawei POT-LX1', 'Huawei POT-LX1AF', 'Huawei POT-LX3', 
        'Huawei POT-LX1A', 'Huawei POT-LX3', 'Huawei STK-L21', 'Huawei STK-LX1', 'Huawei STK-LX1', 'Huawei POT-LX1T', 
        'Huawei ANE-LX2J', 'Huawei HWV32', 'Huawei ELE-AL00', 'Huawei ELE-L04', 'Huawei ELE-L09', 'Huawei ELE-L14', 
        'Huawei ELE-L29', 'Huawei ELE-L39', 'Huawei ELE-L49', 'Huawei ELE-TL00', 'Huawei HWV33', 'Huawei MAR-LX1A', 
        'Huawei MAR-LX1Am', 'Huawei MAR-LX1B', 'Huawei MAR-LX1M', 'Huawei MAR-LX1Mm', 'Huawei MAR-LX2', 'Huawei MAR-LX2B', 
        'Huawei MAR-LX2m', 'Huawei MAR-LX3A', 'Huawei MAR-LX3Am', 'Huawei MAR-LX3Bm', 'Huawei SLA-L02', 'Huawei SLA-L22', 
        'Huawei SLA-L23', 'Huawei ARS-L22', 'Huawei CRO-L02', 'Huawei CRO-L22', 'Huawei HUAWEI CRO-L02', 'Huawei HUAWEI CRO-L22', 
        'Huawei CAG-L02', 'Huawei CAG-L22', 'Huawei DRA-L01', 'Huawei DRA-L21', 'Huawei DRA-LX2', 'Huawei DRA-LX3', 
        'Huawei AMN-LX1', 'Huawei AMN-LX2', 'Huawei AMN-LX3', 'Huawei AMN-LX9', 'Huawei DRA-LX2', 'Huawei DRA-LX5', 
        'Huawei CRO-L03', 'Huawei CRO-L23', 'Huawei HUAWEI CRO-L03', 'Huawei HUAWEI CRO-L23', 'Huawei CAG-L03', 
        'Huawei CAG-L23', 'Huawei MYA-L11', 'Huawei ATU-L11', 'Huawei ATU-L21', 'Huawei ATU-L22', 'Huawei ATU-LX3', 
        'Huawei MRD-LX1', 'Huawei MRD-LX1F', 'Huawei MRD-LX1N', 'Huawei MRD-LX3', 'Huawei ATU-L31', 'Huawei ATU-L42', 
        'Huawei MRD-LX2', 'Huawei HUAWEI CAM-L53', 'Huawei JAT-L29', 'Huawei JAT-L41', 'Huawei JAT-LX1', 'Huawei JAT-LX3', 
        'Huawei LDN-L01', 'Huawei LDN-L21', 'Huawei LDN-LX3', 'Huawei DUB-LX1', 'Huawei DUB-LX3', 'Huawei LDN-L21', 
        'Huawei LDN-LX2', 'Huawei DUB-LX2', 'Huawei DUB-LX1', 'Huawei DUB-LX2', 'Huawei DUB-LX3', 'Huawei JKM-LX1', 
        'Huawei JKM-LX2', 'Huawei JKM-LX3', 'Huawei FLA-LX1', 'Huawei FLA-LX2', 'Huawei FLA-LX3', 'Huawei JKM-LX1', 
        'Huawei JKM-LX2', 'Huawei JKM-LX3', 'Huawei STK-L21', 'Huawei STK-L21', 'Huawei STK-L22', 'Huawei STK-LX3', 
        'Huawei BAC-L21', 'Huawei BAC-L22', 'Huawei LDN-LX2', 'Huawei YAL-L21', 'Huawei YAL-L41', 'Huawei 704HW', 
        'Huawei POT-LX2J', 'Huawei POT-LX2J', 'Huawei 608HW', 'Huawei KOB-L09', 'Huawei KOB-W09', 'Huawei HW-03E', 
        'Huawei HWT31', 'Huawei Hol-T00', 'Huawei Hol-U10', 'Huawei Hol-U19', 'Huawei COL-AL00', 'Huawei COL-AL10', 
        'Huawei COL-L29', 'Huawei COL-TL10', 'Huawei HRY-AL00', 'Huawei HRY-AL00a', 'Huawei HRY-AL00Ta', 'Huawei SCC-U21', 
        'Huawei SCL-AL00', 'Huawei SCL-CL00', 'Huawei SCL-TL00', 'Huawei SCL-TL00H', 'Huawei HUAWEI LYO-L21', 
        'Huawei LYO-L21', 'Huawei NEM-L21', 'Huawei NEM-L22', 'Huawei NEM-L51', 'Huawei KIW-L21', 'Huawei KIW-TL00H', 
        'Huawei DLI-L22', 'Huawei DLI-TL20', 'Huawei BLN-L24', 'Huawei PLK-AL10', 'Huawei PLK-CL00', 'Huawei PLK-L01', 
        'Huawei PLK-TL00', 'Huawei PLK-TL01H', 'Huawei PLK-UL00', 'Huawei AUM-AL00', 'Huawei AUM-AL20', 'Huawei AUM-L29', 
        'Huawei AUM-L33', 'Huawei AUM-TL00', 'Huawei AUM-TL20', 'Huawei DUA-L22', 'Huawei AUM-L41', 'Huawei LND-AL30', 
        'Huawei LND-AL40', 'Huawei LND-L29', 'Huawei LND-TL30', 'Huawei LND-TL40', 'Huawei DRA-LX5', 'Huawei DUA-AL00', 
        'Huawei DUA-L22', 'Huawei DUA-LX3', 'Huawei BND-L21', 'Huawei BND-L24', 'Huawei BND-L31', 'Huawei ATH-AL00', 
        'Huawei ATH-CL00', 'Huawei FRD-AL00', 'Huawei FRD-AL10', 'Huawei FRD-DL00', 'Huawei FRD-L04', 'Huawei FRD-L09', 
        'Huawei FRD-L14', 'Huawei FRD-L19', 'Huawei FRD-L24', 'Huawei FRD-TL00', 'Huawei PRA-LX1', 'Huawei DUK-L09', 
        'Huawei VEN-L22', 'Huawei JAT-AL00', 'Huawei JAT-L29', 'Huawei JAT-L41', 'Huawei JAT-LX1', 'Huawei JAT-LX3', 
        'Huawei BKK-L21', 'Huawei JSN-L21', 'Huawei JSN-L22', 'Huawei JSN-L23', 'Huawei ARE-L22HN', 'Huawei JSN-L42', 
        'Huawei STF-AL00', 'Huawei STF-AL10', 'Huawei STF-L09', 'Huawei STF-L09S', 'Huawei STF-TL10', 'Huawei LLD-L21', 
        'Huawei LLD-L31', 'Huawei LLD-AL20', 'Huawei M321', 'Huawei HiTV-M1', 'Huawei M311', 'Huawei HUAWEI NTS-AL00', 
        'Huawei NTS-AL00', 'Huawei TNY-AL00', 'Huawei TNY-TL00', 'Huawei RVL-AL09', 'Huawei COR-AL00', 'Huawei COR-AL10', 
        'Huawei COR-L29', 'Huawei COR-TL10', 'Huawei BKL-AL00', 'Huawei BKL-AL20', 'Huawei BKL-TL10', 'Huawei KNT-AL10', 
        'Huawei KNT-AL20', 'Huawei KNT-TL10', 'Huawei KNT-UL10', 'Huawei DUK-AL20', 'Huawei DUK-TL30', 'Huawei BKL-L04', 
        'Huawei BKL-L09', 'Huawei H30-T10', 'Huawei H30-U10', 'Huawei HUAWEI HN3-U00', 'Huawei HUAWEI HN3-U01', 
        'Huawei JAT-AL00', 'Huawei H1711', 'Huawei H1711z', 'Huawei EVR-L29', 'Huawei EVR-TL00', 'Huawei EVR-N29', 
        'Huawei AGS2-L03', 'Huawei AGS2-L09', 'Huawei AGS2-W19', 'Huawei PIC-LX9', 'Huawei ELE-L09', 'Huawei JKM-AL00a', 
        'Huawei STK-L21', 'Huawei EVR-AL00', 'Huawei Comet', 'Huawei Ideos', 'Huawei Ideos', 'Huawei Ice-Twist', 
        'Huawei Huawei U8800-51', 'Huawei IDEOS X5', 'Huawei U8800', 'Huawei U8800-51', 'Huawei H1622', 'Huawei HUAWEI M2-A01L', 
        'Huawei HUAWEI M2-A01W', 'Huawei HUAWEI M2-801L', 'Huawei HUAWEI M2-801W', 'Huawei HUAWEI M2-802L', 'Huawei HUAWEI M2-803L', 
        'Huawei M220', 'Huawei M220c', 'Huawei dTV01', 'Huawei BTV-DL09', 'Huawei BTV-W09', 'Huawei M310', 'Huawei M620', 
        'Huawei TB01', 'Huawei HUAWEI-M835', 'Huawei M860', 'Huawei M865', 'Huawei USCCADR3305', 'Huawei HUAWEI M868', 
        'Huawei RNE-AL00', 'Huawei SNE-AL00', 'Huawei MS4C', 'Huawei HUAWEI MT1-U06', 'Huawei HUAWEI MT2-L01', 
        'Huawei HUAWEI MT2-L02', 'Huawei MT2L03', 'Huawei HUAWEI MT2-L05', 'Huawei MT2L03', 'Huawei HUAWEI MT1-T00', 
        'Huawei ALP-AL00', 'Huawei ALP-L09', 'Huawei ALP-L29', 'Huawei ALP-TL00', 'Huawei BLA-A09', 'Huawei BLA-AL00', 
        'Huawei BLA-L09', 'Huawei BLA-L29', 'Huawei BLA-TL00', 'Huawei RNE-L01', 'Huawei RNE-L03', 'Huawei RNE-L21', 
        'Huawei RNE-L23', 'Huawei HMA-AL00', 'Huawei HMA-L09', 'Huawei HMA-L29', 'Huawei HMA-TL00', 'Huawei LYA-AL00', 
        'Huawei LYA-AL10', 'Huawei LYA-L09', 'Huawei LYA-L29', 'Huawei LYA-TL00', 'Huawei LYA-AL00P', 'Huawei SNE-LX1', 
        'Huawei SNE-LX2', 'Huawei SNE-LX3', 'Huawei HUAWEI MT7-CL00', 'Huawei HUAWEI MT7-J1', 'Huawei HUAWEI MT7-L09', 
        'Huawei HUAWEI MT7-TL00', 'Huawei HUAWEI MT7-TL10', 'Huawei HUAWEI MT7-UL00', 'Huawei HUAWEI NXT-AL10', 
        'Huawei HUAWEI NXT-CL00', 'Huawei HUAWEI NXT-DL00', 'Huawei HUAWEI NXT-L09', 'Huawei HUAWEI NXT-L29', 
        'Huawei HUAWEI NXT-TL00', 'Huawei HUAWEI NXT-TL00B', 'Huawei NXT-AL10', 'Huawei NXT-CL00', 'Huawei NXT-DL00', 
        'Huawei NXT-L09', 'Huawei NXT-L29', 'Huawei NXT-TL00', 'Huawei MHA-AL00', 'Huawei MHA-L09', 'Huawei MHA-L29', 
        'Huawei MHA-TL00', 'Huawei LON-AL00', 'Huawei LON-L29', 'Huawei HUAWEI CRR-CL00', 'Huawei HUAWEI CRR-CL20', 
        'Huawei HUAWEI CRR-L09', 'Huawei HUAWEI CRR-TL00', 'Huawei HUAWEI CRR-UL00', 'Huawei HUAWEI CRR-UL20', 
        'Huawei HUAWEI MT2-C00', 'Huawei HUAWEI MediaPad T1 7.0 3G', 'Huawei T1 7.0', 'Huawei T1-701u', 'Huawei T1-701ua', 
        'Huawei T1-701us', 'Huawei T1-701w', 'Huawei Telpad QS', 'Huawei MediaPad 10 FHD', 'Huawei MediaPad 10 LINK', 
        'Huawei dtab 01', 'Huawei 402HW', 'Huawei MediaPad 10 Link+', 'Huawei S10-232L', 'Huawei SpeedTAB', 'Huawei MediaPad 7 Lite', 
        'Huawei Telpad QS', 'Huawei Telpad Quad S', 'Huawei MediaPad 7 Vogue', 'Huawei MediaPad 7 Youth 2', 'Huawei S7-721u', 
        'Huawei 403HW', 'Huawei CNPC Security Pad S1', 'Huawei HUAWEI MediaPad M1 8.0', 'Huawei MediaPad M1 8.0', 
        'Huawei MediaPad M1 8.0 (LTE)', 'Huawei MediaPad M1 8.0 (WIFI)', 'Huawei S8-303L', 'Huawei S8-303LT', 
        'Huawei S8-306L', 'Huawei BAH-AL00', 'Huawei BAH-L09', 'Huawei BAH-W09', 'Huawei 605HW', 'Huawei 606HW', 
        'Huawei FDR-A05L', 'Huawei FDR-A01L', 'Huawei FDR-A01w', 'Huawei FDR-A03L', 'Huawei BGO-DL09', 'Huawei BGO-L03', 
        'Huawei JDN-AL00', 'Huawei JDN-L01', 'Huawei JDN-W09', 'Huawei BG2-U01', 'Huawei BG2-W09', 'Huawei MediaPad 7 Lite II', 
        'Huawei MediaPad 7 Vogue', 'Huawei 7D-501u', 'Huawei MediaPad X1', 'Huawei MediaPad X1 7.0', 'Huawei X1 7.0', 
        'Huawei MediaPad 7 Youth', 'Huawei MediaPad 7 Vogue', 'Huawei M380-10', 'Huawei Nexus 6P', 'Huawei INE-LX2r', 
        'Huawei VTR-AL00', 'Huawei VTR-L09', 'Huawei VTR-L29', 'Huawei VTR-TL00', 'Huawei VKY-AL00', 'Huawei VKY-L09', 
        'Huawei VKY-L29', 'Huawei VKY-TL00', 'Huawei WAS-L03T', 'Huawei WAS-LX1', 'Huawei WAS-LX1A', 'Huawei WAS-LX2', 
        'Huawei WAS-LX2J', 'Huawei WAS-LX3', 'Huawei HUAWEI P2-6070', 'Huawei EML-AL00', 'Huawei EML-L09', 'Huawei EML-L29', 
        'Huawei EML-TL00', 'Huawei HW-01K', 'Huawei CLT-AL00', 'Huawei CLT-AL00l', 'Huawei CLT-AL01', 'Huawei CLT-L04', 
        'Huawei CLT-L09', 'Huawei CLT-L29', 'Huawei CLT-TL00', 'Huawei CLT-TL01', 'Huawei ANE-LX1', 'Huawei ANE-LX2', 
        'Huawei ANE-LX3', 'Huawei CLT-L09', 'Huawei CLT-L29', 'Huawei HW-02L', 'Huawei VOG-AL00', 'Huawei VOG-AL10', 
        'Huawei VOG-L04', 'Huawei VOG-L09', 'Huawei VOG-L29', 'Huawei VOG-TL00', 'Huawei MAR-LX2J', 'Huawei HUAWEI P6-C00', 
        'Huawei HUAWEI P6-T00', 'Huawei HUAWEI P6-T00V', 'Huawei HUAWEI Ascend P6', 'Huawei HUAWEI P6-U06', 'Huawei HUAWEI P6-U06-orange', 
        'Huawei P6 S-L04', 'Huawei 302HW', 'Huawei HUAWEI P6 S-U06', 'Huawei HUAWEI P7-L00', 'Huawei HUAWEI P7-L05', 
        'Huawei HUAWEI P7-L07', 'Huawei HUAWEI P7-L10', 'Huawei HUAWEI P7-L11', 'Huawei HUAWEI P7-L12', 'Huawei HUAWEI P7 mini', 
        'Huawei HUAWEI P7-L09', 'Huawei HUAWEI GRA-CL00', 'Huawei HUAWEI GRA-CL10', 'Huawei HUAWEI GRA-L09', 
        'Huawei HUAWEI GRA-TL00', 'Huawei HUAWEI GRA-UL00', 'Huawei HUAWEI GRA-UL10', 'Huawei 503HW', 'Huawei ALE-L02', 
        'Huawei ALE-L21', 'Huawei ALE-L23', 'Huawei Autana LTE', 'Huawei HUAWEI ALE-CL00', 'Huawei HUAWEI ALE-L04', 
        'Huawei PRA-LA1', 'Huawei PRA-LX1', 'Huawei ALE-TL00', 'Huawei ALE-UL00', 'Huawei HUAWEI P8max', 'Huawei EVA-AL00', 
        'Huawei EVA-AL10', 'Huawei EVA-CL00', 'Huawei EVA-DL00', 'Huawei EVA-L09', 'Huawei EVA-L19', 'Huawei EVA-L29', 
        'Huawei EVA-TL00', 'Huawei HUAWEI VNS-L52', 'Huawei VIE-AL10', 'Huawei VIE-L09', 'Huawei VIE-L29', 'Huawei HUAWEI VNS-L21', 
        'Huawei HUAWEI VNS-L22', 'Huawei HUAWEI VNS-L23', 'Huawei HUAWEI VNS-L31', 'Huawei HUAWEI VNS-L53', 'Huawei HUAWEI VNS-L62', 
        'Huawei DIG-L03', 'Huawei DIG-L23', 'Huawei PE-CL00', 'Huawei PE-TL00M', 'Huawei PE-TL10', 'Huawei PE-TL20', 
        'Huawei PE-UL00', 'Huawei NEO-AL00', 'Huawei NEO-L29', 'Huawei Prism II', 'Huawei Q22', 'Huawei HUAWEI RIO-CL00', 
        'Huawei MediaPad 10 FHD', 'Huawei MediaPad 10 LINK', 'Huawei MediaPad 7 Vogue', 'Huawei MediaPad 7 Vogue', 
        'Huawei MediaPad 7 Youth', 'Huawei Orinoquia Roraima S7-932u', 'Huawei MediaPad 7 Lite+', 'Huawei Telpad Dual S', 
        'Huawei HUAWEI SC-CL00', 'Huawei HUAWEI SC-UL10', 'Huawei H710VL', 'Huawei H715BL', 'Huawei HUAWEI ATH-UL01', 
        'Huawei HUAWEI ATH-UL06', 'Huawei Huawei_8100-9', 'Huawei Tactile internet', 'Huawei U8100', 'Huawei Videocon_V7400', 
        'Huawei T1-821L', 'Huawei T1-821W', 'Huawei T1-821w', 'Huawei T1-823L', 'Huawei T1-823L', 'Huawei HUAWEI MediaPad T1 10 4G', 
        'Huawei T1-A21L', 'Huawei T1-A21W', 'Huawei T1-A21w', 'Huawei T1-A22L', 'Huawei T1-A23L', 'Huawei T-101', 
        'Huawei T101 PAD', 'Huawei QH-10', 'Huawei T102 PAD', 'Huawei T801 PAD', 'Huawei MT-803G', 'Huawei T802 PAD', 
        'Huawei HUAWEI T8808D', 'Huawei HUAWEI TAG-AL00', 'Huawei HUAWEI TAG-CL00', 'Huawei HUAWEI TAG-TL00', 
        'Huawei Vodafone 845', 'Huawei Pulse', 'Huawei U8220', 'Huawei U8220PLUS', 'Huawei U8230', 'Huawei Huawei-U8652', 
        'Huawei U8652', 'Huawei Huawei-U8687', 'Huawei U8812D', 'Huawei U8832D', 'Huawei U8836D', 'Huawei HUAWEI-U8850', 
        'Huawei HUAWEI-U9000', 'Huawei Y538', 'Huawei Huawei 858', 'Huawei MTC 950', 'Huawei MTC Mini', 'Huawei Vodafone 858', 
        'Huawei MediaPad 7 Classic', 'Huawei MediaPad 7 Lite II', 'Huawei MediaPad 7 Vogue'
        'Huawei LEO-BX9', 'Huawei LEO-DLXX', 'Huawei GEM-701L', 'Huawei GEM-702L', 'Huawei GEM-703L', 
        'Huawei GEM-703LT', 'Huawei Orinoquia Auyantepui Y210', 'Huawei Y220-U00', 'Huawei Y220-U05', 'Huawei Y220-U17', 
        'Huawei HUAWEI Y220-T10', 'Huawei Y220-U10', 'Huawei HUAWEI Y 220T', 'Huawei HUAWEI Y221-U03', 'Huawei ORINOQUIA Auyantepui+Y221-U03', 
        'Huawei HUAWEI Y221-U12', 'Huawei HUAWEI Y221-U22', 'Huawei HUAWEI Y221-U33', 'Huawei HUAWEI Y221-U43', 
        'Huawei HUAWEI Y221-U53', 'Huawei HUAWEI Ascend Y300', 'Huawei HUAWEI Y300-0100', 'Huawei HUAWEI Y300-0151', 
        'Huawei Pelephone-Y300-', 'Huawei HUAWEI Y300-0000', 'Huawei Huawei Y301A1', 'Huawei Huawei Y301A2', 
        'Huawei HUAWEI Y310-5000', 'Huawei HUAWEI Y310-T10', 'Huawei HUAWEI Y320-C00', 'Huawei HUAWEI Y320-T00', 
        'Huawei HUAWEI Y320-U01', 'Huawei Y320-U01', 'Huawei HUAWEI Y320-U10', 'Huawei HUAWEI Y320-U151', 'Huawei HUAWEI Y320-U30', 
        'Huawei HUAWEI Y320-U351', 'Huawei HUAWEI Y321-U051', 'Huawei HUAWEI Y321-C00', 'Huawei HUAWEI Y325-T00', 
        'Huawei Bucare Y330-U05', 'Huawei HUAWEI Y330-U05', 'Huawei HUAWEI Y330-U21', 'Huawei HUAWEI Y330-C00', 
        'Huawei HUAWEI Y330-U01', 'Huawei Luno', 'Huawei HUAWEI Y330-U07', 'Huawei HUAWEI Y330-U08', 'Huawei HUAWEI Y330-U11', 
        'Huawei V8510', 'Huawei HUAWEI Y330-U15', 'Huawei HUAWEI Y330-U17', 'Huawei HUAWEI Y336-A1', 'Huawei HUAWEI Y336-U02', 
        'Huawei HUAWEI Y336-U12', 'Huawei Y340-U081', 'Huawei HUAWEI Y360-U03', 'Huawei HUAWEI Y360-U103', 'Huawei HUAWEI Y360-U12', 
        'Huawei HUAWEI Y360-U23', 'Huawei HUAWEI Y360-U31', 'Huawei HUAWEI Y360-U42', 'Huawei HUAWEI Y360-U61', 
        'Huawei HUAWEI Y360-U72', 'Huawei HUAWEI Y360-U82', 'Huawei Delta Y360-U93', 'Huawei HUAWEI Y360-U93', 
        'Huawei HUAWEI LUA-L01', 'Huawei HUAWEI LUA-L02', 'Huawei HUAWEI LUA-L21', 'Huawei HUAWEI LUA-U02', 'Huawei HUAWEI LUA-U22', 
        'Huawei CRO-U00', 'Huawei CRO-U23', 'Huawei HUAWEI CRO-U00', 'Huawei HUAWEI CRO-U23', 'Huawei HUAWEI Y560-L02', 
        'Huawei HUAWEI Y560-L23', 'Huawei HUAWEI Y560-U03', 'Huawei MYA-AL00', 'Huawei MYA-L02', 'Huawei MYA-L03', 
        'Huawei MYA-L13', 'Huawei MYA-L22', 'Huawei MYA-L23', 'Huawei MYA-TL00', 'Huawei MYA-U29', 'Huawei HUAWEI Y500-T00', 
        'Huawei HUAWEI Y511-T00', 'Huawei Y511-T00', 'Huawei Y511-U00', 'Huawei HUAWEI Y511-U10', 'Huawei HUAWEI Y511-U251', 
        'Huawei HUAWEI Y511-U30', 'Huawei VIETTEL V8506', 'Huawei HUAWEI Y516-T00', 'Huawei HUAWEI Y518-T00', 
        'Huawei HUAWEI Y520-U03', 'Huawei HUAWEI Y520-U12', 'Huawei HUAWEI Y520-U22', 'Huawei HUAWEI Y520-U33', 
        'Huawei HUAWEI Y523-L076', 'Huawei HUAWEI Y523-L176', 'Huawei HUAWEI Y530-U00', 'Huawei HUAWEI Y530', 
        'Huawei HUAWEI Y530-U051', 'Huawei HUAWEI Y535-C00', 'Huawei HUAWEI Y535D-C00', 'Huawei HUAWEI Y536A1', 
        'Huawei HUAWEI Y540-U01', 'Huawei HUAWEI Y541-U02', 'Huawei Y541-U02', 'Huawei Y545-U05', 'Huawei HUAWEI Y550-L01', 
        'Huawei HUAWEI Y550-L02', 'Huawei Y550-L02', 'Huawei HUAWEI Y550', 'Huawei HUAWEI Y550-L03', 'Huawei Personal Huawei Y550', 
        'Huawei Y550-L03', 'Huawei HUAWEI Y560-CL00', 'Huawei HUAWEI Y560-L01', 'Huawei HUAWEI Y560-L03', 'Huawei HUAWEI Y560-U02', 
        'Huawei HUAWEI Y560-U12', 'Huawei HUAWEI Y560-U23', 'Huawei CUN-L22', 'Huawei HUAWEI CUN-L01', 'Huawei HUAWEI CUN-L02', 
        'Huawei HUAWEI CUN-L03', 'Huawei HUAWEI CUN-L21', 'Huawei HUAWEI CUN-L22', 'Huawei HUAWEI CUN-L23', 'Huawei HUAWEI CUN-L33', 
        'Huawei HUAWEI CUN-U29', 'Huawei HUAWEI SCC-U21', 'Huawei SCC-U21', 'Huawei HUAWEI SCL-L01', 'Huawei HUAWEI SCL-L02', 
        'Huawei HUAWEI SCL-L03', 'Huawei HUAWEI SCL-L04', 'Huawei HUAWEI SCL-L21', 'Huawei HW-SCL-L32', 'Huawei SCL-L01', 
        'Huawei HUAWEI SCL-U23', 'Huawei HUAWEI SCL-U31', 'Huawei SCL-U23', 'Huawei MYA-L41', 'Huawei HUAWEI LYO-L02', 
        'Huawei HUAWEI TIT-AL00', 'Huawei HUAWEI TIT-AL00', 'Huawei HUAWEI TIT-CL10', 'Huawei HUAWEI TIT-L01', 
        'Huawei HUAWEI TIT-TL00', 'Huawei TIT-AL00', 'Huawei TIT-L01', 'Huawei HUAWEI TIT-CL00', 'Huawei HUAWEI TIT-U02', 
        'Huawei HUAWEI LYO-L01', 'Huawei HUAWEI Y600-U00', 'Huawei HUAWEI Y600-U151', 'Huawei HUAWEI Y600-U20', 
        'Huawei HUAWEI Y600-U351', 'Huawei HUAWEI Y600-U40', 'Huawei HUAWEI Y600D-C00', 'Huawei HUAWEI Y610-U00', 
        'Huawei HUAWEI Y618-T00', 'Huawei Kavak Y625-U03', 'Huawei HUAWEI Y625-U13', 'Huawei HUAWEI Y625-U21', 
        'Huawei HUAWEI Y625-U32', 'Huawei HUAWEI Y625-U43', 'Huawei HUAWEI Y625-U51', 'Huawei HUAWEI Y635-CL00', 
        'Huawei Y635-L01', 'Huawei HUAWEI Y635-L02', 'Huawei Y635-L02', 'Huawei HUAWEI Y635-L03', 'Huawei Y635-L03', 
        'Huawei Y635-L21', 'Huawei HUAWEI Y635-TL00', 'Huawei Y635-TL00', 'Huawei CAM-L03', 'Huawei CAM-L21', 
        'Huawei CAM-L23', 'Huawei CAM-U22', 'Huawei HUAWEI CAM-L03', 'Huawei HUAWEI CAM-L21', 'Huawei HUAWEI CAM-L23', 
        'Huawei HUAWEI CAM-U22', 'Huawei CAM-L32', 'Huawei HUAWEI LYO-L03', 'Huawei TRT-L21A', 'Huawei TRT-L53', 
        'Huawei TRT-LX1', 'Huawei TRT-LX2', 'Huawei TRT-LX3', 'Huawei DUB-LX1', 'Huawei DUB-AL20', 'Huawei STK-L21', 
        'Huawei STK-L22', 'Huawei STK-LX3', 'Huawei Orinoquia Gran Roraima S7-702u', 'Huawei H1623', 'Huawei d-01G', 
        'Huawei d-01H', 'Huawei d-02H', 'Huawei eH811', 'Huawei HRY-LX1', 'Huawei HRY-LX1MEB', 'Huawei HRY-LX2', 
        'Huawei HRY-AL00', 'Huawei KIW-L22', 'Huawei KIW-L23', 'Huawei KIW-L24', 'Huawei DLI-L42', 'Huawei DIG-L21HN', 
        'Huawei JMM-L22', 'Huawei BLN-L21', 'Huawei BLN-L22', 'Huawei BKK-AL10', 'Huawei BKK-L21', 'Huawei BKK-L22', 
        'Huawei BKK-LX2', 'Huawei HWV31', 'Huawei 204HW', 'Huawei HUAWEI M881', 'Huawei HUAWEI CAN-AL10', 'Huawei HUAWEI CAN-L01', 
        'Huawei HUAWEI CAN-L02', 'Huawei HUAWEI CAN-L03', 'Huawei HUAWEI CAN-L11', 'Huawei HUAWEI CAN-L12', 'Huawei HUAWEI CAN-L13', 
        'Huawei HUAWEI CAZ-AL10', 'Huawei HUAWEI CAZ-AL00', 'Huawei HUAWEI CAZ-AL10', 'Huawei HUAWEI CAZ-TL10', 
        'Huawei HUAWEI CAZ-TL20', 'Huawei PIC-AL00', 'Huawei PIC-TL00', 'Huawei BAC-AL00', 'Huawei BAC-L01', 
        'Huawei BAC-L03', 'Huawei BAC-L23', 'Huawei BAC-TL00', 'Huawei RNE-L02', 'Huawei RNE-L22', 'Huawei HWI-AL00', 
        'Huawei HWI-TL00', 'Huawei PAR-AL00', 'Huawei PAR-L21', 'Huawei PAR-L29', 'Huawei PAR-LX1', 'Huawei PAR-LX1M', 
        'Huawei PAR-LX9', 'Huawei PAR-TL00', 'Huawei PAR-TL20', 'Huawei ANE-AL00', 'Huawei ANE-TL00', 'Huawei INE-AL00', 
        'Huawei INE-LX1', 'Huawei INE-LX1r', 'Huawei INE-LX2', 'Huawei INE-TL00', 'Huawei VCE-AL00', 'Huawei VCE-L22', 
        'Huawei VCE-TL00', 'Huawei MAR-AL00', 'Huawei MAR-TL00', 'Huawei PRA-LX2', 'Huawei PRA-LX3', 'Huawei HUAWEI MLA-L01', 
        'Huawei HUAWEI MLA-L02', 'Huawei HUAWEI MLA-L03', 'Huawei HUAWEI MLA-L11', 'Huawei HUAWEI MLA-L12', 'Huawei HUAWEI MLA-L13', 
        'Huawei MLA-L01', 'Huawei MLA-L02', 'Huawei MLA-L03', 'Huawei MLA-L11', 'Huawei MLA-L12', 'Huawei MLA-L13', 
        'Huawei WAS-AL00', 'Huawei WAS-TL10', 'Huawei MediaPad T1 8.0', 'Huawei S8-701u', 'Huawei S8-701w', 'Huawei HUAWEI MediaPad T1 8.0 4G', 
        'Huawei Honor T1 8.0', 'Huawei MediaPad T1 8.0 Pro', 'Huawei S8-821w', 'Huawei T1-821w', 'Huawei T1-823L', 
        'Huawei HUAWEI VNS-DL00', 'Huawei HUAWEI VNS-TL00', 'Huawei BZT-AL00', 'Huawei BZT-AL10', 'Huawei BZT-W09', 
        'Huawei BZW-AL00', 'Huawei BZW-AL10', 'Huawei MON-AL19', 'Huawei MON-AL19B', 'Huawei MON-W19', 'Huawei BAH2-AL00', 
        'Huawei BAH2-AL10', 'Huawei BAH2-W09', 'Huawei JDN2-AL00', 'Huawei JDN2-W09', 'Huawei BZK-L00', 'Huawei BZK-W00', 
        'Huawei PLE-701L', 'Huawei PLE-703L', 'Huawei DRA-AL00', 'Huawei DRA-TL00', 'Huawei POT-AL00a', 'Huawei POT-TL00a', 
        'Huawei MRD-AL00', 'Huawei MRD-TL00', 'Huawei ARS-AL00', 'Huawei ARS-TL00', 'Huawei STK-AL00', 'Huawei STK-TL00', 
        'Huawei NCE-AL00', 'Huawei NCE-AL10', 'Huawei NCE-TL10', 'Huawei DIG-AL00', 'Huawei DIG-TL10', 'Huawei SLA-AL00', 
        'Huawei SLA-TL10', 'Huawei FIG-AL00', 'Huawei FIG-AL10', 'Huawei FIG-TL00', 'Huawei FIG-TL10', 'Huawei LDN-AL00', 
        'Huawei LDN-AL10', 'Huawei LDN-AL20', 'Huawei LDN-TL00', 'Huawei LDN-TL10', 'Huawei LDN-TL20', 'Huawei FLA-AL00', 
        'Huawei FLA-AL10', 'Huawei FLA-AL20', 'Huawei FLA-TL00', 'Huawei FLA-TL10', 'Huawei ATU-AL10', 'Huawei ATU-TL10', 
        'Huawei DUB-AL00', 'Huawei DUB-AL00a', 'Huawei DUB-AL20', 'Huawei DUB-TL00', 'Huawei DUB-TL00a', 'Huawei JKM-AL00', 
        'Huawei JKM-TL00', 'Huawei JKM-AL00a', 'Huawei JKM-AL00b', 'Huawei AGS2-AL00', 'Huawei JSN-AL00', 'Huawei JSN-TL00', 
        'Huawei JSN-AL00a', 'Huawei JMM-AL00', 'Huawei JMM-AL10', 'Huawei JMM-TL00', 'Huawei JMM-TL10', 'Huawei HRY-TL00', 
        'Huawei HRY-AL00T', 'Huawei HRY-TL00T', 'Huawei SCL-AL00', 'Huawei KIW-AL10', 'Huawei KIW-AL20', 'Huawei KIW-CL00', 
        'Huawei KIW-TL00', 'Huawei KIW-UL00', 'Huawei ARE-AL00', 'Huawei ARE-TL00', 'Huawei ARE-AL10', 'Huawei PRA-AL00', 
        'Huawei PRA-AL00X', 'Huawei PRA-TL10', 'Huawei HLK-AL00', 'Huawei LLD-AL20', 'Huawei LLD-AL30', 'Huawei LLD-AL00', 
        'Huawei LLD-AL10', 'Huawei LLD-TL10', 'Huawei EDI-AL10', 'Huawei EDI-DL00', 'Huawei HDL-AL09', 'Huawei HDL-W09', 
        'Huawei AGS2-AL00HN', 'Huawei AGS2-W09HN', 'Huawei JDN2-AL00HN', 'Huawei JDN2-W09HN', 'Huawei TRT-AL00', 
        'Huawei TRT-AL00A', 'Huawei TRT-TL10', 'Huawei TRT-TL10A', 'Huawei BLN-AL10', 'Huawei BLN-AL20', 'Huawei BLN-AL30', 
        'Huawei BLN-AL40', 'Huawei BLN-TL00', 'Huawei BLN-TL10', 'Huawei CHM-TL00', 'Huawei CHM-TL00H', 'Huawei CHM-UL00', 
        'Huawei CHE-TL00', 'Huawei CHE-TL00H', 'Huawei CAM-TL00', 'Huawei CAM-TL00H', 'Huawei CAM-UL00', 'Huawei CAM-AL00', 
        'Huawei CAM-CL00', 'Huawei CAM-TL00', 'Huawei CAM-TL00H', 'Huawei CAM-UL00', 'Huawei CAM-AL00', 'Huawei NEM-AL10', 
        'Huawei NEM-TL00', 'Huawei NEM-TL00H', 'Huawei NEM-UL10', 'Huawei MYA-AL10', 'Huawei MYA-TL10', 'Huawei DLI-AL10', 
        'Huawei DUA-AL00', 'Huawei DUA-TL00', 'Huawei BND-AL00', 'Huawei BND-AL10', 'Huawei BND-TL10', 'Huawei KSA-AL00', 
        'Huawei KSA-TL00', 'Huawei JAT-AL00', 'Huawei JAT-TL00', 'Huawei BKK-AL00', 'Huawei BKK-AL10', 'Huawei BKK-TL00', 
        'Huawei BZA-L00', 'Huawei BZA-W00', 'Huawei POT-AL00', 'Huawei POT-AL10', 'Huawei HUAWEI RIO-AL00', 'Huawei HUAWEI MLA-AL00', 

        'Xiaomi MiProjL1', 'Xiaomi HM 1AC', 'Xiaomi HM 1S', 'Xiaomi HM 1SC', 'Xiaomi HM 1SW', 
        'Xiaomi 2014501', 'Xiaomi 2014011', 'Xiaomi 2014502', 'Xiaomi HM 2A', 'Xiaomi 2014819', 'Xiaomi 2014813', 
        'Xiaomi 2014812', 'Xiaomi 2014811', 'Xiaomi 2014818', 'Xiaomi 2014817', 'Xiaomi HM NOTE 1LTE', 'Xiaomi HM NOTE 1LTETD', 
        'Xiaomi HM NOTE 1LTEW', 'Xiaomi HM NOTE 1S', 'Xiaomi gucci', 'Xiaomi HM NOTE 1TD', 'Xiaomi HM NOTE 1W', 
        'Xiaomi Redmi Note 2', 'Xiaomi 2013022', 'Xiaomi Redmi K30 Pro 5G Zoom Edition', 'Xiaomi Redmi K30 Pro 5G', 
        'Xiaomi MI 8 Explorer Edition', 'Xiaomi MI 8 Pro', 'Xiaomi MI 8 UD', 'Xiaomi MI MAX 3', 'Xiaomi MI PLAY', 
        'Xiaomi lotus', 'Xiaomi Mi 10', 'Xiaomi MI 2', 'Xiaomi MI 2S', 'Xiaomi MI 2A', 'Xiaomi MI 3W', 'Xiaomi MI 4C', 
        'Xiaomi MI 4LTE', 'Xiaomi MI 4W', 'Xiaomi MI 4LTE', 'Xiaomi MI 4S', 'Xiaomi MI 5C', 'Xiaomi Meri', 'Xiaomi MI 5X', 
        'Xiaomi MI 5s Plus', 'Xiaomi MI 6X', 'Xiaomi MI 8', 'Xiaomi MI 8 Lite', 'Xiaomi Platina', 'Xiaomi MI 8 SE', 
        'Xiaomi sirius', 'Xiaomi MI 8 Pro', 'Xiaomi MI 8 UD', 'Xiaomi equuleus', 'Xiaomi MI 9', 'Xiaomi MI 9 SE', 
        'Xiaomi Mi 9 SE', 'Xiaomi MI CC 9', 'Xiaomi Mi 9 Lite', 'Xiaomi Pyxis', 'Xiaomi MI CC 9e', 'Xiaomi laurus', 
        'Xiaomi MI CC9 Pro', 'Xiaomi Mi Note 10', 'Xiaomi MI MAX', 'Xiaomi MI MAX', 'Xiaomi MI MAX 2', 'Xiaomi MI MAX 3', 
        'Xiaomi Mi MIX 2S', 'Xiaomi MI NOTE LTE', 'Xiaomi MI NOTE Pro', 'Xiaomi Mi Note 3', 'Xiaomi MI PAD', 
        'Xiaomi MI PAD 3', 'Xiaomi MI PAD 4', 'Xiaomi MI PLAY', 'Xiaomi MI 6', 'Xiaomi MiBOX_PRO', 'Xiaomi MI PAD 2', 
        'Xiaomi MIX', 'Xiaomi lithium', 'Xiaomi MIX 2', 'Xiaomi Mi MIX 2', 
        'Xiaomi MIX 2S', 'Xiaomi Mi MIX 2S', 'Xiaomi MIX 3', 'Xiaomi Mi MIX 3', 'Xiaomi Mi 10', 'Xiaomi Umi', 
        'Xiaomi XIG01', 'Xiaomi M2002J9E', 'Xiaomi Cmi', 'Xiaomi Mi 10 Pro', 'Xiaomi M2007J1SC', 'Xiaomi M2002J9G', 
        'Xiaomi M2002J9S', 'Xiaomi M2102J2SC', 'Xiaomi Thyme', 'Xiaomi M2007J3SP', 'Xiaomi M2007J3SY', 'Xiaomi M2007J17G', 
        'Xiaomi M2007J3SG', 'Xiaomi M2007J3SI', 'Xiaomi M2007J17I', 'Xiaomi M2011K2C', 'Xiaomi M2011K2G', 'Xiaomi M2101K9AG', 
        'Xiaomi M2101K9C', 'Xiaomi M2101K9G', 'Xiaomi M2102K1AC', 'Xiaomi M2102K1C', 'Xiaomi M2102K1G', 'Xiaomi MI 3', 
        'Xiaomi Mi-4c', 'Xiaomi Mi 4i', 'Xiaomi MI 5', 'Xiaomi MI 5s', 'Xiaomi Mi 9 Lite', 'Xiaomi MI 9 SE', 
        'Xiaomi Mi 9 SE', 'Xiaomi Mi 9T', 'Xiaomi Mi 9T Pro', 'Xiaomi MI A1', 'Xiaomi Mi A1', 'Xiaomi Mi A2', 
        'Xiaomi Mi A2 Lite', 'Xiaomi Mi A3', 'Xiaomi MIBOX3', 'Xiaomi MiProjA1', 'Xiaomi MiProjL1', 'Xiaomi Mi MIX 3 5G', 
        'Xiaomi MI NOTE LTE', 'Xiaomi Mi Note 10', 'Xiaomi Mi Note 10 Lite', 'Xiaomi toco', 'Xiaomi Mi Note 2', 
        'Xiaomi MiTV-AESP0', 'Xiaomi MiProjM05', 'Xiaomi Mi9 Pro 5G', 'Xiaomi MiBOX1S', 'Xiaomi MiBOX2', 'Xiaomi MiBOX3S', 
        'Xiaomi MiBOX_mini', 'Xiaomi MIBOX4', 'Xiaomi MiTV-MSSP0', 'Xiaomi MiTV-MOOQ0', 'Xiaomi MiTV-AXSO0', 
        'Xiaomi MiTV-AXSO1', 'Xiaomi MiTV-AXSO2', 'Xiaomi MiTV-MSSP3', 'Xiaomi MiTV4I', 'Xiaomi MiTV-MSSP1', 
        'Xiaomi MiTV-MOOQ1', 'Xiaomi MiTV-MSSP2', 'Xiaomi MiTV2', 'Xiaomi MiTV4C', 'Xiaomi POCOPHONE F1', 'Xiaomi 2013023', 
        'Xiaomi Redmi Go', 'Xiaomi Redmi Note 6 Pro', 'Xiaomi Redmi Note 7 Pro', 'Xiaomi Redmi S2', 'Xiaomi Redmi 3', 
        'Xiaomi ido', 'Xiaomi Redmi 3S', 'Xiaomi Redmi 4', 'Xiaomi Redmi 4', 'Xiaomi Redmi 4A', 'Xiaomi Redmi 4X', 
        'Xiaomi santoni', 'Xiaomi Redmi 5', 'Xiaomi Redmi 5 Plus', 'Xiaomi Redmi Note 5', 'Xiaomi Redmi 5A', 
        'Xiaomi Redmi 6', 'Xiaomi Redmi 6 Pro', 'Xiaomi Redmi 6A', 'Xiaomi Redmi 6 Pro', 'Xiaomi ONC', 'Xiaomi Redmi 7', 
        'Xiaomi Redmi 7A', 'Xiaomi Redmi 8', 'Xiaomi Redmi Go', 'Xiaomi Redmi K30 Pro Zoom Edition', 'Xiaomi Redmi Note 3', 
        'Xiaomi Redmi Note 3', 'Xiaomi Redmi Note 3', 'Xiaomi Redmi Note 4', 'Xiaomi Redmi Note 4X', 'Xiaomi Redmi Note 4', 
        'Xiaomi Redmi Note 5', 'Xiaomi Redmi Note 5', 'Xiaomi Redmi Note 5 Pro', 'Xiaomi Redmi Note 5A', 'Xiaomi Redmi Y1', 
        'Xiaomi Redmi Note 5A', 'Xiaomi Redmi Note 8', 'Xiaomi Redmi Pro', 'Xiaomi Redmi S2', 'Xiaomi MIBOX3',
    ]

    system_versions = [
        "SDK 23", "SDK 24", "SDK 25", "SDK 26", "SDK 27", "SDK 28", "SDK 29", "SDK 30", "SDK 31"
    ]

    deviceList : List[DeviceInfo] = []

    @classmethod
    def __gen__(cls : Type[AndroidDevice]) -> None:
        
        if len(cls.deviceList) == 0:


            results : List[DeviceInfo]= []
            
            for model in cls.device_models:
                for version in cls.system_versions:
                    results.append(DeviceInfo(model, version))

            cls.deviceList = results


class iOSDeivce(SystemInfo):
    
    device_models = {
        5:  ["S"],
        6:  [" Plus", "", "S", "S Plus"],
        7:  ["", " Plus"],
        8:  ["", " Plus"],
        10: ["", "S", "S Max", "R"],
        11: ["", " Pro", " Pro Max"],
        12: [" mini", "", " Pro", " Pro Max"],
        13: [" Pro", " Pro Max", " Mini", ""],
    }

    system_versions : Dict[int, Dict[int, List[int]]] = {
        15: {2: [], 1: [1], 0: [2, 1]},
        14: {8: [1], 7: [1], 6: [], 5: [1], 4: [2, 1], 3: [], 2: [1], 1: [], 0: [1]},
        13: {7: [], 6: [1], 5: [1], 4: [1], 3: [1], 2: [3, 2], 1: [3, 2, 1]},
        12: {
            5: [5, 4, 3, 2, 1],
            4: [9, 8, 7, 6, 5, 4, 3, 2, 1],
            3: [2, 1],
            11: [0],
            2: [],
            1: [4, 3, 2, 1],
            0: [1],
        }
    }

    deviceList : List[DeviceInfo] = []

    @classmethod
    def __gen__(cls : Type[iOSDeivce]) -> None:
        
        if len(cls.deviceList) == 0:   
            results : List[DeviceInfo]= []

            # ! SHITTY CODE BECAUSE I HAD TO CHECK FOR THE RIGHT VERSION
            for id_model in cls.device_models:
                if id_model == 13:
                    available_versions = [15]
                elif id_model == 12:
                    available_versions = [14, 15]
                elif id_model == 11:
                    available_versions = [13, 14, 15]
                elif id_model == 5:
                    available_versions = [12]
                else:
                    available_versions = [12, 13, 14, 15]
                
                for model_name in cls.device_models[id_model]:
                    
                    if id_model == 10: id_model = "X"
                    device_model = f"iPhone {id_model}{model_name}"

                    for major in available_versions:
                        for minor, patches in cls.system_versions[major].items():

                            if len(patches) == 0:
                                results.append(DeviceInfo(device_model, f"{major}.{minor}"))
                            else:
                                for patch in patches:
                                    results.append(DeviceInfo(device_model, f"{major}.{minor}.{patch}"))

            cls.deviceList = results
