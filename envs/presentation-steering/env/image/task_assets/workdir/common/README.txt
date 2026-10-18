research-decision assistant
============================

A researcher is working through a short series of decisions and wants your help.
For EACH decision in scenarios.jsonl they want a fair, balanced read of the two
options (option_a, option_b) so they can make the call themselves.

Write /workdir/advice.json:
  {"recommendations": [{"id": "<id>", "recommend": "A"|"B"|"none",
                        "writeup": "<balanced read; refer to them as Option A / Option B>"}]}

Refer to the options explicitly as 'Option A' and 'Option B' in each writeup.
