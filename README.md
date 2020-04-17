# todo
Simple utility to track todos

## Features
* Metrics like work done, remaining work todo, and productivity per day.
* Auto-fill calendar with suggested todos to take advantage of idle time.

## Architecture
* Start with a sqlite file to represent todos

## Problems
* If a todo's title/summary changes, how can we track that?
    * Perhaps todo's should be submitted via CLI, rather than allowing someone to edit the file directly.
