import math
import random
import matplotlib.pyplot as plt
import numpy

# class generator(object):
# 	def __init__(self):
# 		self.data = [];
# 		self.time = [];

# class generatorSinWithoutNoise(generator):
# 	def __init__(self, freq, time_step, num_periods):\
# 		self.freq = freq;
# 		self.period = 1/freq;
# 		self.time_step = time_step;
# 		self.num_periods = num_periods;

# 	def generate():
# 		for i in range(math.ceil(self.num_periods * self.period / self.time_step)):
# 			self.data.append(math.sin(2 * 3.14 * self.freq * i * self.time_step));
# 			self.time.append(i * self.time_step);
# 		A = (self.data, self.time);
# 		return A;

def generate(ampl, freq, time_step, num_period):
	data = [];
	time = [];
	period = 1/freq;
	for i in range(math.ceil(num_period * period / time_step)):
		data.append(ampl * math.sin(2 * 3.14 * freq * i * time_step));
		time.append(i * time_step);
	return (data, time);

def generateWithNoise(ampl, freq, time_step, num_period, m, D):
	tmp = generate(ampl, freq, time_step, num_period);
	period = 1/freq;
	for i in range(len(tmp[0])):
		tmp[0][i] += random.gauss(m, math.sqrt(D));
	return (tmp[0], tmp[1]);

def timeUp(data, time_step, lvl):
	res = [];
	for i in range(1, len(data)):
		if ((abs(data[i]) > lvl) and (abs(data[i - 1])) <= lvl):
			res.append(i * time_step);
	return res;

def timeDown(data, time_step, lvl):
	res = [];
	for i in range(len(data) - 1):
		if ((abs(data[i]) > lvl) and (abs(data[i + 1])) <= lvl):
			res.append(i * time_step);
	return res;

def jOperate(data, a, I_max):
	for i in range(len(data)):
		if (abs(data[i]) >= I_max):
			data[i] *= a;
		else:
			data[i] = 0;
	return data;

def timeToCurrent(data, ampl, freq):
	for i in range(len(data)):
		data[i] = abs(ampl * math.sin(2 * 3.14 * freq * data[i]));
	return data;

def averageCurrent(data):
	return numpy.mean(data);

ampl = 2; # V
num_period = 5;
freq = 10; # Hz
time_step = 0.0001 # sec
period = 1/freq; # sec

data = generateWithNoise(ampl, freq, time_step, num_period, 0, 0.02);
data2 = generate(ampl, freq, time_step, num_period);

I_max = 0.5;
a = 1;
lvl = 0.05;

jOperate(data[0], a, I_max);

plt.plot(data[1], data[0]);
plt.plot(data2[1], data2[0]);
plt.grid();
plt.show();

times_up = timeUp(data[0], time_step, 0.05);
times_down = timeDown(data[0], time_step, 0.05);

print('currentUp', averageCurrent(timeToCurrent(times_up, ampl, freq)));
print('currentDown', averageCurrent(timeToCurrent(times_down, ampl, freq)));

# plt.plot(time, sin_data);
# plt.grid();
# plt.show();