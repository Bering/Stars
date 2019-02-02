import os
import pygame
from screen_base import ScreenBase
from button import Button

class StarScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.star = None
		self.selected_planet = None
		self.selected_fleet = None

		filename = os.path.join("images", "selection.png")
		self.selection_marker_surface = pygame.image.load(filename)

		filename = os.path.join("images", "ownermarker.png")
		self.owned_planet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "shipyard.png")
		self.shipyard_surface = pygame.image.load(filename)

		filename = os.path.join("images", "defense.png")
		self.defense_surface = pygame.image.load(filename)

		self.next_turn_button = Button("End Turn", self.on_next_turn_clicked)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.on_next_turn_clicked()
			elif (event.key == pygame.K_g):
				self._app.screens.change_to("Galaxy")
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
			if self.star and self.centered_rect.collidepoint(event.pos):
				self.on_star_clicked()
			elif self.next_turn_button.rect.collidepoint(event.pos):
				self.on_next_turn_clicked()
			else:
				rect = self.centered_rect.copy()
				rect.midleft = self.centered_rect.topright
				if rect.collidepoint(event.pos):
					for f in self.star.fleets:
						if not f.planet:
							self.on_fleet_clicked(f)
							return
				for p in self.star.planets:
					if p.rect.collidepoint(event.pos):
						self.on_planet_clicked(p)
					else:
						rect = p.rect.copy()
						rect.midleft = p.rect.topright
						if rect.collidepoint(event.pos):
							if p.fleets:
								self.on_fleet_clicked(p.fleets[0]) # TODO: What about many fleets at the same planet?

	def update(self, delta_time):
		pass

	def render(self, surface):
		for f in self.star.fleets:
			if not f.planet:
				rect = f.rect.copy()
				rect.midleft = self.centered_rect.topright
				surface.blit(self.fleet_surface, rect)
			elif f.destination_planet:
				rect = f.get_departing_planet_rect(f.destination_planet.rect)
				surface.blit(self.fleet_surface, rect)
				pygame.draw.aaline(surface, (255,255,255), rect.center, f.destination_planet.rect.center)
			elif f.destination_star:
				rect = f.get_departing_planet_rect(self.centered_rect)
				surface.blit(self.fleet_surface, rect)
				pygame.draw.aaline(surface, (255,255,255), rect.center, self.centered_rect.center)
			else:
				rect = f.planet.rect.copy()
				rect.midleft = f.planet.rect.topright
				surface.blit(self.fleet_surface, rect)

			if f == self.selected_fleet:
				if f.planet:
					rect = f.planet.rect.copy()
					rect.midleft = f.planet.rect.topright
				else:
					rect = self.centered_rect.copy()
					rect.midleft = self.centered_rect.topright
				surface.blit(self.selection_marker_surface, rect)

		for p in self.star.planets:
			surface.blit(p.surface, p.rect)

			if self.selected_planet:
				surface.blit(self.selection_marker_surface, self.selected_planet.rect)

			if p.player:
				surface.blit(self.owned_planet_surface, p.rect)

			if p.shipyard_level > 0:
				rect = p.rect.copy()
				rect.midleft = p.rect.bottomright
				surface.blit(self.shipyard_surface, rect)

			if p.defense > 0:
				rect = p.rect.copy()
				rect.midright = p.rect.bottomleft
				surface.blit(self.defense_surface, rect)
			
			surface.blit(p.name_surf, p.name_rect)

		self.centered_rect.center = surface.get_rect().center
		surface.blit(self.centered_surface, self.centered_rect)
		self.name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.star.name_surf, self.name_rect)
		
		self.next_turn_button.rect.topright = surface.get_rect().topright
		self.next_turn_button.render(surface)

	def select_star(self, star):
		"""Setup the screen around this star"""
		self.star = star
		self.selected_planet = None
		self.selected_fleet = None

		self.centered_rect = star.rect.copy()
		self.centered_rect.width *= 3
		self.centered_rect.height *= 3
		self.centered_surface = pygame.transform.smoothscale(star.surface, self.centered_rect.size)

		self.name_rect = self.star.name_surf.get_rect()

	def select_planet(self, planet):
		if self.selected_fleet:
			self.selected_fleet.set_destination_planet(planet)
			self.selected_fleet = None
		else:
			if self.selected_planet == planet:
				screen = self._app.screens.change_to("Planet")
				screen.select_planet(planet)
			else:
				self.selected_planet = planet

	def select_fleet(self, fleet):
		self.selected_fleet = fleet

	def on_star_clicked(self):
		if self.selected_fleet:
			self.selected_fleet.set_destination_star(self.star)
			self.selected_fleet = None
		else:
			self._app.screens.change_to("Galaxy")

	def on_planet_clicked(self, planet):
		self.select_planet(planet)

	def on_fleet_clicked(self, fleet):
		self.select_fleet(fleet)

	def on_next_turn_clicked(self):
		self._app.next_turn()
