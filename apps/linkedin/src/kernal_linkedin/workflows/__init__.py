"""LinkedIn workflows: find_people, engage_posts, create_content."""

from collections.abc import Callable

from kernal_linkedin.workflows import create_content, engage_posts, find_people

WorkflowFn = Callable[[], None]

WORKFLOWS: dict[str, WorkflowFn] = {
    "linkedin.find_people": find_people.run,
    "linkedin.engage_posts": engage_posts.run,
    "linkedin.create_content": create_content.run,
}


def get_workflow(name: str) -> WorkflowFn | None:
    return WORKFLOWS.get(name)
