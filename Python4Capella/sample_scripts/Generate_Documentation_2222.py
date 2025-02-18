# name                 : Extract and Document Diagram Entities and Relationships
# script-type          : Python
# description          : Retrieves entities and relationships from a diagram and generates documentation using OpenAI.
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

import openai
import eclipse.system.ui as ui  # @UnresolvedImport
from py4j.java_gateway import java_import

# Import Java helper classes for Capella
jvm = gateway.jvm  # @UndefinedVariable
java_import(jvm, 'org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper')
CapellaAdapterHelper = jvm.org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper

# Set OpenAI API Key (Ensure you have a valid key)
client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")

# OpenAI model
openaimodel = "gpt-3.5-turbo"

def get_entities_and_relationships_from_diagram(model, diagram_name):
    """Finds a diagram by name and retrieves all its entities and relationships."""
    diagrams = model.get_all_diagrams()
    for diagram in diagrams:
        if diagram.get_name() == diagram_name:
            print(f"Diagram found: {diagram.get_name()}")
            elements = []
            relationships = []

            for element in diagram.get_represented_elements():
                elements.append(element.get_name())
                entity_type = element.__class__.__name__
                
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
            
            return elements, relationships
    
    print(f"Diagram '{diagram_name}' not found.")
    return [], []

if __name__ == '__main__':
    try:
        # Get selected object from Eclipse
        selected = ui.getSelection()
        selected_objs = CapellaAdapterHelper.resolveSemanticObjects(selected.toList(), True)

        for selected_obj in selected_objs:
            session = Sirius.get_session(diagram_representation)
            res = session.getSessionResource().getURI().toPlatformString(True)
            model_path = "/" + res[1:res.rfind(".")] + ".aird"
            
            model = CapellaModel()
            model.open(model_path)
            
            print(f"Selected diagram: {diagram_name}")
            entities, relationships = get_entities_and_relationships_from_diagram(model, diagram_name)
            
            # Prepare OpenAI prompt
            prompt = f"Generate documentation for the diagram '{diagram_name}' with the following entities and relationships:\n\n"
            prompt += "Entities:\n" + "\n".join(entities) + "\n\nRelationships:\n"
            for rel in relationships:
                prompt += f"Type: {rel[0]}\n  - Name: {rel[1]}\n  - From: {rel[2]}\n  - To: {rel[3]}\n\n"
            
            # Send to OpenAI
            response = client.chat.completions.create(
                model=openaimodel,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            ai_response = response.choices[0].message.content
            
            # Update Capella model with generated documentation
            model.start_transaction()
            try:
                selected_obj.setDescription(f"<p>Generated Documentation:</p>{ai_response}")
            except Exception as e:
                model.rollback_transaction()
                print("Error:", e)
                raise
            else:
                model.commit_transaction()
                print("Model Committed")
            
            # Save model
            model.save()
    
    except Exception as e:
        print(f"Unexpected error: {e}")
