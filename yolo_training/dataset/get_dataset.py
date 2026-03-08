

from roboflow import Roboflow
rf = Roboflow(api_key="yaJG5J6GhtNej1k9rnvE")
project = rf.workspace("gmudrone").project("drone_gmu-fnphk")
version = project.version(4)
dataset = version.download("yolo26")
                