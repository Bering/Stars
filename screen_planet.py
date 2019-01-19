import os
import pygame
from screen_base import ScreenBase

class PlanetScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.planet = None

		filename = os.path.join("images", "ownermarker.png")
		self.owned_planet_surface = pygame.image.load(filename)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.change_screen("Quit")
			elif (event.key == pygame.K_g):
				self._app.change_screen("Galaxy")
			elif (event.key == pygame.K_PERIOD):
				self.on_next_planet()
			elif (event.key == pygame.K_p):
				if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
					self.on_prev_planet()
				elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
					self.on_prev_planet()
				else:
					self.on_next_planet()
			elif (event.key == pygame.K_COMMA):
				self.on_prev_planet()

		elif (event.type == pygame.MOUSEBUTTONUP):
			if self.centered_rect.collidepoint(event.pos):
				self.on_planet_clicked()

	def update(self, delta_time):
		pass

	def render(self, surface):
		self.centered_rect.center = surface.get_rect().center
		self.name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.centered_surface, self.centered_rect)
		surface.blit(self.planet.name_surf, self.name_rect)

	def select_planet(self, planet):
		self.planet = planet

		self.centered_rect = planet.rect.copy()
		self.centered_rect.width *= 3
		self.centered_rect.height *= 3
		self.centered_surface = pygame.transform.scale(planet.surface, self.centered_rect.size)

		self.name_rect = self.planet.name_surf.get_rect()
		self.name_rect.midtop = self.centered_rect.midbottom

	def on_planet_clicked(self):
		self._app.change_screen("Star")

	def on_next_planet(self):
		self.select_planet(self._app.local_player.next_planet(self.selected_planet).star)

	def on_prev_planet(self):
		self.select_planet(self._app.local_player.prev_planet(self.selected_planet).star)