# MAGIS Magnetometer Trolley: Server Setup for macOS

Most set-up instructions from the README.md should be applicable for a user running macOS. An issue does arise when the user tries to run:

```
$ systemctl daemon-reload
$ systemctl enable magsys.service
$ service magsys start
$ service magsys status
```

Little note before moving on! Ensure you've changed paths and other things in start_combo and magsys.service!

# Prepare script

Make sure start_combo.sh exists and can be executed

```
chmod +x 'path/start_combo.sh'
```

# Create Launch Agent (.plist)

The main system and service manager for macOS is launchd, so Linux's systemd. So, this are the macOS friendly commands for setting up the server

```
mkdir ~p ~/Library/LaunchAgents
nano ~/Library/LaunchAgents/com.yourname.magsys.plist
```
In that file, paste the script below:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourname.magsys</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/yourname/Magnetometer/python/start_combo.sh</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/yourname/Magnetometer/python</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <false/>

    <key>StandardOutPath</key>
    <string>/Users/yourname/magsys_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yourname/magsys_stderr.log</string>
</dict>
</plist>

```

Save and exit -> Ctrl+O, Enter, then Ctrl+X

# Enable and Start Service
```
launchctl unload ~/Library/LaunchAgents/com.yourname.magsys.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.yourname.magsys.plist
```

# Check Status

```
launchctl list | grep magsys
```