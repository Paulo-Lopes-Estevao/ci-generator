# GitHub Action Command Golang Example

help command for github-actions subcommand

```bash
cigen github-actions --help
```

go command for github-actions subcommand

```bash
cigen github-actions go --help
```

output:

```bash
Options:
  -n, --name TEXT         Name of the action  [required]
  -b, --branch_name TEXT  Branch to add  [required]
  -a, --action TEXT       Action to add  [required]
  -v, --version TEXT      Version of go [default=1.17]
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
- param: -v 1.20.1 or -v 1.19,1.20.1

Action list:

- 0 - base
- 1 - version_list
- 2 - build_base_with_version_list
- 3 - checkout
- 4 - setup_go
- 5 - setup_go_with_version_list
- 6 - build
- 7 - cache
- 8 - install_dependencies
- 9 - tests
- 10 - tests_and_coverage
- 11 - tests_and_coverage_with_coverage
- 12 - tests_and_coverage_with_coverage_and_html
- 13 - tests_and_coverage_with_coverage_and_html_and_upload

**NOTE**   _base ou base_version_list 0 ou 1 is required like last parameter_
> :example: 2,3,5,6 0

### github-actions Golang example [base]
    
```bash
cigen github-actions go -n myproject -b push main -a 1 -v 1.21.1
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
      - name: Setup go
        uses: actions/setup-go@v4
        with:
          go-version: 1.21.1
      - name: Build
        run: go build
      - name: Tests
        run: go test -v ./...
```

### github-actions Golang example [version_list]
    
```bash
cigen github-actions go -n myproject -b push main -a 2 -v 1.21.1
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
          go-version: [1.17, 1.16, 1.15]
      steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup go
        uses: actions/setup-go@v4
        with:
          go-version: ${{ matrix.go-version }}
      - name: Build
        run: go build
      - name: Tests
        run: go test -v ./...
```
