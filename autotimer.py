from __future__ import print_function
import time
from os import system
from activity import *
import json
import datetime
import sys
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *
elif sys.platform in ['linux', 'linux2']:
        import linux as l

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]

def category (activity_name):
    cat = ['Others','Google Chrome', 'Visual Studio Code']
    counter = -1
    for x in cat: 
        counter += 1
        if x in activity_name:
            return counter
        
    return 0
        
        
def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)

        #  had to do this due to telegram creating multiple instance of its self with (1), (2)
        if "Telegram" in _active_window_name:
            _active_window_name = "Telegram"

    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        _active_window_name = (NSWorkspace.sharedWorkspace()
                               .activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)

    return _active_window_name


def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        textOfMyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
        s = NSAppleScript.initWithSource_(
            NSAppleScript.alloc(), textOfMyScript)
        results, err = s.executeAndReturnError_(None)
        return results.stringValue()
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name

try:
    activeList.initialize_me()
except Exception:
    print('No json')


try:
    while True:
        previous_site = ""
        if sys.platform not in ['linux', 'linux2']:
            new_window_name = get_active_window()

            if 'Google Chrome' in new_window_name:
                new_window_name = url_to_name(get_chrome_url()) + " - Google Chrome"


        if sys.platform in ['linux', 'linux2']:
            new_window_name = l.get_active_window_x()
            if 'Google Chrome' in new_window_name:
                new_window_name = l.get_chrome_url_x() + " - Google Chrome"

        
        if active_window_name != new_window_name:
            print(active_window_name)
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        print(time_entry.total_time)
                        activity.total_time += time_entry.total_time
                        activity.time_entries.append(time_entry)

                if not exists:

                    group_name = category(activity_name)
                    total_time = time_entry.total_time
                    activity = Activity(group_name, activity_name,total_time, [time_entry])
                    activeList.activities.append(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name

        time.sleep(1)
    

    
except KeyboardInterrupt:
    with open('activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
