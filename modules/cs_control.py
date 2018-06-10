class CSControl:

### Utility module for reading and writing Yamaha Reface CS synthesizer
### tone generator settings via MIDI.
### (C) Carl-Fredrik Enell 2018

    ## There are several MIDI implementations for Python.
    ## MIDO seemed to be the most versatile.
    ## Note that MIDO is a frontend that requires an actual backend
    ## such as portmidi, rtmidi or pygames.
    import mido
        
    def __init__(self,channel=0):

        ## Reface CS MIDI implementation configurations.
        ## See the MIDI implementation manual, available online.
        ## <find the URL>
        
        # Dict of Reface CS tone generator controls.
        # NB. There are two ways to control the tone generator:
        # Control Change and SysEx messages.
        # Using Control Change messages here. This requires
        # MIDI control to be enabled- see the Reface manual.
        self.sound_control = {
            'LFOAssign'   : 78,
            'LFODepth'  : 77,
            'LFOSpeed'  : 76,
            'Portamento': 20,
            'OSCType'   : 80,
            'OSCTexture': 81,
            'OSCMod'    : 82,
            'FILTERCutoff'   : 74,
            'FILTERResonance': 71,
            'EGBalance': 83,
            'EGA'      : 73,
            'EGD'      : 75,
            'EGS'      : 79,
            'EGR'      : 72,
            'EFFECTType'     : 17,
            'EFFECTDepth'    : 18,
            'EFFECTRate'     : 19,
        }

        # Reface CS LFO assignments
        self.lfo_assign = {
            'OFF': 0,
            'AMP': 32,
            'FILTER': 64,
            'PITCH': 95,
            'OSC': 127,
        }

        self.lfo_return = {
            0: 'OFF',
            1: 'AMP',
            2: 'FILTER',
            3: 'PITCH',
            4: 'OSC'
        }
        
        # Reface CS oscillator types
        self.osc_type = {
            'SAW'  : 0,
            'PULSE': 32,
            'SYNC' : 64,
            'RING' : 95,
            'FM'   : 127
        }

        self.osc_return = {
            0: 'SAW',
            1: 'PULSE',
            2: 'SYNC',
            3: 'RING',
            4: 'FM'
        }

        # Reface CS effect types
        self.eff_type = {
            'DIST'   : 0,
            'CHO_FLA': 32,
            'PHASER' : 64,
            'DELAY'  : 95,
            'OFF'    : 127
        }

        self.eff_return = {
            0:'DIST',
            1:'CHO_FLA',
            2:'PHASER',
            3:'DELAY',
            4:'OFF'
        }



        ## Enumerate devices
        if ('reface CS MIDI 1' in self.mido.get_input_names()):
            self.Input=self.mido.open_input('reface CS MIDI 1')
        else:
            raise IOError('No Reface device found!')

        if ('reface CS MIDI 1' in self.mido.get_output_names()):
            self.Output=self.mido.open_output('reface CS MIDI 1')
        else:
            raise IOError('No Reface device found!')
      
        # store selected MIDI channel no
        self.channel=channel
        
    ### Main in and out functions        
    def csreadsysex(self,request):

        count=1
        msg=self.mido.Message('sysex',data=request)
        
        while True:

            if (count%100==0):
                #Retry request
                self.Output.send(msg)

            # Get reply
            msg_in=self.Input.receive()
            if msg_in.type=='sysex':
                if msg_in.data[0:11]  == tuple((67, 0, 127, 28, 0, 4, 3, 14, 15, 0, 96)):
                    # Header
                    pass
                elif msg_in.data[0:11] == tuple((67, 0, 127, 28, 0, 4, 3, 15, 15, 0, 95)):
                    # Footer
                    break
                else:
                    settings=list(msg_in.data)
                    
            count=count+1
        
        return settings

    def csreadsound(self):

        # Sysex tone generator dump request
        dumpreq=[0x43,0x20,0x7F,0x1C,0x03,0x0E,0x0F,0x00]   
        dump=self.csreadsysex(dumpreq)
        dump=dump[12:] # Sound settings
 
        # Build sound dict
        sound_dict={}
        for controlname in ['LFOAssign',  
                            'LFODepth',
                            'LFOSpeed',
                            'Portamento',
                            'OSCType',
                            'OSCTexture',
                            'OSCMod',
                            'FILTERCutoff',
                            'FILTERResonance',
                            'EGBalance',
                            'EGA',
                            'EGD', 
                            'EGS', 
                            'EGR', 
                            'EFFECTType', 
                            'EFFECTDepth',
                            'EFFECTRate']:

            value=int(dump.pop(0))

            # Map possible values
            if (controlname=='LFOAssign'):
                value=self.lfo_return[value]
            
            elif (controlname=='OSCType'):
                value=self.osc_return[value]
                
            elif (controlname=='EFFECTType'):
                value=self.eff_return[value]  
        
            sound_dict[controlname]=value

        return self.channel, sound_dict
    
    def cswrite(self,sound_dict):
        ## Write a dictionary of sound parameters to Yamaha Reface CS
    
        msg=self.mido.Message('control_change')
        msg.channel=self.channel
        
        for (controlname, value) in sound_dict.iteritems():

            # Check values
            if (controlname=='LFOAssign'):
                value=self.lfo_assign[value]
            elif (controlname=='OSCType'):
                value=self.osc_type[value]
            elif (controlname=='EFFECTType'):
                value=self.eff_type[value]
            else:
                value=int(value)
            assert value in range(0,128) # Byte value 0..127
            
            msg.control=self.sound_control[controlname]
            msg.value=value

            try:
                self.Output.send(msg)
            except:
                raise IOError('Could not write to Reface CS device')


    def __enter__(self):
        return self

    def __exit__(self):
        self.Input.close()
        self.Output.close()

        
