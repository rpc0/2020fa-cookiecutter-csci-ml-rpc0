# csci_utils.luigi.task

from luigi import LocalTarget
from functools import partial

from dask.bytes.core import get_fs_token_paths


class Requirement:
    """
    Using Descriptor protocol, this class creates new instances of Tasks using existing instances of Tasks
    when only some of the parameters have changed.
    """

    def __init__(self, task_class, **params):
        self.task_class = task_class
        self.params = params

    def __get__(self, task, cls):
        if task is None:
            return self

        return task.clone(self.task_class, **self.params)


class Requires:
    """Composition to replace :meth:`luigi.task.Task.requires`

    Example::

        class MyTask(Task):
            # Replace task.requires()
            requires = Requires()
            other = Requirement(OtherTask)

            def run(self):
                # Convenient access here...
                with self.other.output().open('r') as f:
                    ...

        >>> MyTask().requires()
        {'other': OtherTask()}

    """

    def __get__(self, task, cls):
        if task is None:
            return self

        return lambda: self(task)

        # Bind self/task in a closure
        return partial(self.__call__, task)

    def __call__(self, task):
        """Returns the requirements of a task

        Assumes the task class has :class:`.Requirement` descriptors, which
        can clone the appropriate dependences from the task instance.

        :returns: requirements compatible with `task.requires()`
        :rtype: dict
        """
        # Search task.__class__ for Requirement instances
        # return
        return {
            key: getattr(task, key)
            for key, value in task.__class__.__dict__.items()
            if isinstance(value, Requirement)
        }


# csci_utils.luigi.task

class TargetOutput:
    '''
    Composition to replace :meth:`luigi.task.Task.output`
    Example::
        class MyTask(Task):
            # Replace task.requires()
            output = TargetOutput (
                file_pattern="data/output.txt",
                target_class=LocalTarget,
            )
        >>> MyTask().output()
        LocalTarget("data/output.txt")
    """
    '''
    def __init__(
            self,
            file_pattern="{task.__class__.__name__}",
            ext="",
            target_class=LocalTarget,
            **target_kwargs):
        self.file_pattern = file_pattern
        self.ext = ext
        self.target_class = target_class
        self.target_kwargs = target_kwargs

    def __get__(self, task, cls):
        if task is None:
            return self

        return partial(self.__call__, task)
        # return lambda: self(task)

    def __call__(self, task):      
        # Use either ext to specify extensions or no ext in which case custom params go to 
        revised_kwargs = {i: self.target_kwargs[i] for i in self.target_kwargs if i != "ext"}

        # If glob is specified, 
        if "glob" in self.target_kwargs:
            target_path = self.file_pattern.format(task=task)
            revised_glob = self.target_kwargs["glob"].format(task=task) + self.ext.format(task=task)
            revised_kwargs["glob"] = revised_glob
        else:
            target_path = self.file_pattern.format(task=task) + self.ext.format(task=task)

        # Note that these targets force you to specify directory datasets with an ending /; Dask (annoyingly) is
        # inconsistent on this, so you may find yourself manipulating paths inside ParquetTarget and CSVTarget
        # differently. The user of these targets should not need to worry about these details!
        path_sep = get_fs_token_paths(target_path)[0].sep
        if target_path[-1] != path_sep:
            if target_path[-1] == "/":
                target_path = target_path[:-1]
            target_path = target_path + path_sep
        fs, _, _ = get_fs_token_paths(target_path)

        if "{ext}" not in self.file_pattern and not "" == self.ext:
            target_path = target_path + self.ext

        return self.target_class(target_path, **revised_kwargs)


