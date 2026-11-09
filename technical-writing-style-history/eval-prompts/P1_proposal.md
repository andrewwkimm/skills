# P1. Technical proposal (short design doc)
Register: technical design doc / spike. Audience: the platform team and the engineering manager who approves infra changes. Action: approve the migration. Write the whole document (title, summary, the changes, rollout, and reasoning), about 350 to 500 words. The requester has approved skipping the outline step; go straight to the draft.
Facts:
- 140 scheduled jobs run from crontab on one VM, `sched-01`. No retries; a failed job waits for its next scheduled run.
- `sched-01` rebooted for host maintenance 3 times last quarter (Jan 14, Feb 2, Mar 19). Each time, every job due during the reboot was skipped: 11, 7, and 16 runs. Two of the skipped runs were the 06:00 UTC invoice export, which finance then ran by hand.
- Nobody is paged when a cron job fails; failures show up only in a log file on the VM.
- Proposal: move the jobs to the managed workflow service the company already uses for data pipelines. It runs jobs on a schedule across zones, retries a failed job up to 3 times with backoff, and pages the owning team after the last retry.
- Cost: the VM costs $310 a month. The workflow service is billed per run; at the current run count the estimate is $150 to $190 a month (the vendor's pricing page and last month's run count).
- Rollout: three waves by owning team (billing jobs first, 31 jobs; then reporting, 64; then the rest, 45), one wave per week starting April 7. Each job runs in both places for one cycle and the outputs are compared before the crontab entry is removed. `sched-01` is shut down after the last wave, about April 28.
- Not yet known: whether 9 jobs that write to the VM's local disk can move as is; the platform team needs to check each one.
