class CSControl:

### Utility module for reading and writing Yamaha Reface CS synthesizer
### tone generator settings via MIDI SysEx
### (C) Carl-Fredrik Enell 2018

    ## There are several MIDI implementations for Python.
    ## PyGame selected here since it is commonly available.
    from pygame import midi
    
    
    def __init__(self,channel):

        ## Reface CS MIDI implementation configurations.
        ## See the MIDI implementation manual, available online.
        ## <find the URL>
        
        # Dict of Reface CS tone generator controls.
        # NB. There are two ways to control the tone generator:
        # 1. MIDI Control Change message- works only when MIDI Control is enabled
        # 2. SysEx MIDI parameter
        # Usinv Control Change here, so make sure MIDI control is ON.
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

        # Reface CS oscillator types
        self.osc_type = {
            'SAW'  : 0,
            'PULSE': 32,
            'SYNC' : 64,
            'RING' : 95,
            'FM'   : 127
        }

        # Reface CS effect types
        self.eff_type = {
            'DIST'   : 0,
            'CHO_FLA': 32,
            'PHASER' : 64,
            'DELAY'  : 95,
            'OFF'    : 127
        }


        
        ## Start MIDI communication
        self.midi.init()

        ## Enumerate devices
        found_in=False
        found_out=False
        for mididev in range(self.midi.get_count()):
            (mididriver,midiname,midiin,midiout,midiopen) = self.midi.get_device_info(mididev)
            if (midiname.find('reface CS MIDI') > -1):
                if (midiin == 1):
                    self.Input=self.midi.Input(mididev)
                    found_in=True
                if (midiout == 1):
                    self.Output=self.midi.Output(mididev,0)
                    found_out=True

        if(not(found_in)):
            raise IOError('No Reface CS input device found!')

        if(not(found_out)):
            raise IOError('No Reface CS output device found!')

        # store selected MIDI channel no
        self.channel=channel
        
    ### Main in and out functions        
    def csread(self):
        pass #FIXME

    def cswrite(self,sound_dict):
        ## Write a dictionary of sound parameters to Yamaha Reface CS
       
        # Initialise message
        status=0xB0 + self.channel # Control change channel N 
        msg=[]

        # Build control message
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
                
            # message list: [[[status,control,value],timestamp],...]
            out=[[status,self.sound_control[controlname],value],0] # timestamp 0 = immediately
            msg.append(out)

        try:
            self.Output.write(msg)
        except:
            raise IOError('Could not write to Reface CS device')


    def __enter__(self):
        return self

    def __exit__(self):
        self.midi.quit()
        
