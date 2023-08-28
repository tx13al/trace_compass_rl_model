class Syscall:
    def __init__(self, event_type, cpu_id, tid, prio, parsed_start_time, parsed_end_time, start_time, end_time, content):
        self.event_type = event_type
        self.cpu_id = cpu_id
        self.tid = tid
        self.prio = prio
        self.content = content
        self.parsed_start_time = parsed_start_time
        self.parsed_end_time = parsed_end_time
        self.start_time = start_time
        self.end_time = end_time
        self.duration = parsed_end_time - parsed_start_time
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def __str__(self):
        return f"Event Type: {self.event_type}, CPU ID: {self.cpu_id}, TID: {self.tid}, PRIO: {self.prio}, Start_time: {self.start_time}, End_time: {self.end_time}, Duration: {round(self.duration)}, Content:{self.content}"
