class Event:
    def __init__(self, timestamp, event_type, cpu_id, tid, prio,  content):
        self.event_type = event_type
        self.timestamp = timestamp
        self.cpu_id = cpu_id
        self.tid = tid
        self.prio = prio
        self.content = content

    def __str__(self):
        return f"Timestamp: {self.timestamp}, Event(Type: {self.event_type}, CPU_ID: {self.cpu_id}, TID: {self.tid}, PRIO: {self.prio}, Content: {self.content})"