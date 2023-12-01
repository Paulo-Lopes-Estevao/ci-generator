# ci generator

CI generator is a tool to generate CI configuration files for your project.
It's a command line tool that can be used to generate CI configuration files for your project. It's written in Python and uses templates to generate the files.

Possible CI systems are:

- [x] Github Actions
- [ ] Jenkins
- [ ] Docker
- [ ] Gitlab CI

They can integrate with the following tools:

- SonarQube
- SonarCloud
- Test coverage
- DockerFile
- DockerCompose

## Installation

Multiplatform Linux, Windows, MacOs

```bash
pip install ci-generator
```

## Usage

```bash
cigen --help
```

### Github Actions

```bash
cigen github-actions --help
```

github-actions subcommand can be used to generate Build and Test Github Actions configuration files.

github-actions Golang example:

```bash
cigen github-actions go -n myproject -b push main -a 1 -v 1.21.1
```

github-actions Python example:

```bash
cigen github-actions python -n myproject -b push main -a 1 -v 3.9.6
```

### Jenkins

```bash
cigen jenkins --help
```

jenkins subcommand can be used to generate Build and Test Jenkins configuration files.

jenkins Golang example:

```bash
cigen jenkins go -n myproject -b push main -a 1 -v 1.21.1
```

jenkins Python example:

```bash
cigen jenkins python -n myproject -b push main -a 1 -v 3.9.6
```

### Docker

```bash
cigen docker --help
```

docker subcommand can be used to generate Docker configuration files.

docker example:

```bash
cigen docker -n dockerfile -i golang -v 1.21.1 -s multi
```

### Gitlab CI

```bash
cigen gitlab-ci --help
```

gitlab-ci subcommand can be used to generate Build and Test Gitlab CI configuration files.

gitlab-ci Golang example:

```bash
cigen gitlab-ci go -n myproject -b push main -a 1 -v 1.21.1
```

gitlab-ci Python example:

```bash
cigen gitlab-ci python -n myproject -b push main -a 1 -v 3.9.6
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
