import numpy as np
import smo_kernel as smok
import test_toolkit as testkit


def test_svm(filename, c, tolerance, max_iter, k_tuple):
    """
    :param filename: input .txt file
    :param c: float
    :param tolerance: float
    :param max_iter: mat iteration
    :param k_tuple: ('name', parameter)
    :return:
    """
    # pre-processing
    train_matrix, cv_matrix, test_matrix = testkit.split_data(filename)
    t_x, t_y = testkit.separate_x_y(train_matrix)
    # train the data set with smo
    m, n = t_x.shape
    a, b = smok.smo_platt(t_x, t_y, c, tolerance, max_iter, k_tuple)
    # find the support vectors
    sv_indexes = np.array(np.nonzero(a))[0]
    a_list = a[sv_indexes]
    sv_list = t_x[sv_indexes]
    sv_labels = t_y[sv_indexes]
    print('Support vectors: %d \n' % sv_indexes.shape[0])
    # calculate train error
    error_count = 0
    for i in range(m):
        kernel_of_samples = smok.kernel_list(sv_list, t_x[i], k_tuple)
        predict = np.sign(np.dot((a_list * sv_labels).T, kernel_of_samples) + b)
        if predict != t_y[i]:
            error_count += 1
    print ('Training error: %f \n' % (float(error_count)/float(m)))
    # calculate cross validation error
    cv_error_count = 0
    cv_x, cv_y = testkit.separate_x_y(cv_matrix)
    cv_m, cv_n = cv_x.shape
    for i in range(cv_m):
        kernel_of_samples = smok.kernel_list(sv_list, cv_x[i], k_tuple)
        predict = np.sign(np.dot((a_list * sv_labels).T, kernel_of_samples) + b)
        if predict != cv_y[i]:
            cv_error_count += 1
    print ('Cross validation error: %f \n' % (float(error_count)/float(m)))


# --------------------TEST SAMPLE--------------------------
# test_svm('test_data/testSetRBF.txt', 0.1, 0.0001, 40, ('rbf', 1.0))