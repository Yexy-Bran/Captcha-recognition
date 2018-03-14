# Captcha-recognition

  captcha_generate.py 
  生成12X12的大写字母和数字的图像
  
  creat_index_file.py 
  由上述生成的图片输出标签文件train.txt和val.txt
  
  mv_data.py 
  移动图片到指定路径
  
  Captcha/create_dataset.sh 
  创建lmdb格式的训练数据集和验证数据集

  Captcha/lenet_train_test.prototxt  
  训练模型文件
  
  Captcha/lenet_solver_adam.prototxt 
  Solver文件
  
  Captcha/deploy.prototxt   
  测试模型文件
  
  Captcha/classify.py 
  处理验证码图片并识别其中字符
