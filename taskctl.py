import sys
import os
import json
from datetime import datetime
from argparse import ArgumentParser
from datetime import datetime
from tabulate import tabulate


def main():
    try:
        tasks = init_task_json()
    except:
        print("Error initializing task JSON file.")
        raise
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
                raise ValueError("Invalid task list data format")
            isValidTasks = [is_valid_task(task) for task in tasks]
            if not all(isValidTasks):
                raise ValueError("Invalid task data format found in the list")
            task_ids = [task['id'] for task in tasks]
            if len(task_ids) != len(set(task_ids)):
                raise ValueError("Duplicate task IDs found")
            if sorted(task_ids) != task_ids:
                raise ValueError("Task IDs are not sorted")  # Could be warning
    return tasks


def is_valid_task(task):
    if not isinstance(task, dict):
        return False
    else:
        required_keys = ['id', 'description',
                         'status', 'createdAt', 'updatedAt']
        contains_required_keys = all(
            [key in required_keys for key in task.keys()])
        if not contains_required_keys:
            return False
        try:
            datetime.fromisoformat(task['createdAt'])
            datetime.fromisoformat(task['updatedAt'])
        except:
            raise
        return True


def parse_obj(taskDict):
    if isinstance(taskDict, dict):
        return {k: parse_obj(v) for k, v in taskDict.items()}
    else:
        raise ValueError("Invalid task data format")


if __name__ == '__main__':
    main()
