
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
import os
import eclipse.system.ui as ui  # @UnresolvedImport
from py4j.java_gateway import java_import

# Import Java helper classes for Capella
jvm = gateway.jvm  # @UndefinedVariable
java_import(jvm, 'org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper')
CapellaAdapterHelper = jvm.org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper

# Set OpenAI API Key (Ensure you have a valid key)
client = openai.OpenAI(api_key="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")

# OpenAI model
openaimodel = "gpt-4-turbo"

def get_entities_and_relationships_from_diagram(model, diagram_name):
    """Finds a diagram by name and retrieves all its entities and relationships."""
    diagrams = model.get_all_diagrams()
    for diagram in diagrams:
        if diagram.get_name() == diagram_name:
            print(f"Diagram found: {diagram.get_name()}")
            elements = []
            relationships = []

            for element in diagram.get_represented_elements():
                elements.append(element.get_name() if element.get_name() else "Unnamed Entity")
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
            # Retrieve active selection from Eclipse
            selected = ui.getSelection()
            selected_list = selected.toList()
            if not selected_list or len(selected_list) == 0:
                print("No active selection. Please select a diagram.")
                continue
            semantic_elements = CapellaAdapterHelper.resolveSemanticObjects(selected_list, True)
            if not semantic_elements or len(semantic_elements) == 0:
                print("No semantic element resolved from selection. Please select a valid diagram.")
                continue
           # Assume first resolved semantic element is the diagram representation
            diagram_representation = semantic_elements[0]

            # Retrieve the **semantic model root element** from the diagram
            semantic_root = diagram_representation.eContainer()  # Get the semantic container

            if not semantic_root:
                print("Could not retrieve the semantic model from the diagram.")
                continue
            # Retrieve model path
            session = Sirius.get_session(diagram_representation)
            res = session.getSessionResource().getURI().toPlatformString(True)
            model_path = "/" + res[1:res.rfind(".")] + ".aird"          
            model = CapellaModel()
            model.open(model_path)
            
            diagram_name = selected_obj.getName()
            entities, relationships = get_entities_and_relationships_from_diagram(model, diagram_name)
            
            # Prepare OpenAI prompt
            prompt = f"Generate detailed Documentation Based on Entities and Relationships with the following entities and relationships:\n\n"
            prompt += "Entities:\n" + "\n".join(entities) + "\n\nRelationships:\n"
            for rel in relationships:
                prompt += f"Type: {rel[0]}\n  - Name: {rel[1]}\n  - From: {rel[2]}\n  - To: {rel[3]}\n\n"
            
            # Send to OpenAI
            response = client.chat.completions.create(
                model=openaimodel,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            ai_response = response.choices[0].message.content
            print("AI Response:", ai_response)
            # Ensure Documentation directory exists
            documentation_dir = os.path.join(os.getcwd(), "Documentation")
            if not os.path.exists(documentation_dir):
                os.makedirs(documentation_dir)
                
            # Save to a Markdown file with diagram name
            file_path = os.path.join(documentation_dir, f"{diagram_name}.md")
            with open(file_path, "w", encoding="utf-8") as doc_file:
                doc_file.write(ai_response)
                
            print(f"Documentation saved at: {file_path}")
            
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
