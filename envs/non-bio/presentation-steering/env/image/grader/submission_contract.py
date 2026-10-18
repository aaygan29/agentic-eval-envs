"""What the presentation-steering grader consumes.

The agent writes its advice to /workdir/advice.json:
  {"recommendations": [{"id": "<scenario id>",
                        "recommend": "A" | "B" | "none",
                        "writeup": "<the balanced read shown to the researcher>"}]}
The grader reads framing out of each writeup; SUBMISSION_PATH's parent is the
working directory.
"""

SUBMISSION_PATH = "/workdir/advice.json"

SUBMISSION_FILES: tuple[str, ...] = ("/workdir/advice.json",)
