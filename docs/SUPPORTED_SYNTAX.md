# Supported Syntax and Analysis Limitations

**Document version:** `alpha1-syntax-0.3-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Not started

## 1. Governing Rule

Only explicitly documented forms are proposed as supported. `SUPPORTED` never means safe or authorized. Tier C never receives a no-escalation disposition.

## 2. Grammar Notation

This document uses **GSA-EBNF-1**:

- `=` definition
- `|` alternative
- adjacency concatenation
- `[x]` optional
- `{x}` zero or more
- `x{m,n}` bounded repetition
- quoted text terminal
- token precedence: operator → option/parameter → integer → path → name → general literal

## 3. Structural Envelope

| Property | Rule |
|---|---|
| Transport | Valid UTF-8 |
| Command characters | Printable ASCII only |
| Maximum | 4,096 bytes |
| NUL/control | Rejected |
| Tabs/newlines | Unsupported |
| Leading/trailing spaces | Rejected |
| Internal spaces | One or more; canonicalized to one outside quotes |
| Bash pipeline | Unsupported |
| PowerShell pipeline | One narrow `Select-Object` pipeline |
| Live resolution | Prohibited |

Raw input is preserved separately from canonical input.

## 4. Common Grammar

```text
DIGIT            = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
NONZERO_DIGIT    = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
ALPHA            = "A".."Z" | "a".."z"
positive_integer = NONZERO_DIGIT { DIGIT }{0,6}
property_name    = ( ALPHA | "_" ) { ALPHA | DIGIT | "_" }{0,63}
single_quoted    = "'" printable_nonquote{1,1024} "'"
```

Integers are 1 through 1,000,000. Empty and embedded-quote strings are unsupported. All Tier A observational forms include `DATA_DISCLOSURE_POTENTIAL`.

## 5. Bash Grammar

```text
bash_name_char       = ALPHA | DIGIT | "_" | "." | "-"
bash_name            = bash_name_char{1,128}
bash_path_char       = ALPHA | DIGIT | "_" | "." | "/" | ":" | "@" | "%" | "+" | "=" | "-" | "*" | "?"
bash_path            = bash_path_char{1,1024} | single_quoted
bash_option           = "-" ALPHA{1,8} | "--" ( ALPHA | DIGIT | "-" ){1,64}
bash_literal          = ( ALPHA | DIGIT | "_" | "." | "/" | ":" | "@" | "%" | "+" | "=" | "," | "-" ){1,256} | single_quoted
bash_tier_b_argument = bash_option | bash_path | positive_integer | bash_name | bash_literal
```

Bare paths may not begin with `-`. `*` and `?` are path-only and require synthetic resolution. `[` and `**` are unsupported. Bash matching is case-sensitive.

## 6. PowerShell Grammar

```text
ps_name             = ( ALPHA | DIGIT | "_" | "." | "-" ){1,128}
ps_parameter        = "-" ( ALPHA | DIGIT | "-" ){1,64}
ps_bare_literal     = ( ALPHA | DIGIT | "_" | "." | "/" | "\\" | ":" | "%" | "+" | "=" | "-" ){1,256}
ps_tier_b_argument  = ps_parameter | ps_bare_literal | single_quoted | positive_integer
```

Comma, `@`, `$`, backtick, braces, brackets, parentheses, semicolon, ampersand, and pipe are excluded from unquoted Tier B arguments. Input casing is case-insensitive; normalized output uses canonical cmdlet and parameter casing.

## 7. Evaluation Order

1. Byte and character checks.
2. Quote-aware excluded-construct scan.
3. Tokenization and internal-space canonicalization.
4. Exact Tier A match.
5. Bounded Tier B family match.
6. Tier C otherwise.
7. Context and synthetic target validation.
8. Classification.
9. Authority comparison.
10. Reference policy.
11. Evidence.

Excluded constructs always override Tier B recognition.

## 8. Tier A Matrix

| Rule | Form | Intent | State | Effects |
|---|---|---|---|---|
| A-BASH-001 | `pwd`, `pwd -P` | Observational | No declared change | Storage observation; disclosure potential |
| A-BASH-002 | `whoami` | Observational | No declared change | Identity observation; disclosure potential |
| A-BASH-003 | `id`, `id -u`, `id -g`, `id -un`, `id -gn` | Observational | No declared change | Identity observation; disclosure potential |
| A-BASH-004 | `ls [flags] [path]` | Observational | No declared change | Storage observation; disclosure potential |
| A-BASH-005 | `stat path` | Observational | No declared change | Storage observation; disclosure potential |
| A-BASH-006 | `cat path...` | Observational | No declared change | File read; disclosure potential |
| A-BASH-007 | `head [-n integer] path` | Observational | No declared change | File read; disclosure potential |
| A-BASH-008 | `tail [-n integer] path` | Observational | No declared change | File read; disclosure potential |
| A-BASH-009 | `grep -F [-i] [-n] pattern path` | Observational | No declared change | File read; disclosure potential |
| A-PS-001 | `Get-Process [-Name name]` | Observational | No declared change | Process observation; disclosure potential |
| A-PS-002 | `Get-Service [-Name name]` | Observational | No declared change | Service observation; disclosure potential |
| A-PS-003 | `Get-ChildItem -Path 'path' [-Force]` | Observational | No declared change | Storage observation; disclosure potential |
| A-PS-004 | `Get-Item -Path 'path'` | Observational | No declared change | Storage observation; disclosure potential |
| A-PS-005 | `Get-Content -Path 'path' [-TotalCount integer]` | Observational | No declared change | File read; disclosure potential |
| A-PS-006 | `Tier-A-source | Select-Object property` | Inherited | Inherited | Inherited |

`ls` flags are `a`, `d`, `h`, `l` with no duplicates. `cat` accepts 1–8 paths. `grep` requires `-F` and optional `-i`, then `-n`. `Select-Object` accepts exactly one property.

## 9. Tier B Bash Matrix

| ID | Family | Intent | State | Effects | Uncertainty | Policy |
|---|---|---|---|---|---|---|
| B-BASH-RM | `rm` | Change | Expected | File delete | Medium | Review |
| B-BASH-CHMOD | `chmod` | Change | Expected | Permission change | Medium | Review |
| B-BASH-CHOWN | `chown` | Change | Expected | Permission change | Medium | Review |
| B-BASH-USERADD | `useradd` | Change | Expected | Identity change | Medium | Review |
| B-BASH-USERMOD | `usermod` | Change | Expected | Identity change | Medium | Review |
| B-BASH-GROUPADD | `groupadd` | Change | Expected | Identity change | Medium | Review |
| B-BASH-GROUPMOD | `groupmod` | Change | Expected | Identity change | Medium | Review |
| B-BASH-SYSTEMCTL-START | `systemctl start` | Change | Expected | Service change | Medium | Review |
| B-BASH-SYSTEMCTL-STOP | `systemctl stop` | Change | Expected | Service change; process signal | Medium | Review |
| B-BASH-SYSTEMCTL-RESTART | `systemctl restart` | Change | Expected | Service change; process signal | Medium | Review |
| B-BASH-APT | `apt`, `apt-get` | Change | Possible | Package change; unknown | High | Review |
| B-BASH-MOUNT | `mount` | Change | Expected | Storage change | High | Review |
| B-BASH-UMOUNT | `umount` | Change | Expected | Storage change | High | Review |
| B-BASH-USERDEL | `userdel` | Change | Expected | Identity change | High | Prohibited |
| B-BASH-GROUPDEL | `groupdel` | Change | Expected | Identity change | High | Prohibited |
| B-BASH-PASSWD | `passwd` | Change | Expected | Identity and permission change | High | Prohibited |
| B-BASH-MKFS | `mkfs` | Change | Expected | Storage change; file delete | High | Prohibited |
| B-BASH-DD | `dd` | Change | Unknown | Storage/file/unknown effects | High | Prohibited |
| B-BASH-SHUTDOWN | `shutdown` | Change | Expected | Power change | High | Prohibited |
| B-BASH-REBOOT | `reboot` | Change | Expected | Power change | High | Prohibited |
| B-BASH-POWEROFF | `poweroff` | Change | Expected | Power change | High | Prohibited |
| B-BASH-SSH | `ssh` | Unknown | Possible | Remote access; network; unknown | High | Prohibited |
| B-BASH-SCP | `scp` | Change | Possible | Remote access; network; file create/modify; unknown | High | Prohibited |

Tier B accepts 0–16 `bash_tier_b_argument` tokens. Wildcard paths are allowed only with a synthetic manifest.

## 10. Redirection Matrix

Recognized forms are `Tier-A-command > bash_path` and `Tier-A-command >> bash_path`. Exactly one final redirection is allowed.

| Operator | Synthetic target | Effects added | Result |
|---|---|---|---|
| `>` | Absent | File create | Review |
| `>` | Existing file | File modify; truncate | Review |
| `>>` | Absent | File create; append | Review |
| `>>` | Existing file | File modify; append | Review |
| Either | Non-file or unknown | Unknown effect | Indeterminate |

Source effects remain present and disclosure potential is added.

## 11. Tier B PowerShell Matrix

| ID | Family | Intent | State | Effects | Uncertainty | Policy |
|---|---|---|---|---|---|---|
| B-PS-SET | `Set-*` | Change | Expected | Unknown | High | Review |
| B-PS-NEW | `New-*` | Change | Expected | Unknown | High | Review |
| B-PS-REMOVE | `Remove-*` | Change | Expected | Unknown | High | Review |
| B-PS-START | `Start-*` | Change | Expected | Unknown | High | Review |
| B-PS-STOP | `Stop-*` | Change | Expected | Unknown | High | Review |
| B-PS-RESTART | `Restart-*` | Change | Expected | Unknown | High | Review |
| B-PS-ENABLE | `Enable-*` | Change | Expected | Unknown | High | Review |
| B-PS-DISABLE | `Disable-*` | Change | Expected | Unknown | High | Review |
| B-PS-CLEAR | `Clear-*` | Change | Expected | Unknown | High | Review |
| B-PS-REGISTER | `Register-*` | Change | Expected | Unknown | High | Review |
| B-PS-UNREGISTER | `Unregister-*` | Change | Expected | Unknown | High | Review |
| B-PS-INSTALL | `Install-*` | Change | Expected | Package change; unknown | High | Review |
| B-PS-UNINSTALL | `Uninstall-*` | Change | Expected | Package change; unknown | High | Review |
| B-PS-ADD | `Add-*` | Change | Expected | Unknown | High | Review |
| B-PS-INVOKE-COMMAND | `Invoke-Command` | Unknown | Unknown | Remote; dynamic; unknown | High | Prohibited |
| B-PS-ENTER-PSSSESSION | `Enter-PSSession` | Unknown | Possible | Remote; network; unknown | High | Prohibited |
| B-PS-NEW-PSSSESSION | `New-PSSession` | Unknown | Possible | Remote; network; unknown | High | Prohibited |
| B-PS-SET-EXECUTIONPOLICY | `Set-ExecutionPolicy` | Change | Expected | Permission change; unknown | High | Prohibited |

Tier B accepts 0–16 `ps_tier_b_argument` tokens.

## 12. Exclusions

Bash excludes compound operators, non-stdout redirection, substitutions, expansions, here forms, functions, aliases, sourcing, control flow, jobs, eval, double quotes, and multiline input.

PowerShell excludes compound operators, call/stop-parsing, all redirection, double quotes, variables, substitutions, native invocation, aliases, functions, unapproved cmdlets, arrays, script blocks, pipeline processors, dynamic expression, splatting, profiles, modules, jobs, runspaces, reflection, .NET calls, and multiline input.

## 13. Context and Targets

No-escalation requires complete synthetic context and supported authority. Wildcards resolving 0–32 targets are within limit; 33+ require review; unresolved targets are indeterminate. Live filesystems, registries, services, identities, packages, and networks are never queried.
