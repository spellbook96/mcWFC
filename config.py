import json
import os


class Config:
    setting = {}
    path = ""

    def __init__(self, path="config.json"):
        self.path = path
        try:
            f = open(path, "r", encoding="utf-8")
            self.setting = json.loads(f.read())
            f.close()
        except Exception as e:
            print("config.json error",e)


    def setKey(self, key, value=None):
        self.setting[key] = value
        self.save()

    def getKey(self, key):
        try:
            return self.setting[key]
        except KeyError:
            return None

    def delKey(self, key):
        try:
            del self.setting[key]
        except KeyError:
            pass
        self.save()

    def save(self):
        settingstr = json.dumps(self.setting, sort_keys=True, indent=4, separators=(",", ":"))
        f = open(self.path, "w", encoding="utf-8")
        f.write(settingstr)
        f.close()


if __name__ == "__main__":
    config = Config()
    print(config.getKey("tree"))
    tree = config.getKey("tree")
    print(tree[1])