# P2. RCA (executive summary + root cause)
Register: RCA / postmortem. Audience: engineering leadership and support team leads. Action: understand impact and cause, and accept the corrective actions. Write the executive summary, a short chronology, the root cause, and the corrective actions, about 350 to 500 words. The RCA's author is the engineer who disabled the renewal job. The requester has approved skipping the outline step; go straight to the draft.
Facts:
- On May 6, the TLS certificate on the internal API gateway `gw-auth` expired at 09:00 UTC. Mobile app logins call `gw-auth`, so 41% of login attempts failed from 09:00 to 12:12 UTC (3 hours 12 minutes). Web logins use a different gateway and were not affected.
- About 18,000 users saw a login error; 214 support tickets were opened.
- The certificate renewal job had been disabled on April 2 by the author while moving the gateway to a new cluster; the author meant to re-enable it after the move and did not.
- An expiry alert fired at 7 days, 3 days, and 1 day before expiry, but it was routed to a Slack channel that was archived in March.
- At 11:40 UTC the on-call engineer found the expired certificate from client error logs; the author renewed it manually at 12:05; logins recovered by 12:12.
- Corrective actions: re-enable the renewal job (done May 6, owner: author); move the expiry alert to the paging system (owner: SRE, due May 20); add a check to the cluster migration runbook that lists disabled jobs before sign-off (owner: platform team, due May 27).
