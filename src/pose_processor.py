from openpose import pyopenpose as op


class PoseProcessor(object):
    def __init__(self, op_wrapper: op.WrapperPython):
        self._op_wrapper = op_wrapper

    def process(self, image) -> list:
        datum = op.Datum()
        datum.cvInputData = image
        self._opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        if datum.poseKeypoints is None:
            return []

        return datum.poseKeypoints.tolist()
