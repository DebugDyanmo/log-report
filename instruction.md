There is an Apache-style access log at `/app/access.log`. Parse it and produce a

JSON summary report at `/app/report.json`.



Your solution must:



1\. Count the total number of requests (non-empty lines) in the log as `total\_requests`.

2\. Count the number of unique client IP addresses as `unique\_ips`.

3\. Identify the single most frequently requested path as `top\_path`.

4\. Write the results to `/app/report.json` as valid JSON containing exactly these

&#x20;  three keys: `total\_requests` (integer), `unique\_ips` (integer), and `top\_path`

&#x20;  (string) — no other keys.



The task is complete once `/app/report.json` exists, is valid JSON with exactly

those three keys, and each value matches what can be independently computed from

`/app/access.log`.

