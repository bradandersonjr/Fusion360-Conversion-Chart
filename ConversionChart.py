#Author-Brad Anderson Jr
#Description-Conversion Chart

import adsk.core, adsk.fusion, traceback

app = adsk.core.Application.cast(None)
ui = adsk.core.UserInterface.cast(None)
palette = adsk.core.Palette.cast(None)
ctrl = adsk.core.CommandControl.cast(None)

handlers = []

conversionChartName = 'Conversion Chart'
conversionChartVersion = '1.0'
conversionChartAuthor = 'Brad Anderson Jr'
conversionChartContact = 'brad@bradandersonjr.dev'

# Event handler for the commandExecuted event.
class ShowPaletteCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        global palette, ui
        try:

            cmdDef = ui.commandDefinitions.itemById('showConversionChart')
            if palette.isVisible:
                palette.isVisible = False
                ctrl.commandDefinition.name = 'Show Conversion Chart'
                cmdDef.name = 'Show Conversion Chart'
            else:
                palette.isVisible = True
                ctrl.commandDefinition.name = 'Hide Conversion Chart'
                cmdDef.name = 'Hide Conversion Chart'

        except:
            ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()), conversionChartName, 0, 0)

# Event handler for the commandCreated event.
class ShowPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.command
            onExecute = ShowPaletteCommandExecuteHandler()
            command.execute.add(onExecute)
            handlers.append(onExecute)

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()), conversionChartName, 0, 0)

def run(context):

    global ui, app, palette, ctrl
    global process

    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        qatRToolbar = ui.toolbars.itemById('QATRight')

        showPaletteCmdDef = ui.commandDefinitions.addButtonDefinition('showConversionChart', 'Show Conversion Chart', 'Display a conversion chart for fractions, decimals, and millimeters in Fusion 360.', './resources')

        # Connect to Command Created event.
        onCommandCreated = ShowPaletteCommandCreatedHandler()
        showPaletteCmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        ctrl = qatRToolbar.controls.addCommand(showPaletteCmdDef, 'HealthStatusCommand', False)

        palette = ui.palettes.add('ConversionChartPalette', 'Conversion Chart', 'chart.html', False, True, False, 800, 980)
        palette.isVisible = False
        
        # Dock the palette to the right side of Fusion window.
        palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight
        palette.dockingOptions = adsk.core.PaletteDockingOptions.PaletteDockOptionsToVerticalOnly(True)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()), this_addin_name, 0, 0)


def stop(context):

    global palette

    try:

        cmdDef = ui.commandDefinitions.itemById('showConversionChart')
        if cmdDef:
            cmdDef.deleteMe()

        qatRToolbar = ui.toolbars.itemById('QATRight')
        cmd = qatRToolbar.controls.itemById('showConversionChart')
        if cmd:
            cmd.deleteMe()

        palette = ui.palettes.itemById('ConversionChartPalette')
        if palette:
            palette.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()), conversionChartName, 0, 0)
