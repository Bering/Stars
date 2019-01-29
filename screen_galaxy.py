import os
import pygame
from screen_base import ScreenBase
from button import Button

class GalaxyScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_star = None
		self.selected_fleet = None
		
		filename = os.path.join("images", "selection.png")
		self.selection_marker_surface = pygame.image.load(filename)

		filename = os.path.join("images", "ownermarker.png")
		self.owned_star_surface = pygame.image.load(filename)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "shipyard.png")
		self.shipyard_surface = pygame.image.load(filename)

		self.next_turn_button = Button("End Turn", self.on_next_turn_clicked)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.on_next_turn_clicked()
			elif (event.key == pygame.K_PERIOD):
				self.on_next_planet()
			elif (event.key == pygame.K_COMMA):
				self.on_prev_planet()
			elif (event.key == pygame.K_p):
				if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
					self.on_prev_planet()
				elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
					self.on_prev_planet()
				else:
					self.on_next_planet()
		
		elif (event.type == pygame.MOUSEBUTTONUP):
			for s in self._app.world.stars:
				if s.rect.collidepoint(event.pos):
					self.on_select_star(s)

			for player in self._app.players + self._app.ais:
				for fleet in player.fleets:
					if fleet.rect.collidepoint(event.pos):
						self.on_start_moving_fleet(fleet) # TODO: What about many fleets at the same star?

			if self.next_turn_button.rect.collidepoint(event.pos):
				self.on_next_turn_clicked()

	def update(self, delta_time):
		pass

	def render(self, surface):
		for s in self._app.world.stars:
			surface.blit(s.surface, s.rect)

			for p in s.planets:
				if p.player:
					surface.blit(self.owned_star_surface, s.rect)

				if p.shipyard_level > 0:
					rect = s.rect.copy()
					rect.midleft = s.rect.bottomright
					surface.blit(self.shipyard_surface, rect)
			
			surface.blit(s.name_surf, s.name_rect)

		for player in self._app.players + self._app.ais:
			for f in player.fleets:
				if f.destination_star:
					pygame.draw.aaline(surface, (255,255,255), f.rect.center, f.destination_star.rect.center)
				surface.blit(self.fleet_surface, f.rect)
			
		if self.selected_star:
			surface.blit(self.selection_marker_surface, self.selected_star.rect)

		if self.selected_fleet:
			surface.blit(self.selection_marker_surface, self.selected_fleet.rect)

		self.next_turn_button.rect.topright = surface.get_rect().topright
		self.next_turn_button.render(surface)

	def select_star(self, star):
		if self.selected_fleet:
			self.selected_fleet.set_destination_star(star)
			self.selected_fleet = None
		else:
			if self.selected_star == star:
				screen = self._app.screens.change_to("Star")
				screen.select_star(star)
			else:
				self.selected_star = star

	def on_select_star(self, star):
		self.select_star(star)

	def on_next_turn_clicked(self):
		self._app.next_turn()

	def on_start_moving_fleet(self, fleet):
		self.selected_fleet = fleet
