import json
import os
import logging
from api.models import VM
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Loads json from json_data directory by file name'

    def handle(self, *args, **kwargs):
        try:
            self.clean_vms()
            file_path = f'{os.getenv("JSON_DATA_PATH")}'
            logging.info(f"Parsing VM json file: {file_path}")
            with open(file_path, 'r') as cloud_env_json:
                cloud_env_object = json.load(cloud_env_json)
                self.populate_vms(cloud_env_object['vms'])
                self.apply_vm_rules(cloud_env_object['fw_rules'])
        except Exception as e:
            raise CommandError(f'Error occurred while parsing VM json: {e}')

        logging.info("Successfully parsed VM json file")

    def clean_vms(self):
        logging.info("Purging the DB before populating")
        for node in VM.nodes.all():
            node.delete()
        logging.info("Successfully purged the DB")

    def populate_vms(self, vms):
        logging.info("Populating VMs from json file")
        for vm in vms:
            new_vm = VM(vm_id=vm['vm_id'], name=vm['name'], tags=vm['tags'])
            new_vm.save()
        logging.info("Successfully populated VMs from json file")

    def apply_vm_rules(self, rules):
        logging.info("Applying firewall rules from json file")
        for fw_rule in rules:
            vms = (vm for vm in VM.nodes if fw_rule['source_tag'] in vm.tags)
            for vm in vms:
                vm.apply_fw_rule(fw_rule)
                vm.save()
        logging.info("Successfully applied firewall rules from json file")
