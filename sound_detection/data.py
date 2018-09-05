# script responsible for generating audio sample of specific sounds waves.  Supports
# exporting those samples to WAV files for confirmation.

from __future__ import division

import numpy as np
import os
import json
import operator
import random
import time
import math
import wave

import signal
import time

import scipy.io.wavfile

class SoundGenerator():
	
	def __init__(self,volume,duration,sampleRate):
		self.volume = volume
		self.duration = duration
		self.sampleRate = sampleRate
		self.freq = self.sampleRate / 100
		
	def generateSinSound(self):
		input = ( np.sin( 2 * np.pi * np.arange(self.sampleRate*self.duration) * self.freq / self.sampleRate ) * self.volume).astype(np.float32)
		output = np.array([0,1])
		return input,output
	
	def generateSilenceSound(self):
		input = (np.zeros(int(self.sampleRate*self.duration) )).astype(np.float32)
		output = np.array([1,0])
		return input,output
	
	def generateNoiseSound(self):
		input = ( (np.random.uniform(-1.0,1.0,int(self.sampleRate*self.duration)) ) * self.volume).astype(np.float32)
		output = np.array([1,0])
		return input,output
	
	def generateSounds(self,num):
		input_sounds = np.zeros((num,int(self.sampleRate*self.duration)), dtype='float32')
		output_sounds = np.zeros((num,2), dtype='float32')
		
		soundGenerators = [
			self.generateSinSound, 
			self.generateSilenceSound, 
			self.generateNoiseSound]
		
		for i in range(0,num):
			input,output = random.choice(soundGenerators)()
			np.copyto(input_sounds[i],input)
			np.copyto(output_sounds[i],output)
		
		return input_sounds,output_sounds
	
	def saveSoundToFile(self,filename,input):
		scipy.io.wavfile.write(filename,self.sampleRate,input)
		

if __name__ == '__main__':
		
	generator = SoundGenerator(0.2, 1.0, 44100.0)
	input_sounds,output_sounds = generator.generateSounds(10)
	
	for i in range(0,len(input_sounds)):
		generator.saveSoundToFile("/tmp/generated%d.wav" % (i), input_sounds[i])
	
	