import tensorflow as tf
from tensorflow.train import list_variables, load_variable
from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file


def inspect(ckpt_path, tensor_name=""):
    print_tensors_in_checkpoint_file(
        file_name=ckpt_path, tensor_name=tensor_name, all_tensors=False
    )


def inspect_huggingface_model(HFClass, bert_model="bert-base-uncased"):
    model = HFClass.from_pretrained(bert_model)
    return model.trainable_weight


def rename_variables(tvars, patterns, prefix="", save=False, outp_fn="converted.ckpt"):
    """
        This function need to be invoked outside of tf.Session()
        tvars: tf.trainable_variables, 
        pattern: OrderedDict, {pattern: replacement}, pattern appears later has higher priority

    return a list of renamed variables 
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
    if not name2nparr:
        name2nparr = {}

    name2nparr.update({var.name: var.numpy() for var in tvars})
    return name2nparr


def convert_ckpt_file_to_dict(path):
    return {name: load_variable(ckpt_dir_or_file=path, name=name) for name, shape in list_variables(path)}
