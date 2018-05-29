from vcat.stage_graph import StageGraph
from vcat.stage_piping import StagePiping
from vcat.stage_context import StageContext
from vcat.stage_connector_wrapper import StageConnectorWrapper


class Pipeline(object):

    def __init__(self, pipeline_context):
        self.graph = StageGraph()
        self.pipeline_context = pipeline_context
        self._stage_context = StageContext(self.pipeline_context)
        self._stage_piping = StagePiping(self)

    def stage(self, function, *args, **kwargs):
        current_stage = self._stage_context.make_stage(
            function, *args, **kwargs)
        return StageConnectorWrapper(self.graph.stage(current_stage), self.pipeline_context, self._stage_context)

    def join(self, upstream_connector_wrappers, function, *args, **kwargs):
        upstream_connectors = [
            wrapper._connector for wrapper in upstream_connector_wrappers]
        current_stage = self._stage_context.make_stage(
            function, *args, **kwargs)
        return StageConnectorWrapper(self.graph.join(current_stage, upstream_connectors), self.pipeline_context, self._stage_context)

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)