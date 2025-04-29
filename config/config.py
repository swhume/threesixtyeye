"""
config.py loads the configuration settings for the 360i programs from config.ini
"""
import configparser
from pathlib import Path
import logging

class AppSettings:
    """
    Provides the configuration settings for the 360i code. Loads the settings from config.ini
    """
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        config = configparser.ConfigParser()
        config_file = self._get_config_file()
        config.read(config_file)
        self.gh_token_raw_data = None
        self.gh_user_name_raw_data = None
        self.gh_repo_name_raw_data = None
        self.gh_repo_path_raw_data = None
        self.api_key = None
        self.base_url = None
        self.study_oid = None
        if config.has_section('RawDataSource'):
            self.gh_token_raw_data = config.get(section='RawDataSource', option='gh_token')
            self.gh_user_name_raw_data = config.get(section='RawDataSource', option='gh_user_name')
            self.gh_repo_name_raw_data = config.get(section='RawDataSource', option='gh_repo_name')
            self.gh_repo_path_raw_data = config.get(section='RawDataSource', option='gh_repo_path')
        if config.has_section('DSJAPI'):
            if config.has_option('DSJAPI', 'api_key'):
                self.api_key = config.get('DSJAPI', 'api_key')
            if config.has_option('DSJAPI', 'base_url'):
                self.base_url = config.get('DSJAPI', 'base_url')
        if config.has_section('Study'):
            if config.has_option('Study', 'study_oid'):
                self.study_oid = config.get('Study', 'study_oid')
        self.data_path = config.get('Data', 'data_path')
        if config.has_section('LinkML'):
            if config.has_option('LinkML', 'ndjson_linkml_yaml'):
                self.ndjson_linkml = config.get('LinkML', 'ndjson_linkml_yaml')
        if config.has_section('Commands'):
            if config.has_option('Commands', 'python'):
                self.python_command = config.get('Commands', 'python')
        if config.has_section('SourceSystem'):
            if config.has_option('SourceSystem', 'name'):
                self.source_system_name = config.get('SourceSystem', 'name')
            if config.has_option('SourceSystem', 'version'):
                self.source_system_version = config.get('SourceSystem', 'version')
        if config.has_section('Schema'):
            if config.has_option('Schema', 'odm132'):
                self.odm132_schema = config.get('Schema', 'odm132')
            if config.has_option('Schema', 'define20'):
                self.define20_schema = config.get('Schema', 'define20')


    def _get_config_file(self) -> str:
        """
        Gets the path to the configuration file 'config.ini' and checks if the file exists.
        :raises Exception: If 'config.ini' is not found; the application is unable to cannot proceed without it.
        :return: The absolute path to the 'config.ini' configuration file.
        """
        config_file =  Path(__file__).parent.joinpath("config.ini")
        if not Path(config_file).absolute().exists():
            self.logger.error(f"360i {config_file} file not found. You cannot continue without the config.ini file.")
            raise Exception("config.ini file not found. You cannot continue with the config.ini file.")
        return config_file
