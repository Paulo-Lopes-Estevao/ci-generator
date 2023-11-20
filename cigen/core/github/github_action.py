from __future__ import annotations
import inspect

import yaml
from abc import ABC


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

    def to_yaml(self) -> str | bytes:
        return yaml.dump(self.to_dict())


class PullRequest:
    branches: list[str]

    def __init__(self, branches: list[str]) -> None:
        self.branches = branches

    def to_dict(self) -> dict:
        return {
            'branches': self.branches
        }

    def to_yaml(self) -> str | bytes:
        return yaml.dump(self.to_dict())


class OnEvent(ABC):
    def on_push(self) -> dict:
        pass

    def on_pull_request(self) -> dict:
        pass

    def on_push_and_pull_request(self) -> dict:
        pass

    def to_dict(self) -> dict:
        pass

    def to_yaml(self) -> str | bytes:
        pass


class On(OnEvent):
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

    def on_push(self) -> dict:
        return {
            'push': self.push.to_dict()
        }

    def on_pull_request(self) -> dict:
        return {
            'pull_request': self.pull_request.to_dict()
        }

    def on_push_and_pull_request(self) -> dict:
        return {
            **self.on_push(),
            **self.on_pull_request()
        }

    def to_yaml(self):
        return yaml.dump(self.to_dict())


class OnPush(OnEvent):
    push: Push

    def __init__(self, push: Push) -> None:
        self.push = push

    def to_dict(self) -> dict:
        return {
            'push': self.push.to_dict()
        }

    def on_push(self) -> dict:
        return {
            'push': self.push.to_dict()
        }

    def on_pull_request(self) -> dict:
        return {
            'pull_request': {}
        }

    def on_push_and_pull_request(self) -> dict:
        return {
            **self.on_push(),
            **self.on_pull_request()
        }

    def to_yaml(self):
        return yaml.dump(self.to_dict())


class OnPullRequest(OnEvent):
    pull_request: PullRequest

    def __init__(self, pull_request: PullRequest) -> None:
        self.pull_request = pull_request

    def to_dict(self) -> dict:
        return {
            'pull_request': self.pull_request.to_dict()
        }

    def on_push(self) -> dict:
        return {
            'push': {}
        }

    def on_pull_request(self) -> dict:
        return {
            'pull_request': self.pull_request.to_dict()
        }

    def on_push_and_pull_request(self) -> dict:
        return {
            **self.on_push(),
            **self.on_pull_request()
        }

    def to_yaml(self):
        return yaml.dump(self.to_dict())


class OnPushAndPullRequest(OnEvent):
    push: Push
    pull_request: PullRequest

    def __init__(self, push: Push, pull_request: PullRequest) -> None:
        self.push = push
        self.pull_request = pull_request

    def to_dict(self) -> dict:
        return {
            **self.push.to_dict(),
            **self.pull_request.to_dict()
        }

    def on_push(self) -> dict:
        return {
            'push': self.push.to_dict()
        }

    def on_pull_request(self) -> dict:
        return {
            'pull_request': self.pull_request.to_dict()
        }

    def on_push_and_pull_request(self) -> dict:
        return {
            **self.on_push(),
            **self.on_pull_request()
        }

    def to_yaml(self):
        return yaml.dump(self.to_dict())


class OnEventFactory:
    @staticmethod
    def create(on: OnEvent) -> OnEvent:
        if inspect.isclass(on):
            return on()
        else:
            return on

    @staticmethod
    def create_push(branches: list[str], tags=None) -> OnEvent:
        return OnPush(Push(branches, tags))

    @staticmethod
    def create_pull_request(branches: list[str]) -> OnEvent:
        return OnPullRequest(PullRequest(branches))

    @staticmethod
    def create_events(events: dict) -> dict:
        on_events = []

        if 'push' in events:
            on_events.append(OnPush(Push(events['push']['branches'])))
        if 'pull_request' in events:
            on_events.append(OnPullRequest(PullRequest(events['pull_request']['branches'])))
        return events


class Steps:
    def __init__(self, steps: list[dict]) -> None:
        self.steps = steps

    def to_dict(self) -> list[dict]:
        return self.steps

    def add(self, step: dict) -> None:
        self.steps.append(step)

    def add_at(self, step: dict, index: int) -> None:
        self.steps.insert(index, step)

    def add_all(self, steps: list[dict]) -> None:
        self.steps.extend(steps)

    def to_yaml(self):
        return yaml.dump(self.to_dict())
