import os
from configobj import ConfigObj

# 配置文件
cfg_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), "config.ini")
config = ConfigObj(cfg_file, encoding='UTF8')


class SettingsUtils:
    """
    读取项目配置文件
    """
    @staticmethod
    def get_val(section, key):
        """
        根据section和key获取值
        :param section: ini文件中section
        :param key: ini文件中key
        :return: 对应值
        """
        return config[section][key]


class CommonConfig:
    websocket_port = SettingsUtils.get_val('env', 'websocket_port')
    rtsp_url = SettingsUtils.get_val('env', 'rtsp_url')
