import json

#parameters are the value you want to log and the name is a term used to refer to the value
def write(name, value, logFile="log.json"):
    writeData = {}
    writeData[name] = value
    with open(logFile, 'r+') as f:
        data = json.load(f)
        data.update(writeData)
        f.seek(0)
        json.dump(data, f)
    print('%s, %s' % (name, value))

#writes to a value in an object inside of the log file (e.g. "test": {"num": 12, "string": "Hello World"}  log.subWrite("test", "num", 41))
def subWrite(name, subName, value, logFile="log.json"):
    val = read(name, logFile)
    val[subName] = value
    write(name, val, logFile)

def read(name, logFile="log.json"):
    with open(logFile, 'r') as f:
        try:
            return json.load(f)[name]
        except Exception as e: 
            # print(e)
            print("Value not found")
        
def delete(name, logFile="log.json"):
    with open(logFile, 'r') as data_file:
        data = json.load(data_file)

    data.pop(name, None)

    with open(logFile, 'w') as data_file:
        data = json.dump(data, data_file)