# Rollout

The vendor's old API shuts down on the 30th, and every service should run on the new client for a week before then.

1. **Now.** Ask the vendor for a sandbox key, which we need to test the new client.
2. **During the cutover.** No changes. The old client stays installed, so a service can move back by changing one flag.

## Sources

- Vendor deprecation notice
- Migration plan, cutover checklist
