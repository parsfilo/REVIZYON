#!/bin/bash
DISPLAY=:0 lxterminal --geometry=50x20+0+0 --working-directory="/home/pi/Desktop/REVIZYON/NODE_SERVER/" --command="nodemon -x 'node server.js || touch server.js'" &
