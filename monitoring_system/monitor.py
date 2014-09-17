
class Postman():
    def __init__(self,user = 'openstack',password = 'f771926707300b7eeaf58d42',\
                    ip = '192.168.10.20',port = 5672):
        import pika 
        credentials = pika.PlainCredentials(user,password)
        parameters = pika.ConnectionParameters(ip,port,'/',credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='mainboard',
                        type='direct')
    def __del__(self):
        self.connection.close()

    def send(self,severity,msg):
        import json
        data = json.dumps(msg)
        self.channel.basic_publish(exchange='mainboard',
                      routing_key=severity,
                      body=data)


if __name__ == '__main__':
    from machineinfo.MachineInfo import MachineInfo as mf
    from time import sleep
    bearer = Postman()
    minfo = mf()
    while True:
        m = minfo.GetStats()
        bearer.send("load",m)
        sleep(5)


