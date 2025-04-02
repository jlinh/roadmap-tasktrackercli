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
    command, args = parse_command()
    try:
        command(tasks, **vars(args))
    except:
        print("Error executing command.")
        raise


def get_supported_commands():
    return {
        'add': {
            'action': add_task,
            'help': 'Add a new task',
            'args': [
                {
                    'name': 'description',
                    'type': ascii,
                    'help': 'Description of the new task'
                }
            ]
        },
        'update': {
            'action': update_task,
            'help': 'Update an existing task',
            'args': [
                {
                    'name': 'id',
                    'type': int,
                    'help': 'ID of the task to update'
                },
                {
                    'name': 'description',
                    'type': ascii,
                    'help': 'New description of the task'
                }
            ]
        },
        'delete': {
            'action': delete_task,
            'help': 'Delete a task',
            'args': [
                {
                    'name': 'id',
                    'type': int,
                    'help': 'ID of the task to delete'
                }
            ]
        },
        'mark-in-progress': {
            'action': mark_in_progress,
            'help': 'Mark a task as in progress',
            'args': [
                {
                    'name': 'id',
                    'type': int,
                    'help': 'ID of the task to mark as in progress'
                }
            ]
        },
        'mark-done': {
            'action': mark_done,
            'help': 'Mark a task as done',
            'args': [
                {
                    'name': 'id',
                    'type': int,
                    'help': 'ID of the task to mark as done'
                }
            ]
        },
        'list': {
            'action': list_tasks,
            'help': 'List all tasks or with a specific status',
            'args': [
                {
                    'name': '--status',
                    'type': str.lower,
                    'required': False,
                    'help': 'Filter tasks by status',
                    'choices': [None, 'in-progress', 'done', 'todo'], 'default': None,
                }
            ]
        }
    }


def parse_command():
    parser = ArgumentParser(prog='taskctl', description='Task Tracker')
    subparser = parser.add_subparsers(dest='command')
    commands = get_supported_commands()
    for command, command_info in commands.items():
        command_parser = subparser.add_parser(
            command, help=command_info['help'])
        for arg in command_info['args']:
            if 'required' in arg and arg['required']:
                print(arg)
                command_parser.add_argument(
                    arg['name'], default=arg['default'], type=arg['type'], choices=arg['choices'], required=arg['required'], help=arg['help'])
            else:
                command_parser.add_argument(
                    arg['name'], type=arg['type'], help=arg['help'])

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    command = commands[vars(args).pop('command')]['action']
    return command, args


def add_task(tasks, description):
    # Generate a new task ID
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = max(int(task['id']) for task in tasks) + 1
    # Create a new task
    new_task = {
        "id": str(new_id),
        "description": description,
        "status": "Todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    # Append the new task to the tasks list
    tasks.append(new_task)
    # Write the updated tasks list to the JSON file
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    # Print the new task
    print("Task added successfully:")
    # Print the new task in a table format
    table = []
    table.append([new_task['id'], new_task['description'],
                  new_task['status'], new_task['createdAt'], new_task['updatedAt']])
    # Print the new task in a table format
    print(tabulate(table, headers=[
          'ID', 'Description', 'Status', 'Created At', 'Updated At']))


def update_task(args):
    pass


def delete_task(args):
    pass


def mark_in_progress(args):
    pass


def mark_done(args):
    pass


def list_tasks(args):
    pass
    # tasks = init_task_json()
    # if args.status == 'all':
    #     filtered_tasks = tasks
    # else:
    #     filtered_tasks = [task for task in tasks if task['status'] == args.status]
    # table = []
    # for task in filtered_tasks:
    #     table.append([task['id'], task['description'],
    #                   task['status'], task['createdAt'], task['updatedAt']])
    # print(tabulate(table, headers=['ID', 'Description', 'Status', 'Created At', 'Updated At']))


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


if __name__ == '__main__':
    main()
