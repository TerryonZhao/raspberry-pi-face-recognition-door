import bluetooth
import time
 
def servo_init():#初始化指令
	bd_addr = "00:23:07:34:C5:05" #arduino连接的蓝牙模块的地址
	port = 1
	 
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port)) #创建连接
	 
	sock.send("1") #发送数据
	sock.close()  #关闭连接
	
def bt_open():#开门指令
	bd_addr = "00:23:07:34:C5:05" 
	port = 1
	 
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port)) 
	 
	sock.send("2") 
	sock.close()  

def bt_close():#关门指令
	bd_addr = "00:23:07:34:C5:05" 
	port = 1
	 
	sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM )
	sock.connect((bd_addr, port)) 
	 
	sock.send("3") 
	sock.close()
	
if __name__ == "__main__":
    print('close')
    bt_close()
    time.sleep(3)
    print('open')
    bt_open()


