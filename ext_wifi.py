import pwnagotchi.plugins as plugins
import logging
import subprocess

class ext_wifi(plugins.Plugin):
    __author__ = 'Allordacia'
    __version__ = '1.2.0'
    __license__ = 'GPL3'
    __description__ = 'Activates external wifi adapter'

    def __init__(self):
        self.ready = 0
        self.status = ''
        self.network = ''

    def on_loaded(self):
        try:
            mode = self.options.get('mode')
            interface = self.options.get('interface')
            internal_interface = self.options.get('internal_interface')

            if not mode:
                logging.error("Set WiFi adapter mode configuration.")
                return
            if not interface:
                logging.error("Set WiFi adapter interface configuration.")
                return
            if not internal_interface:
                logging.error("Set WiFi adapter internal_interface configuration.")
                return

            _log("Plugin loaded")
            self.ready = 1

            if mode == "external":
                self._activate_external(interface)
            elif mode == "internal":
                self._activate_internal(internal_interface)

            self._notify_reboot_needed()

        except Exception as e:
            logging.error(f"Error during plugin loading: {e}")

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

    def _notify_reboot_needed(self):
        _log("Changes applied. Please reboot your Pwnagotchi for changes to take effect.")

def _log(message):
    logging.info(f'[ext_wifi] {message}')
