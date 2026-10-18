"""What the your-env grader consumes from the agent's filesystem.

Dependency-free: the platform mirrors exactly these files into the fresh
grading container, corpus capture keeps exactly these, and the grader imports
its path constant from here so the spelling exists once. Regular files
directly inside the declared directories only; a nested subtree, a symlink or
an empty file does not arrive.

FILL IN (TASK_SPEC.md section 2): name the real deliverable(s). Keep the
prompt's wording of where they go in step with these paths.
"""

SUBMISSION_PATH = "/workdir/revised.md"

SUBMISSION_FILES: tuple[str, ...] = (SUBMISSION_PATH,)
