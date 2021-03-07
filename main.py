from anytree import NodeMixin, RenderTree


class RS_Node(NodeMixin):
	def __init__(self, begin, end, target, cell_num, parent=None):
		super(RS_Node).__init__()
		self.name = f'{begin}{"-"*(cell_num-2)}{end},{target}'  #if cell_num > 1 else f'{begin},{target}'
		self.begin = begin
		self.end = end
		self.target = target
		self.parent = parent
		self.cell_num = cell_num

	def add_child(self, c):
		if self.children is None:
			self.children = [
			    c,
			]
		else:
			self.children.append(c)


class RS:
	def __init__(self, row: int, col: int, target: int, debug: bool = False) -> None:

		self.target = target
		self.cell_num = row + col - 1
		self.min = 1
		self.max = row

		self.debug = debug

		self.answer = []
		self.paths = []

		self.root = RS_Node(begin=self.min, end=self.max, target=self.target, cell_num=self.cell_num)

	def move(self):
		nodes = []
		nodes.append(self.root)
		while len(nodes) > 0:
			if self.debug: self.get_answer(save=False)
			node = nodes.pop()
			target = node.target - node.begin - node.end
			cell_num = node.cell_num - 2
			if cell_num <= 0:  # reach end already, no child for the node
				continue

			for i in (0, 1):
				for j in (-1, 0):
					begin = node.begin + i
					end = node.end + j
					if (begin > end or cell_num == 1 and target != begin or cell_num == 1 and begin != end
					    or cell_num == 2 and target != (begin + end)):
						if self.debug: print(f'\tFail {begin}{"_"*(cell_num-2)}{end},{target}')
						pass
					else:
						if self.debug: print(f'\tSucc {begin}{"_"*(cell_num-2)}{end},{target}')
						child = RS_Node(begin=begin, end=end, target=target, cell_num=cell_num, parent=node)
						nodes.append(child)

	def get_answer(self, save: bool = False):
		# print('-' * 20)
		max_depth = int(self.cell_num / 2)

		for pre, fill, node in RenderTree(self.root):
			if self.debug: print(f'{pre}{node.name}')

			if node.depth == max_depth:
				cells = []
				if node.cell_num == 1:
					cells.append(node.begin)
				else:
					cells.append(node.end)
					cells.insert(0, node.begin)
				p = node.parent
				while p:
					cells.append(p.end)
					cells.insert(0, p.begin)
					p = p.parent
				if save: self.answer.append(cells)
				if self.debug: print(f'{cells}')

	def verify_n_show_cells(self):
		total_valid = 0
		total_invalid = 0

		for cells in self.answer:
			begin = cells[0]
			sum = 0
			valid = True
			for cell in cells:
				if cell == begin or cell == begin + 1:
					begin = cell
					sum += cell
				else:
					valid = False
					break

			if sum != self.target:
				valid = False

			if valid:
				total_valid += 1
				if self.debug: print(f'{cells}')
			else:
				total_invalid += 1
				if self.debug: print(f'{cells} is not valid')
		if self.debug: print(f'total valid {total_valid}, total_invalid {total_invalid}')

	def get_paths(self):
		for cells in self.answer:
			path = []
			for i in range(1, len(cells)):
				if cells[i] == cells[i - 1]:
					path.append('R')
				elif cells[i] == cells[i - 1] + 1:
					path.append('D')
				else:
					path.append('J')

			self.paths.append(path)

		for path in self.paths:
			print(f'{self.target} {"".join(path)}')


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='right sum operation')

	parser.add_argument('-r', '--rows', type=int, required=True)
	parser.add_argument('-c', '--cols', type=int, required=True)
	parser.add_argument('-t', '--target', type=int, required=True)

	parser.add_argument('-D', '--debug', action='store_true', help='show more debug info')

	args = parser.parse_args()

	rs = RS(args.rows, args.cols, args.target, debug=args.debug)
	rs.move()
	rs.get_answer(save=True)
	rs.verify_n_show_cells()
	rs.get_paths()
