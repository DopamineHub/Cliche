import datetime
import json
import os
import uuid


def parse_scripts(lines):
    imports = {}
    scripts = []
    cur_script_name = ''
    cur_script_uuid = None
    cur_script_desc = ''
    cur_script_code = []
    cur_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for ln in lines:
        ln = ln.strip('\n')
        if ln.startswith('def '):
            # new function found
            if cur_script_name:
                scripts.append({
                    'uuid': cur_script_uuid or str(uuid.uuid1()),
                    'target': 'Django-3',
                    'app': None,
                    'name': cur_script_name,
                    'description': cur_script_desc,
                    'imports': imports,
                    'parameters': {
                        'request': 'HttpRequest',
                        'options': 'dict',
                    },
                    'code': '\n'.join(cur_script_code),
                    'created_time': cur_time,
                    'modified_time': cur_time,
                })
                cur_script_uuid = None
            cur_script_name = ln.split('(')[0].split()[1]
            cur_script_desc = ''
            cur_script_code = []

        elif ln.startswith('from '):
            import_tokens = ln.split()
            import_tokens = [
                tk for tk in import_tokens if
                tk not in ['from', 'import']
            ]
            imports[import_tokens[1]] = import_tokens[0]

        elif ln.startswith('    ') and cur_script_name:
            ln = ln[4:]
            if (
                    ln.startswith('"""') and
                    ln.endswith('"""')
            ):
                ln = ln.strip(' "')
                if ln.startswith('desc:'):
                    cur_script_desc = ln[len('desc:'):].strip()
                elif ln.startswith('uuid:'):
                    cur_script_uuid = ln[len('uuid:'):].strip()
            else:
                cur_script_code.append(ln)

        elif ln.startswith('#'):
            pass  # do nothing
            # ln = ln[1:].strip(' -')
            # cur_script_uuid = str(uuid.UUID(ln)) if ln else None

        elif len(ln) != 0:
            raise AssertionError('unknown line')

    if cur_script_name:
        scripts.append({
            'uuid': cur_script_uuid or str(uuid.uuid1()),
            'target': 'Django-3',
            'app': None,
            'name': cur_script_name,
            'description': cur_script_desc,
            'imports': imports,
            'parameters': {
                'request': 'HttpRequest',
                'options': 'dict',
            },
            'code': '\n'.join(cur_script_code),
            'created_time': cur_time,
            'modified_time': cur_time,
        })

    return scripts


if __name__ == '__main__':
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    target_models = []
    target_require = os.path.join(cur_dir, 'requirements.json')
    target_desc = os.path.join(cur_dir, 'description.md')
    target_code = os.path.join(cur_dir, 'code.py')
    target_scripts = os.path.join(cur_dir, 'scripts.py')

    target_fields = {}

    with open(target_require, 'r') as f:
        target_fields['requirements'] = json.load(f)

    with open(target_desc, 'r') as f:
        target_fields['description'] = f.read()

    with open(target_code, 'r') as f:
        target_fields['code'] = f.read()

    target_models.append({
        'model': 'cliche_builders.ClicheBuildTarget',
        'pk': 'Django-3',
        'fields': target_fields,
    })

    with open(target_scripts, 'r') as f:
        scripts_lines = f.readlines()

    for fields in parse_scripts(scripts_lines):
        target_models.append({
            'model': 'cliche_scripts.ClicheScript',
            'pk': None,
            'fields': fields,
        })

    with open(os.path.join(cur_dir, 'dist.json'), 'w+') as f:
        f.write(json.dumps(target_models))
