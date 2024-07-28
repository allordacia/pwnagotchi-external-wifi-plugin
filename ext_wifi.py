import pwnagotchi.plugins as plugins
import logging
import subprocess

class ext_wifi(plugins.Plugin):
    __author__ = 'chris@holycityhosting.com'
    __version__ = '1.2.0'
    __license__ = 'GPL3'
    __description__ = 'Activates external wifi adapter'

    def __init__(self):
        self.ready = 0
        self.status = ''
        self.network = ''

    def on_loaded(self):
        required_options = ['mode', 'interface', 'internal_interface']
        for opt in required_options:
            if opt not in self.options or self.options[opt] is None:
                logging.error(f"Set WiFi adapter {opt} configuration.")
                return
        
        _log("Plugin loaded")
        self.ready = 1
        mode = self.options['mode']
        interface = self.options['interface']
        internal_interface = self.options['internal_interface']
        
        if mode == "external":
            self._activate_external(interface)
        else:
            self._activate_internal(internal_interface)
        
        self._reset_services()

    def _activate_external(self, interface):
        files_to_update = [
            '/usr/bin/bettercap-launcher',
            '/usr/local/share/bettercap/caplets/pwnagotchi-auto.cap',
            '/usr/local/share/bettercap/caplets/pwnagotchi-manual.cap',
            '/etc/pwnagotchi/config.toml',
            '/usr/bin/pwnlib'
        ]
        for file in files_to_update:
            self._replace_in_file(file, 'mon0', interface)
        _log("External adapter activated")

    def _activate_internal(self, internal_interface):
        files_to_update = [
            '/usr/bin/bettercap-launcher',
            '/usr/local/share/bettercap/caplets/pwnagotchi-auto.cap',
            '/usr/local/share/bettercap/caplets/pwnagotchi-manual.cap',
            '/etc/pwnagotchi/config.toml',
            '/usr/bin/pwnlib'
        ]
        for file in files_to_update:
            self._replace_in_file(file, 'mon0', internal_interface)
        _log("Internal adapter activated")

    def _replace_in_file(self, filepath, old, new):
        try:
            subprocess.run(f'sed -i s/{old}/{new}/g {filepath}', shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to update {filepath}: {e}")

    def _reset_services(self):
        services_to_restart = [
            'bettercap',
            'pwnagotchi'
        ]
        for service in services_to_restart:
            try:
                subprocess.run(f'systemctl restart {service}', shell=True, check=True)
                _log(f"Service {service} restarted")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to restart service {service}: {e}")

def _log(message):
    logging.info(f'[ext_wifi] {message}')
