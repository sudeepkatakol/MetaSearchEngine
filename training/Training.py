import tensorflow as tf

# x is the doc vector
x = tf.placeholder(tf.float32, [None, 300])

W = tf.Variable(tf.zeros([300, 8]))
b = tf.Variable(tf.zeros([8]))

# softmax logits
ans = tf.nn.softmax(tf.matmul(x, W) + b)
# So, ans = softax(W*x+ b)

# A one-hot vector dependent on the class
t = tf.placeholder(tf.float32, [None, 8])

# these parameters have been obtained using cross_validation data
learning_rate = 0.40
beta = 10 **(-4)
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=t, logits=ans))+beta*tf.nn.l2_loss(W)
train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

sess = tf.InteractiveSession()
# We first have to create an operation to initialize the variables we created:
tf.global_variables_initializer().run()

steps = 4000
for _ in range(steps):
    training_loss = sess.run(train_step, feed_dict={x: X_train, t: y_train})
test_loss = sess.run(cross_entropy, feed_dict={x: X_test, t: y_test})

training_loss = sess.run(cross_entropy, feed_dict={x: X_train, t: y_train})
print training_loss
print test_loss
# Output:
#	0.993639 
#	0.978417 