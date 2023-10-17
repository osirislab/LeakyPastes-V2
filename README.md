# What is this?
A small project to archive public pastebin posts. This is a work in progress and may be used for security research.


## How does it work?
This repository checks https://pastebin.com/archive every 6 hours and looks at the most recent public pastes.


## csv format
```
id, title, author, date, syntax, content
```