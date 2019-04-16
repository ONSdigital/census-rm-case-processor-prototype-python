class BaseReceiver:
    event_type = None

    def __init__(self, message_processor):
        self.message_processor = message_processor
        super().__init__()

    @classmethod
    def get_event_type(cls):
        if not cls.event_type:
            raise Exception('event_type must be declared on all event receivers')
        return cls.event_type
