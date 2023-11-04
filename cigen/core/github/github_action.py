import yaml

class Push:
    branches: list[str]
    tags: list[str]

    def __init__(self, branches: list[str], tags=None) -> None:
        if tags is None:
            tags = []
        self.branches = branches
        self.tags = tags

    def to_dict(self) -> dict:
        if len(self.tags) == 0:
            return {
                'branches': self.branches
            }
        else:
            return {
                'branches': self.branches,
                'tags': self.tags
            }

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict())


class PullRequest:
    branches: list[str]

    def __init__(self, branches: list[str]) -> None:
        self.branches = branches

    def to_dict(self) -> dict:
        return {
            'branches': self.branches
        }


class On:
    push: Push
    pull_request: PullRequest

    def __init__(self, push: Push, pull_request: PullRequest) -> None:
        self.push = push
        self.pull_request = pull_request

    def to_dict(self) -> dict:
        return {
            'push': self.push.to_dict(),
            'pull_request': self.pull_request.to_dict()
        }

    def onPush(self) -> dict:
        return {
            'push': self.push.to_dict()
        }

    def onPullRequest(self) -> dict:
        return {
            'pull_request': self.pull_request.to_dict()
        }

    def onPushAndPullRequest(self) -> dict:
        return {
            **self.onPush(),
            **self.onPullRequest()
        }

    def to_yaml(self):
        return yaml.dump(self.to_dict())


class Steps:
    def __init__(self, steps: list[dict]) -> None:
        self.steps = steps

    def to_dict(self) -> list[dict]:
        return self.steps

    def add(self, step: dict) -> None:
        self.steps.append(step)

    def addAt(self, step: dict, index: int) -> None:
        self.steps.insert(index, step)

    def addAll(self, steps: list[dict]) -> None:
        self.steps.extend(steps)

    def to_yaml(self):
        return yaml.dump(self.to_dict())
