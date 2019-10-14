import pymongo
import bson
import time

from pydantic import BaseModel
from typing import Dict, Any, Optional

from .constants import *

class Log(BaseModel):
    t: float            # 日志时间戳
    l: int              # 日志级别
    o: Dict[str, Any]   # 日志内容

class LogInDB(Log):
    _id: bson.ObjectId  # oid

class Logger(object):

    def __init__(self, url="mongodb://root:example@localhost:27017/", database="logging", collection="log", level: int=INFO, size: int=20000000000, capped: bool=True):
        self.url = url
        self.databaseName = database
        self.collectionName = collection
        self.size = size
        self.capped = capped
        self.level = level
        
    def getLevelName(self, level: int) -> Optional[str]:
        if level == 0:
            return "NOTSET"
        elif level == 10:
            return "DEBUG"
        elif level == 20:
            return "INFO"
        elif level == 30:
            return "WARNING"
        elif level == 40:
            return "ERROR"
        elif level == 50:
            return "CRITICAL"
        else:
            return None

    def getLogCollection(self) -> pymongo.collection.Collection:
        client = pymongo.MongoClient(self.url)
        db = client[self.databaseName]
        if self.capped:
            try:
                collcetion = db.create_collection(self.collectionName, capped=True, size=self.size)
                collcetion.create_index('t')
                collcetion.create_index('l')
            except pymongo.errors.CollectionInvalid:
                return db[self.collectionName]
            else:
                return collcetion
        else:
            return db[self.collectionName]

    def log(self, message, level: int=NOTSET):
        if isinstance(message, str):
            data = {
                'msg': message
            }
        elif isinstance(message, dict):
            data = message
        else:
            return 

        c = self.getLogCollection()
        if self.getLevelName(level) is not None and level >= self.level:
            c.insert_one({
                't': time.time(),
                'l': level,
                'o': data
            })

    def debug(self, message):
        self.log(message, level=DEBUG)

    def info(self, message):
        self.log(message, level=INFO)

    def warning(self, message):
        self.log(message, level=WARNING)

    def error(self, message):
        self.log(message, level=ERROR)

    def critical(self, message):
        self.log(message, level=CRITICAL)

    def get(self, level: int=NOTSET, since: Optional[float]=None, latest: Optional[int]=None, exact: bool=False):
        c = self.getLogCollection()
        if since is None:
            if exact:
                logs = c.find({
                    'l': level
                }, sort=[(
                    '$natural', -1
                )])
            else: 
                logs = c.find({
                    'l': {
                        '$gt': level
                    }
                }, sort=[(
                    '$natural', -1
                )])
        else:
            if exact:
                logs = c.find({
                    't': since,
                    'l': {
                        '$gt': level
                    }
                }, sort=[(
                    '$natural', -1
                )])
            else:
                logs = c.find({
                    't': {
                        '$gt': since
                    },
                    'l': {
                        '$gt': level
                    }
                }, sort=[(
                    '$natural', -1
                )])
        if latest is None or latest <= 0:
            logModels = [LogInDB(**log) for log in logs]
        else:
            logModels = [LogInDB(**log) for log in logs[:latest]]

        return logModels
    
