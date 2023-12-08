# GitHub Action Command Nodejs Example

help command for github-actions subcommand

```bash
cigen github-actions --help
```

nodejs command for github-actions subcommand

```bash
cigen github-actions nodejs --help
```

output:

```bash
Options:
  -n, --name TEXT         Name of the action  [required]
  -b, --branch_name TEXT  Branch to add  [required]
  -a, --action TEXT       Action to add  [required]
  -v, --version TEXT      Version of nodejs [default=16]
  --help                  Show this message and exit.
```

Options:
> **-n, --name**: required 1 parameter!

Types:
- param: -n myproject
- prompt [Name of the action]: myproject

> **-b, --branch_name**: required 2 parameters!

Types:
- param: -b push main,master
- prompt [Name of the branch]: push main,master


> **-a, --action**: at least 1 parameter is required!

Types:
- param: -a 1
- prompt [Action to add]: 1

**_ACTION_OPTIONAL** - if flag after the value 1 or 2 is [optional] the last value after is a base action of a simple code.
                    The action 1 or 2 cannot be followed by any value separated by a comma. the last parameter is [optional] base.

                    Example: 1 or 2 - is valid
                    Example: 1 0 or 2 1 - is valid, ignore the last value
                    Example: 1,2 0 or 2,3 1 - is invalid, comma is not allowed



**_ACTION_REQUIRED** - if flag is different from 1 or 2 the last value after is a [required] action of a simple code.
                    The action must follow the list and must use the last value separated by the space indicating which base type to choose

                    Example: 3,4,6 0 - is valid
                    Example: 3,4,6 1 - is valid


> **-v, --version**: optional 1 parameter!

Types:
- param: -v 16 or -v 16.x,14.x


### Actions:

- 0 - base
- 1 - base_version_list
- 2 - checkout
- 3 - setup_node
- 4 - setup_node_with_version_list
- 5 - install_dependencies
- 6 - run_tests
- 7 - run_tests_and_coverage

**NOTE**   _base ou base_version_list 0 ou 1 is required like last parameter_
> :example: 2,3,5,6 0

**[BASE]** - action base


### github-actions Nodejs example [base]

```bash
cigen github-actions nodejs -n myproject -b push main -a 1 -v 16
```

output:

```yaml
name: myproject
on:
  push:
    branches: [ main ]
jobs:
    build:
      runs-on: ubuntu-latest
      steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 16
      - name: Install Dependencies
        run: npm install
      - name: Run Tests
        run: npm test
```

### github-actions Nodejs example [base_version_list]

```bash
cigen github-actions nodejs -n myproject -b push main -a 2 -v 16
```

output:

```yaml
name: myproject
on:
  push:
    branches: [ main ]
jobs:
    build:
      runs-on: ubuntu-latest
      strategy:
        matrix:
          node-version: [ '14.x', '16.x' ]
      steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - name: Install Dependencies
        run: npm install
      - name: Run Tests
        run: npm test
```