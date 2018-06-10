class CSControl:

### Utility module for reading and writing Yamaha Reface CS synthesizer
### tone generator settings via MIDI.
### (C) Carl-Fredrik Enell 2018

    ## There are several MIDI implementations for Python.
    ## MIDO seemed to be the most versatile.
    ## Note that MIDO is a frontend that requires an actual backend
    ## such as portmidi, rtmidi or pygames.
    import mido
        
    def __init__(self,channel):

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
    def csread(self):
        pass #FIXME

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

        
