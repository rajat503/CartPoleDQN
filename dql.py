import tensorflow as tf

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

#create session
sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[4])
target = tf.placeholder(tf.float32, shape=[2])

g=tf.reshape(x, [4,1])
y=tf.transpose(g)
W_fc1 = weight_variable([4, 200])
b_fc1 = bias_variable([200])
h_fc1 = tf.nn.relu(tf.matmul(y, W_fc1) + b_fc1)

W_fc2 = weight_variable([200, 200])
b_fc2 = bias_variable([200])
h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)

W_fc3 = weight_variable([200, 2])
b_fc3 = bias_variable([2])

q_values = tf.matmul(h_fc2, W_fc3) + b_fc3

action  = tf.argmax(q_values, 1)
q_a_max = tf.reduce_max(q_values)

loss = tf.reduce_sum(tf.square(tf.sub(target, q_values)))
with tf.name_scope('loss'):
    # loss = tf.clip_by_value(loss, -200, 200)
    tf.scalar_summary('TD Error', loss)

train_step = tf.train.AdamOptimizer(1e-5).minimize(loss)

merged = tf.merge_all_summaries()
train_writer = tf.train.SummaryWriter('./train', sess.graph)
sess.run(tf.initialize_all_variables())

def getAction(state):
    a, q_s = sess.run([action, q_values], feed_dict={x:state})
    a=int(a[0])
    q_s=q_s[0]
    return q_s, a

def learn(initial_state,reward_p, state, i, q_s, a):
    q_t1_max = sess.run([q_a_max], feed_dict={x: state})
    q_s[a] = reward_p + 0.9 * float(q_t1_max[0])
    for _ in range(20):
        _, error, summary = sess.run([train_step, loss, merged], feed_dict={target: q_s, x: initial_state})
    train_writer.add_summary(summary, i)