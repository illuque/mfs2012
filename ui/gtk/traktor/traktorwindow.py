from gi.repository import Gtk
from . import constants

MENU_UI = '''
<ui>
    <menubar name="MenuBar">
        <menu action="TraktorMenu">
            <menuitem action="About" />
        </menu>
    </menubar>
</ui>
'''

class TraktorWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('Traktor')
        self.set_size_request(500, 300)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        self.ui_manager = self._setup_ui_manager()
        menu_bar = self.ui_manager.get_widget('/MenuBar')
        box.pack_start(menu_bar, False, False, 0)

        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(search_box, False, False, 0)

        self.program_combo = self._get_combo()
        search_box.pack_start(self.program_combo, False, False, 0)
        program_entry = self._get_entry()
        search_box.pack_start(program_entry, False, False, 0)

        self.connect('delete-event', self._quit)

    def _setup_ui_manager(self):
        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(MENU_UI)
        accel_group = ui_manager.get_accel_group()
        self.add_accel_group(accel_group)
        action_group = Gtk.ActionGroup('Actions')
        action_group.add_actions([
                ('TraktorMenu', None, '_Traktor', None, None, None),
                ('About', Gtk.STOCK_ABOUT,
                 '_About', None, 'About this application',
                 self._on_about_action),
                ])
        ui_manager.insert_action_group(action_group)
        return ui_manager

    def _on_about_action(self, action):
        about = Gtk.AboutDialog()
        about.set_program_name("Traktor")
        about.run()
        about.destroy()

    def _quit(self, window, event):
        Gtk.main_quit()

    def run(self):
        self.show_all()
        Gtk.main()

    def _get_combo(self):
        tv_programs = [(`constants.SEARCH_ALL_TYPE`, 'All'), (`constants.SEARCH_EPISODES_TYPE`, 'Episodes'), (`constants.SEARCH_MOVIES_TYPE`, 'Movies'), (`constants.SEARCH_SHOWS_TYPE`, 'Shows')]
        program_combo = Gtk.ComboBoxText()
        for tv_program in tv_programs:
            program_combo.append(tv_program[0], tv_program[1])
        program_combo.set_active_id(`constants.SEARCH_ALL_TYPE`)
        return program_combo

    def _get_entry(self):
        search_entry = Gtk.Entry()
        search_entry.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_FIND)
        search_entry.set_placeholder_text("Search...")
        search_entry.connect("icon-press", self._on_search_icon_pressed)
        search_entry.connect("activate", self._on_search_enter_pressed)
        return search_entry

    def _on_search_icon_pressed(self, program_entry, icon_pos, event):
        query = self._get_query(program_entry)
        print "Selected: id=%s, type=%s, text=%s" % (query)

    def _on_search_enter_pressed(self, program_entry):
        query = self._get_query(program_entry)
        print "Selected: id=%s, type=%s, text=%s" % (query)

    def _get_query(self, program_entry):
        return (self.program_combo.get_active_id(), self.program_combo.get_active_text(), program_entry.get_text())
