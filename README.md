# random_wallpaper_url
Retrieves random wallpaper URL from https://wall.alphacoders.com/
The URL then could be used with any external downloader

```terminal
wget $(python random_wallpaper_url.py)
``` 
Shell script example which could be used to periodically change desktop background (**feh** need to be present in the system):

```
wget --limit-rate=20k -O /tmp/background.jpg $(python random_wallpaper_url.py) && DISPLAY=":0" feh --bg-fill /tmp/background.jpg
```

In case of gnome-shell (tested in Ubuntu 20.04):
```
#!/usr/bin/env bash
PID=$(pgrep -f 'gnome-session' | head -n1)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)
gsettings set org.gnome.desktop.background picture-uri $(python3 random_wallpaper_url.py)
```
