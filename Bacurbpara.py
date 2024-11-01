from PyQt5.QtGui import QIcon
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QDialog, QMessageBox, QApplication
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsWkbTypes, QgsFeatureRequest  # Add QgsFeatureRequest here
from qgis.utils import iface

class BacurbparaDialog(QDialog):
    def __init__(self, parent=None):
        super(BacurbparaDialog, self).__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), 'Bacurbpara.ui')
        uic.loadUi(ui_path, self)
     
        # Connect buttons to methods - group update

        self.btnUpdateArea_sq.clicked.connect(self.Update_area_sq)  # Cal Area fields
        self.btnUpdateArea_ha.clicked.connect(self.Update_area_ha)  # Cal Area fields
        self.btnUpdateUnitNr.clicked.connect(self.Update_unit_number)  # Cal Unit field
        self.btnUpdatePOP.clicked.connect(self.Update_population)  # Cal Population field
        self.btnUpdateGFA.clicked.connect(self.Update_gfa)  # Cal GFA field
        self.btnUpdateFAR.clicked.connect(self.Update_far)  # Cal FAR field
        self.btnUpdateCoverage.clicked.connect(self.update_coverage)  # Update Coverage
        self.btnUpdateFlmin.clicked.connect(self.update_floormin)  # Update Floor Min
        self.btnUpdateFlmax.clicked.connect(self.update_floormax)  # Update Floor Max
        self.btnUpdatePodfl.clicked.connect(self.update_Podfl)  # Update Podium field

        # Connect buttons to methods - Group Calculation
        self.btnCalAll.clicked.connect(self.Cal_all_fields)  # Cal all fields
        self.btnCalAll_LowRes.clicked.connect(self.Cal_all_lowres_fields)  # Cal all fields
        self.btnCalArea.clicked.connect(self.start_Cal_area)  # Cal Area fields
        self.btnCalUnit.clicked.connect(self.Cal_unit_number)  # Cal Unit field
        self.btnCalUnit_LowRes.clicked.connect(self.Cal_unit_lowres_number)  # Cal Unit Lowres field
        self.btnCalPOP.clicked.connect(self.Cal_population)  # Cal Population field
        self.btnCalGFA.clicked.connect(self.Cal_gfa)  # Cal GFA field
        self.btnCalFAR.clicked.connect(self.Cal_far)  # Cal FAR field
 
        # Connect buttons to methods - pther
        self.btnClose.clicked.connect(self.close_dialog)  # Close dialog button

    def validate_numeric(self, value, field_name, allow_zero=False):
        """Validate that value is a positive float or integer. Allow zero if specified."""
        try:
            val = float(value)
            if val < 0 or (val == 0 and not allow_zero):
                raise ValueError
            return True
        except ValueError:
            message = f"Please enter a non-negative number for {field_name} (≥ 0)." if allow_zero else f"Please enter a positive number for {field_name}."
            QMessageBox.warning(self, "Invalid Input", message)
            return False

    def update_field(self, field_name, value, allow_zero=False):
        """Updates the specified field with error checking and progress tracking."""
        layer = iface.activeLayer()
        if not layer.isEditable():
            layer.startEditing()

        # Ensure field exists
        if field_name not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(field_name, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Progress bar setup
        features = list(layer.selectedFeatures() if self.checkBox_selected_features.isChecked() else layer.getFeatures())
        total_features = len(features)
        self.progressBar.setMaximum(total_features)
        self.progressBar.setValue(0)

        # Update field
        updated_count = 0
        error_count = 0
        layer.startEditing()
        
        for i, feature in enumerate(features):
            if not self.validate_numeric(value, field_name, allow_zero=allow_zero):
                layer.rollback()
                return
            
            try:
                feature[field_name] = value
                layer.updateFeature(feature)
                updated_count += 1
            except Exception:
                error_count += 1

            self.progressBar.setValue(i + 1)
            QApplication.processEvents()
        
        if error_count == 0:
            layer.commitChanges()
            QMessageBox.information(self, "Completed", f"Updated {field_name} for {updated_count} features successfully.")
        else:
            layer.rollback()
            QMessageBox.warning(self, "Update Error", f"Failed to update {field_name}. Changes rolled back.")

    def get_field_names(self):
        area_sq_field = "area_sq" # default field name
        area_ha_field = "area_ha" # default field name
        selected_features = self.checkBox_selected_features.isChecked()
        return area_sq_field, area_ha_field, selected_features

    def get_parameters(self):
        try:
            area_sq = float(self.lineEdit_area_sq_value.text())
            area_ha = float(self.lineEdit_area_ha_value.text())
            coverage = float(self.lineEdit_coverage_value.text())
            floor_min = float(self.lineEdit_floor_min_value.text())
            floor_max = float(self.lineEdit_floor_max_value.text())
            podium_fl = float(self.lineEdit_podium_fl_value.text())
            unit_area = float(self.lineEdit_unit_area_value.text())
            unit_number = float(self.lineEdit_unit_number_value.text())
            unit_person = float(self.lineEdit_unit_person_value.text())
            pop_value = float(self.lineEdit_population_value.text())
            GFA_value = float(self.lineEdit_GFA_value.text())
            FAR_value = float(self.lineEdit_FAR_value.text())
            return area_sq, area_ha, coverage, floor_min, floor_max, podium_fl, unit_area, unit_number, unit_person, pop_value, GFA_value, FAR_value
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values in all input fields.")
            return None

# =============== UPDATE FUNCTIONS ======================

    def Update_area_sq(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        area_sq, _, _, _, _, _, _, _, _, _, _, _ = parameters
        self.update_field("Area_sq", area_sq, allow_zero=True)

    def Update_area_ha(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, area_ha, _, _, _, _, _, _, _, _, _, _ = parameters
        self.update_field("Area_ha", area_ha, allow_zero=True)

    def update_coverage(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, coverage, _, _, _, _, _, _, _, _, _ = parameters
        self.update_field("Coverage", coverage, allow_zero=True)

    def update_floormin(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, floor_min, _, _, _, _, _, _, _, _ = parameters
        self.update_field("FloorMin", floor_min, allow_zero=True)

    def update_floormax(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, floor_max, _, _, _, _, _, _, _ = parameters
        self.update_field("FloorMax", floor_max, allow_zero=True)

    def update_Podfl(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, podium_fl, _, _, _, _, _, _ = parameters
        self.update_field("Podium", podium_fl, allow_zero=True)

    def Update_unit_number(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, _, unit_number, _, _, _, _ = parameters
        self.update_field("UnitNumber", unit_number, allow_zero=True)

    def Update_population(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, _, _, unit_person, pop_value, _, _ = parameters
        calculated_population = unit_person * pop_value
        self.update_field("Population", calculated_population, allow_zero=True)

    def Update_gfa(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, _, _, _, _, GFA_value, _ = parameters
        self.update_field("GFA", GFA_value, allow_zero=True)

    def Update_far(self):
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, _, _, _, _, _, FAR_value = parameters
        self.update_field("FAR", FAR_value, allow_zero=True)

# =============== CALCULATOIN FUNCTIONS ======================

    def start_layer_editing(self, layer):
        """Start editing mode on the layer, if not already enabled."""
        if layer and not layer.isEditable():
            layer.startEditing()
        return layer.isEditable()

    def Cal_unit_number(self):
        """Calculate Unit Number based on field values in the layer and UnitArea from parameters."""
        area_sq_field, _, selected_features_only = self.get_field_names()

        # Get active layer and start editing
        layer = iface.activeLayer()
        if not layer:
            QMessageBox.warning(self, "Layer Error", "No active layer found. Please select a valid layer.")
            return
        if not self.start_layer_editing(layer):
            QMessageBox.warning(self, "Layer Error", "Failed to enter edit mode.")
            return

        # Retrieve UnitArea from parameters
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, unit_area, _, _, _, _, _ = parameters  # Extract UnitArea

        # Ensure 'Unit' field exists
        unit_field = "Unit"
        if unit_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(unit_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Set up progress bar and update counter
        features = list(layer.selectedFeatures() if selected_features_only else layer.getFeatures())
        total_features = len(features)
        self.progressBar.setMaximum(total_features)
        updated_count = 0

        # Calculate unit number for each feature
        for i, feature in enumerate(features):
            try:
                area_sq = feature[area_sq_field]
                coverage = feature['Coverage']
                floor_max = feature['FloorMax']
                podium_fl = feature['Podium']
                
                unit_value = round((area_sq * (coverage / 100) * (floor_max - podium_fl)) / unit_area, 0)
                feature[unit_field] = unit_value
                layer.updateFeature(feature)
                updated_count += 1
            except KeyError as e:
                QMessageBox.warning(self, "Field Error", f"Missing required field: {str(e)}")
                continue
            
            # Update progress bar
            self.progressBar.setValue(i + 1)
            QApplication.processEvents()

        layer.commitChanges()
        QMessageBox.information(self, "Completed", f"Unit field updated for {updated_count} features.")

    def Cal_unit_lowres_number(self):
        """Calculate Unit Number based on field values in the layer and UnitArea from parameters."""
        area_sq_field, _, selected_features_only = self.get_field_names()

        # Get active layer and start editing
        layer = iface.activeLayer()
        if not layer:
            QMessageBox.warning(self, "Layer Error", "No active layer found. Please select a valid layer.")
            return
        if not self.start_layer_editing(layer):
            QMessageBox.warning(self, "Layer Error", "Failed to enter edit mode.")
            return

        # Retrieve UnitArea from parameters
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, unit_area, _, _, _, _, _ = parameters  # Extract UnitArea

        # Ensure 'Unit' field exists
        unit_field = "Unit"
        if unit_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(unit_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Set up progress bar and update counter
        features = list(layer.selectedFeatures() if selected_features_only else layer.getFeatures())
        total_features = len(features)
        self.progressBar.setMaximum(total_features)
        updated_count = 0

        # Calculate unit number for each feature
        for i, feature in enumerate(features):
            try:
                area_sq = feature[area_sq_field]
                coverage = feature['Coverage']
                floor_max = feature['FloorMax']
                podium_fl = feature['Podium']
                
                unit_value = round((area_sq * (coverage / 100) ) / unit_area, 0)
                feature[unit_field] = unit_value
                layer.updateFeature(feature)
                updated_count += 1
            except KeyError as e:
                QMessageBox.warning(self, "Field Error", f"Missing required field: {str(e)}")
                continue
            
            # Update progress bar
            self.progressBar.setValue(i + 1)
            QApplication.processEvents()

        layer.commitChanges()
        QMessageBox.information(self, "Completed", f"Unit field updated for {updated_count} features.")

    def Cal_population(self):
        """Calculate Population field based on the formula (Unit * unit_person) using layer field values and UnitPerson from parameters."""
        
        layer = iface.activeLayer()
        if not layer:
            QMessageBox.warning(self, "Layer Error", "No active layer found. Please select a valid layer.")
            return
        if not self.start_layer_editing(layer):
            QMessageBox.warning(self, "Layer Error", "Failed to enter edit mode.")
            return

        # Retrieve UnitPerson from parameters
        parameters = self.get_parameters()
        if not parameters:
            return
        _, _, _, _, _, _, _, _, unit_person, _, _, _ = parameters  # Extract UnitPerson

        # Ensure 'Population' field exists
        population_field = "Population"
        if population_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(population_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Set up progress bar and update counter
        features = list(layer.selectedFeatures() if self.checkBox_selected_features.isChecked() else layer.getFeatures())
        total_features = len(features)
        self.progressBar.setMaximum(total_features)
        updated_count = 0

        for i, feature in enumerate(features):
            try:
                unit_value = feature['Unit']
                population_value = round(unit_value * unit_person, 0)
                feature[population_field] = population_value
                layer.updateFeature(feature)
                updated_count += 1
            except KeyError as e:
                QMessageBox.warning(self, "Field Error", f"Missing required field: {str(e)}")
                continue

            # Update progress bar
            self.progressBar.setValue(i + 1)
            QApplication.processEvents()

        layer.commitChanges()
        QMessageBox.information(self, "Completed", f"Population field updated for {updated_count} features.")

    def Cal_gfa(self):
        """Calculate GFA field based on the formula (area_sq * coverage * floor_max) using layer field values."""
        area_sq_field, _, selected_features_only = self.get_field_names()
        
        layer = iface.activeLayer()
        if not layer:
            QMessageBox.warning(self, "Layer Error", "No active layer found. Please select a valid layer.")
            return
        if not self.start_layer_editing(layer):
            QMessageBox.warning(self, "Layer Error", "Failed to enter edit mode.")
            return

        # Ensure 'GFA' field exists
        gfa_field = "GFA"
        if gfa_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(gfa_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Set up progress bar and update counter
        features = list(layer.selectedFeatures() if selected_features_only else layer.getFeatures())
        total_features = len(features)
        self.progressBar.setMaximum(total_features)
        updated_count = 0

        for i, feature in enumerate(features):
            try:
                area_sq = feature[area_sq_field]
                coverage = feature['Coverage']
                floor_max = feature['FloorMax']
                gfa_value = round(area_sq * (coverage / 100) * floor_max, 0)
                feature[gfa_field] = gfa_value
                layer.updateFeature(feature)
                updated_count += 1
            except KeyError as e:
                QMessageBox.warning(self, "Field Error", f"Missing required field: {str(e)}")
                continue

            # Update progress bar
            self.progressBar.setValue(i + 1)
            QApplication.processEvents()

        layer.commitChanges()
        QMessageBox.information(self, "Completed", f"GFA field updated for {updated_count} features.")

    def Cal_far(self):
        """Calculate FAR field based on the formula ((area_sq * coverage * floor_max) / area_sq) using layer field values."""
        area_sq_field, _, selected_features_only = self.get_field_names()
        
        layer = iface.activeLayer()
        if not layer:
            QMessageBox.warning(self, "Layer Error", "No active layer found. Please select a valid layer.")
            return
        if not self.start_layer_editing(layer):
            QMessageBox.warning(self, "Layer Error", "Failed to enter edit mode.")
            return

        # Ensure 'FAR' field exists
        far_field = "FAR"
        if far_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(far_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Set up progress bar and update counter
        features = list(layer.selectedFeatures() if selected_features_only else layer.getFeatures())
        total_features = len(features)
        self.progressBar.setMaximum(total_features)
        updated_count = 0

        for i, feature in enumerate(features):
            try:
                area_sq = feature[area_sq_field]
                coverage = feature['Coverage']
                floor_max = feature['FloorMax']
                far_value = round((area_sq * (coverage / 100) * floor_max) / area_sq, 1)
                feature[far_field] = far_value
                layer.updateFeature(feature)
                updated_count += 1
            except KeyError as e:
                QMessageBox.warning(self, "Field Error", f"Missing required field: {str(e)}")
                continue

            # Update progress bar
            self.progressBar.setValue(i + 1)
            QApplication.processEvents()

        layer.commitChanges()
        QMessageBox.information(self, "Completed", f"FAR field updated for {updated_count} features.")

    def start_Cal_area(self):
        """Calculate Area_sq and Area_ha fields based on feature geometry with progress tracking.
        Handles invalid geometries and provides detailed error messages.
        """
        area_sq_field, area_ha_field, selected_features_only = self.get_field_names()
        layer = iface.activeLayer()

        if layer is None:
            QMessageBox.warning(self, "Layer Error", "No active layer found. Please select a valid layer.")
            return
        if layer.wkbType() not in [QgsWkbTypes.Polygon, QgsWkbTypes.MultiPolygon]:  # Check geometry type
            QMessageBox.warning(self, "Layer Error", "Selected layer is not a polygon layer.")
            return

        # Start editing
        layer.startEditing()

        # Add fields if they do not exist
        if area_sq_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(area_sq_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        if area_ha_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(area_ha_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        # Select features based on checkbox setting
        request = QgsFeatureRequest()
        if selected_features_only:
            request.setFilterFids([f.id() for f in layer.selectedFeatures()])
        features = layer.getFeatures(request)
        
        # Count features for progress bar
        total_features = len(list(features))  
        self.progressBar.setMaximum(total_features)
        features = layer.getFeatures(request)  # Reload features after counting

        # Calculate area fields with error handling
        updated_count = 0
        for i, feature in enumerate(features):
            try:
                area = feature.geometry().area()
                if area <= 0:
                    raise ValueError("Area calculation failed or is non-positive")
                area_sq = area
                area_ha = area / 10000
            except Exception as e:
                QMessageBox.warning(self, "Calculation Error", f"Error calculating area for feature {feature.id()}: {str(e)}")
                continue

            feature[area_sq_field] = area_sq
            feature[area_ha_field] = area_ha
            if not layer.updateFeature(feature):
                QMessageBox.warning(self, "Update Error", f"Error updating feature {feature.id()}")
                continue
            updated_count += 1

            # Update progress bar
            self.progressBar.setValue(i + 1)
            QApplication.processEvents()  # Immediate UI update

        # Commit changes
        layer.commitChanges()
        QMessageBox.information(self, "Completed", f"Area fields updated for {updated_count} features.")


        """Cal FAR field based on the formula ((area_sq * coverage * floor_max) / area_sq) with validation."""
        area_sq_field, _, _ = self.get_field_names()
        parameters = self.get_parameters()
        if not parameters:
            return
        coverage, _, floor_max, _, _, _ = parameters

        if not (self.validate_numeric(coverage, "Coverage") and
                self.validate_numeric(floor_max, "Floor Max")):
            return

        layer = iface.activeLayer()
        if not layer.isEditable():
            layer.startEditing()
        
        far_field = "FAR"
        if far_field not in [field.name() for field in layer.fields()]:
            layer.dataProvider().addAttributes([QgsField(far_field, QVariant.Double, "double", 10, 2)])
            layer.updateFields()

        features = layer.selectedFeatures() if self.checkBox_selected_features.isChecked() else layer.getFeatures()
        for feature in features:
            area_sq = feature[area_sq_field]
            far_value = round((area_sq * (coverage / 100) * floor_max) / area_sq, 1)
            feature[far_field] = far_value
            layer.updateFeature(feature)

        layer.commitChanges()
        QMessageBox.information(self, "Completed", "FAR field updated.")

    def Cal_all_fields(self):
        """Run all field Cal functions to update all calculated fields."""
        if not self.get_parameters():
            return
        self.start_Cal_area()        # Cal Area_sq and Area_ha
        self.Cal_gfa()               # Cal GFA
        self.Cal_far()               # Cal FAR
        self.Cal_unit_number()       # Cal Unit Number
        self.Cal_population()        # Cal Population

    def Cal_all_lowres_fields(self):
        """Run all field Cal functions to update all calculated fields."""
        if not self.get_parameters():
            return
        self.start_Cal_area()               # Cal Area_sq and Area_ha
        self.Cal_gfa()                      # Cal GFA
        self.Cal_far()                      # Cal FAR
        self.Cal_unit_lowres_number()       # Cal Unit Number
        self.Cal_population()               # Cal Population

    def close_dialog(self):
        """Close the dialog."""
        self.close()

class BacurbparaPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.action = QAction(QIcon(icon_path), "Update All", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Bacurbpasra Plugin", self.action)

    def unload(self):
        self.iface.removePluginMenu("Bacurbpara Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if not self.dialog:
            self.dialog = BacurbparaDialog()
        self.dialog.show()
