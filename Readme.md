
#Running basic patterns
1. Put `rpi_neopixels.py` on a raspberry pi
2. Edit `rpi_neopixels.py` and scroll to the bottom. Uncomment a function to run the pattern
3. Ensure that DEVELOPER_MODE in `rpi_neopixels.py` is set to `False`

#Running a sound Visualizer (Windows + RPi)
1. Put `rpi_neopixels.py` on a raspberry pi
2. Edit `rpi_neopixels.py` and scroll to the bottom. Uncomment one of the `run_visualiser` functions
3. Take note of the local ip adress of the RPi (This can be found by typing `ifconfig` in a terminal)

4. Put `pc_sound_stream.py` on a Windows Machine
5. Edit `pc_sound_stream.py` and set IP_ADDRESS to the ip of the RPi
6. Run the python script on the RPi and then the one on the pc.


By default sound is sampled from the microphone. If you want to get music directly from your computer you have 2 choices:
	A: Use "Stereo Mix" as your microphone so your computer sounds are piped to your microphone
		1. Control Panel > Hardware and Sound > Sound > Recording
		2. Right Click on any device and make sure "Show Disabled Devices" is checked
		3. If the "Stereo Mix" device is greyed out and marked as Disabled, right click it and select Enable
		4. Select "Stereo Mix" and press the "Set Default" button
		
		You computer sounds should now be passed through to your microphone. 
		If Stereo Mix does not exist for you or does not seem to work, your soundcard might not support it.
		
	B: Use a program such as Voice Meeter [https://www.vb-audio.com/Voicemeeter/index.htm]
		This method is more complex but my personal preference. Voice Meeter allows you to take control of audio inputs and outputs.
		 
		