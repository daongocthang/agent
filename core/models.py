from dataclasses import dataclass, field


@dataclass
class Step:
    name: str
    command: str
    precheck: str = ""
    verify: str = ""
    rollback: str = ""


@dataclass
class Recipe:
    name: str
    steps: list[Step] = field(default_factory=list)
    note: str = ""


@dataclass
class Result:
    returncode: int
    output: str

    @property
    def success(self):
        return self.returncode == 0
