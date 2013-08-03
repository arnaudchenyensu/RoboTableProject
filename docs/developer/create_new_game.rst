How to create a new game?
=========================

If you want to create a new game, you will have to create a new class that inherits from the Game class. Then you need to override the method start. When you override this method, you'll need first to call these methods::

    self.game_management.start(self.addr_main_server, self.is_main_server(), self.addr)
    self.x_factors = self.game_management.x_factors
    self.y_factors = self.game_management.y_factors
    self.servers = self.game_management.servers

You then write every thing you want to execute for your game and finish by these lines::

    self.gui.after(100, self._update_map)
    self.gui.mainloop()

In the example above, the method _update_map will be call every 100ms, and therefore, you will have to override this method (for updating your drawings, check state of the game...).

