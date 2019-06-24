"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.job import Job
from foundations_internal.stage_context import StageContext
from foundations.context_aware import ContextAware


class StageConnectorWrapper(object):
    """
    ### The three numerals at the begining are a marker for not generating user documentation for the class.
    """

    def __init__(self, stage, pipeline_context, stage_context, stage_config):
        self._stage = stage
        self._pipeline_context = pipeline_context
        self._stage_context = stage_context
        self._stage_config = stage_config

        self._stage_context.uuid = self.uuid()
        self._pipeline_context.add_stage_context(self._stage_context)

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._stage.uuid()

    def stage(self, function, *args, **kwargs):
        from foundations import foundations_context

        return foundations_context.pipeline().stage(function, self, *args, **kwargs)

    def require(self, *required_args):
        def _require(*args):
            return args[-1]

        builder = self._make_builder()
        builder = self._set_builder_stage(
            builder, _require, required_args + (self,), {})
        builder = self._set_builder_hierarchy(builder)

        return builder.build(self._stage)

    def persist(self):
        self._stage_config.persist()
        return self

    def set_global_cache_name(self, name):
        self._stage_config.cache(name)
        return self

    def enable_caching(self):
        """
        Activates caching of the result of current stage and any other stages that it depends on.

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            stage object -- The same object to which this method belongs.

        Raises:
            - This method doesn't raise exceptions.

        Example:
            ```python
            import foundations
            from data_helper import load_data
            from algorithms import train_model

            load_data = foundations.create_stage(load_data)
            train_model = foundations.create_stage(train_model)
            data = load_data()
            model = train_model(data)
            model.enable_caching()
            model.run()
            ```
        """
        self._stage_config.enable_caching()
        for argument in self._stage.stage_args():
            argument.enable_caching()
        for argument in self._stage.stage_kwargs().values():
            argument.enable_caching()
        return self

    def disable_caching(self):
        self._stage_config.disable_caching()
        return self

    def run(self, params_dict=None, job_name=None, **kw_params):
        """
        Deploys and runs the current stage and the stages on which it depends in the configured execution
        environment, creating a new job.

        Arguments:
            job_name {string} -- optional name for the job that would be created.
            params_dict {dict} -- optional way to pass values to stages that receive Foundation's Hyperparameter object(s).

        Returns:
            deployment {DeploymentWrapper} -- An object that allows tracking the deployment.

        Raises:
            TypeError -- When the type of an argument passed to the function wrapped by this stage is not supported.

        Notes:
            The new job runs asynchronously, the current process can continue execution.

            You can pass hyperparameters values using both *params_dict* or keyword arguments syntax.

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model(data1=foundations.Hyperparameter(), data2=foundations.Hyperparameter())
            model.run(job_name='Experiment number 2', params_dict={'data1': 'value1'}, data2='value2')
            ```
        """
        from foundations.job_deployer import deploy_job

        if params_dict is None:
            params_dict = {}

        all_params = params_dict.copy()
        all_params.update(kw_params)

        return deploy_job(self, job_name, all_params)

    def run_same_process(self, **filler_kwargs):
        return self._stage.run(None, None, **filler_kwargs)

    def _make_builder(self):
        from foundations_internal.stage_connector_wrapper_builder import StageConnectorWrapperBuilder
        return StageConnectorWrapperBuilder(self._pipeline_context)

    def _set_builder_stage(self, builder, function, args, kwargs):
        return builder.stage(self.uuid(), function, args, kwargs)

    def _set_builder_hierarchy(self, builder):
        return builder.hierarchy([self.uuid()])

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def name(self):
        function_name_and_uuid = self.function_name() + ' ' + self.uuid()
        return function_name_and_uuid

    def function_name(self):
        return self._stage.function_name()

    def split(self, num_children):
        """
        When a function is wrapped in a stage and it has more than one return value (the return value
        is a sequence), the wrapping stage cannot obtain how many values are contained in the returned
        sequence due to language constraints. This method allows to specify the number of children values
        and splits the result in a corresponding sequence of stages that can be passed forward.

        Arguments:
            num_children {int} -- number of children values contained in the stage result.

        Returns:
            children_stages {sequence} -- A sequence of children stages.

        Raises:
            TypeError -- If the current stage does not contain a sequence of values.
            IndexError -- If the number of children values is less than __num_children__.

        Notes:
            The exceptions thrown by this method only occur after the wrapped function is executed inside the
            stage, when Foundations applies the splitting logic to the results. As a consequence,
            these exceptions are thrown at a later time, when the stage is being executed in a job.

        Example:
            ```python
            import foundations
            from algorithms import retrieve_latitude, retrieve_longitude, train_with_coordinates

            def get_coordinates():
                x_coord = retrieve_longitude()
                y_coord = retrieve_latitude()
                return x_coord, y_coord

            get_coordinates = foundations.create_stage(get_coordinates)
            train_with_coordinates = foundations.create_stage(train_with_coordinates)
            x_coord, y_coord = get_coordinates().split(2)
            model = train_with_coordinates(x_coord, y_coord)
            model.run()
            ```
        """
        from foundations.utils import split_at

        children = []

        for child_index in range(num_children):
            child = self.stage(split_at, child_index)
            children.append(child)

        return children

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return super(StageConnectorWrapper, self).__getattr__(name)

        def call_method_on_instance(instance, *args, **kwargs):
            result = getattr(instance, name)(*args, **kwargs)
            if result is None:
                return instance
            return result

        def auto_stage(*args, **kwargs):
            return self.stage(call_method_on_instance, *args, **kwargs)

        return auto_stage

    def __getitem__(self, key):
        def getitem(data, key):
            return data[key]

        return self.stage(getitem, key)

    def random_search(self, params_range_dict, max_iterations):
        """
        Replaces the .run() call on a stage and launches multiple jobs with random combinations of the hyperparameters passed in.

        Arguments:
            params_range_dict {dict} -- a dictionary containing FloatingHyperparameter or DiscreteHyperparameter objects
            max_iterations {int} -- parameter to specify number of total loops to run

        Returns:
            deployments {dict} -- a dictionary containing individual deployment objects mapped by job_id

        Raises:
            ValueError -- When the value of a Hyperparameter passed into the function is not iterable.
            AttributeError -- When the dictionary passed in does not contain a Hyperparameter object.
            TypeError -- When the type of an argument passed to the function wrapped by this stage is not supported.

        Example:
            ```python
            import foundations
            from algorithms import train_model

            foundations.set_project_name('random_search_example')
            train_model = foundations.create_stage(train_model)
            model = train_model(data1=foundations.Hyperparameter())

            # Launches 5 jobs where random values between 0.25 and 1 at increments of 0.025 are selected
            # Ex: 5 independent jobs where the data1 values are (0.25, 0.55, 0.425, 0.7, 0.325)
            model.random_search( 
                params_dict={'data1': foundations.FloatingHyperparameter(0.25, 1, 0.025), 5})
            
            # Results from the 5 jobs can be retrieved with get_metrics_for_all_jobs
            print(foundations.get_metrics_for_all_jobs('random_search_example')
            ```
        """
        from foundations.set_random_searcher import SetRandomSearcher

        set_random_searcher = SetRandomSearcher(
            params_range_dict, max_iterations)
        return set_random_searcher.run_param_sets(self)

    def grid_search(self, params_range_dict, max_iterations=None):
        """
        Replaces the .run() call on a stage and launches multiple jobs with every combinations of the hyperparameters passed in.

        Arguments:
            params_range_dict {dict} -- a dictionary containing FloatingHyperparameter or DiscreteHyperparameter objects
            max_iterations {int} -- optional parameter to specify maximum number of total loops to run, none by default which will loop through every possible combination of Hyperparameter values passed in.

        Returns:
            deployments {dict} -- a dictionary containing individual deployment objects mapped by job_id

        Raises:
            ValueError -- When the value of an Hyperparameter passed into the function is not iterable.
            AttributeError -- When the dictionary passed in does not contain a Hyperparameter object.
            TypeError -- When the type of an argument passed to the function wrapped by this stage is not supported.

        Example:
            ```python
            import foundations
            from algorithms import train_model

            foundations.set_project_name('grid_search_example')
            train_model = foundations.create_stage(train_model)
            model = train_model(data1=foundations.Hyperparameter(), data2=foundations.Hyperparameter())

            # Launches 9 jobs where the values of data1 and data2 are the exactly same as the ones defined in the Hyperparameters
            # Ex: 9 independent jobs where the data1 values are exactly(0.25, 0.125, 1) 
            # for each exact step value of data2 (4, 5, 6) in the distribution
            model.grid_search(
                params_dict={'data1': foundations.DiscreteHyperparameter([0.25, 0.125, 1.0]),
                                'data2': foundations.FloatingHyperparameter(4, 6, 1)})

            # Results from the 9 jobs can be retrieved with get_metrics_for_all_jobs
            print(foundations.get_metrics_for_all_jobs('grid_search_example')
            ```
        """
        from foundations.set_grid_searcher import SetGridSearcher

        grid_searcher = SetGridSearcher(params_range_dict, max_iterations)
        return grid_searcher.run_param_sets(self)

    def adaptive_search(self, set_of_initial_params, params_generator_function, error_handler=None):
        from foundations.adaptive_searcher import AdaptiveSearcher

        adaptive_searcher = AdaptiveSearcher(
            set_of_initial_params, params_generator_function, error_handler)
        adaptive_searcher.search(self)
