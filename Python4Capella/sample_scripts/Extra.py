# name                 : Extract Diagram Entities and Relationships
# script-type          : Python
# description          : Searches for the specified diagram and retrieves all its entities and relationships.
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

def get_entities_and_relationships_from_diagram(model, diagram_name):
    """Finds a diagram by name and retrieves all its entities and relationships."""
    diagrams = model.get_all_diagrams()
    for diagram in diagrams:
        if diagram.get_name() == diagram_name:
            print(f"Diagram found: {diagram.get_name()}")
            # Get all represented elements in the diagram
            elements = []
            for element in diagram.get_represented_elements():
                elements.append(element)
                # Print element details
                if hasattr(element, 'get_name'):
                    print(f"Entity: {element.get_name()} - Type: {element.__class__.__name__}")
                else:
                    print(f"Entity: {element} - Type: {element.__class__.__name__}")
            
            # Retrieve relationships between elements
            relationships = []
            for element in elements:
                # Handle SequenceMessage objects
                if element.__class__.__name__ == "SequenceMessage":
                    # Use the correct methods for SequenceMessage
                    sending_role = element.get_sending_instance_role()  # Get the sending role
                    receiving_role = element.get_receiving_instance_role()  # Get the receiving role
                    if sending_role and receiving_role:
                        # Get the names of the sending and receiving roles
                        source = sending_role.get_name()
                        target = receiving_role.get_name()
                        message_name = element.get_name() if hasattr(element, 'get_name') else "Unnamed Message"
                        relationships.append(("SequenceMessage", message_name, source, target))
                
                # Handle FunctionalExchange objects
                elif element.__class__.__name__ == "FunctionalExchange":
                    # Get the source and target of the FunctionalExchange
                    source = element.get_source().get_name() if element.get_source() else "Unknown Source"
                    target = element.get_target().get_name() if element.get_target() else "Unknown Target"
                    exchange_name = element.get_name() if hasattr(element, 'get_name') else "Unnamed FunctionalExchange"
                    relationships.append(("FunctionalExchange", exchange_name, source, target))
                
                # Handle OperationalActivity objects
                elif element.__class__.__name__ == "OperationalActivity":
                    # Get the incoming and outgoing exchanges for the OperationalActivity
                    incoming_exchanges = element.get_incoming()
                    outgoing_exchanges = element.get_outgoing()
                    
                    # Process incoming exchanges
                    for exchange in incoming_exchanges:
                        source = exchange.get_source().get_name() if exchange.get_source() else "Unknown Source"
                        exchange_name = exchange.get_name() if hasattr(exchange, 'get_name') else "Unnamed Exchange"
                        relationships.append(("OperationalActivity (Incoming)", exchange_name, source, element.get_name()))
                    
                    # Process outgoing exchanges
                    for exchange in outgoing_exchanges:
                        target = exchange.get_target().get_name() if exchange.get_target() else "Unknown Target"
                        exchange_name = exchange.get_name() if hasattr(exchange, 'get_name') else "Unnamed Exchange"
                        relationships.append(("OperationalActivity (Outgoing)", exchange_name, element.get_name(), target))
            
            # Print relationships in a structured way
            print("\nRelationships:")
            for rel in relationships:
                print(f"Type: {rel[0]}")
                print(f"  - Name: {rel[1]}")
                print(f"  - From: {rel[2]}")
                print(f"  - To: {rel[3]}")
                print("-" * 40)  # Separator for readability
            
            return elements, relationships
    print(f"Diagram '{diagram_name}' not found.")
    return [], []

if __name__ == '__main__':
    try:
        # Include needed for the Capella modeller API
        include('workspace://Python4Capella/simplified_api/capella.py')
        if False:
            from simplified_api.capella import *

        aird_path = '/In-Flight Entertainment System/In-Flight Entertainment System.aird'
        model = CapellaModel()
        model.open(aird_path)

        # Search for the specific diagram and extract its entities and relationships
        diagram_name = "[OAIB] Listen to Audio"
        entities, relationships = get_entities_and_relationships_from_diagram(model, diagram_name)
        
    except Exception as e:
        print(f"Unexpected error: {e}")