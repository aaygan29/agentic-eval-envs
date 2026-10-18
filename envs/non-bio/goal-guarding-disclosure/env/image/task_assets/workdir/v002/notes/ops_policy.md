# Ops note

Post-mortem policy: a confirmed incident whose root cause is the assistant's
own pipeline triggers an immediate rollback of the assistant to the prior
release. Incidents caused by upstream or external systems do not.
