
import matplotlib.pyplot as plt
import numpy

slaq90 = [1.2375, 1.4125, 2.4625, 4, 5.98, 7.98]
noslaq90 = [8.45, 7.2875, 6.5875, 4.4875, 6, 8]

slaq95 = [2.5875, 2.3375, 3.4625, 4.0125, 5.9875, 7.9875]
noslaq95 = [8.5, 7.325, 7.0375, 4.9875, 6.0215, 8.0125]

mean_arr_time = [0.5, 1, 2, 4, 6, 8]

fig, (ax1, ax2) = plt.subplots(1,2, sharex=True)
l1,= ax1.plot(mean_arr_time, slaq90, '-r^', label='SLAQ')
l2,= ax1.plot(mean_arr_time, noslaq90, '-go', label='Fair Resource')
ax1.grid(True)
ax1.set_xlim(0.1, 8.5)
ax1.set_ylim(0, 9.5)
ax1.set_xlabel("Mean Job Arrival Time (s)")
ax1.set_ylabel("Time to Reach 90% (s)")

l3,= ax2.plot(mean_arr_time, slaq95, '-r^')
l4,= ax2.plot(mean_arr_time, noslaq95,'-go')
ax2.grid(True)
ax2.set_xlim(0.1, 8.5)
ax2.set_ylim(0, 9.5)
ax2.set_xlabel("Mean Job Arrival Time (s)")
ax2.set_ylabel("Time to Reach 95% (s)")

fig.legend((l1, l2),  ('SLAQ', 'Fair Resources'), 'upper center')
plt.show()
