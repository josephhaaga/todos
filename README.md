# todo
Simple command line utility to track tasks.

```sh
$ todo add "clean up README"
Created task #9
Inserted TODO #9: clean up README 

$ todo start 9
Started #9 clean up README @est(1.0h)

$ todo show
#1 complete tag functionality @est(1.0h)
#4 Add pre-commit @est(1.0h)
#5 fill_calendar() @est(1.0h)
#6 Log Shape idea @est(1.0h)
#7 add note functionality @est(1.0h)
#8 update README @est(1.0h)

$ todo get 9 

        #9 clean up README
            status: IN_PROGRESS
            estimate: 1.0h
            inserted: 2020-05-05
            location: /Users/josephhaaga/Documents/code/todo-app
        
$ todo complete 9
Finished #9 clean up README @est(1.0h)

$ todo get 9

        #9 clean up README
            status: COMPLETED
            estimate: 1.0h
            inserted: 2020-05-05
            location: /Users/josephhaaga/Documents/code/todo-app
        

```

## Usage
```sh
$ todo
Usage: app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add       Add a task to the database.
  complete  Finish working on a task.
  delete    Delete a task.
  estimate  Set the time estimate for a task.
  get
  now
  show
  start     Start working on task.
  then      Suggests tasks to work on next.
```


## Planned Features
* Metrics like work done, remaining work todo, and productivity per day.
* Auto-fill calendar with suggested todos to take advantage of idle time.

