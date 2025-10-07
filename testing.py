#!/usr/bin/env python3
"""
make_fake_secrets.py

Creates a set of sample files that intentionally contain fake secrets with variable names:
- token
- auth_token
- access_token
- refresh_token
- bearer_token

All tokens are synthetic and clearly fake (do NOT use them for real services).
Use these files to test secret scanners / dorking scripts.
"""

from pathlib import Path
import base64
import json
import textwrap

OUT = Path("fake_secrets_samples")
OUT.mkdir(exist_ok=True)

# clearly fake token values
FAKES = {
    "token": "FAKE_TOKEN_ABC123_DO_NOT_USE",
    "auth_token": "FAKE_AUTH_TOKEN_456XYZ_DO_NOT_USE",
    "access_token": "FAKE_ACCESS_TOKEN_789QWE_DO_NOT_USE",
    "refresh_token": "FAKE_REFRESH_TOKEN_000RST_DO_NOT_USE",
    "bearer_token": "FAKE_BEARER_TOKEN_111ZZZ_DO_NOT_USE"
}

FAKES = {
    "token": "FAKE_TOKEN_ABC123_DO_NOT_USE",
    "auth_token": "FAKE_AUTH_TOKEN_456XYZ_DO_NOT_USE",
    "access_token": "FAKE_ACCESS_TOKEN_789QWE_DO_NOT_USE",
    "refresh_token": "FAKE_REFRESH_TOKEN_000RST_DO_NOT_USE",
    "bearer_token": "FAKE_BEARER_TOKEN_111ZZZ_DO_NOT_USE"
}

# 1) Python module with direct assignments
py_content = textwrap.dedent(f"""
# sample_config.py - direct secret assignments (bad practice)
token = "{FAKES['token']}"
auth_token = "{FAKES['auth_token']}"
access_token = "{FAKES['access_token']}"
refresh_token = "{FAKES['refresh_token']}"
bearer_token = "{FAKES['bearer_token']}"
""").strip()
(OUT / "sample_config.py").write_text(py_content)

# 2) .env file style
env_lines = "\n".join(f"{k.upper()}={v}" for k, v in FAKES.items())
(OUT / ".env").write_text(env_lines)

# 3) JSON config file
json_content = {
    "service": "example",
    "credentials": {
        "token": FAKES["token"],
        "auth_token": FAKES["auth_token"],
        "access_token": FAKES["access_token"]
    },
    "refresh": {
        "refresh_token": FAKES["refresh_token"]
    }
}
(OUT / "config.json").write_text(json.dumps(json_content, indent=2))

# 4) YAML config
yaml_content = textwrap.dedent(f"""
service: example
credentials:
  token: {FAKES['token']}
  bearer_token: {FAKES['bearer_token']}
""").strip()
(OUT / "config.yaml").write_text(yaml_content)

# 5) JS file with exported secrets and template strings
js_content = textwrap.dedent(f"""
// secrets.js - insecure examples
module.exports = {{
  token: "{FAKES['token']}",
  auth_token: "{FAKES['auth_token']}",
  access_token: "{FAKES['access_token']}"
}};

// concatenated appearance
const bearer_token = "BEARER_" + "{FAKES['bearer_token']}";
console.log("loaded secrets");
""").strip()
(OUT / "secrets.js").write_text(js_content)

# 6) HTML with an embedded script and comment containing a secret
html_content = textwrap.dedent(f"""
<!-- index.html -->
<html>
  <head><title>Fake Secret Demo</title></head>
  <body>
    <!-- auth_token: {FAKES['auth_token']} -->
    <script>
      // token present in script tag
      var token = "{FAKES['token']}";
      // disguised but present: access_token="{{{FAKES['access_token']}}}"
    </script>
  </body>
</html>
""").strip()
(OUT / "index.html").write_text(html_content)

# 7) File with Base64-encoded secret (some scanners decode)
b64_payload = base64.b64encode(FAKES["access_token"].encode()).decode()
(OUT / "secrets_b64.txt").write_text(f"base64_access: {b64_payload}\n# decodes to: {FAKES['access_token']}")

# 8) Dockerfile-style / CI env usage patterns
dockerfile = textwrap.dedent(f"""
# Dockerfile snippet
ENV TOKEN={FAKES['token']}
# CI variable pattern
# export AUTH_TOKEN={FAKES['auth_token']}
""").strip()
(OUT / "Dockerfile.sample").write_text(dockerfile)

# 9) README with an example which should be ignored by scanners (placeholder pattern)
readme = textwrap.dedent("""
README.md

Placeholders below should NOT be flagged by good scanners (they look like templates):
- token: {{TOKEN}}
- auth_token: ${AUTH_TOKEN}
""").strip()
(OUT / "README.md").write_text(readme)

# 10) A "safe" example where token is referenced but not hard-coded (should not be flagged)
safe_py = textwrap.dedent("""
# safe_usage.py - demonstrates reading from env (preferred)
import os
token = os.getenv('TOKEN')  # should come from environment, not hard-coded
""").strip()
(OUT / "safe_usage.py").write_text(safe_py)

# Print a short index for the user
index = textwrap.dedent(f"""
Fake secret samples created in: {OUT.resolve()}

Files:
- sample_config.py       (python variables: token, auth_token, access_token, refresh_token, bearer_token)
- .env                   (ENV style variables)
- config.json            (json with token, auth_token, access_token)
- config.yaml            (yaml with bearer_token)
- secrets.js             (nodejs module + concatenated bearer_token)
- index.html             (comment + script secret)
- secrets_b64.txt        (base64-encoded access token)
- Dockerfile.sample      (ENV pattern)
- README.md              (template placeholders - should not be flagged)
- safe_usage.py          (example of safe env usage)

All tokens are synthetic and contain 'FAKE' in the value to avoid accidental real usage.
""").strip()
(OUT / "INDEX.txt").write_text(index)

print(index)
