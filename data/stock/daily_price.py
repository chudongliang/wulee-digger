import json
import datetime

class DailyPrice(object):

    def __init__(self,id , date , open):
        self.id = id
        self.date = date
        self.open = open

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, str):
            if len(value) == 6 and value.isdigit():
                self._id = value
            else:
                raise ValueError('id has to be a six digit')
        else:
            raise ValueError('id has to be a string')

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if isinstance(value, datetime.datetime):
            if value < datetime.datetime(1990, 1, 1):
                raise ValueError('daily price data has to be greater than 1990.1.1')
            else:
                self._date = value
        else:
            raise ValueError('daily price data has to be datetime')

    @property
    def open(self):
        return self._open

    @open.setter
    def open(self, value):
        if isinstance(value, (int, float)):
            if isinstance(value, float):
                if len(str(value).split('.')[1]) > 3:
                    raise ValueError('max 3 precision for a price')
        else:
            raise ValueError('open price has to be a float')
        self._open = value

#json_encoded_user = json.dumps(
#    pos,
#    default=json_util.default
#)

#def datetime_handler(x):
#    if isinstance(x, datetime.datetime):
#        return x.isoformat()
#    raise TypeError("Unknown type")

#json_encoded_user = json.dumps(pos, default=datetime_handler)


#print(json_encoded_user)