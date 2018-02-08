from __future__ import print_function
import sys
from distutils.version import LooseVersion as semvar


version_only = False

def say(*args, **kwargs):
    if not version_only:
        print(*args, **kwargs)


def main():
    error_msg = '\n\n*** Warning: %s, baseline imitation learning agent will not be available. ' \
                'HINT: Check out our CUDA / cuDNN install tips on the README ' \
                '\n\n'

    say('Checking for valid Tensorflow installation')
    try:
        # noinspection PyUnresolvedReferences
        import tensorflow as tf
        check = tf.constant('string tensors are not tensors but are called tensors in tensorflow')
        with tf.Session(config=tf.ConfigProto(log_device_placement=False,
                                              gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.01,
                                                                        allow_growth=True))) as sess:
            if not get_available_gpus():
                say('\n\n*** Warning: %s \n\n' %
                      'Tensorflow could not find a GPU, performance will be severely degraded on CPU. '
                      'HINT: Try "pipenv install tensorflow-gpu"')
                exit(1)
            sess.run(check)
            say('Tensorflow is working on the GPU.')

    except ImportError:
        say(error_msg % 'Tensorflow not installed', file=sys.stderr)
        exit(1)
    except Exception:
        say(error_msg % 'Tensorflow not working', file=sys.stderr)
        exit(1)

    min_version = '1.1'
    if semvar(tf.__version__) < semvar(min_version):
        warn_msg = 'Tensorflow %s is less than the minimum required version (%s)' % (tf.__version__, min_version)
        say(error_msg % warn_msg, file=sys.stderr)
        exit(1)
    else:
        say('Tensorflow %s detected - meets min version (%s)' % (tf.__version__, min_version))
        if version_only:
            print(tf.__version__)


def get_available_gpus():
    from tensorflow.python.client import device_lib
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']


if __name__ == '__main__':
    version_only = '--version-only' in sys.argv
    main()
