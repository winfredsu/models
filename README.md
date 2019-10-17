# TensorFlow Models

This repository contains a number of different models implemented in [TensorFlow](https://www.tensorflow.org):

The [official models](official) are a collection of example models that use TensorFlow's high-level APIs. They are intended to be well-maintained, tested, and kept up to date with the latest stable TensorFlow API. They should also be reasonably optimized for fast performance while still being easy to read. We especially recommend newer TensorFlow users to start here.

The [research models](https://github.com/tensorflow/models/tree/master/research) are a large collection of models implemented in TensorFlow by researchers. They are not officially supported or available in release branches; it is up to the individual researchers to maintain the models and/or provide support on issues and pull requests.

The [samples folder](samples) contains code snippets and smaller models that demonstrate features of TensorFlow, including code presented in various blog posts.

The [tutorials folder](tutorials) is a collection of models described in the [TensorFlow tutorials](https://www.tensorflow.org/tutorials/).

## Contribution guidelines

If you want to contribute to models, be sure to review the [contribution guidelines](CONTRIBUTING.md).

## License

[Apache License 2.0](LICENSE)

# Modifications for HW-Friendly Quant-Aware-Training
- In `research/slim`:
    - modify the bottleneck block and add a resnet18 in `nets/resnet_v1.py`
- In `research/object_detection`:
    - add ssd_resnet18_v1_ppn in `builders/model_builder.py`
    - add batchnorm in detection heads in `predictors/heads/box_heads.py` and `predictors/heads/class_heads.py`
    - add ssd_resnet18_v1_ppn in `models/ssd_resnet_v1_ppn_feature_extractor.py`, and also fix the depth_multiplier and activation problem

