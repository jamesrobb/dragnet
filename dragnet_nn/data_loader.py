import random

class data_loader:

	# path to a file where the matrices/labels are
	matrices_path = None
	labels_path = None

	fh_matrices = None
	fh_labels = None

	all_matrices = []
	all_labels = []

	rolling_index = 0

	# for when we don't want to use labels for the data
	load_labels = True

	def __init__(self, _matrices_path, _labels_path = None):
		self.matrices_path = _matrices_path
		self.labels_path = _labels_path

		self.fh_matrices = open(self.matrices_path)

		if _labels_path is None:
			self.load_labels = False
		else:
			self.fh_labels = open(self.labels_path)

	def __del__(self):
		self.close_files()

	def all_data(self):

		self.all_matrices = self.all_data_fh(self.fh_matrices)

		if self.load_labels:
			self.all_labels = self.all_data_fh(self.fh_labels)

		return self.all_matrices, self.all_labels

	def all_data_fh(self, fh):

		ret_arr = []

		while True:

			line = fh.readline().rstrip("\n")

			if line == "":
				break

			ret_arr.append([float(x) for x in line.split(",")])

		return ret_arr


	def close_files(self):

		if self.fh_matrices is not None:
			self.fh_matrices.close()

		if self.fh_labels is not None:
			self.fh_labels.close()


	def next_batch_rolling(self, batch_size):

		if len(self.all_matrices) == 0:
			self.all_data()

		ret_matrices = self.next_batch_rolling_fh(batch_size, self.all_matrices)

		if self.load_labels:
			self.rolling_index = abs((self.rolling_index - batch_size) % len(self.all_matrices))
			ret_labels = self.next_batch_rolling_fh(batch_size, self.all_labels)
		else:
			ret_labels = []

		return ret_matrices, ret_labels

	def next_batch_rolling_fh(self, batch_size, source_arr):

		ret_arr = []

		for i in range(0, batch_size):

			ret_arr.append(source_arr[self.rolling_index])
			self.rolling_index = (self.rolling_index + 1) % len(self.all_matrices)

		return ret_arr