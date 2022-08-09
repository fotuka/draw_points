import os.path
import os
from dataclasses import dataclass
from sys import platform
import getpass

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis._core import Qgis, QgsProject, QgsVectorFileWriter
from qgis.core import QgsVectorLayer

from .calculation import *
from .draw_points_dialog import DrawPointsDialog

NO_CONFIGURATION = None
SIMPLE_GRID_CONFIGURATION = 'grid'
SLOPE_GRID_CONFIGURATION = 'gridslope'
SIMPLE_SNOW_CONFIGURATION = 'snow'
ADVANCED_SNOW_CONFIGURATION = 'snowadvanced'
NEW_TXT = 'New txt'
TEMP_XY_CSV = '/temp_xy.csv'


@dataclass
class Info:
    path = 'xy.csv'
    type = 'regexp'
    delimiter = '%20'
    useheader = 'No'
    maxfields = '10000'
    detecttypes = 'yes'
    xfield = 'field_1'
    yfield = 'field_2'
    crs = 'EPSG:4326'
    spatialindex = 'no'
    subsetindex = 'no'
    watchfile = 'no'
    xfield_text = 'field_1:text'
    yfield_text = 'field_2:text'

    def get_uri(path: str, crs: str, delimiter: str) -> str:
        Info.path = path
        Info.crs = Info.cut_crs(crs)
        Info.delimiter = delimiter
        uri = ('file:' + Info.path + '?type=' + Info.type + '&delimiter=' + Info.delimiter + '&useHeader=' + Info.useheader
               + '&maxFields=' + Info.maxfields + '&detectTypes=' + Info.detecttypes + '&xField=' + Info.xfield + '&yField='
               + Info.yfield + '&crs=' + Info.crs + '&spatialIndex=' + Info.spatialindex + '&subsetIndex=' + Info.subsetindex
               + '&watchFile=' + Info.watchfile + '&field=' + Info.xfield_text + '&field=' + Info.yfield_text)
        return uri

    def cut_crs(crs: str) -> str:
        crs_cutted = crs
        crs_cutted = crs_cutted.split(': ')[1]
        crs_cutted = crs_cutted.split('>')[0]
        return crs_cutted


def get_temp_dir(name: str) -> str:
    path = 'Your platform is unsupported, try linux or windows'
    if platform == 'linux' or platform == 'linux2':
        path = 'var/tmp/' + name
    elif platform == "win32":
        path = 'C:/Users/' + getpass.getuser() + '/AppData/Local/Temp/' + name
    return path


class DrawPoints:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DrawPoints_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&Draw Points')
        self.dlg = DrawPointsDialog()
        self.choose = NO_CONFIGURATION
        self.first_start = None
        self.dlg.choose_grid_button.clicked.connect(self.click_choose_grid)
        self.dlg.choose_gridslope_button.clicked.connect(self.click_choose_gridslope)
        self.dlg.choose_snow_button.clicked.connect(self.click_choose_snow)
        self.dlg.choose_snowadvanced_button.clicked.connect(self.click_choose_snowadvanced)
        self.dlg.choose_path.clicked.connect(self.select_output_file)
        self.dlg.apply_button.clicked.connect(self.apply)
        self.counter = 0

    def tr(self, message):
        return QCoreApplication.translate('DrawPoints', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = ':/plugins/draw_points/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Draw points'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.first_start = True

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Draw Points'),
                action)
            self.iface.removeToolBarIcon(action)
        # if self.counter != 0:
        #     osz.remove(self.get_temp_dir(TEMP_XY_CSV))

    def clear_all_types_input(self):
        self.dlg.snow_radius.setValue(0)
        self.dlg.snow_lines_amount.setValue(0)
        self.dlg.snow_dots_amount.setValue(0)
        self.dlg.grid_height.setValue(0)
        self.dlg.grid_length.setValue(0)
        self.dlg.grid_vertical_lines_amount.setValue(0)
        self.dlg.grid_horizontal_lines_amount.setValue(0)
        self.dlg.rotate.setValue(0)
        self.dlg.coords_x.setValue(0)
        self.dlg.coords_y.setValue(0)
        self.dlg.save_in.clear()

    def grid_hide(self):
        self.dlg.grid_widget.hide()
        self.clear_all_types_input()

    def grid_show(self):
        self.snow_hide()
        self.dlg.grid_widget.show()
        self.dlg.rotate_widget.show()
        self.dlg.coords_widget.show()
        self.dlg.top_widget.show()
        self.dlg.coords_label.setText('Координаты левого нижнего угла')

    def snow_hide(self):
        self.dlg.snow_widget.hide()
        self.clear_all_types_input()

    def snow_show(self):
        self.grid_hide()
        self.dlg.snow_widget.show()
        self.dlg.rotate_widget.show()
        self.dlg.coords_widget.show()
        self.dlg.top_widget.show()
        self.dlg.coords_label.setText('Координаты центра')

    def click_choose_grid(self):
        self.grid_show()
        self.clear_all_types_input()
        self.choose = SIMPLE_GRID_CONFIGURATION

    def click_choose_gridslope(self):
        self.grid_show()
        self.clear_all_types_input()
        self.choose = SLOPE_GRID_CONFIGURATION

    def click_choose_snow(self):
        self.snow_show()
        self.clear_all_types_input()
        self.choose = SIMPLE_SNOW_CONFIGURATION

    def click_choose_snowadvanced(self):
        self.snow_show()
        self.clear_all_types_input()
        self.choose = ADVANCED_SNOW_CONFIGURATION

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Select   output file ", "", '*.shp')
        self.dlg.save_in.setText(filename)

    def hide_all(self):
        self.grid_hide()
        self.snow_hide()
        self.dlg.rotate_widget.hide()
        self.dlg.coords_widget.hide()
        self.dlg.top_widget.hide()

    def add_temp_layer_from_csv(self, path: str, crs, delimiter: str):
        uri = Info.get_uri(path, str(crs), delimiter)
        self.lyr = QgsVectorLayer(uri, NEW_TXT, 'delimitedtext', crs=crs)
        QgsProject.instance().addMapLayer(self.lyr)

    @staticmethod
    def del_layer(name: str):
        layer = QgsProject.instance().mapLayersByName(name)[0]
        QgsProject.instance().removeMapLayers([layer.id()])

    @staticmethod
    def convert_temp_layer_to_shp(layer, path: str):
        QgsVectorFileWriter.writeAsVectorFormat(layer, path, "UTF-8", layer.crs(), "ESRI Shapefile",
                                                layerOptions=['SHPT=POINT'])

    def create_simple_grid_configuration(self):
        grid_height = self.dlg.grid_height.value()
        grid_length = self.dlg.grid_length.value()
        grid_horizontal_lines_amount = self.dlg.grid_horizontal_lines_amount.value()
        grid_vertical_lines_amount = self.dlg.grid_vertical_lines_amount.value()
        self.figure = Grid(grid_length, grid_height, grid_horizontal_lines_amount, grid_vertical_lines_amount)
        self.figure.create()

    def create_slope_grid_configuration(self):
        grid_height = self.dlg.grid_height.value()
        grid_length = self.dlg.grid_length.value()
        grid_horizontal_lines_amount = self.dlg.grid_horizontal_lines_amount.value()
        grid_vertical_lines_amount = self.dlg.grid_vertical_lines_amount.value()
        self.figure = GridSlope(grid_length, grid_height, grid_horizontal_lines_amount, grid_vertical_lines_amount)
        self.figure.create()

    def create_simple_snow_configuration(self):
        snow_dots_amount = self.dlg.snow_dots_amount.value()
        snow_lines_amount = self.dlg.snow_lines_amount.value()
        snow_radius = self.dlg.snow_radius.value()
        self.figure = Snow(snow_radius, snow_dots_amount, snow_lines_amount)
        self.figure.create()

    def create_advanced_snow_configuration(self):
        snow_dots_amount = self.dlg.snow_dots_amount.value()
        snow_lines_amount = self.dlg.snow_lines_amount.value()
        snow_radius = self.dlg.snow_radius.value()
        self.figure = SnowAdvanced(snow_radius, snow_dots_amount, snow_lines_amount)
        self.figure.create()

    def move_all(self):
        self.figure.xy = self.figure.rotate(self.dlg.rotate.value())
        self.figure.xy = self.figure.move_x(self.dlg.coords_x.value())
        self.figure.xy = self.figure.move_y(self.dlg.coords_y.value())

    def create_actual_configuration(self):
        if self.choose == SIMPLE_GRID_CONFIGURATION:
            self.create_simple_grid_configuration()

        if self.choose == SLOPE_GRID_CONFIGURATION:
            self.create_slope_grid_configuration()

        if self.choose == SIMPLE_SNOW_CONFIGURATION:
            self.create_simple_snow_configuration()

        if self.choose == ADVANCED_SNOW_CONFIGURATION:
            self.create_advanced_snow_configuration()

    def apply(self):
        self.create_actual_configuration()
        self.move_all()
        self.figure.export(get_temp_dir(TEMP_XY_CSV))
        if self.counter == 0:
            self.add_temp_layer_from_csv(get_temp_dir(TEMP_XY_CSV),
                                         self.dlg.system_of_coords.crs(), '%20')
        else:
            self.add_temp_layer_from_csv(get_temp_dir(TEMP_XY_CSV),
                                         self.dlg.system_of_coords.crs(), '%20')
            self.del_layer(NEW_TXT)
        self.counter += 1

    def run(self):
        self.dlg.show()
        self.clear_all_types_input()
        self.hide_all()
        result = self.dlg.exec_()
        if result:
            self.create_actual_configuration()
            self.move_all()
            self.figure.export(get_temp_dir('/temp_xy.csv'))
            if self.counter == 0:
                self.add_temp_layer_from_csv(get_temp_dir(TEMP_XY_CSV), self.dlg.system_of_coords.crs(), '%20')
            else:
                self.add_temp_layer_from_csv(os.path.dirname(os.path.abspath(__file__)) + TEMP_XY_CSV,
                                             self.dlg.system_of_coords.crs(), '%20')
                self.del_layer(NEW_TXT)

            if self.dlg.save_in.text() != '':
                path = self.dlg.save_in.text()
                self.convert_temp_layer_to_shp(self.lyr, path)

            self.iface.messageBar().pushMessage(
                'Success',
                level=Qgis.Success, duration=3)
