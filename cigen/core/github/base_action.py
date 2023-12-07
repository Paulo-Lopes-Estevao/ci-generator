def base_action(name, on, steps):
    action_base = {
        'name': name,
        "on": on,
        'jobs': {
            'build': {
                'name': 'Build',
                'runs-on': 'ubuntu-latest',
                'steps': steps.to_dict()
            }
        }
    }
    return order_json(action_base, ['name', 'on', 'jobs'])


def base_version_list_action(name, on, steps, version):
    # :TODO: add option to choose version setup and others actions

    matrix = strategies_matrix('v4', version, steps)

    action_base = {
        'name': name,
        'on': on,
        'jobs': {
            'build': {
                'name': 'Build',
                'runs-on': 'ubuntu-latest',
                'strategy': matrix,
                'steps': steps.to_dict()
            }
        }
    }
    return order_json(action_base, ['name', 'on', 'jobs'])


def strategies_matrix(version_setup, version_list, step_actions_setup):
    action_setup = step_actions_setup.to_dict()[1]['uses']

    if version_setup is None:
        version_setup = "v4"

    node = 'actions/setup-node@' + version_setup
    go = 'actions/setup-go@' + version_setup
    python = 'actions/setup-python@' + version_setup

    matrices = {
        node: {
            'matrix':
                {
                    'node-version': matrix_node(version_list)
                },
        },
        go: {
            'matrix': {
                'go-version': matrix_go(version_list)
            }
        },
        python: {
            'matrix': {
                'python-version': matrix_python(version_list)
            }
        }
    }

    return matrices[action_setup]


def matrix_node(version_list):
    if version_list == [] or version_list == "" or version_list is None:
        version_list = ['14.x', '15.x']
    return version_list


def matrix_go(version_list):
    if version_list == [] or version_list == "" or version_list is None:
        version_list = ['1.19', '1.20', '1.21.x']
    return version_list


def matrix_python(version_list):
    if version_list == [] or version_list == "" or version_list is None:
        version_list = ['3.8', '3.9']
    return version_list


def order_json(json_obj, ordem):
    ordered_json = {key: json_obj[key] for key in ordem if key in json_obj}

    remaining_keys = [key for key in json_obj if key not in ordem]
    ordered_json.update({key: json_obj[key] for key in remaining_keys})

    for key, value in ordered_json.items():
        if isinstance(value, dict):
            ordered_json[key] = order_json(value, ordem)
        elif isinstance(value, list):
            ordered_json[key] = [order_json(item, ordem) if isinstance(item, dict) else item for item in value]

    return ordered_json
