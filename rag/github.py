#TODO: remove type errors from this file

from __future__ import annotations
from git import Repo, RemoteProgress
from rich import console, progress
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitRemoteProgress(RemoteProgress):
    OP_CODES = [
        "BEGIN",
        "CHECKING_OUT",
        "COMPRESSING",
        "COUNTING",
        "END",
        "FINDING_SOURCES",
        "RECEIVING",
        "RESOLVING",
        "WRITING",
    ]
    OP_CODE_MAP = {
        getattr(RemoteProgress, _op_code): _op_code for _op_code in OP_CODES
    }

    def __init__(self) -> None:
        super().__init__()
        self.progressbar = progress.Progress(
            progress.SpinnerColumn(),
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            "eta",
            progress.TimeRemainingColumn(),
            progress.TextColumn("{task.fields[message]}"),
            console=console.Console(),
            transient=False,
        )
        self.progressbar.start()
        self.active_task = None

    def __del__(self) -> None:
        self.progressbar.stop()

    @classmethod
    def get_curr_op(cls, op_code: int) -> str:
        """Get OP name from OP code."""
        op_code_masked = op_code & cls.OP_MASK
        return cls.OP_CODE_MAP.get(op_code_masked, "?").title()

    def update(
        self,
        op_code: int,
        cur_count: str | float,
        max_count: str | float | None = None,
        message: str | None = "",
    ) -> None:
        if op_code & self.BEGIN:
            self.curr_op = self.get_curr_op(op_code)
            self.active_task = self.progressbar.add_task(
                description=self.curr_op,
                total=max_count,
                message=message,
            )

        self.progressbar.update(
            task_id=self.active_task,
            completed=cur_count,
            message=message,
        )

        if op_code & self.END:
            self.progressbar.update(
                task_id=self.active_task,
                message=f"[bright_black]{message}",
            )

def download_github_repo(github_url: str, local_path: str) -> None:
    logger.info(f"file: github function: download_github_repo cloning repository: {github_url} in directory: {local_path}")
    print(f"Cloning git repository from {github_url}...")
    try:
        Repo.clone_from(github_url, local_path, progress=GitRemoteProgress())
        print("Repository cloned successfully")
    except Exception as err:
        print("Could not clone repository")
        logger.info(f"file: github function: download_github_repo error in cloning repository: {err}")

#TODO: Write a test for this function
# github_test_url = "https://github.com/ganga-devs/ganga"
# storage_path = "./cache/data/repo"
# download_github_repo(github_test_url, storage_path)
