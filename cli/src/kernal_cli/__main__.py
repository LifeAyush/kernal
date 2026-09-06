import argparse
import sys
from collections.abc import Callable

from kernal_cli.helpers import database_url
from kernal_core.storage import WorkflowRunRecord, configure, init_schema, is_available
from kernal_core.workflows import execute
from kernal_linkedin.workflows import get_workflow


def _run(workflow_name: str) -> int:
    url: str | None = database_url()
    configure(url)
    if not is_available():
        print("DATABASE_URL is not set", file=sys.stderr)
        return 1
    init_schema()
    fn: Callable[[], None] | None = get_workflow(workflow_name)
    if fn is None:
        print(f"Unknown workflow: {workflow_name}", file=sys.stderr)
        return 1
    row: WorkflowRunRecord = execute(workflow_name, fn)
    error: str = row.error or ""
    print(f"{row.id} {row.status} {error}".rstrip())
    return 0


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="kernal")
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(
        dest="command",
        required=True,
    )
    run_parser: argparse.ArgumentParser = subparsers.add_parser("run", help="Execute a workflow")
    run_parser.add_argument("workflow_name")
    args: argparse.Namespace = parser.parse_args()
    if args.command == "run":
        raise SystemExit(_run(args.workflow_name))


if __name__ == "__main__":
    main()
