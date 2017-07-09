#!/usr/bin/env python3

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator

from pylab import *

import logging
logger = logging.getLogger(__name__)

def create_date(month,year):
    """Creates the date"""

    date = dt.datetime(int(year), int(month), 1)
    mdate = matplotlib.dates.date2num(date)

    return mdate


def test_data():
    # Data
    pos = arange(0.5,5.5,0.5) # TODO what is this?

    ylabels = []
    ylabels.append('Hardware Design & Review')
    ylabels.append('Hardware Construction')
    ylabels.append('Integrate and Test Laser Source')
    ylabels.append('Objective #1')
    ylabels.append('Objective #2')
    ylabels.append('Present at ASMS')
    ylabels.append('Present Data at Gordon Conference')
    ylabels.append('Manuscripts and Final Report')

    effort = []
    effort.append([0.2, 1.0])
    effort.append([0.2, 1.0])
    effort.append([0.2, 1.0])
    effort.append([0.3, 0.75])
    effort.append([0.25, 0.75])
    effort.append([0.3, 0.75])
    effort.append([0.5, 0.5])
    effort.append([0.7, 0.4])

    customDates = []
    customDates.append([create_date(5,2014),create_date(6,2014)])
    customDates.append([create_date(6,2014),create_date(8,2014),create_date(8,2014)])
    customDates.append([create_date(7,2014),create_date(9,2014),create_date(9,2014)])
    customDates.append([create_date(10,2014),create_date(3,2015),create_date(3,2015)])
    customDates.append([create_date(2,2015),create_date(6,2015),create_date(6,2015)])
    customDates.append([create_date(5,2015),create_date(6,2015),create_date(6,2015)])
    customDates.append([create_date(6,2015),create_date(7,2015),create_date(7,2015)])
    customDates.append([create_date(4,2015),create_date(8,2015),create_date(8,2015)])

    task_dates = {}
    for i,task in enumerate(ylabels):
        task_dates[task] = customDates[i]
        # task_dates['Climatology'] = [create_date(5,2014),create_date(6,2014),create_date(10,2013)]
        # task_dates['Structure'] = [create_date(10,2013),create_date(3,2014),create_date(5,2014)]
        # task_dates['Impacts'] = [create_date(5,2014),create_date(12,2014),create_date(2,2015)]
        # task_dates['Thesis'] = [create_date(2,2015),create_date(5,2015)]

    return (ylabels, effort, task_dates, pos)

def plot_gantt(fig, ax, data):
    # Plot the data

    # data = {
    #   0: [{'duration': 3, 'earlyStart': 0}, {'duration': 3, 'earlyStart': 0}, {'duration': 4, 'earlyStart': 12}, {'duration': 4, 'earlyStart': 19}],
    #   1: [{'duration': 3, 'earlyStart': 0}, {'duration': 3, 'earlyStart': 0}, {'duration': 4, 'earlyStart': 12}, {'duration': 4, 'earlyStart': 19}]
    # }


    for worker_id, worker_activites in data.items():
        left = 0
        for activity in worker_activites:
            if activity.source.earlyStart > left:
                left = activity.source.earlyStart

            ax.barh((worker_id*1)+0.5, activity.duration, height=1, left=left, align='center', color='blue', edgecolor='black', linewidth=2)

            left += activity.duration


    # for i in range(0,len(ylabels)):
    #     ax.barh(i*1, 3, height=1, left=2, align='center', color='blue', edgecolor='black', linewidth=2)

    # Format the y-axis

    # locsy, labelsy = yticks(pos,ylabels)
    # plt.setp(labelsy, fontsize = 14)
    #ax.set_yticklabels(pos,ylabels)

    # Format the x-axis
    #ax.axis('tight')
    # ax.set_ylim(ymin = -0.1, ymax = 4.5)
    ax.grid(color = 'g', linestyle = ':')

    #ax.xaxis_date() #Tell matplotlib that these are dates...

    # rule = rrulewrapper(MONTHLY, interval=1)
    # loc = RRuleLocator(rule)
    # formatter = DateFormatter("%b '%y")

    # ax.xaxis.set_major_locator(loc)
    # ax.xaxis.set_major_formatter(formatter)
    # labelsx = ax.get_xticklabels()
    # plt.setp(labelsx, rotation=30, fontsize=12)

    # Format the legend
    # font = font_manager.FontProperties(size='small')
    # ax.legend(loc=1,prop=font)

    # Finish up
    ax.invert_yaxis()
    fig.autofmt_xdate()
