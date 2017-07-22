#!/usr/bin/env python3

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator

from pylab import *

import logging
logger = logging.getLogger(__name__)


def plot_gantt(fig, ax, data):
    for worker_id, worker_activites in data.items():
        left = 0
        for activity in worker_activites:
            if activity.source.earlyStart > left:
                left = activity.source.earlyStart

            # Get label with character limit
            name = activity.name[0:min(15, len(activity.name))]

            ax.barh((worker_id*1)+0.5, activity.duration, height=1, left=left, align='center', color='blue', edgecolor='black', linewidth=2, tick_label='bannaa')
            label = ax.text(left + (activity.duration/2), (worker_id*1)+0.5, name, verticalalignment='center', horizontalalignment='center', rotation=90)


            left += activity.duration

    # Format the y-axis
    ax.set_ylabel('Worker')
    ax.set_yticks([i+0.5 for i in data.keys()])
    ax.set_yticklabels(['worker %i' % (i+1) for i in data.keys()], rotation=90)
    ax.invert_yaxis()

    # Format grid
    ax.grid(color = 'g', linestyle = ':')

    ax.set_title('Schedule')
    ax.set_xlabel('Time (hours)')
