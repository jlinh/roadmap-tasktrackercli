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
                    'type': str,
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
                    'type': str,
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
            'subcommands': {
                'in-progress': {
                    'action': list_tasks,
                    'help': 'List all tasks in progress',
                    'args': []
                },
                'done': {
                    'action': list_tasks,
                    'help': 'List all tasks done',
                    'args': []
                },
                'todo': {
                    'action': list_tasks,
                    'help': 'List all tasks to do',
                    'args': []
                }
            },
            'action': list_tasks,
            'help': 'List all tasks or with a specific status',
            'args': []
            # 'args': [
            #     {
            #         'name': 'status',
            #         'type': str.lower,
            #         'help': 'Filter tasks by status',
            #         'choices': [None, 'in-progress', 'done', 'todo'], 'default': None,
            #     }
            # ]
        },
        # 'list': {
        #     'action': list_tasks,
        #     'help': 'List all tasks or with a specific status',
        #     'args': [
        #         {
        #             'name': '--status',
        #             'type': str.lower,
        #             'help': 'Filter tasks by status',
        #             'choices': [None, 'in-progress', 'done', 'todo'], 'default': None,
        #         }
        #     ]
        # }
    }


def parse_command():
    parser = ArgumentParser(prog='taskctl', description='Task Tracker')
    subparser = parser.add_subparsers(dest='command')
    commands = get_supported_commands()
    for command, command_info in commands.items():
        command_parser = subparser.add_parser(
            command, help=command_info['help'])
        if 'subcommands' in command_info:
            subsubparser = command_parser.add_subparsers(dest='subcommand')
            for subcommand, subcommand_info in command_info['subcommands'].items():
                subcommand_parser = subsubparser.add_parser(
                    subcommand, help=subcommand_info['help'])

        else:
            for arg in command_info['args']:
                command_parser.add_argument(
                    arg['name'], type=arg['type'], help=arg['help'])

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    command = commands[vars(args).pop('command')]['action']
    return command, args


def display_tasks(tasks):
    # Create a table to display the tasks
    table = []
    for task in tasks:
        table.append([task['id'], task['description'],
                      task['status'], task['createdAt'], task['updatedAt']])
    # Print the table
    print(tabulate(table, headers=[
          'ID', 'Description', 'Status', 'Created At', 'Updated At']))


def write_tasks_to_file(tasks):
    # Write the updated tasks list to the JSON file
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=2)


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
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    # Append the new task to the tasks list
    tasks.append(new_task)
    # Write the updated tasks list to the JSON file
    write_tasks_to_file(tasks)
    # Print the new task
    print("Task added successfully.")
    # Print the new task in a table format
    display_tasks(tasks)


def update_task(tasks, id, description):
    # Find the task with the given ID
    selected_task = [task for task in tasks if task['id'] == str(id)][0]
    if selected_task is None:
        print(f"Task with ID {id} not found.")
        return
    # Update the task's description
    selected_task['description'] = description
    # Update the task's updatedAt timestamp
    selected_task['updatedAt'] = datetime.now().isoformat()
    # Write the updated tasks list to the JSON file
    write_tasks_to_file(tasks)
    # Print the updated task
    print("Task updated successfully.")
    # Print the new task in a table format
    display_tasks(tasks)


def delete_task(tasks, id):
    # Find the task with the given ID
    selected_task = [task for task in tasks if task['id'] == str(id)][0]
    if selected_task is None:
        print(f"Task with ID {id} not found.")
        return
    # Remove the task from the tasks list
    tasks.remove(selected_task)
    # Update the task's updatedAt timestamp
    selected_task['updatedAt'] = datetime.now().isoformat()
    # Write the updated tasks list to the JSON file
    write_tasks_to_file(tasks)
    # Print the deleted task
    print("Task deleted successfully.")
    # Print the new task in a table format
    display_tasks(tasks)


def mark_status(tasks, id, status):
    # Find the task with the given ID
    selected_task = [task for task in tasks if task['id'] == str(id)][0]
    if selected_task is None:
        print(f"Task with ID {id} not found.")
        return
    # Update the task's status to "In Progress"
    selected_task['status'] = status
    # Update the task's updatedAt timestamp
    selected_task['updatedAt'] = datetime.now().isoformat()
    # Write the updated tasks list to the JSON file
    write_tasks_to_file(tasks)
    # Print the updated task
    print(f"Task marked as {status} successfully.")
    # Print the new task in a table format
    display_tasks(tasks)


def mark_in_progress(tasks, id):
    mark_status(tasks, id, 'in-progress')


def mark_done(tasks, id):
    mark_status(tasks, id, 'done')


def list_tasks(tasks, subcommand=None):
    # Check if a subcommand is provided
    if subcommand is not None:
        status = subcommand
    else:
        status = None
    # Check if the tasks list is empty
    if len(tasks) == 0:
        print("No tasks found.")
        return
    # If a subcommand is provided, filter tasks by status
    # Check if the status is valid
    if status not in [None, 'in-progress', 'done', 'todo']:
        print(f"Invalid status: {status}")
        return
    # Filter tasks based on the status
    if status is None:
        filtered_tasks = tasks
    else:
        # Filtering tasks by status:
        filtered_tasks = [task for task in tasks if task['status'] == status]
    # Display the filtered tasks
    if len(filtered_tasks) == 0:
        print(f"No tasks found with status: {status}")
        return
    # Print the filtered tasks in a table format
    display_tasks(filtered_tasks)


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
