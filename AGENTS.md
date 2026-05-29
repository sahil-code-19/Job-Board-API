# FastAPI Therapist

After running `fastapi-therapist . --verbose`:
1. Trust the output — issues are verified, no need to re-read files to confirm
2. Go directly to the reported `file:line` for each issue
3. Fix errors first, then warnings
4. After fixing, re-run `fastapi-therapist . --verbose` to verify the score improved
5. Never scan files manually to find issues — the therapist already did that
