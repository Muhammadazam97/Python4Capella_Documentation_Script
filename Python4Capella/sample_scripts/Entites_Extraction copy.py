# name                 : Diagrams Extraction
# script-type          : Python
# description          : Exports diagrams of the selected Element
# popup                : enableFor(org.polarsys.capella.core.data.capellacore.CapellaElement)

# Include necessary Capella Modeller API
include('workspace://Python4Capella/simplified_api/capella.py')
if False:
    from simplified_api.capella import *

# Include requirement API
include('workspace://Python4Capella/simplified_api/requirement.py')
if False:
    from simplified_api.requirement import *

# Include utilities
include('workspace://Python4Capella/utilities/CapellaPlatform.py')
if False:
    from utilities.CapellaPlatform import *


import eclipse.system.ui as ui  # @UnresolvedImport
from py4j.java_gateway import java_import

# Import Java helper classes for Capella
jvm = gateway.jvm  # @UndefinedVariable
java_import(jvm, 'org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper')
CapellaAdapterHelper = jvm.org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper

if __name__ == '__main__':
    try:
       # include needed for the Capella modeller API
        include('workspace://Python4Capella/simplified_api/capella.py')
        if False:
            from simplified_api.capella import *

        aird_path = '/In-Flight Entertainment System/In-Flight Entertainment System.aird'
        model = CapellaModel()
        model.open(aird_path)


        diagrams = model.get_all_diagrams()
        for diagram in diagrams:
            print(diagram.get_name())

    except Exception as e:
        print(f"Unexpected error: {e}")
