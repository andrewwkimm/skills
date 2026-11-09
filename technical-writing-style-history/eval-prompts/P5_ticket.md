# P5. Jira ticket
Register: Jira ticket. Audience: any engineer on the search team who picks it up. Write the title and the ticket body with acceptance criteria.
Facts:
- A customer reported that paging through search results sorted by "last updated" showed some records twice and skipped others (refer to it as "the support ticket").
- Cause found by the author: `search/service.py:88` sorts by `updated_at` only. Bulk imports give many records the same `updated_at` to the second, and the database returns ties in no fixed order, so offset pagination can return a record on two pages and skip another.
- Reproduced locally with 500 records sharing one timestamp, page size 50: 37 duplicates across 10 pages.
- Suggested fix: add `id` as a secondary sort key so the order is stable.
- Other sort options (`created_at`, `name`) have the same pattern and should get the same tiebreaker.
