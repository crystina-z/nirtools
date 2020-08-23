import tensorflow as tf
from tensorflow.train import list_variables, load_variable
from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file


def inspect(ckpt_path, tensor_name=""):
    """
    read the tensorflow checkpoint file and print out the name and shape of all the tensors
    or the one given

    :param ckpt_path: tensorflow checkpoint file path
    :param tensor_name: the name of desired tensor, default to be ""
    :return:
    """
    print_tensors_in_checkpoint_file(
        file_name=ckpt_path, tensor_name=tensor_name, all_tensors=False
    )


def inspect_huggingface_model(HFClass, bert_model="bert-base-uncased", return_value=False):
    """
    fetch all trainable tensors from the given huggingface tensorflow model

    :param HFClass: The model class
    :param bert_model:
    :return: all trainable variables
    """
    model = HFClass.from_pretrained(bert_model)
    weights = model.trainable_weights
    return [(v.name, v.shape) for v in weights]


def rename_variables(tvars, patterns, prefix="", save=False, outp_fn="converted.ckpt"):
    """
    rename the given tensorflow trainable variables by replacing the keys in patterns with the values,
    and prepend the prefix

    This function need to be invoked inside of tf.Session()

    :param tvars: tf.trainable_variables
    :param patterns: OrderedDict, {pattern: replacement}, pattern appears later has higher priority
    :param prefix: prefix to be appended before all the tensors' name
    :param save: whether to save the converted tensor into dist, if True, the outp_fn must be a valid path name
    :param outp_fn: the path to save the converted tensors, would be ignored if `save` is set to False,
        default "converted.ckpt"
    :return: a list of renamed variables
    """
    def convert(name):
        for ori, tgt in patterns.items():
            name = name.replace(ori, tgt)
        return name

    renamed_tvars = []
    with tf.Session().as_default() as sess:
        for var in tvars:
            varname = prefix + convert(var.name)
            renamed_tvars.append(tf.Variable(var, name=varname))

        if save:
            saver = tf.train.Saver(renamed_tvars)
            sess.run(tf.global_variables_initializer())
            saver.save(sess, outp_fn)
    return renamed_tvars


def convert_tvars_to_dict(tvars, name2nparr=None):
    """
    convert the input training variables to a dictionary

    :param tvars: the tensorflow trainable variables
    :param name2nparr: a dictionary in same format with output, if given, the converted tvars will be added to this
    :return: the dictionary in the format of {dict: np.Array}
    """
    if not name2nparr:
        name2nparr = {}

    name2nparr.update({var.name: var.numpy() for var in tvars})
    return name2nparr


def convert_ckpt_file_to_dict(path):
    """
    load the tensorflow dictionary from checkpoint file and convert it to a dictionary mapping name to value

    :param path: the checkpoint file path
    :return: the dictionary in the format of {dict: np.Array}
    """
    return {name: load_variable(ckpt_dir_or_file=path, name=name) for name, shape in list_variables(path)}
