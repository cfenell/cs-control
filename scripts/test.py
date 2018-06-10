#! /usr/bin/python



import mido
mo=mido.open_output('reface CS MIDI 1')
mi=mido.open_input('reface CS MIDI 1')

#
# Sysex tone generator dump request
dumpreq=[0x43,0x20,0x7F,0x1C,0x03,0x0E,0x0F,0x00]
msg=mido.Message('sysex',data=dumpreq)

mo.send(msg)
count=0

while True:
    if count==100:
        #Retry
        mo.send(msg)
    msg=mi.receive()
    if msg.type=='sysex':
        if msg.data[0:11]  == tuple((67, 0, 127, 28, 0, 4, 3, 14, 15, 0, 96)):
            # Header
            pass
        elif msg.data[0:11] == tuple((67, 0, 127, 28, 0, 4, 3, 15, 15, 0, 95)):
            # Footer
            break
        else:
            dump=msg.data
    count=count+1
            
print(dump)


