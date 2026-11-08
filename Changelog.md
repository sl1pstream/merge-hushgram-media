## 2026-11-07
- Changed the method for moving files entirely - Instead of waiting 2 seconds per file, scripts will now check against a file's stable age and skip files that are "too new", deeming them as still being modified
- More efficient duplicate checking
- Lower STABLE_AGE from 5 to 2. Feel free to change this back if you're trying to run this on your toaster
