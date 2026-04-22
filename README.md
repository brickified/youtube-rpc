# Youtube RPC
Discord rich presence for Youtube.

## How does this work?
- The userscript reads the properties of the playing video, then sends that data to a local server.
- Then that local server uses Pypresence to show your video progress and status.

## How do i use it?
- Add the userscript.js file to Tampermonkey and enable it.
- Before you run the server, open the server.py and set the APPLICATION_ID variable to your discord application's id.
- After you're done, run the local server on your PC.

## Notes
- This only works on PC, on your browser.
- Requirements: Python 3, Tampermonkey
- Python libraries needed: pypresence, requests, urllib
