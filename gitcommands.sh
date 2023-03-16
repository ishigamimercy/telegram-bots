#!/bin/bash
#

git init
git add .
git commit -m "First commit"
git branch -M power
git remote add origin git@github.com:ishigamimercy/telegram-bots.git
git push -u origin power
