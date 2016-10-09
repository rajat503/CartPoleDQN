import tensorflow as tf

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

#create session
sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[None, 4])
target = tf.placeholder(tf.float32, shape=[None,1])


W_fc1 = weight_variable([4, 50])
b_fc1 = bias_variable([50])
h_fc1 = tf.nn.relu(tf.matmul(x, W_fc1) + b_fc1)

W_fc2 = weight_variable([50, 50])
b_fc2 = bias_variable([50])
h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)

W_fc3 = weight_variable([50, 2])
b_fc3 = bias_variable([2])

q_values = tf.matmul(h_fc2, W_fc3) + b_fc3

action  = tf.argmax(q_values, 1)
q_a_max = tf.reduce_max(q_values, reduction_indices=1)

loss = tf.reduce_sum(tf.square(tf.sub(target, q_a_max)))
with tf.name_scope('loss'):
    # loss = tf.clip_by_value(loss, 0, 1)
    tf.scalar_summary('TD Error', loss)

train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

merged = tf.merge_all_summaries()
train_writer = tf.train.SummaryWriter('./train', sess.graph)
sess.run(tf.initialize_all_variables())

def getAction(state):
    a = sess.run([action], feed_dict={x: [state]})
    a=int(a[0])
    return a

def learn(sample):
    st=[]
    a=[]
    reward=[]
    en=[]
    t=[]

    for i in sample:
        st.append(i[0])
        a.append(i[1])
        reward.append(i[2])
        en.append(i[3])

    for __ in range(20):
        q_t1_max = sess.run([q_a_max], feed_dict={x: en})

        for i in range(len(q_t1_max[0])):
            t.append([reward[i] + 0.9 * q_t1_max[0][i]])

        gg, summary = sess.run([train_step, merged], feed_dict={target: t, x: st})
    train_writer.add_summary(summary, i)