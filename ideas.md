# Project Structure

Database class should allow us to dynamically construct queries (https://stackoverflow.com/a/30531801)
    * Service should be able to construct whatever query it wants, without having to import any tinydb classes (e.g. Query, where)

follow best practices for Click apps
    * https://dbader.org/blog/mastering-click-advanced-python-command-line-apps
    * store config in a file

# Usability

fix timezone info for `started_at`, `completed_at`, and `inserted_at`
    * currently using a different timezone; or consider UTC time?

Add current TODO to a status bar on zsh?

lowercase all tags and convert spaces into dashes (to standardize tags)
    * we probably need a utils module for this function, as well as printing, formatting, etc.

# Features

Drop into an ipython env with the service loaded so I can quickly write one-off scripts
    * e.g. set all the tasks' status to `IN_PROGRESS`

`todo start` should also accept a string, so users can add & start a task in one command
    * starting a todo with the `feat` tag should create a new branch!

`todo next` will suggest a Todo, and users can respond Y or N
    * if Y, that task will be started
    * if N, recommend the next task
    * if D, delete the task
    * renaming this to `then`, since `next` is a reserved word in Python

When a dependency is completed, the downstream tasks should get Scheduled/added to my Today list

`note "Here is a note about the task I'm currently working on"` should attach a note to that task object in the db

add `generate_report(date)` to summarize tasks worked on in a given day, to make JIRA time logs easier

statistics

add `fill_calendar` functionality
    * suggest how-best to allocate my time
    * estimate what date I will complete all my todo items 
    * group semantically similar items (e.g. "work on OneDash" should occur right before "OneDash Office Hours" so it's fresh in my head, and to minimize "switching gears")

utility script to walk thru a source code directory and add these TODO comments to the database! And supplement them with info about where they were found!

Add function to list available tags

Add a Tags collection so we can persist Tag foreground/background colors

todo list should default to in-progress
        * --all flag option should allow users to view all todos

function to view current status (e.g. timer showing elapsed time on `IN_PROGRESS` todos)

I should be able to pipe long-running command results to a Slack message
    * e.g. Slack the output of Nimbus deploy to San/Krishna without requiring me to watch the terminal and use Slack manually


Add time-tracking/hour-logging functionality behind a feature flag
    * pushes logged time to Jira, Github, or any other time tracking software

Get more ideas from todotxt
    * http://todotxt.org/

