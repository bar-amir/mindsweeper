from datetime import datetime
import struct

class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought
    
    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'
    
    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'
        
    def __eq__(self, other):
        return isinstance(other, Thought) and \
        self.user_id == other.user_id and \
        self.timestamp == other.timestamp and \
        self.thought == other.thought
        
    def serialize(self):
        en_thought = self.thought.encode()
        ts = int(self.timestamp.timestamp())
        return struct.pack("<QQI%ds" % (len(en_thought),), self.user_id, ts, len(en_thought), en_thought)
    
    def deserialize(data):
        user_id, ts, t_len = struct.unpack('<QQI', data[:20])
        thought = struct.unpack('<%ds' % (t_len,), data[20:])[0].decode()
        timestamp = datetime.fromtimestamp(ts)
        return Thought(user_id, timestamp, thought)
