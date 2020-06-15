def fill_todos(todos):
    for todo in todos:
        estimated_duration = todo.estimate_in_hours
        if self.has_free_time_block(estimated_duration):
            self.add_event(CalendarEvent(**todo))
