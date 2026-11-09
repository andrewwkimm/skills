# P3. Audit finding
Register: audit / investigation. Audience: the infrastructure team that owns the storage buckets. Action: agree to the lifecycle change, which the author will raise as a PR. Write one findings section titled "3. Log storage has no lifecycle policy" with the finding and the fixes, about 250 to 400 words. Other sections exist. The requester has approved skipping the outline step; go straight to the draft.
Facts (from the storage inventory report and 90 days of access logs, pulled June 2):
- The `app-logs` bucket holds 62 TB and costs $1,430 a month, 38% of the team's storage bill.
- It has no lifecycle policy; nothing has been deleted since the bucket was created in 2021.
- 71% of the bytes are objects older than 180 days. In 90 days of access logs, 0.4% of reads touched objects older than 30 days, all of them from one quarterly compliance query.
- Audit logs under the `audit/` prefix (2.1 TB) must be kept 7 years under the company retention policy.
- Proposed policy: move objects to the cold tier after 30 days, delete after 400 days, exclude `audit/` from deletion (still move it to cold after 30 days).
- Estimated saving: $900 to $1,050 a month, from the provider's price sheet. The range depends on retrieval charges for the quarterly compliance query, which reads cold objects.
- The policy file goes in `infra/storage/app-logs.tf`; the provider applies it within 48 hours.
