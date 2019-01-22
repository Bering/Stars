class ProductionManager:

	def __init__(self, planet):
		self.projects = {
			"Farms" : ProdPop(planet),
			"Mines" : ProdInd(planet),
			"Laboratories" : ProdSci(planet),
			"Defenses" : ProdDef(planet),
			"Scout" : ProdScout(planet),
			"Colony" : ProdColony(planet),
			"Frigate" : ProdFrigate(planet),
			"Destroyer" : ProdDestroyer(planet),
		}
		self.current_project = None

	def change_to(self, project_name):
		if project_name not in self.projects:
			raise KeyError("Invalid production project name: " + project_name)

		self.current_project = self.projects[project_name]
		self.current_project.change_to()

	def next_turn(self):
		if self.current_project:
			self.current_project.next_turn()


class ProductionBase:

	def __init__(self, planet, name, desc, cost):
		self.planet = planet
		self.name = name
		self.desc = desc
		self.cost = cost
		self.progress = 0

	def change_to(self):
		# TODO: Should we keep the progress made during the previous project?
		self.progress = 0

	def next_turn(self):
		self.progress += self.planet.industry

		item_count = 0

		while(self.progress > self.cost):
			self.progress -= self.cost
			item_count += 1

		self.effect(item_count)

	def effect(self, item_count):
		pass


class ProdPop(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Farms", "Increase population", 5)

	def effect(self, item_count):
		self.planet.population += item_count

class ProdInd(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Mines", "Increase industry", 5)

	def effect(self, item_count):
		self.planet.industry += item_count

class ProdSci(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Laboratories", "Increase science", 5)

	def effect(self, item_count):
		self.planet.science += item_count

class ProdDef(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Defense platforms", "Increase defense", 10)

	def effect(self, item_count):
		self.planet.defense += item_count

class ProdScout(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Scout", "Unarmed. Longer range.", 10)

	def effect(self, item_count):
		for n in range(item_count):
			self.planet.build_ship("Scout")

class ProdColony(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Colony Ship", "Unarmed. Settlers for new colony.", 1000)

	def effect(self, item_count):
		for n in range(item_count):
			self.planet.build_ship("Colony")

class ProdFrigate(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Frigate", "Basic warship.", 100)

	def effect(self, item_count):
		for n in range(item_count):
			self.planet.build_ship("Frigate")

class ProdDestroyer(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Destroyer", "Great against frigates.", 1000)

	def effect(self, item_count):
		for n in range(item_count):
			self.planet.build_ship("Destroyer")

# TODO: Starbases?, More, Refit
