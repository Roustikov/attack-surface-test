from neomodel import (
    StructuredNode,
    ArrayProperty,
    StringProperty,
    NeomodelException,
    RelationshipTo,
    StructuredRel
    )


class FwRuleRel(StructuredRel):
    fw_id = StringProperty()
    source_tag = StringProperty()
    destination_tag = StringProperty()


class VM(StructuredNode):
    vm_id = StringProperty()
    name = StringProperty()
    tags = ArrayProperty(StringProperty())
    inbound_rules = RelationshipTo('VM', 'CONNECTS_TO', model=FwRuleRel)

    def apply_fw_rule(self, fw_rule):
        try:
            dest_vms = (
                vm for vm in VM.nodes if fw_rule['dest_tag'] in vm.tags)
            for dest_vm in dest_vms:
                self.inbound_rules.connect(dest_vm, {
                    'fw_id': fw_rule['fw_id'],
                    'source_tag': fw_rule['source_tag'],
                    'destination_tag': fw_rule['dest_tag']})
            return self
        except Exception as e:
            raise NeomodelException(
                f'Error occurred while applying firewall rule. {e}')
