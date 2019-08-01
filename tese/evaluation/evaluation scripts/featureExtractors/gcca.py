import numpy as np
import scipy.linalg as la
import sys
import sklearn.preprocessing as sk

# data is a list of of views, represented as matrices with shape (N, F) where N is the number of samples and F is the number of features
class wgcca(object):

  def __init__(self, components, regularizers=1e-4, weights=None):
    self._components = components
    self._regularizers = regularizers
    self._weights = weights
    self._g = None


  def fit(self, data, inv_qr=None, mask=None, incremental=False):
    views = len(data)
    if self._weights and len(self._weights) != views:
      raise Exception('the number of custom weights must equal the number of views')
    if not self._weights:
      self._weights = [1.0] * views

    samples = data[0].shape[0]
    for view_idx in range(views):
      if data[view_idx].shape[0] != samples:
        raise Exception('all views must contain the same number of samples')

    if not isinstance(self._regularizers, list):
      self._regularizers = [self._regularizers] * views

    if not mask:
      mask = np.ones((samples, views))

    if inv_qr and len(inv_qr) != views:
      raise Exception('inverse matrices must match view dimensions')

    if inv_qr:
      for view_idx in range(views):
        if inv_qr[view_idx] is not None and (inv_qr[view_idx].shape[0] != data[view_idx].shape[1] or inv_qr[view_idx].shape[1] != data[view_idx].shape[1]):
          raise Exception('inverse matrices must match view dimensions')

    mask = np.dot(mask, np.diag(self._weights))
    mask_sum = np.sum(mask, axis=1)

    mask_sum[mask_sum==0] = 1e-8

    root_inv_mask = np.diag(1.0 / np.sqrt(mask_sum))

    left_vectors, transforms, transforms_unnorm = [], [], []
    g_prime, s_tilde, g_prime_scaled, s_tilde_scaled = np.zeros((samples, self._components)), np.zeros(self._components), np.zeros((samples, self._components)), np.zeros(self._components)
    if incremental and self._g is not None:
      g_prime, g_prime_scaled, s_tilde, s_tilde_scaled = self._g, self._g_scaled, self._lbda, self._lbda_scaled

    for view_idx in range(views):
      left, values, _ = la.svd(data[view_idx], full_matrices=False, check_finite=False)

#      values = values[:self._components]
#      left = left[:,:self._components]

      square_inv_values = 1.0 / (values * values + self._regularizers[view_idx])

      t = np.diag(np.sqrt(values * square_inv_values * values))

      t_unnorm = np.diag(values + self._regularizers[view_idx])

      if incremental:
        ajtj = np.dot(root_inv_mask, np.sqrt(self._weights[view_idx]) * np.dot(left, t))
        ajtj_scaled = np.dot(root_inv_mask, np.sqrt(self._weights[view_idx]) * np.dot(left, t_unnorm))

        g_prime, s_tilde = self._batch_incremental_pca(ajtj, g_prime, s_tilde)
        g_prime_scaled, s_tilde_scaled = self._batch_incremental_pca(ajtj_scaled, g_prime_scaled, s_tilde_scaled)

      else:
        left_vectors += [left]
        transforms += [t]
        transforms_unnorm += [t_unnorm]

    if incremental:
      self._g, self._g_scaled = g_prime, g_prime_scaled
      self._lbda, self._lbda_scaled = s_tilde, s_tilde_scaled

    else:
      m_tilde = np.dot(root_inv_mask, np.concatenate([np.sqrt(weight) * np.dot(left, transform) for weight, left, transform in zip(self._weights, left_vectors, transforms)], axis=1))

      q, r = la.qr(m_tilde, mode='economic')

      u, lbda, _ = la.svd(r, full_matrices=False, check_finite=False)

      self._g = np.dot(q, u[:,:self._components])
      self._lbda = lbda[:self._components]

      m_tilde = np.dot(root_inv_mask, np.concatenate([np.sqrt(weight) * np.dot(left, transform) for weight, left, transform in zip(self._weights, left_vectors, transforms_unnorm)], axis=1))

      q, r = la.qr(m_tilde, mode='economic')

      u, lbda, _ = la.svd(r, full_matrices=False, check_finite=False)

      self._lbda_scaled = lbda[:self._components]
      self._g_scaled = np.dot(self._g, np.diag(self._lbda_scaled[:self._components]))

    self._u, self._u_unnorm, self._part_u = [], [], []

    for view_idx in range(views):
      cjj_inv = None
      if inv_qr is not None and inv_qr[view_idx] is not None:
        cjj_inv = inv_qr[view_idx]
      else:
        r = la.qr(data[view_idx], mode='r')[0]
        cjj_inv = la.inv(np.dot(r.T, r) + self._regularizers[view_idx] * np.eye(data[view_idx].shape[1]))
      pinv = np.dot(cjj_inv, data[view_idx].T)

      self._part_u += [pinv]
      self._u += [np.dot(pinv, self._g)]
      self._u_unnorm += [np.dot(pinv, self._g_scaled)]

    return self


  def transform(self, data, mask=None, scale=False):
    views = len(data)
    print("views: ", views)
    if len(self._weights) != views:
      raise Exception('incompatible number of views')

    samples = data[0].shape[0]
    for view_idx in range(views):
      if data[view_idx].shape[0] != samples:
        raise Exception('all views must contain the same number of samples')

    if not mask:
      mask = np.ones((samples, views))

    u_transforms = self._u_unnorm if scale else self._u

    embeddings = []
    for view_idx in range(views):
      embeddings += [np.dot(data[view_idx], u_transforms[view_idx])[None,:]]
    embeddings = np.concatenate(embeddings, axis=0)

    weighting = mask * self._weights
    weighting_sum = np.sum(weighting, axis=1, keepdims=True)

    embeddings = np.reshape(weighting.T, (views, samples, 1)) * embeddings

#    g_sum = np.sum(embeddings, axis=0)
#    g_prime = g_sum / weighting_sum
    for i in range (0, views):
        print("Shape data view", i, ":", data[i].shape) 
        print("Shape embeddings view", i, ":", embeddings[i].shape)
    print("Shape embeddings: ", embeddings.shape)  
    return embeddings


  def inverse_transform(self, data, scale=False):
    views = len(data)
    if len(self._weights) != views:
      raise Exception('incompatible number of views')

    samples = data[0].shape[0]
    for view_idx in range(views):
      if data[view_idx].shape[0] != samples:
        raise Exception('all views must contain the same number of samples')

    u_transforms = self._u_unnorm if scale else self._u

    features = []
    for view_idx in range(views):
      features += [np.dot(data[view_idx], la.pinv2(u_transforms[view_idx]))] if data[view_idx] is not None else []

    return features


  def _batch_incremental_pca(self, x, g, s):
    r, b = g.shape[1], x.shape[0]

    xh = np.dot(g.T, x)
    h = x - np.dot(g, xh)
    j, w = la.qr(h, overwrite_a=True, mode='full', check_finite=False)

    q = np.bmat([[np.diag(s), xh], [np.zeros((b,r)), w]])

    g_new, st_new, _ = la.svd(q, full_matrices=False, check_finite=False)
    st_new = st_new[:r]
    g_new = np.asarray(np.dot(np.concatenate([g, j], axis=1), g_new[:,:r]))

    return g_new, st_new


  def save(self, model_path):
    for idx in range(len(self._weights)):
      np.save('{}.w.{:0>2}.npy'.format(model_path, idx), np.array([self._weights[idx]]))
      np.save('{}.u.{:0>2}.npy'.format(model_path, idx), self._u[idx])
      np.save('{}.s.{:0>2}.npy'.format(model_path, idx), self._u_unnorm[idx])


  def load(self, model_path):
    self._u, self._u_unnorm, self._weights = [], [], []
    for idx in range(len(self._regularizers)):
      self._weights += [np.load('{}.w.{:0>2}.npy'.format(model_path, idx))[0]]
      self._u += [np.load('{}.u.{:0>2}.npy'.format(model_path, idx))]
      self._u_unnorm += [np.load('{}.s.{:0>2}.npy'.format(model_path, idx))]
      



#while (len(viewChroma[:,0]) < len(viewMFCC[:,0])):
    #print("nr_frames_chroma lesser than nr_frames_mfcc, removing 1 frame from MFCC")
    #viewMFCC = np.delete(viewMFCC, (0), axis=0)
#while (len(viewMFCC[:,0]) < len(viewChroma[:,0])):
    #print("nr_frames_chroma greater than nr_frames_mfcc, removing 1 frame from Chroma")
    #viewMFCC = np.delete(viewMFCC, (0), axis=0)
def scale_norm(view):
    view = sk.scale(view, with_std=False, axis=1)
    view = sk.normalize(view, axis=1, norm = 'l2')
    return view

def main(args):
    path_mfcc = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/extractedFeatures/3features.csv"
    path_chroma = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/extractedFeatures/2features.csv"
    path_cqt = "/afs/l2f/home/jar/Documents/tese/Tese/tese/evaluation/evaluation scripts/extractedFeatures/1features.csv"
    paths = {"1": path_cqt, "2": path_chroma, "3": path_mfcc}
    views = []
    n_features = int(args[1])
    
    
    for feature in args[2:]:
        for key in paths:
            if (feature == key):
                path = paths[feature]
                view = np.transpose(scale_norm(np.loadtxt(path, delimiter=',')))
                views.append(view)
    
    min_features = len(views[0][:,0])
    for view in views:
        if len(view[:,0]) < min_features:
            min_features = len(view[:,0])
    
    for i in range(0, len(views)):
        counter = 0
        while (len(views[i][:,0]) > min_features):
            counter += 1
            views[i] = np.delete(views[i], (0), axis=0)
        print(counter, "frames were removed")

    for view in views:
        print(view.shape)
            
    data_train = []
    for view in views:
        data_train.append(view)
        
    data_test = []
    for view in views:
        data_test.append(view)

    model = wgcca(n_features)
    model.fit(data_train)
    t = model.transform(data_test)
    t_mean = np.mean(np.array(t), axis=0)
    path_csv = "../extractedFeatures/features.csv"
    t_final = np.transpose(t_mean)
    np.savetxt(path_csv, t_final, delimiter=',')


        
if __name__ == "__main__":
    main(sys.argv)
        

