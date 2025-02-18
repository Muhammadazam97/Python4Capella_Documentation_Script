

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
            elements = []
            relationships = []

            for element in diagram.get_represented_elements():
                elements.append(element)
                entity_type = element.__class__.__name__
                print(f"Entity: {element.get_name() if hasattr(element, 'get_name') else 'Unknown'} - Type: {entity_type}")
                
                if entity_type == "SequenceMessage":
                    source = element.get_sending_instance_role()
                    target = element.get_receiving_instance_role()
                    relationships.append(("SequenceMessage", element.get_name(), 
                                          source.get_name() if source else "Unknown Source", 
                                          target.get_name() if target else "Unknown Target"))

                elif entity_type == "FunctionalExchange":
                    source = element.get_source_function() if hasattr(element, 'get_source_function') else None
                    target = element.get_target_function() if hasattr(element, 'get_target_function') else None
                    relationships.append(("FunctionalExchange", element.get_name(), 
                                          source.get_name() if source else "Unknown Source", 
                                          target.get_name() if target else "Unknown Target"))
                
                elif entity_type == "OperationalActivity":
                    incoming_exchanges = element.get_incoming() if hasattr(element, 'get_incoming') else []
                    outgoing_exchanges = element.get_outgoing() if hasattr(element, 'get_outgoing') else []

                    for exchange in incoming_exchanges:
                        source = exchange.get_source_function() if hasattr(exchange, 'get_source_function') else None
                        relationships.append(("OperationalActivity (Incoming)", exchange.get_name(), 
                                              source.get_name() if source else "Unknown Source", 
                                              element.get_name()))
                    
                    for exchange in outgoing_exchanges:
                        target = exchange.get_target_function() if hasattr(exchange, 'get_target_function') else None
                        relationships.append(("OperationalActivity (Outgoing)", exchange.get_name(), 
                                              element.get_name(), 
                                              target.get_name() if target else "Unknown Target"))

            print("\nRelationships:")
            for rel in relationships:
                print(f"Type: {rel[0]}\n  - Name: {rel[1]}\n  - From: {rel[2]}\n  - To: {rel[3]}")
                print("-" * 40)
            
            return elements, relationships
    
    print(f"Diagram '{diagram_name}' not found.")
    return [], []

if __name__ == '__main__':
    try:
        include('workspace://Python4Capella/simplified_api/capella.py')
        if False:
            from simplified_api.capella import *
        
        aird_path = '/In-Flight Entertainment System/In-Flight Entertainment System.aird'
        model = CapellaModel()
        model.open(aird_path)

        diagram_name = "[OAIB] Listen to Audio"
        entities, relationships = get_entities_and_relationships_from_diagram(model, diagram_name)
        
    except Exception as e:
        print(f"Unexpected error: {e}")