import sys
import os
import json
from argparse import ArgumentParser
from datetime import datetime
from tabulate import tabulate


def main():
    pass
    tasks = init_task_json()
    print(tasks)


def parse_command():
    parser = ArgumentParser(prog='taskctl', description='Task Tracker')
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('task', help='Task to execute command on')
    parser.add_argument('--start', help='Start time of task')
    parser.add_argument('--end', help='End time of task')
    parser.add_argument('--duration', help='Duration of task')
    parser.add_argument('--status', help='Status of task')
    parser.add_argument('--note', help='Note of task')
    parser.add_argument('--list', help='List all tasks', action='store_true')
    parser.add_argument('--delete', help='Delete task', action='store_true')
    parser.add_argument('--clear', help='Clear all tasks', action='store_true')
    args = parser.parse_args()
    return args


def init_task_json():
    if not os.path.exists('tasks.json'):
        with open('tasks.json', 'w') as f:
            json.dump([], f)
    else:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            if not isinstance(tasks, list):
                raise ValueError("Invalid task data format")
    return tasks


if __name__ == '__main__':
    main()
