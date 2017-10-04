python create_lmdb.py

compute_image_mean -backend=lmdb /home/ghanghas.s/deeplearning/input/train_lmdb /home/ghanghas.s/deeplearning-cats-dogs-tutorial/input/mean.binaryproto

 python /home/ubuntu/caffe/python/draw_net.py /home/ghanghas.s/deeplearning/caffe_models/caffe_model_1/caffenet_train_val_1.prototxt /home/ghanghas.s/deeplearning/caffe_models/caffe_model_1/caffe_model_1.png


 caffe train --solver /home/ghanghas.s/deeplearning/caffe_models/caffe_model_1/solver_1.prototxt 2>&1 | tee /home/ghanghas.s/deeplearning/caffe_models/caffe_model_1/model_1_train.log


python /home/ghanghas.s/deeplearning/code/plot_learning_curve.py /home/ghanghas.s/deeplearning/caffe_models/caffe_model_1/model_1_train.log /home/ghanghas.s/deeplearning/caffe_models/caffe_model_1/caffe_model_1_learning_curve.png




caffe train --solver=/home/ghanghas.s/deeplearning/caffe_models/caffe_model_2/solver_2.prototxt --weights /shared/apps/caffe/caffe-master/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel 2>&1 | tee /home/ghanghas.s/deeplearning/caffe_models/caffe_model_2/model_2_train.log