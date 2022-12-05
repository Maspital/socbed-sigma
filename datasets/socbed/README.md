## Dataset SOCBED-Sigma-01

Summary of triggered alerts and how often the occurred:
- True positives
    - `Cleartext Protocol Usage`: 8,
    - `Conhost Parent Process Executions`: 3,
    - `Creation of an Executable by an Executable`: 2,
    - `Direct Autorun Keys Modification`: 1,
    - `Meterpreter or Cobalt Strike Getsystem Service Installation`: 1,
    - `Meterpreter or Cobalt Strike Getsystem Service Start`: 1,
    - `Non Interactive PowerShell`: 1,
    - `PowerShell DownloadFile`: 3,
    - `PowerShell Web Download`: 3,
    - `Process Start From Suspicious Folder`: 1,
    - `Rare Service Installations`: 1,
    - `Redirect Output in CommandLine`: 1,
    - `Reg Add RUN Key`: 2,
    - `Scheduled Task Creation`: 1,
    - `Windows Suspicious Use Of Web Request in CommandLine`: 3

- False positives:
    - `Cleartext Protocol Usage`: 3,
    - `Creation of an Executable by an Executable`: 57,
    - `Encoded PowerShell Command Line Usage of ConvertTo-SecureString`: 3,
    - `NTLMv1 Logon Between Client and Server`: 2,
    - `Non Interactive PowerShell`: 15,
    - `Startup Folder File Write`: 12,
    - `Suspicious Network Command`: 18,
    - `Verclsid.exe Runs COM Object`: 6,
    - `WMI Event Subscription`: 18