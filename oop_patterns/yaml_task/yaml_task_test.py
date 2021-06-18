from yaml_task import *
import yaml


# def easy_level_constructor(loader, node):
#     data = loader.construct_mapping(node)
#     _map = EasyLevel.Map()
#     _obj = EasyLevel.Objects()
#     _obj.config = data
#     return {'map': _map, 'obj': _obj}
#
#
# def medium_level_constructor(loader, node):
#     data = loader.construct_mapping(node)
#     _map = MediumLevel.Map()
#     _obj = MediumLevel.Objects()
#     _obj.config = data
#     return {'map': _map, 'obj': _obj}
#
#
# def hard_level_constructor(loader, node):
#     data = loader.construct_mapping(node)
#     _map = HardLevel.Map()
#     _obj = HardLevel.Objects()
#     _obj.config = data
#     return {'map': _map, 'obj': _obj}
#
#
# loader = yaml.Loader
# loader.add_constructor('!easy_level', easy_level_constructor)
# loader.add_constructor('!medium_level', medium_level_constructor)
# loader.add_constructor('!hard_level', hard_level_constructor)


Levels = yaml.load(
    '''
levels:
    - !easy_level {}
    - !medium_level
        enemy: ['rat']
    - !hard_level
        enemy:
            - rat
            - snake
            - dragon
        enemy_count: 10
''')
print(Levels)
print(Levels['levels'][0]['obj'].config)
print(Levels['levels'][1]['obj'].config)
print(Levels['levels'][2]['obj'].config)

Levels2 = {'levels': []}
_map = EasyLevel.Map()
_obj = EasyLevel.Objects()
Levels2['levels'].append({'map': _map, 'obj': _obj})

_map = MediumLevel.Map()
_obj = MediumLevel.Objects()
_obj.config = {'enemy': ['rat']}
Levels2['levels'].append({'map': _map, 'obj': _obj})

_map = HardLevel.Map()
_obj = HardLevel.Objects()
_obj.config = {'enemy': ['rat', 'snake', 'dragon'], 'enemy_count': 10}
Levels2['levels'].append({'map': _map, 'obj': _obj})

print(Levels2)
print(Levels2['levels'][0]['obj'].config)
print(Levels2['levels'][1]['obj'].config)
print(Levels2['levels'][2]['obj'].config)
