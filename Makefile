TODO_ID := $(shell eval python3 todos/main.py add \"Create and start a todo\" | cut -d " " -f 3 | sed 's/[\#:]//g')

d:
	# @echo $(TODO_ID)
	python3 todos/main.py start $(TODO_ID)
