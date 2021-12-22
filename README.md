# Tiny URL shortener

This is a very small and minimal URL shortening service written in PHP and Python 3. To install, simply clone the repository and place the files in a directory of your choice.

To configure, create a .config file following the .config.sample file. As an example, if your domain is example.com and the directory hosting the service is /s/, the config file would look like:

```
[general]
dbpath = ./db.json
lengthlimit = 7
digits = yes
agelimit = 0
domain = example.com/s
```

Ensure that permissions are correct! To start shortening URLs, simply navigate to http://example.com/s/create/.
